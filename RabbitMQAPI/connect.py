class ConncectRabbitMQ:

    def __init__(self, username=None, password=None, *kargs):

        if username == None or password == None:
            raise "Not input password or username"

        self.username=username
        self.password=password

        self.address = kargs[0]
        self.port = kargs[1]

    def connect(self):
        pass
