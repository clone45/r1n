# run_agent.py
#
# This is the main entry point for the Agent. 
# It initializes the agent and the IO handler, and then listens for incoming messages. 
 
import os
import sys
import argparse
import signal
import json
import uuid
import logging
from src.logging.logging_config import setup_papertrail_logging
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import default
from src.repositories.ProfilesRepository import ProfilesRepository
from src.repositories.RolesRepository import RolesRepository

# Prepare and configure Papertrail logging
setup_papertrail_logging('run_agent')
logger = logging.getLogger('run_agent')

# Import the Agent and CommandLineIOHandler classes
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.agents.agent_factory import AgentFactory
from src.io.rabbit_mq_io_handler import RabbitMQIOHandler

agent = None

profiles_repository = ProfilesRepository()
roles_repository = RolesRepository()

def signal_handler(signum, frame):
    global agent
    if agent is not None:
        print("Ctrl-C detected, shutting down agent...")
        agent.shutdown()
    sys.exit(0)

#
# receive message from the message queue
# Typically this will come either the user interface or from another agent

def receive_message(ch, method, properties, body):

    global agent

    ch.basic_ack(delivery_tag=method.delivery_tag)

    # Check if body is a json string.  If not, log a warning and return
    try:
        incoming_message = json.loads(body.decode())
    except json.JSONDecodeError as e:
        logger.warn(f"Message not JSON: {body}")
        return

    logger.debug(f"Received message: {json.dumps(incoming_message)}"); 

    if incoming_message["message_type"] == "ui.ready":
        agent.notify_ui_of_new_agent()
        return
    
    if incoming_message["message_type"] == "system.register_presence":
        agent.register_presence()
        return
    
    if incoming_message["message_type"] == "team.dismiss":
        agent.shutdown(incoming_message)
        return
    
    if incoming_message["message_type"] == "message":
        agent.interact(incoming_message)
        return
    
    if incoming_message["message_type"] == "file.upload":
        agent.upload_file(incoming_message)
        return

    # Complain 
    logger.warn(f"Unhandled message: {json.dumps(incoming_message)}")


def main():

    global agent

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Load the environment variables
    load_dotenv()

    logger.info("======== Starting run_agent.py ========")

    amqp_domain = os.getenv('AMQP_DOMAIN', 'localhost')
    amqp_port = os.getenv('AMQP_PORT', '5672')
    amqp_username = os.getenv('RABBITMQ_USER', 'guest')
    amqp_password = os.getenv('RABBITMQ_PASS', 'guest')

    # Argument parsing
    parser = argparse.ArgumentParser(description='Run the OpenAI Agent')
    parser.add_argument('--reset', action='store_true', help='Re-register the assistance')
    parser.add_argument('--instance_uuid', default=str(uuid.uuid4()), help='The agent instance UUID')
    parser.add_argument('--thread', default='', help='Optional.  Used to continue an existing conversation.')
    parser.add_argument('--profile_uuid', help='Specify the agent profile UUID')

    args = parser.parse_args()

    logger.info(json.dumps({
        "AMQP_DOMAIN": amqp_domain,
        "AMQP_PORT": amqp_port,
        "AMQP_USERNAME": amqp_username,
        "CWD": os.getcwd(),
        "SYS_PATH": sys.path,
        "instance_uuid": args.instance_uuid,
        "profile_uuid": args.profile_uuid,
        "thread": args.thread
    }, default=default))

    # Determine the agent's queue and outbox names
    instance_uuid = args.instance_uuid
    agent_general_queue_name = f"queue_{instance_uuid}"  # Inbox for receiving messages

    # The profile_uuid is used to reference the profile file name in config/profiles
    # An example is config/profiles/7e86b06a-f896-4b4e-b7c4-7ab44fe42ab0.json
    # Example contents of the profile file:
    # {
    #     "uuid": "7e86b06a-f896-4b4e-b7c4-7ab44fe42ab0",    
    #     "name": "Rin",
    #     "role_uuid": "54f9fd90-7205-450e-a195-24e9b43bbb25",
    #     "avatar": "rin.png",
    #     "description": "You are a friendly agent named Rin.",
    #     "welcome_message": "Hey... I'm glad you're here."
    # }

    profile_data = profiles_repository.get(args.profile_uuid)
    role_data = roles_repository.get(profile_data['role_uuid'])

    # get string containing profile data json
    logger.debug(f"Profile data: {json.dumps(profile_data, default=default)}")
    logger.debug(f"Role data: {json.dumps(role_data, default=default)}")

    # Initialize the IO handler with the callback
    logger.debug(f"Instantiating io_handler for general messaging")

    queues = [
        {"queue": agent_general_queue_name, "callback": receive_message, "exchanges": ["broadcast_queue"]}
    ]

    # amqp_url = f"amqp://{amqp_username}:{amqp_password}@{amqp_domain}:{amqp_port}"
    io_handler = RabbitMQIOHandler(
        domain=amqp_domain, 
        port=amqp_port,
        username=amqp_username,
        password=amqp_password,
        queues=queues
    )
    
    # Initialize the primary agent with the IO handler, the LLM adapter, and the message logger
    logger.debug(f"Instantiating Agent from role {profile_data['role_uuid']} and reset_assistant: {args.reset}")

    #
    # Create the agent using the AgentFactory
    #

    factory = AgentFactory()

    agent = factory.create_agent(
        instance_uuid=instance_uuid,
        profile=profile_data,
        role=role_data,
        reset_assistant=args.reset,
        thread=args.thread,
        io_handler=io_handler)

    # print the agent's name and PID
    logger.debug(f"Listening for incoming message on {agent_general_queue_name}")

    io_handler.start_consuming()

    # keep the agent running indefinitely
    while True:
        pass


if __name__ == '__main__':
    main()
