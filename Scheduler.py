from ServerB1 import *
from ServerB2 import *
from Source import *
from QueueB1 import *
from QueueB2 import *
from ServerR import *


class Scheduler:
    currentTime = 0
    eventList = []

    def __init__(self):
        # creació dels objectes que composen el meu model
        self.source = Source(self)
        #########################################
        self.QueueB1 = QueueB1()
        self.QueueB2 = QueueB2()
        self.ServerB1 = ServerB1(self)
        self.ServerB2 = ServerB2(self)
        #########################################
        self.ServerR = ServerR(self)

        self.source.crearConnexio(self.QueueB1, self.QueueB2)
        #######################################
        self.QueueB1.crearConnexio(self.source, self.ServerB1)
        self.QueueB2.crearConnexio(self.source, self.ServerB2)
        #######################################
        self.ServerB1.crearConnexio(self.ServerR, self.QueueB1)
        self.ServerB2.crearConnexio(self.ServerR, self.QueueB2)
        self.ServerR.crearConnexio(self.ServerB1, self.ServerB2)

        self.simulationStart = Event(self, 'SIMULATION_START', 0, None)
        self.afegirEsdeveniment(self.simulationStart)

    def run(self):
        # configurar el model per consola, arxiu de text...
        self.configurarModel()

        # rellotge de simulacio a 0
        self.currentTime = 0
        # bucle de simulació (condició fi simulació llista buida)
        while self.eventList:
            # recuperem event simulacio
            event = self.donamEsdeveniment()
            # actualitzem el rellotge de simulacio
            self.currentTime = event.time
            # deleguem l'acció a realitzar de l'esdeveniment a l'objecte que l'ha generat
            # també podríem delegar l'acció a un altre objecte
            event.object.tractarEsdeveniment(event)

        # recollida d'estadístics
        self.recollirEstadistics()

    def afegirEsdeveniment(self, event):
        # inserir esdeveniment de forma ordenada
        self.eventList.append(event)

    def donamEsdeveniment(self):
        # agafar el primer element de la llista
        event = self.eventList.__getitem__(0)
        self.eventList.pop()
        return event

    def tractarEsdeveniment(self, event):
        print("LLEGO A SIMULATION START")
        if event.type == "SIMULATION_START":
            self.QueueB1.simulationStart()
            self.QueueB2.simulationStart()
            self.ServerB1.simulationStart()
            self.ServerB2.simulationStart()
            self.ServerR.simulationStart()
            self.source.simulationStart()

    def recollirEstadistics(self):
        SOURCE = self.source.entitatsCreades
        QB1 = self.QueueB1.entitatsTractades
        QB2 = self.QueueB1.entitatsTractades
        SB1 = self.QueueB1.entitatsTractades
        SB2 = self.QueueB1.entitatsTractades
        print("ENTITATS TRACTADES EN TOTAL: \n")
        print("%d \n", SOURCE)
        print("ENTITATS TRACTADES EN QUEUEB1: ")
        print("%d \n", QB1)
        print("ENTITATS TRACTADES EN QUEUEB2: ")
        print("%d \n", QB2)
        print("ENTITATS TRACTADES EN SERVERB1: ")
        print("%d \n", SB1)
        print("ENTITATS TRACTADES EN SERVERB2: ")
        print("%d \n", SB2)
        print("PERCENTATGE D'ENTITATS TRACTADES PER CADA BOTIGA: \n")
        PB1 = (QB1/SOURCE)*100
        PB2 = (QB2/SOURCE)*100
        print("BOTIGA 1: %d \n", PB1)
        print("BOTIGA 2: %d \n", PB2)

    def configurarModel(self):
        # PARAMETRITZAR TEMPS ENTRE ARRIBADES A LA SOURCE
        print("INTRODUEIX EL MINIM TEMPS ENTRE ARRIBADES: \n")
        min = int(input())
        print("INTRODUEIX EL MAXIM TEMPS ENTRE ARRIBADES: \n")
        max = int(input())
        self.source.min = min
        self.source.max = max


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
