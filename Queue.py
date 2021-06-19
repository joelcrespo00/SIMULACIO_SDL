from enumerations import Enumerations
from Event import *


class Queue:
    def __init__(self, scheduler, nom):
        self.scheduler = scheduler
        self.state = None
        self.entitatsTractades = 0
        self.entitats = []
        self.num_entitats = 0
        self.nom = nom

    def crearConnexio(self, source, server):
        self.source = source
        self.server = server

    def recullEntitat(self, time, entitat):
        self.entitatsTractades += 1
        if self.entitats:
            self.num_entitats += 1
            self.entitats.append(entitat)
            self.state = Enumerations.noempty
        else:
            event_nou = Event(self, "NEW EVENT", time, entitat)
            self.scheduler.afegirEsdeveniment(event_nou)

    def enviarEsdeveniment(self, event):
        self.server.recullEntitat(event.time, event.entity)

    def tractarEsdeveniment(self, event):
        if event.type == "NEW ENTITY":
            self.recullEntitat(event.time, event.entity)
        elif event.type == "NEW EVENT":
            event_server = Event(self.server, "NEW SERVICE", event.time, event.entity)
            if self.server.state == Enumerations.idle:
                self.scheduler.afegirEsdeveniment(event_server)
            else:
                self.entitats.append(event.entity)
                self.num_entitats += 1
                self.state = Enumerations.noempty
        elif event.type == "FINISH PROCESS SERVER":
            if self.entitats:
                event_nou = Event(self, "NEW EVENT", event.time, self.entitats.pop())
                self.scheduler.afegirEsdeveniment(event_nou)
                self.num_entitats -= 1
            else:
                self.state = Enumerations.empty
                self.server.state = Enumerations.idle

    def simulationStart(self):
        self.state = Enumerations.empty
        self.entitatsTractades = 0
