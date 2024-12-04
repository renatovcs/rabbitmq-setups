import pika

def setup_rabbitmq():
    # Configurações do RabbitMQ
    host = "localhost"
    port = 5672
    username = "guest"
    password = "guest"

    # Nome da exchange e fila
    exchange_name = "data_exchange"
    queue_name = "data_queue"
    routing_key = ""

    # Conexão
    credentials = pika.PlainCredentials(username, password)
    connection_parameters = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    # Criar a exchange
    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type="direct",
        durable=True
    )

    # Criar a fila
    channel.queue_declare(
        queue=queue_name,
        durable=True
    )

    # Criar o binding
    channel.queue_bind(
        exchange=exchange_name,
        queue=queue_name,
        routing_key=routing_key
    )

    print(f"Exchange '{exchange_name}' e fila '{queue_name}' criadas com sucesso!")
    connection.close()

if __name__ == "__main__":
    setup_rabbitmq()
