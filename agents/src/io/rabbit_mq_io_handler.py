import pika
import json
import time

class RabbitMQIOHandler:
    def __init__(self, domain, port, username, password, queues=None):
        if queues is None:
            queues = []

        # self._connection = pika.BlockingConnection(pika.URLParameters(amqp_url))

        # Setup the credentials and connection parameters
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters(host=domain,
                                                  port=port,
                                                  credentials=credentials)

        # Try to establish a connection
        self._connection = pika.BlockingConnection(parameters)

        self._channel = self._connection.channel()

        for queue_info in queues:
            queue_name = queue_info['queue']
            callback = queue_info['callback']
            exchanges = queue_info.get('exchanges', [])

            # Declare the queue
            self._channel.queue_declare(queue=queue_name, durable=True)

            # Declare exchanges and bind the queue to these exchanges
            for exchange in exchanges:
                self._channel.exchange_declare(exchange=exchange, exchange_type='fanout')
                self._channel.queue_bind(exchange=exchange, queue=queue_name)

            # Set up the consumer
            self._channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)


    def start_consuming(self):
        try:
            print("[*] Waiting for messages. To exit press CTRL+C")
            self._channel.start_consuming()
        except KeyboardInterrupt:
            self._channel.stop_consuming()
        finally:
            self._connection.close()

    def channel_is_closed(self):
        return self._channel.is_closed
    
    def channel_is_open(self):
        return self._channel.is_open

    def stop_consuming(self):
        self._channel.stop_consuming()

    def send_output(self, from_name: str, from_queue: str, from_persona: str, to_name: str, to_queue: str, to_persona: str, cc_queue: str = "", message_type: str = "message", content: str = ""):
        message_data = {
            "content": content,
            "from_name": from_name,
            "from_queue": from_queue,
            "from_persona": from_persona,
            "to_name": to_name,
            "to_queue": to_queue,
            "to_persona": to_persona,
            "cc_queue": cc_queue,
            "message_type": message_type,
            "timestamp": time.time()
        }

        print(f"Sending message {message_data} to {to_queue}")

        # Convert the dictionary to a JSON string
        message_json = json.dumps(message_data)

        # Ensure the channel is open
        if self._channel is None or not self._channel.is_open:
            print("Channel is not open. Message not sent.")
            return

        # Send the message
        self._channel.basic_publish(exchange='',
                                    routing_key=to_queue,
                                    body=message_json)
        
        if cc_queue:
            self._channel.basic_publish(exchange='',
                                        routing_key=cc_queue,
                                        body=message_json)
        
    def broadcast_message(self, to_exchange: str, message_type: str, content: str):
        message_data = {
            "content": content,
            "message_type": message_type,
            "timestamp": time.time()
        }

        # Convert the dictionary to a JSON string
        message_json = json.dumps(message_data)

        # Ensure the channel is open
        if self._channel is None or not self._channel.is_open:
            print("Channel is not open. Message not sent.")
            return

        # Send the message
        self._channel.basic_publish(exchange=to_exchange,
                                    routing_key='',
                                    body=message_json)

    def graceful_shutdown(self):
        if self._channel is not None and self._channel.is_open:
            self._channel.close()