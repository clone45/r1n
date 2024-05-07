from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
from dotenv import load_dotenv
import atexit
import logging
from src.logging.logging_config import setup_papertrail_logging
from src.repositories.TeamsRepository import TeamsRepository


# Prepare and configure Papertrail logging
setup_papertrail_logging('agent_manager')
logger = logging.getLogger('agent_manager')

# Create a new Flask app
app = Flask(__name__)
CORS(app)

load_dotenv()

AGENTS_DIR = os.getenv('AGENTS_DIR', './agents')

teams_repository = TeamsRepository()

def cleanup_before_shutdown():
    print("Cleaning up resources before shutting down...")

def launch_agent_same_window(profile_uuid):
    agents_dir = os.getenv('AGENTS_DIR', './agents')
    script_path = os.path.join(agents_dir, 'run_agent.py')

    command = ["python", script_path, "--profile_uuid", profile_uuid]
    process = subprocess.Popen(command)
    
    return {'profile_uuid': profile_uuid, 'status': 'launched', 'pid': process.pid}

@app.route('/launch/<uuid>', methods=['POST'])
def launch_team(uuid):
    # team = load_team(uuid)
    team = teams_repository.get(uuid)
    if not team:
        return jsonify({'error': f"Team with UUID {uuid} does not exist."}), 404
    
    profile_uuids = team['profile_uuids']
    agent_count = len(profile_uuids)

    responses = []

    for profile_uuid in profile_uuids:
        response = launch_agent_same_window(profile_uuid)
        responses.append(response)

    return jsonify({'message': f"Launched team with UUID: {uuid}", 'agents': responses, 'agent_count': agent_count})


@app.route('/teams', methods=['GET'])
def get_teams():
    # teams = load_teams_and_profiles()
    teams = teams_repository.list_teams_and_profiles()
    if teams is not None:
        return jsonify(teams)
    else:
        return jsonify({'error': 'Failed to load teams and profiles'}), 500


@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})

# Register the cleanup function
atexit.register(cleanup_before_shutdown)

if __name__ == "__main__":

    pid = os.getpid()

    logger.info(f"=== Starting Agent Manager PID:{pid} ===")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    app.run(debug=False, port=8000)
