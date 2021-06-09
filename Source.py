# millor treballar amb define o algun sistema simular a l'enum de C++
from enumerations import Enumerations
from numpy.random import random
from random import uniform
from Event import *


class Source:

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        self.entitatsCreades = 0
        self.state = Enumerations.idle
        self.scheduler = scheduler
        self.queue1 = None
        self.queue2 = None
        self.min = 0
        self.max = 1

    def crearConnexio(self, queue1, queue2):
        self.queue1 = queue1
        self.queue2 = queue2

    def tractarEsdeveniment(self, event):
        if (event.type == 'SIMULATION START'):
            self.simulationStart()

        if (event.type == 'NEXT ARRIVAL'):
            self.processNextArrival(event)

    def simulationStart(self):
        nouEvent = self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def processNextArrival(self, event):
        # Cal crear l'entitat 
        entitat = self.crearEntitat(self)
        # Mirar si es pot transferir a on per toqui
        cua = random()
        if (cua % 2 == 0):  ##ENVIAR A QueueB1
            # transferir entitat
            self.queue1.recullEntitat(event.time, entitat)
        else:  # ENVIAR A SERVERB2
            # transferir entitat
            self.queue2.recullEntitat(event.time, entitat)
        # Cal programar la següent arribada
        nouEvent = self.properaArribada(event.time)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def properaArribada(self, time):
        # cada quan generem una arribada (aleatorietat)
        tempsEntreArribades = self.tArribades()
        # incrementem estadistics si s'escau
        self.entitatsCreades = self.entitatsCreades + 1
        self.state = Enumerations.busy
        # programació propera arribada
        return Event(self, 'NEXT ARRIVAL', time + tempsEntreArribades, None)

    def tArribades(self):
        min = self.min
        max = self.max
        return uniform(min, max)

    def crearEntitat(self, self1):
        pass
