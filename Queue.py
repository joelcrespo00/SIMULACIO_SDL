


class Queue:
    def __init__(self):
        # inicialitzar element de simulació
        self.state = None
        self.entitatsTractades=0 ##Saber cuantes van a aquesta cua
        self.esdeveniments = [] #esdeveniments en la cua

    def crearConnexio(self,source,server):
        self.source=source
        self.server=server

    def recullEntitat(self,time,entitat):
        self.entitatsTractades=entitat
        self.programarFinalServei(time,entitat)

    def enviarEsdeveniment(self, event):
        self.server.#enviar esdeveniment

    def tractarEsdeveniment(self, event):
        if (self.server.state == idle):
            self.enviarEsdeveniment(event)

        if (event.tipus=='END_SERVICE'):
            self.processarFiServei(event)

    def simulationStart(self,event):
        self.state=empty
        self.entitatsTractades=0

    def programarFinalServei(self, time,entitat):
        # que triguem a fer un servei (aleatorietat)
        tempsServei = _alguna_funcio ()
        # incrementem estadistics si s'escau
        self.entitatsTractades=self.entitatsTractades+1
        self.state = busy
        # programació final servei
        return Event(self,'END_SERVICE', time+ tempsServei,entitat)

    def processarFiServei(self,event):
        # Registrar estadístics
        self.entitatsTractades=self.entitatsTractades+1
        # Mirar si es pot transferir a on per toqui
        if (server.estat==idle):
            #transferir entitat (es pot fer amb un esdeveniment immediat o invocant a un métode de l'element)
            server.recullEntitat(event.time,event.entitat)
        else:
            if (queue.estat==idle):
                queue.recullEntitat(event.time,event.entitat)
            ...
        self.estat=idleeeee

    ...

