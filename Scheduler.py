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
            event.objecte.tractarEsdeveniment(event)

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
        if (event.tipus == "SIMULATION_START"):
            pass
            # comunicar a tots els objectes que cal preparar-se

    def recollirEstadistics(self):
        pass

    def configurarModel(self):
        pass


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
