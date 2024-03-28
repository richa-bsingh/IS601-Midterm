"""Test the app"""
from app import App

def test_app_start_exit_command(capfd, monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    # Simulate user entering 'exit'
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    app.start()  # Start the application without expecting SystemExit

    # # Since there's no SystemExit, we can directly assert on the output if needed
    # captured = capfd.readouterr()
    # # Add assertions here if there's specific output expected upon exiting


def test_app_get_environment_variable(mocker):
    """Test the dot env variables"""
    # Patch the os.environ to simulate different environments
    mocker.patch.dict('os.environ', {'ENVIRONMENT': 'DEVELOPMENT'})
    app_dev = App()
    assert app_dev.get_environment_variable('ENVIRONMENT') == 'DEVELOPMENT', "Failed for DEVELOPMENT environment"

    mocker.patch.dict('os.environ', {'ENVIRONMENT': 'TESTING'})
    app_test = App()
    assert app_test.get_environment_variable('ENVIRONMENT') == 'TESTING', "Failed for TESTING environment"

    mocker.patch.dict('os.environ', {}, clear=True)  # Simulate no ENVIRONMENT variable set
    app_prod = App()
    assert app_prod.get_environment_variable('ENVIRONMENT') == 'PRODUCTION', "Failed for default PRODUCTION environment"

    # Additional check for the assertion you provided
    current_env = app_prod.get_environment_variable('ENVIRONMENT')
    assert current_env in ['DEVELOPMENT', 'TESTING', 'PRODUCTION'], f"Invalid ENVIRONMENT: {current_env}"

def test_app_start_unknown_command(capfd, monkeypatch):
    """Test how the REPL handles an unknown command before exiting."""
    # Simulate user entering an unknown command followed by 'exit'
    inputs = iter(['999', 'exit'])  # Use a command that's expected to be invalid
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    app = App()
    app.start()  # Start the application without expecting SystemExit

    # Verify that the unknown command was handled as expected
    captured = capfd.readouterr()
    assert "Invalid selection. Please enter a valid number." in captured.out or "Only numbers are allowed, wrong input." in captured.out
