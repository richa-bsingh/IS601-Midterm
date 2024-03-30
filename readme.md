# Midterm - Advanced Python Calculator

## Project Overview
This is an advanced Python-based calculator application. This application is designed to underscore integrates clean, maintainable code, the application of design patterns, comprehensive logging, dynamic configuration via environment variables, sophisticated data handling with Pandas, and a command-line interface (REPL) for real-time user interaction.

## Functionalities Implemented
### Running the app - `python main.py`.

![alt text](<md-docs/Screenshot 2024-03-29 at 7.11.42 PM.png>)

For detail description of all the commands showcased above: Please view [Commands](md-docs/commands.md)

### Command-Line Interface (REPL)
Implemented a Read-Eval-Print Loop (REPL) to facilitate direct interaction with the calculator, history and openAI command.
- Execution of arithmetic operations (Add, Subtract, Multiply, and Divide) are supported for calculator.
- Management of calculation history (Load, Save, Clear, Delete).
- Access to extended functionalities through dynamically loaded plugins.

### Plugin System
Created a flexible plugin system to allow seamless integration of new commands or features. This system allows:
- Dynamically load and integrate plugins without modifying the core application code.
- Include a REPL  "Menu" command to list all available plugin commands, ensuring user discoverability and interaction. 

### Calculation History Management with Pandas
Utilized Pandas to manage a robust calculation history, enabling users to:
- Load, save, clear, and delete history records through the REPL interface.

### Professional Logging Practices
Established a comprehensive logging system to record:
- Detailed application operations, data manipulations, errors, and informational messages.
- Differentiate log messages by severity (INFO, WARNING, ERROR) for effective monitoring.
- Dynamic logging configuration through environment variables for levels and output destinations.

### Advanced Data Handling with Pandas
Employ Pandas for:
- Efficient data reading and writing to CSV files.
- Managing calculation history.

### Design Patterns for Scalable Architecture (to check w tabrez)
Incorporated key design patterns to address software design challenges. Below are the features and the incorporated design patterns implemented for them:
- **Command Pattern:** Organise REPL instructions to facilitate efficient calculations and history management.
- **Singleton Pattern:** A single instance of a class is guaranteed by the singleton pattern, which also offers a global point of access to it. The Singleton pattern is used by the `CommandHistoryManager` class.
- **Factory Method:** Using this design approach, the menu command loads all registered plugins as app commands by accepting an instance of `commandHandler`.
- **Memento Pattern:** The Memento pattern, which is used to externalise and capture an object's internal state so that the object can be restored to that state later, is similar in functionality to `CommandHistoryManager`.
- **Strategy Pattern:** The operations within HistoryCommand (load history, save history, clear history, delete history record) can be seen as different strategies for handling command history. Each operation is encapsulated within its method.

Please view [Design Patterns](md-docs/designpattern.md) for additional details on how each design pattern is implemented and what is the challenge that it covers.

## Development, Testing, and Documentation Completions
### Testing and Code Quality
- Achieve a 90% test coverage with Pytest.
- Ensured the code quality and adherence to PEP 8 standards, verified by Pylint.
![alt text](<md-docs/Screenshot 2024-03-29 at 7.13.53 PM.png>)

### Version Control Best Practices
- Utilize logical commits that clearly group feature development and corresponding tests, evidencing clear development progression.

### Comprehensive Documentation
The entire development process is documented in various md files for detailed explanation and references.

## Demo Video:
<a href="http://www.youtube.com/watch?feature=player_embedded&v=yUtpDwKM-vg
" target="_blank"><img src="https://img.youtube.com/vi/yUtpDwKM-vg/3.jpg" 
alt="Demo video" width="240" height="180" border="3"/></a>

# Features added in the application:
#### Functionality
- **Calculator Operations**
- **History Management**
- **Configuration via Environment Variables**
- **REPL Interface**

#### Design Patterns
- **Implementation and Application**
- **Documentation and Explanation**

#### Testing and Code Quality
- **Comprehensive Testing with Pytest**
- **Code Quality and Adherence to Standards**

#### Version Control, Documentation, and Logging
- **Commit History**
- **README Documentation**
- **Logging Practices**