from app.commands import Command
import pytest
from app import App
from unittest.mock import MagicMock
from app.plugins.calculator import CalculatorCommand
import sys
from app.commands import CommandHandler
from app.plugins.menu import MenuCommand
import logging

def test_app_greet_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'greet' command and its logging."""
    inputs = iter(['6', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output
        captured = capfd.readouterr()
        assert "Hello, World!" in captured.out

        # Now, check the log messages
        assert "Executing GreetCommand." in caplog.text
        assert "GreetCommand executed successfully." in caplog.text




def test_app_menu_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'menu' command and its logging."""
    inputs = iter(['7','0','exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        try:
            app.start()  # Start the application without expecting SystemExit

            # Capture and assert the expected output
            captured = capfd.readouterr()
            assert "Available commands:" in captured.out
            # Assert that the menu display was logged
            assert "Displaying main menu to user." in caplog.text

            # Since the user selects 'exit', which is simulated by input, check the log for exit confirmation
            assert "User selected to exit the program." in caplog.text
        except SystemExit as e:
            assert str(e) == "Exiting program."

# Mock operation classes
class MockAddCommand(Command):
    def execute(self):
        logging.info("Performing addition")

class MockSubtractCommand(Command):
    def execute(self):
        logging.info("Performing subtraction")

@pytest.fixture
def mock_operations(monkeypatch):
    # Mock the load_operations method to return a fixed set of operations
    def mock_load_operations(self):
        return {'1': MockAddCommand(), '2': MockSubtractCommand()}
    monkeypatch.setattr(CalculatorCommand, "load_operations", mock_load_operations)

def test_calculator_display_operations_and_exit(capfd, monkeypatch, mock_operations):
    # Simulate user selecting '0' to exit the operations menu
    monkeypatch.setattr('builtins.input', lambda _: '0')
    calculator_cmd = CalculatorCommand()
    calculator_cmd.execute()

    captured = capfd.readouterr()
    assert "\nCalculator Operations:" in captured.out
    assert "1. MockAddCommand" in captured.out
    assert "2. MockSubtractCommand" in captured.out
    assert "0. Back" in captured.out

# inputs = iter(['1', '0'])
# monkeypatch.setattr('builtins.input', lambda _: next(inputs, 'default_value'))

def test_calculator_execute_operation(capfd, monkeypatch):
    # Simulate user selecting an operation ('1'), entering two numbers, and then choosing to exit ('0')
    inputs = ['1', '2', '3', '0']  # Example: '1' to select the first operation, '2' and '3' as operands, '0' to exit
    input_generator = (input for input in inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))

    calculator_cmd = CalculatorCommand()
    calculator_cmd.execute()

    captured = capfd.readouterr()
    # Adjust the assertion to match the actual expected result output
    assert "The result is 5.0" in captured.out


# Mock commands to register with the CommandHandler
class MockCommand(Command):
    def execute(self):
        print("Mock command executed.")

@pytest.fixture
def command_handler_with_commands():
    handler = CommandHandler()
    handler.register_command('test', MockCommand())
    handler.register_command('help', MockCommand())
    return handler

def test_menu_command_display_and_exit(capfd, monkeypatch, command_handler_with_commands):
    # Mock input to select '0' and exit
    monkeypatch.setattr('builtins.input', lambda _: '0')
    # Mock sys.exit to prevent the test from exiting
    mock_exit = MagicMock()
    monkeypatch.setattr(sys, 'exit', mock_exit)
    
    menu_cmd = MenuCommand(command_handler_with_commands)
    menu_cmd.execute()

    captured = capfd.readouterr()
    assert "\nMain Menu:" in captured.out
    assert "1. Test" in captured.out
    assert "2. Help" in captured.out
    assert "Enter the number of the command to execute, or '0' to exit." in captured.out
    mock_exit.assert_called_once_with("Exiting program.")  # Verify sys.exit was called

def test_menu_command_invalid_selection(capfd, monkeypatch, command_handler_with_commands):
    # Simulate an invalid selection followed by exit
    inputs = iter(['999', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # Mock sys.exit to prevent the test from exiting
    monkeypatch.setattr(sys, 'exit', MagicMock())

    menu_cmd = MenuCommand(command_handler_with_commands)
    menu_cmd.execute()

    captured = capfd.readouterr()
    assert "Invalid selection. Please enter a valid number." in captured.out