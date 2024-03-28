import sys
import logging
from app.commands import Command

class ExitCommand(Command):
    def execute(self):
        logging.info("Executing ExitCommand - Application exiting...")  # Log before exiting
        print("Exiting...")  # Optional: provide immediate feedback to the user in the terminal
        sys.exit(0)  # Use sys.exit(0) to indicate a clean exit