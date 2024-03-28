from abc import ABC, abstractmethod
import logging
import pandas as pd
from datetime import datetime
import os

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}
        logging.info("CommandHandler initialized.")

    def register_command(self, command_name: str, command_instance: Command):
        self.commands[command_name] = command_instance
        logging.info(f"Command '{command_name}' registered.")

    def execute_command(self, command_name: str):
        try:
            logging.info(f"Executing command: {command_name}")
            self.commands[command_name].execute()
        except KeyError:
            logging.warning(f"No such command: {command_name}")
            print(f"No such command: {command_name}")

    def list_commands(self):
        logging.info("Listing available commands.")
        for index, command_name in enumerate(self.commands, start=1):
            print(f"{index}. {command_name}")

    def get_command_by_index(self, index: int):
        try:
            command_name = list(self.commands.keys())[index]
            return command_name
        except IndexError:
            logging.error("Attempted to access a command by an invalid index.")
            return None

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class CommandHistoryManager(metaclass=Singleton):
    def __init__(self):
        self.history_file = 'data/command_history.csv'
        if os.path.exists(self.history_file):
            self.history = pd.read_csv(self.history_file)
            # Ensure that only the latest 5 are loaded
            self.history = self.history.tail(5)
        else:
            self.history = pd.DataFrame(columns=['Timestamp', 'Command'])

    def add_command(self, command_name):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_entry = pd.DataFrame([[now, command_name]], columns=['Timestamp', 'Command'])
        self.history = pd.concat([self.history, new_entry], ignore_index=True).tail(5)
        self.save_history()

    def get_history(self):
        # Return a list of command names for backward compatibility
        return self.history['Command'].tolist()

    def clear_history(self):
        self.history = pd.DataFrame(columns=['Timestamp', 'Command'])
        self.save_history()

    def save_history(self):
        """Saves the current command history to a CSV file."""
        self.history.to_csv(self.history_file, index=False)

    def load_history(self):
        """Loads the command history from a CSV file into a DataFrame."""
        if os.path.exists(self.history_file):
            return pd.read_csv(self.history_file)
        return pd.DataFrame(columns=['Timestamp', 'Command'])