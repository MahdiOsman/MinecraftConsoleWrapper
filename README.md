```markdown
# Minecraft Server Control Panel

This project is a Python-based GUI application for controlling a Minecraft server. It allows you to start, stop, and interact with the server through a graphical interface, built using `tkinter` and `customtkinter`.

## Features

- **Start/Stop Server:** Easily start or stop the server using a single button.
- **Server Log:** Real-time log display of the server's output, including server information and errors.
- **Player Management:** View players currently connected to the server. Allows kicking players directly from the UI.
- **Command Entry:** Send commands directly to the server from the interface.
- **Crash Handling:** Automatically restart the server if it crashes unexpectedly.

## Requirements

- Python 3.x
- `tkinter` (usually comes pre-installed with Python)
- `customtkinter` library

To install `customtkinter`, you can use pip:

```bash
pip install customtkinter
```

## Installation and Setup

1. Clone this repository to your local machine:

```bash
git clone https://github.com/MahdiOsman/MinecraftConsoleWrapper.git
cd MinecraftConsoleWrapper
```

2. Place your Minecraft server's `start.bat` script in the same directory as the Python script.

3. Run the application using Python:

```bash
python main.py
```

## How It Works

- The GUI initializes with a **Start/Stop Server** button, a log window, a player list, and controls to send server commands and kick players.
- When you start the server, it will run the `start.bat` file located in the script's directory.
- The server's output is captured and displayed in real-time in the log window.
- Player join and leave events are detected and automatically update the player list.
- You can manually send commands or kick players through the GUI.

### File Structure

```
minecraft-server-panel/
│
├── server_panel.py      # Main application script
├── start.bat            # Minecraft server startup script (user provided)
└── README.md            # Project documentation
```

## Usage

- **Starting the Server:** Click the "Start Server" button to run the server. The log will show feedback once the server starts.
- **Stopping the Server:** Once the server is running, the "Start Server" button will turn into a "Stop Server" button. Click it to stop the server.
- **Sending Commands:** Type your command in the input box at the bottom and press "Send" or hit `Enter`.
- **Player Management:** The player list on the left side of the panel will show the names of currently connected players. Select a player and click "Kick Player" to remove them from the server.
- **Clearing the Log:** Click the "Clear" button to empty the log window.

## Notes

- Make sure the `start.bat` script properly starts your Minecraft server and is located in the same directory as `server_panel.py`.
- The server will automatically restart after a crash with a 5-second delay to avoid rapid restarts.

## Contributing

Contributions are welcome! If you encounter bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```

You can customize the file as needed (e.g., add your GitHub username in the clone link). This `README.md` provides an overview of your project, installation instructions, and details on how to use it.
