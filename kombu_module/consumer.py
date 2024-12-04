from kombu import Connection, Queue, Consumer, Exchange
from decouple import config

class RabbitmqConsumer:
    def __init__(self, callback):
        self.__host = config("RABBITMQ_URL", default="amqp://guest:guest@localhost:5672/")
        self.__queue = config("RABBITMQ_QUEUE", default="data_queue")
        self.__callback = self.__wrap_callback(callback)
        self.__connection = Connection(self.__host)
        self.__queue_instance = self.__create_queue()

    def __create_queue(self):
        exchange = Exchange("default", type="direct", durable=True)
        queue = Queue(name=self.__queue, exchange=exchange, routing_key=self.__queue, durable=True)
        queue.declare(channel=self.__connection.channel())
        return queue

    def __wrap_callback(self, callback):
        def kombu_callback(body, message):
            ch = None  # Kombu não fornece canal diretamente
            method = None  
            properties = message.properties  # Propriedades da mensagem
            callback(ch, method, properties, body)
            message.ack()  # Confirma a mensagem manualmente
        return kombu_callback

    def start(self):
        print(f"Consumindo o RabbitMQ no endereço {self.__host}:{self.__port}")
        with Consumer(self.__connection, queues=[self.__queue_instance], callbacks=[self.__callback], accept=["json"]):
            try:
                while True:
                    try:
                        self.__connection.drain_events(timeout=10)
                    except TimeoutError:
                        print("Sem mensagens por enquanto.")
            except KeyboardInterrupt:
                print("Parando de consumir da fila.")
