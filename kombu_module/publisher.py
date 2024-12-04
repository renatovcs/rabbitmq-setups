import json
from kombu import Connection, Exchange, Producer
from decouple import config
from typing import Dict

class RabbitmqPublisher:
    def __init__(self) -> None:
        self.__host = config("RABBITMQ_URL", default="amqp://guest:guest@localhost:5672/")
        self.__exchange_name = config("RABBITMQ_EXCHANGE", default="data_exchange")
        self.__exchange_type = config("RABBITMQ_EXCHANGE_TYPE", default="direct")
        self.__routing_key = config("RABBITMQ_ROUTING_KEY", default="")
        self.__connection = self.__create_connection()
        self.__exchange = self.__create_exchange()

    def __create_connection(self):
        # Cria a conexão com o RabbitMQ
        return Connection(self.__host)

    def __create_exchange(self):
        # Declara a troca (Exchange)
        return Exchange(self.__exchange_name, type=self.__exchange_type, durable=True)

    def send_message(self, body: Dict):
        # Publica a mensagem na Exchange com o routing_key
        with self.__connection as connection:
            producer = Producer(connection)
            producer.publish(
                body,
                exchange=self.__exchange,
                routing_key=self.__routing_key,
                serializer="json",
                declare=[self.__exchange],  # Declara a troca automaticamente, caso não exista
            )
            print(f"[RabbitmqPublisher] Sent: {body}")

