# millor treballar amb define o algun sistema simular a l'enum de C++
from enumerations import Enumerations
from Event import *
from numpy.random import random


class ServerR:

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        self.entitatsTractades = 0
        self.state = Enumerations.idle
        self.scheduler = scheduler
        self.entitatActiva = None

    def crearConnexio(self, server1, server2):
        self.server1 = server1
        self.server2 = server2

    def recullEntitat(self, time, entitat, via):
        self.entitatsTractades += 1
        self.state = Enumerations.busy
        self.entitatActiva = entitat
        event_proces = self.programarFinalServei(time, entitat)
        if via == 1:
            event_proces.type = "NEW SERVICE R FROM B1"
        else:
            event_proces.type = "NEW SERVICE R FROM B2"
        self.tractarEsdeveniment(event_proces)

    def tractarEsdeveniment(self, event):
        event_nou = (self.server1, "FINISH PROCESS SERVERR", event.time, event.entity)
        if event.type == 'NEW SERVICE R FROM B1':
            self.server1.tractarEsdeveniment(event_nou)
        else:
            self.server2.tractarEsdeveniment(event_nou)
        self.state = Enumerations.idle
        self.entitatActiva = None

    def simulationStart(self):
        self.state = Enumerations.idle
        self.entitatsTractades = 0

    def programarFinalServei(self, time, entitat):
        # que triguem a fer un servei (aleatorietat)
        tempsServei = self.tServei_R()
        # incrementem estadistics si s'escau
        # programació final servei
        return Event(self, 'END_SERVICE', time + tempsServei, entitat)

    def tServei_R(self):
        return random.uniform(min=5, max=10)
