from twisted.internet import reactor, protocol

class QuoteProtocol(protocol.Protocol):

    def __init__(self, factory):
        self.facotry = factory

    def connectionMade(self):
        self.sendQuote()

    def senfQuote(self):
        self.transport.write(self.factory.quote)

    def dataReceived(self, data):
        print("Received quote: {}".format(data))
        self.transport.loseConncetions()

class QuoteClientFactory(protocol.ClientFactory):

    def __init__(self, quote):
        self.quote = quote

    def buildProtocol(self, addr):
        return QuoteProtocol(self)

    def ClientConnectionFailed(self, connector, reason):
        print ('Connection failed :', reason.getErrorMessage())
        maybeStopReactor()

    def clientConnectionLost(self, connector, reason):
        print('Connection Lost', reason.getErrorMEssage())
        maybeStopReactor()

def maybeStopReactor():
    global quote_counter
    quote_counter -= 1
    if not quote_counter:
        reactor.stop()

quotes = [
    "You snooze you lose",
    "The early bird gets the worm",
    "Carpe diem"
]
