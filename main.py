import tkinter as tk
import customtkinter as ctk
import subprocess
import threading
import queue
import re
import os
import time

# Initialize the queue for server output
output_queue = queue.Queue()

# Global variable for server process
server_process = None
server_running = False

# Ensure paths are correct
server_directory = os.path.dirname(os.path.abspath(__file__))

def start_server():
    global server_process, server_running
    if not server_running:
        # Command to run the batch file
        batch_file = os.path.join(server_directory, "start.bat")

        try:
            log_text.insert(ctk.END, f"Starting server with batch file: {batch_file}\n", "info")
            server_process = subprocess.Popen(
                batch_file,
                cwd=server_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=True,  # Important for running batch files
                text=True
            )
            server_running = True
            threading.Thread(target=read_output, daemon=True).start()
            start_stop_button.configure(text="Stop Server", command=stop_server)
            status_label.configure(text="Server Status: Running")
            log_text.insert(ctk.END, "Server started...\n", "start_stop")
        except Exception as e:
            log_text.insert(ctk.END, f"Error starting server: {e}\n", "error")

def stop_server():
    global server_process, server_running
    if server_process:
        try:
            server_process.stdin.write("stop\n")
            server_process.stdin.flush()
            server_process.terminate()
            server_process.wait()  # Wait for process to terminate
        except Exception as e:
            log_text.insert(ctk.END, f"Error stopping server: {e}\n", "error")
        finally:
            server_process = None
            server_running = False
            start_stop_button.configure(text="Start Server", command=start_server)
            status_label.configure(text="Server Status: Stopped")
            log_text.insert(ctk.END, "Server stopped...\n", "start_stop")

def read_output():
    global server_process
    while server_process:
        output = server_process.stdout.readline()
        if output:
            output_queue.put(output)
            update_player_list(output)
        if server_process.poll() is not None:
            log_text.insert(ctk.END, "Server process has stopped.\n", "error")
            handle_server_crash()

def handle_server_crash():
    global server_running
    server_running = False
    start_stop_button.configure(text="Start Server", command=start_server)
    status_label.configure(text="Server Status: Stopped")
    log_text.insert(ctk.END, "Server crashed or stopped unexpectedly. Restarting...\n", "error")
    time.sleep(5)  # Wait before restarting to avoid rapid restarts
    start_server()

def update_log():
    try:
        while True:
            line = output_queue.get_nowait()
            if "ERROR" in line:
                log_text.insert(ctk.END, line, "error")
            elif "INFO" in line:
                log_text.insert(ctk.END, line, "info")
            else:
                log_text.insert(ctk.END, line)
            log_text.see(ctk.END)
    except queue.Empty:
        pass
    root.after(100, update_log)

def send_command(event=None):
    command = command_entry.get()
    if server_process and command.strip():
        server_process.stdin.write(command + "\n")
        server_process.stdin.flush()
        command_entry.delete(0, tk.END)

def clear_log():
    log_text.delete(1.0, tk.END)

def update_player_list(output):
    join_pattern = re.compile(r'joined the game')
    leave_pattern = re.compile(r'left the game')
    list_pattern = re.compile(r'There are \d+ of a max of \d+ players online: (.*)')

    if join_pattern.search(output):
        player_name = output.split(' ')[-4]
        if player_name not in player_list.get(0, tk.END):
            player_list.insert(tk.END, player_name)

    elif leave_pattern.search(output):
        player_name = output.split(' ')[-4]
        if player_name in player_list.get(0, tk.END):
            player_list.delete(player_list.get(0, tk.END).index(player_name))

    elif list_pattern.search(output):
        players_section = list_pattern.search(output).group(1)
        player_names = [name.strip() for name in players_section.split(', ') if name.strip()]
        player_list.delete(0, tk.END)  # Clear the list
        for player in player_names:
            player_list.insert(tk.END, player)

def kick_player():
    selected_player_index = player_list.curselection()
    if selected_player_index:
        selected_player = player_list.get(selected_player_index)
        server_process.stdin.write(f"kick {selected_player}\n")
        server_process.stdin.flush()

# Initialize the main window
root = ctk.CTk()
root.title("Minecraft Server Panel")
root.geometry("800x400")

# Apply a dark theme
ctk.set_appearance_mode("dark")

# Configure grid layout to be resizable
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)

# Frame for the player list and kick button
left_frame = ctk.CTkFrame(root, fg_color="#2e2e2e")
left_frame.grid(row=1, column=0, sticky="ns", padx=10, pady=10, rowspan=2)

# Text widget for the server log
log_text = ctk.CTkTextbox(root, fg_color="#1e1e1e", text_color="#ffffff")
log_text.grid(row=1, column=1, columnspan=4, sticky="nsew", padx=10, pady=10)
log_text.tag_config("start_stop", foreground="cyan")
log_text.tag_config("error", foreground="red")
log_text.tag_config("info", foreground="green")

# Listbox for player names
player_list = tk.Listbox(left_frame, bg="#2e2e2e", fg="#ffffff", selectbackground="#444444", selectforeground="#ffffff", highlightthickness=0, bd=0)
player_list.pack(expand=True, fill=tk.BOTH)

# Button to kick the selected player
kick_button = ctk.CTkButton(left_frame, text="Kick Player", command=kick_player)
kick_button.pack(pady=5)

# Entry widget for command input
command_entry = ctk.CTkEntry(root, fg_color="#2e2e2e", text_color="#ffffff")
command_entry.grid(row=2, column=1, sticky="ew", padx=10)
command_entry.bind("<Return>", send_command)  # Bind Enter key to send_command function

# Button to send the command
send_button = ctk.CTkButton(root, text="Send", command=send_command, width=80, height=30)
send_button.grid(row=2, column=2, pady=5, padx=5)

# Button to clear the log
clear_button = ctk.CTkButton(root, text="Clear", command=clear_log, width=80, height=30)
clear_button.grid(row=2, column=3, pady=5, padx=5)

# Start/Stop server button
start_stop_button = ctk.CTkButton(root, text="Start", command=start_server, width=80, height=30)
start_stop_button.grid(row=2, column=4, pady=5, padx=5)

status_label = ctk.CTkLabel(root, text="Server Status: Stopped", text_color="#ffffff")
status_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

# Update log periodically
root.after(100, update_log)

# Run the main loop
root.mainloop()
