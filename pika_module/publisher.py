import json
import pika

from decouple import config
from typing import Dict


class RabbitmqPublisher:
    def __init__(self) -> None:
        self.__host = config("RABBITMQ_HOST", default="localhost")
        self.__port = config("RABBITMQ_PORT", default=5672, cast=int)
        self.__username = config("RABBITMQ_USERNAME", default="guest")
        self.__password = config("RABBITMQ_PASSWORD", default="guest")
        self.__exchange = config("RABBITMQ_EXCHANGE", default="data_exchange")        
        self.__routing_key = ""
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        return channel
    
    def send_mensage(self, body: Dict):
        self.__channel.basic_publish(
            exchange=self.__exchange ,
            routing_key=self.__routing_key,
            body=json.dumps(body),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
