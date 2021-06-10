from enumerations import Enumerations
from random import uniform
from random import randrange
from Event import *


class Source:

    def __init__(self, scheduler):
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
        if event.type == 'SIMULATION START':
            self.simulationStart()

        if event.type == 'NEXT ARRIVAL':
            self.processNextArrival(event)

    def simulationStart(self):
        nouEvent = self.properaArribada(0)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def processNextArrival(self, event):
        entitat = self.crearEntitat(self)
        cua = randrange(10)
        if cua % 2 == 0:  ##ENVIAR A QueueB1
            self.queue1.recullEntitat(event.time, entitat)
        else:  # ENVIAR A SERVERB2
            self.queue2.recullEntitat(event.time, entitat)
        nouEvent = self.properaArribada(event.time)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def properaArribada(self, time):
        tempsEntreArribades = self.tArribades()
        self.entitatsCreades = self.entitatsCreades + 1
        self.state = Enumerations.busy
        return Event(self, 'NEXT ARRIVAL', time + tempsEntreArribades, None)

    def tArribades(self):
        min = self.min
        max = self.max
        return uniform(min, max)

    def crearEntitat(self, self1):
        return None
