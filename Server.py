from enumerations import *
from Event import *
from random import uniform


class Server:

    def __init__(self, scheduler, name):
        self.entitatsTractades = 0
        self.state = Enumerations.idle
        self.scheduler = scheduler
        self.entitatActiva = None
        self.name = name
        self.min = 0
        self.max = 1

    def crearConnexio(self, server2, queue):
        self.queue = queue
        self.server = server2

    def recullEntitat(self, time, entitat):
        self.entitatsTractades += 1
        self.state = Enumerations.busy
        self.entitatActiva = entitat
        event_proces = self.programarFinalServei(time, entitat)
        s = "NEW PROCESS SERVER R FROM"+self.name
        event_serverR = Event(self.server, s, event_proces.time, entitat)
        self.scheduler.afegirEsdeveniment(event_serverR)

    def enviarEsdevenimentServerR(self, event):
        self.server.recullEntitat(event.time, event.entity, self.name)

    def tractarEsdeveniment(self, event):
        s = "NEW PROCESS SERVER R FROM"+self.name
        if event.type == s:
            if self.server.state == Enumerations.idle:
                self.scheduler.afegirEsdeveniment(event)
            else:
                self.waitforavailability()
                self.scheduler.afegirEsdeveniment(event)
        if event.type == 'FINISH PROCESS SERVERR':
            s = "FINISH PROCESS SERVER "+self.name
            event_fi_servei = Event(self.queue, s, event.time, event.entity)
            self.state = Enumerations.idle
            self.entitatActiva = None
            self.scheduler.afegirEsdeveniment(event_fi_servei)

    def waitforavailability(self):
        while self.server.state == Enumerations.busy:
            pass

    def simulationStart(self):
        self.state = Enumerations.idle
        self.entitatsTractades = 0

    def programarFinalServei(self, time, entitat):
        tempsServei = self.tServei_B1()
        return Event(self, 'END_SERVICE', time + tempsServei, entitat)

    def tServei_B1(self):
        return uniform(self.min, self.max)
