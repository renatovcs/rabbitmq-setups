from pika_module.publisher import RabbitmqPublisher as PikaPublisher
from pika_module.consumer import RabbitmqConsumer as PikaConsumer
from kombu_module.publisher import RabbitmqPublisher as KombuPublisher
from kombu_module.consumer import RabbitmqConsumer as KombuConsumer
from pika_module.setup import setup_rabbitmq

def my_callback(ch, method, properties, body):
    print(body)

rabbitmq_publisher = PikaPublisher()
rabbitmq_publisher.send_mensage({"ola": "mundo"})

rabbitmq_consumer = PikaConsumer(my_callback)
rabbitmq_consumer.start()

# rabbitmq_publisher = KombuPublisher()
# rabbitmq_publisher.send_message({"ola": "mundo"})

# rabbitmq_consumer = KombuConsumer(my_callback)
# rabbitmq_consumer.start()
