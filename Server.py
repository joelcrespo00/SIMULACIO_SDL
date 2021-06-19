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
        self.event_block = None

    def crearConnexio(self, server2, queue):
        self.queue = queue
        self.server = server2

    def recullEntitat(self, time, entitat):
        self.entitatsTractades += 1
        self.entitatActiva = entitat
        s = "NEW PROCESS SERVER R"
        tempsServei = self.tServei_B1()
        event_serverR = Event(self, s, time + tempsServei, entitat)
        self.scheduler.afegirEsdeveniment(event_serverR)

    def enviarEsdevenimentServerR(self, event):
        self.server.recullEntitat(event.time, event.entity, self.name)

    def tractarEsdeveniment(self, event):
        if event.type == "NEW SERVICE":
            self.recullEntitat(event.time, event.entity)
        elif event.type == "NEW PROCESS SERVER R":
            if self.server.state == Enumerations.idle:
                event.object = self.server
                self.state = Enumerations.busy
                self.scheduler.afegirEsdeveniment(event)
            else:
                self.state = Enumerations.block
                self.event_block = event
        elif event.type == 'FINISH PROCESS SERVERR':
            s = "FINISH PROCESS SERVER"
            event_fi_servei = Event(self.queue, s, event.time, None)
            if self.state == Enumerations.block:
                self.event_block.object = self.server
                self.event_block.time = event.time
                self.scheduler.afegirEsdeveniment(self.event_block)
                self.event_block = None
                self.state = Enumerations.busy
            else:
                self.state = Enumerations.idle
                self.entitatActiva = None
            self.scheduler.afegirEsdeveniment(event_fi_servei)

    def simulationStart(self):
        self.state = Enumerations.idle
        self.entitatsTractades = 0

    def tServei_B1(self):
        return uniform(self.min, self.max)
