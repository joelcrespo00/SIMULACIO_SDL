from enumeracions import *
from Server import *
from Event import *


class Queue:
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
            self.entitats += entitat
        else:
            event_nou = Event(self, "NOVA ENTITAT", time, None) #A LA MATEIXA CUA
            self.tractarEsdeveniment(event_nou)

    def enviarEsdeveniment(self, event):
        self.server.recullEntitat(event)  # enviar esdeveniment

    def tractarEsdeveniment(self, event):
        if event.type == "NOVA ENTITAT": #PROVE DE LA CUA
            if self.server.state == idle:
                event_server = Event(self.server, "NEW SERVICE B1", event.time, None)
                self.enviarEsdeveniment(event_server)
                self.server.state = busy
            else:
                event_server = Event(self.server, "NEW SERVICE B1", event.time, None)
                self.esdeveniments += event
                self.entitats += 1
        if event.type == "FINISH PROCESS SERVERB1": #PROVE DEL SERVIDOR
            if self.esdeveniments.count() > 0:
                event_server = self.esdeveniments.pop()
                event_server.time = event.time
                self.enviarEsdeveniment(event_server)
                self.entitats -= 1
            else:
                self.state = empty
                self.server.state = idle

    def simulationStart(self, event):
        self.state = empty
        self.entitatsTractades = 0


