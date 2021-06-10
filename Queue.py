from enumerations import Enumerations
from Event import *


class Queue:
    def __init__(self, scheduler, nom):
        self.scheduler = scheduler
        self.state = None
        self.entitatsTractades = 0
        self.esdeveniments = []
        self.entitats = 0
        self.nom = nom

    def crearConnexio(self, source, server):
        self.source = source
        self.server = server

    def recullEntitat(self, time, entitat):
        self.entitatsTractades += 1
        if self.esdeveniments:
            self.entitats += 1
            event_nou = Event(self, "NOVA ENTITAT", time, entitat)
            self.esdeveniments.append(event_nou)
        else:
            event_nou = Event(self, "NOVA ENTITAT", time, entitat)
            self.scheduler.afegirEsdeveniment(event_nou)

    def enviarEsdeveniment(self, event):
        self.server.recullEntitat(event.time, event.entity)

    def tractarEsdeveniment(self, event):
        if event.type == "NEW SERVICE":
            self.recullEntitat(event.time, event.entity)
        elif event.type == "NOVA ENTITAT":
            s = "NEW SERVICE " + self.nom
            event_server = Event(self.server, s, event.time, event.entity)
            if self.server.state == Enumerations.idle:
                self.server.state = Enumerations.busy
                self.scheduler.afegirEsdeveniment(event_server)
            else:
                self.esdeveniments.append(event_server)
                self.entitats += 1
                self.state = Enumerations.noempty
        elif event.type == "FINISH PROCESS SERVER B1" or event.type == "FINISH PROCESS SERVER B2":
            if self.esdeveniments:
                event_server = self.esdeveniments.pop()
                event_server.time = event.time
                self.entitats -= 1
                self.scheduler.afegirEsdeveniment(event_server)
            else:
                self.state = Enumerations.empty
                self.server.state = Enumerations.idle

    def simulationStart(self):
        self.state = Enumerations.empty
        self.entitatsTractades = 0
