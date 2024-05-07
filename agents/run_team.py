# run_team.py 

import subprocess
import platform
import json
import argparse
from dotenv import load_dotenv
import os
from src.repositories.TeamsRepository import TeamsRepository

teams_repository = TeamsRepository()

def launch_agent_same_window(profile_uuid):
    command = ["python", "agents/run_agent.py", "--profile_uuid", profile_uuid]
    subprocess.Popen(command)

def launch_agent_new_window(profile_uuid, os_type):
    if os_type == "Windows":
        command = f"start cmd /k python agents/run_agent.py --profile_uuid {profile_uuid}"
    elif os_type == "Darwin":
        command = f"osascript -e 'tell app \"Terminal\" to do script \"python agents/run_agent.py --profile_uuid {profile_uuid}\"'"
    elif os_type == "Linux":
        command = f"x-terminal-emulator -e python agents/run_agent.py --profile_uuid {profile_uuid}"
    else:
        # For unsupported OS, run in the same window
        return launch_agent_same_window(profile_uuid)

    print(f"Launching agent with command: {command}\n\n")

    subprocess.Popen(command, shell=True)

def main():
    parser = argparse.ArgumentParser(description='Launch a team of agents.')
    parser.add_argument('--team_uuid', help='UUID of the team to launch', required=True)
    parser.add_argument('--tile', action='store_true', help='Launch each agent in a new window')
    args = parser.parse_args()

    print(f"run_team.py: Launching team with UUID: {args.team_uuid}")
    print(f"run_team.py: Current working directory: {os.getcwd()}")

    team = teams_repository.get(args.team_uuid)
    profile_uuids = team['profile_uuids']

    os_type = platform.system()

    for profile_uuid in profile_uuids:

        if args.tile:
            launch_agent_new_window(profile_uuid, os_type)
        else:
            launch_agent_same_window(profile_uuid)

        print(f"Launched agent '{profile_uuid}'.")

if __name__ == "__main__":
    main()
