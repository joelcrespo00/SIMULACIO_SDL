# millor treballar amb define o algun sistema simular a l'enum de C++
from enumeracions import *
from numpy.random import random

from Server import *
from scipy.stats import uniform


class Source:

    def __init__(self, scheduler):
        # inicialitzar element de simulació
        entitatsCreades = 0
        self.state = idle
        self.scheduler = scheduler
        self.queue1 = None
        self.queue2 = None

    def crearConnexio(self, queue1, queue2):
        self.queue1 = queue1
        self.queue2 = queue2

    def tractarEsdeveniment(self, event):
        if (event.tipus == 'SIMULATION START'):
            self.simulationStart(event)

        if (event.tipus == 'NEXT ARRIVAL'):
            self.processNextArrival()
        ...

    def simulationStart(self, event):
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
        nouEvent = self.properaArribada(event.temps)
        self.scheduler.afegirEsdeveniment(nouEvent)

    def properaArribada(self, time):
        # cada quan generem una arribada (aleatorietat)
        tempsEntreArribades = self.tArribades()
        # incrementem estadistics si s'escau
        self.entitatsCreades = self.entitatsCreades + 1
        self.state = busy
        # programació primera arribada
        return Event(self, 'NEXT ARRIVAL', time + tempsEntreArribades, None)

    def tArribades(self):
        return random.uniform(min=0, max=50)

    def crearEntitat(self, self1):
        pass
