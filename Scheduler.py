from Server import *
from Source import *
from Queue import *
from ServerR import *


class Scheduler:
    currentTime = 0
    eventList = []

    def __init__(self):
        # creació dels objectes que composen el meu model
        self.source = Source(self)
        #########################################
        self.QueueB1 = Queue(self, "B1")
        self.QueueB2 = Queue(self, "B2")
        self.ServerB1 = Server(self, "B1")
        self.ServerB2 = Server(self, "B2")
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
        self.maxtime = 0

    def run(self):
        self.configurarModel()
        self.currentTime = 0
        while self.eventList and self.currentTime < self.maxtime:
            event = self.donamEsdeveniment()
            self.currentTime = event.time
            event.object.tractarEsdeveniment(event)

        print("SIMULACIÓ ACABADA")
        self.recollirEstadistics()

    def order(self, event):
        return event.time

    def afegirEsdeveniment(self, event):
        self.eventList.append(event)
        self.eventList.sort(key=self.order)

    def donamEsdeveniment(self):
        event = self.eventList.__getitem__(0)
        self.eventList.pop(0)
        return event

    def tractarEsdeveniment(self, event):
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
        QB2 = self.QueueB2.entitatsTractades
        SB1 = self.ServerB1.entitatsTractades
        SB2 = self.ServerB2.entitatsTractades
        SR = self.ServerR.entitatsTractades
        print("ENTITATS TRACTADES EN TOTAL: \n")
        print(str(SOURCE) + "\n")
        print("ENTITATS TRACTADES EN QUEUEB1: ")
        print(str(QB1) + "\n")
        print("ENTITATS TRACTADES EN QUEUEB2: ")
        print(str(QB2) + "\n")
        print("ENTITATS TRACTADES EN SERVERB1: ")
        print(str(SB1) + "\n")
        print("ENTITATS TRACTADES EN SERVERB2: ")
        print(str(SB2) + "\n")
        print("ENTITATS TRACTADES EN SERVERR: ")
        print(str(SR) + "\n")
        print("PERCENTATGE D'ENTITATS TRACTADES PER CADA BOTIGA: \n")
        PB1 = (QB1 / SOURCE) * 100
        PB2 = (QB2 / SOURCE) * 100
        print("BOTIGA 1: " + str(PB1) + "\n")
        print("BOTIGA 2: " + str(PB2) + "\n")

    def configurarModel(self):
        # PARAMETRITZAR TEMPS ENTRE ARRIBADES A LA SOURCE
        print("INTRODUEIX EL MINIM TEMPS ENTRE ARRIBADES: \n")
        min = int(input())
        print("INTRODUEIX EL MAXIM TEMPS ENTRE ARRIBADES: \n")
        max = int(input())
        print("INTRODUEIX EL MAXIM TEMPS DE SIMULACIÓ: \n")
        maxt = int(input())
        print("INTRODUEIX EL MINIM TEMPS DE SERVEI DEL SERVIDOR DE LA BOTIGA 1: \n")
        minb1 = int(input())
        print("INTRODUEIX EL MAXIM TEMPS DE SERVEI DEL SERVIDOR DE LA BOTIGA 1: \n")
        maxb1 = int(input())
        print("INTRODUEIX EL MINIM TEMPS DE SERVEI DEL SERVIDOR DE LA BOTIGA 2: \n")
        minb2 = int(input())
        print("INTRODUEIX EL MAXIM TEMPS DE SERVEI DEL SERVIDOR DE LA BOTIGA 2: \n")
        maxb2 = int(input())
        print("INTRODUEIX EL MINIM TEMPS DE SERVEI DEL SERVIDOR EN COMU: \n")
        mins = int(input())
        print("INTRODUEIX EL MAXIM TEMPS DE SERVEI DEL SERVIDOR EN COMU: \n")
        maxs = int(input())
        self.maxtime = maxt
        self.source.min = min
        self.source.max = max
        self.ServerB1.min = minb1
        self.ServerB1.max = maxb1
        self.ServerB2.min = minb2
        self.ServerB2.max = maxb2
        self.ServerR.min = mins
        self.ServerR.max = maxs


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.run()
