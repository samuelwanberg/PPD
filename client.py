#!/usr/bin/env python
import pika
import uuid
import os
import time
import random

class Pacient:

    def __init__(self, name):

        self.name = name
        credentials = pika.PlainCredentials('admin', 'password')
        self.connection = pika.BlockingConnection(
                 pika.ConnectionParameters(host='rabbitmq.catalao.ufg.br', credentials=credentials))

        self.channel = self.connection.channel()
        # Fila de callback para receber mesg de retorno do servidor, exclusive=True garante não persistência da fila
        result = self.channel.queue_declare(self.name)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True )# confirmação e sincronização do recebimento do procedimento remoto

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id: # Condição de parada no caso que a resposta do procedimento for correta
            self.response = body

    def call(self, n):
        self.response = None # response remote procedure call
        self.corr_id = str(uuid.uuid4()) # metodo que gera um uuid unico para indentificao do objeto, sendo gerado randomicamente (uuid4())

        self.channel.basic_publish(
            exchange='',  # exchange padrão
            routing_key=self.name,  # Conectar Fila que ira acionar procedimento remoto
            properties=pika.BasicProperties(
                reply_to=self.callback_queue, # Submete ao servidor rpc fila de callback para restulado da chamada RPC
                correlation_id=self.corr_id, # Útil para Correlaciona as respostas das chamadas RPC
                ),
            body=str(n)) # Corpo da messagem ou argumento da função fibonacci invocada remotamente

        while self.response is None:
            self.connection.process_data_events()

        return int(self.response)

def medicaoPressaoSist():
    return random.choice(range(50,221))

def medicaoPressaoDist(sist):
    return random.choice(range(20, sist - 20))

def call():
    pacient = Pacient('SamuelWanberg')
    i = 0
    while(i <= 1000):
        sist = int(medicaoPressaoSist())
        dist = medicaoPressaoDist(sist)
        print("{0} {1}".format(sist, dist))
        i = i+1
call()
