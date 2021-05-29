# millor treballar amb define o algun sistema simular a l'enum de C++
from enumerations import *
from Event import *
from numpy.random import random


class ServerB1:

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        self.entitatsTractades = 0
        self.state = Enumerations.idle
        self.scheduler = scheduler
        self.entitatActiva = None

    def crearConnexio(self, server2, queue):
        self.queue = queue
        self.server = server2

    def recullEntitat(self, time, entitat):
        self.entitatsTractades += 1
        self.state = Enumerations.busy
        self.entitatActiva = entitat
        event_proces = self.programarFinalServei(time, entitat)
        event_serverR = Event(self.server, "NEW SERVICE R FROM B1", event_proces.time, entitat)
        self.tractarEsdeveniment(event_serverR)

    def enviarEsdevenimentServerR(self, event):
        self.server.recullEntitat(event.entity, 1)

    def tractarEsdeveniment(self, event):
        if event.type == 'NEW SERVICE R':
            if self.server.state.idle:
                self.enviarEsdevenimentServerR(event)
            else:
                while self.server.state.busy:
                    pass
                self.enviarEsdevenimentServerR(event)
        if event.type == 'FINISH PROCESS SERVERR':
            event_fi_servei = Event(self.queue, "FINISH PROCESS SERVERB1", event.time, event.entity)
            self.queue.tractarEsdeveniment(event_fi_servei)
            self.state = Enumerations.idle
            self.entitatActiva = None

    def simulationStart(self, event):
        self.state = Enumerations.idle
        self.entitatsTractades = 0

    def programarFinalServei(self, time, entitat):
        # que triguem a fer un servei (aleatorietat)
        tempsServei = self.tServei_B1()
        # incrementem estadistics si s'escau
        # programació final servei
        return Event(self, 'END_SERVICE', time + tempsServei, entitat)

    def tServei_B1(self):
        return random.uniform(min=20, max=50)
