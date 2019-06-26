from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, protocol
#from hashlib import hash256
'''
class ReplicationAction:

    def __init__(self):
        pass

    def firewall(self):
        pass
'''

class ReplicaManagerProtocol(LineReceiver):

    def __init__(self, factory):
        self.factory = factory
        self.statusCode = 200
        self.state = 'NEW'

    def lineReceived(self, line):

        if self.state == 'NEW':
            self.handle_NEW(line)

    def connectionLost(self, reason):
        self.sendLine("200".encode())

    def handle_NEW(self, line):
        print(self.state)

        if not self.factory.Primary:
            self.state = 'CLOSE'
            self.statusCode = 300
            self.handle_CLOSE()

        self.state = "REGISTER"
        self.handle_REGISTER(line)

    def handle_REGISTER(self, line):

        print(self.state)
        self.factory.clients[hash(self)] = self
        print(self.factory.clients)

        '''
        if hash(line) in self.factory.requests.items():
            self.state = 'RESPONSE'
            self.statusCode = 100
            self.handle_RESPONSE()
            return

        self.factory.clients[ hash(line) ] = self
        self.handle_EXECUTION(line)
        '''
        self.connectionLost('OK')
        return

    def handle_EXECUTION(self, req):

        '''
        try:
            self.rabbit = RabbitMQ()
        except:
            print("Error ReplicaManagerProtocol - ReqServer - rabbit ")

        self.rabbit.publisher(req)
        '''

    def handle_AWAIT(self):
        pass

    def handle_COORDINATION(self):
        pass

    def handle_REPLICATION(self):
        pass

    def handle_RESPONSE(self):
        pass

    def handle_CLOSE(self):
        pass

class ReplicaManagerServer(Factory):

    '''
        Class Factory for connection mode
    '''

    def __init__(self):
        self.clients = {}
        self.Primary = True

    def buildProtocol(self, addr):
        return ReplicaManagerProtocol(self)

reactor.listenTCP(9000, ReplicaManagerServer())
reactor.run()
