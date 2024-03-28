"""Test all the commands of the app"""
import logging
import sys
from unittest.mock import MagicMock, patch
import pytest
from app import App

from app.commands import Command, CommandHandler, CommandHistoryManager
from app.plugins.calculator import CalculatorCommand
from app.plugins.history import HistoryCommand
from app.plugins.menu import MenuCommand

def test_app_greet_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'greet' command and its logging."""
    inputs = iter(['3', 'exit'])
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
    inputs = iter(['5','0','exit'])
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
    """Class mocker for performing addition"""
    def execute(self):
        logging.info("Performing addition")

class MockSubtractCommand(Command):
    """Class mocker for performing subtraction"""
    def execute(self):
        logging.info("Performing subtraction")

@pytest.fixture
def mock_operations(monkeypatch):
    """Mock the load_operations method to return a fixed set of operations"""
    def mock_load_operations(self):
        return {'1': MockAddCommand(), '2': MockSubtractCommand()}
    monkeypatch.setattr(CalculatorCommand, "load_operations", mock_load_operations)

def test_calculator_display_operations_and_exit(capfd, monkeypatch, mock_operations):
    """Simulate user selecting '0' to exit the operations menu"""
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
    """Simulate user selecting an operation ('1'), entering two numbers, and then choosing to exit ('0')"""
    inputs = ['1', '2', '3', '0']  # Example: '1' to select the first operation, '2' and '3' as operands, '0' to exit
    input_generator = (input for input in inputs)
    monkeypatch.setattr('builtins.input', lambda _: next(input_generator))

    calculator_cmd = CalculatorCommand()
    calculator_cmd.execute()

    captured = capfd.readouterr()
    # Adjust the assertion to match the actual expected result output
    assert "The result is 5.0" in captured.out
class MockCommand(Command):
    """Mock commands to register with the CommandHandler"""
    def execute(self):
        print("Mock command executed.")

@pytest.fixture
def command_handler_with_commands():
    """pytest fixtures"""
    handler = CommandHandler()
    handler.register_command('test', MockCommand())
    handler.register_command('help', MockCommand())
    return handler

def test_menu_command_display_and_exit(capfd, monkeypatch, command_handler_with_commands):
    """Mock input to select '0' and exit"""
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
    """Simulate an invalid selection followed by exit"""
    inputs = iter(['999', '0'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # Mock sys.exit to prevent the test from exiting
    monkeypatch.setattr(sys, 'exit', MagicMock())

    menu_cmd = MenuCommand(command_handler_with_commands)
    menu_cmd.execute()

    captured = capfd.readouterr()
    assert "Invalid selection. Please enter a valid number." in captured.out

def test_app_divide_command_success(capfd, monkeypatch, caplog):
    """Test successful division."""
    inputs = iter(['1', '2', '2', '2', '0', 'exit'])  # Simulate user inputs for the numbers and exiting
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output for successful division
        captured = capfd.readouterr()
        assert "The result is 1.0" in captured.out

        # Check the log messages for successful execution
        assert "Executing Divide command." in caplog.text
        assert "Division result: 1.0" in caplog.text

def test_app_divide_command_zero_division(capfd, monkeypatch, caplog):
    """Test division by zero scenario."""
    # Ensure the sequence of inputs matches the expected application flow.
    # The addition of 'exit' at the end ensures the application loop can terminate gracefully.
    inputs = iter(['1', '2', '10', '0', '0', 'exit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.WARNING):
        app = App()
        app.start()

        captured = capfd.readouterr()
        assert "Cannot divide by zero. Please enter a valid second number." in captured.out or "Invalid selection. Please enter a valid number." in captured.err

def test_app_multiply_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'multiply' command and its logging."""
    # Assuming '3' selects the Multiply command in your command list, followed by the numbers to multiply
    inputs = iter(['1', '3', '5', '4', '0', 'exit'])  # Adjust '3' if the position of Multiply command differs
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output
        captured = capfd.readouterr()
        assert "The result is 20.0" in captured.out

        # Now, check the log messages
        assert "Executing Multiply command." in caplog.text
        assert "Multiplication result: 20.0" in caplog.text

def test_app_subtract_command(capfd, monkeypatch, caplog):
    """Test that the REPL correctly handles the 'subtract' command and its logging."""
    # Assuming '4' selects the Subtract command in your command list, followed by the numbers to subtract
    inputs = iter(['1', '4', '10', '3', '0', 'exit'])  # Adjust '4' if the position of Subtract command differs
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with caplog.at_level(logging.INFO):
        app = App()
        app.start()

        # Capture and assert the expected output for subtraction
        captured = capfd.readouterr()
        assert "The result is 7.0" in captured.out

        # Now, check the log messages for the execution of the Subtract command
        assert "Executing Subtract command." in caplog.text
        assert "Subtraction result: 7.0" in caplog.text


@pytest.fixture
def mock_command_history_manager():
    """Mock history manager"""
    with patch('app.commands.CommandHistoryManager', autospec=True) as mock:
        # Setup mock to return a predefined history
        mock.return_value.get_history.return_value = ['greet', 'exit']
        yield mock

def test_app_history_command_operations(mock_command_history_manager, capfd, caplog):
    """Test history command in REPL"""
    # Setup the input values for the test to simulate user selecting 'Load History' and then 'Back'
    with patch('builtins.input', side_effect=['6', '1', '0']):
        history_command = HistoryCommand()
        history_command.execute()

    # Capture and assert the expected output for loading the history
    captured = capfd.readouterr()
    expected_output_lines = ["Command History Operations:", "1. Load History", "2. Save History", "3. Clear History", "4. Delete History Record"]
    for expected_line in expected_output_lines:
        assert expected_line in captured.out

    # Test 'Clear History' operation by simulating user input
    with patch('builtins.input', side_effect=['3', '0', 'exit']):
        with patch.object(CommandHistoryManager, 'clear_history', autospec=True) as mock_clear_history:
            history_command.execute()
            mock_clear_history.assert_called_once()

    # Capture output to check clear history operation confirmation
    captured = capfd.readouterr()
    assert "History cleared successfully." in captured.out
