import pika

from decouple import config

class RabbitmqConsumer:
    def __init__(self, callback) -> None:
        self.__host = config("RABBITMQ_HOST", default="localhost")
        self.__port = config("RABBITMQ_PORT", default=5672, cast=int)
        self.__username = config("RABBITMQ_USERNAME", default="guest")
        self.__password = config("RABBITMQ_PASSWORD", default="guest")
        self.__queue = config("RABBITMQ_QUEUE", default="data_queue")
        self.__callback = callback
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

        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )

        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel

    def start(self):
        print(f"Consumindo o RabbitMQ no endereço {self.__host}:{self.__port}")
        try:
            self.__channel.start_consuming()
        except KeyboardInterrupt:
            print("Parando de consumir da fila.")

