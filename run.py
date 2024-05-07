import subprocess
import platform
import pygetwindow as gw

def close_windows_by_title(title):
    windows = gw.getWindowsWithTitle(title)
    for window in windows:
        if window.title.startswith(title):
            window.close()
            print(f"Closed window: {window.title}")

def launch_node_server(os_type):
    command = "node server/server.js"
    if os_type == "Windows":
        proc = subprocess.Popen(f'start "Node Server" cmd /k {command}', shell=True)
    else:
        proc = subprocess.Popen(command, shell=True)
    return proc.pid

def launch_user_interface(os_type):
    ui_directory = "frontend"
    if os_type == "Windows":
        proc = subprocess.Popen(f'start "User Interface" /D {ui_directory} npm start', shell=True)
    else:
        proc = subprocess.Popen(f'cd {ui_directory} && npm start', shell=True)
    return proc.pid

def launch_agent_manager(os_type):
    if os_type == "Windows":
        proc = subprocess.Popen(f'start "Agent Manager" python agents/agent_manager.py', shell=True)
    else:
        proc = subprocess.Popen(f"python agents/agent_manager.py", shell=True)
    return proc.pid

def main():
    os_type = platform.system()
    pids = []

    # Launch Node server
    pids.append(launch_node_server(os_type))
    print("Node server launched.")

    # Launch User Interface
    pids.append(launch_user_interface(os_type))
    print("User interface launched.")

    # Launch Agent Manager
    pids.append(launch_agent_manager(os_type))
    print("Agent manager launched.")

    # Example: Stop all processes
    input("Press Enter to stop all processes...")
    close_windows_by_title("Node Server")
    close_windows_by_title("User Interface")
    close_windows_by_title("Agent Manager")
    close_windows_by_title("Windows PowerShell")

if __name__ == "__main__":
    main()
