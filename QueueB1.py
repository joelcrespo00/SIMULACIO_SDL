from enumerations import Enumerations
from Event import *


class QueueB1:
    def __init__(self):
        # inicialitzar element de simulació
        self.state = None
        self.entitatsTractades = 0  ##Saber cuantes van a aquesta cua per estadistics
        self.esdeveniments = []  # esdeveniments en la cua
        self.entitats = 0

    def crearConnexio(self, source, server):
        self.source = source
        self.server = server

    def recullEntitat(self, time, entitat):
        self.entitatsTractades += 1
        if self.entitats:
            self.entitats += 1
        else:
            event_nou = Event(self, "NOVA ENTITAT", time, entitat) #A LA MATEIXA CUA
            self.tractarEsdeveniment(event_nou)

    def enviarEsdeveniment(self, event):
        self.server.recullEntitat(event.entity)  # QueueB1.pyenviar esdeveniment

    def tractarEsdeveniment(self, event):
        if event.type == "NOVA ENTITAT": #PROVE DE LA CUA
            event_server = Event(self.server, "NEW SERVICE B1", event.time, event.entity)
            if self.server.state == Enumerations.idle:
                self.enviarEsdeveniment(event_server)
                self.server.state = Enumerations.busy
            else:
                self.esdeveniments += event_server
                self.entitats += 1
                self.state = Enumerations.noempty
        if event.type == "FINISH PROCESS SERVERB1": #PROVE DEL SERVIDOR
            if self.esdeveniments:
                event_server = self.esdeveniments.pop()
                event_server.time = event.time
                self.enviarEsdeveniment(event_server)
                self.entitats -= 1
            else:
                self.state = Enumerations.empty
                self.server.state = Enumerations.idle

    def simulationStart(self, event):
        self.state = Enumerations.empty
        self.entitatsTractades = 0


