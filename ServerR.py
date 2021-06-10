from enumerations import Enumerations
from Event import *
from random import uniform


class ServerR:

    def __init__(self, scheduler):
        self.entitatsTractades = 0
        self.state = Enumerations.idle
        self.scheduler = scheduler
        self.entitatActiva = None
        self.min = 0
        self.max = 1

    def crearConnexio(self, server1, server2):
        self.server1 = server1
        self.server2 = server2

    def recullEntitat(self, time, entitat, via):
        self.entitatsTractades += 1
        self.state = Enumerations.busy
        self.entitatActiva = entitat
        event_proces = self.programarFinalServei(time, entitat)
        if via == "B1":
            event_proces.object = self.server1
            event_proces.type = "NEW SERVICE R FROM B1"
        else:
            event_proces.object = self.server2
            event_proces.type = "NEW SERVICE R FROM B2"
        self.scheduler.afegirEsdeveniment(event_proces)

    def tractarEsdeveniment(self, event):
        event_nou = Event(self, "FINISH PROCESS SERVERR", event.time, event.entity)
        if event.type == 'NEW SERVICE R FROM B1':
            event_nou.object = self.server1
            self.state = Enumerations.idle
            self.entitatActiva = None
            self.scheduler.afegirEsdeveniment(event_nou)
        else:
            event_nou.object = self.server2
            self.state = Enumerations.idle
            self.entitatActiva = None
            self.scheduler.afegirEsdeveniment(event_nou)

    def simulationStart(self):
        self.state = Enumerations.idle
        self.entitatsTractades = 0

    def programarFinalServei(self, time, entitat):
        tempsServei = self.tServei_R()
        return Event(self, 'END_SERVICE', time + tempsServei, entitat)

    def tServei_R(self):
        return uniform(self.min, self.max)
