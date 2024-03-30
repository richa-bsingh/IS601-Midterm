# Design Patterns Implemented in the project

## Command Pattern: 
The Command pattern is especially helpful in a Read-Eval-Print Loop (REPL) application for the following reasons:

- Modularity: The application's structure is tidy and well-organized since each command is contained in its own class.
- Extensibility: Easy updates and maintenance are made possible by the simple addition of new commands, which don't need changing the existing code.
- Undo Operations: Facilitates the implementation of undo capabilities by preserving a record of instructions executed, hence enabling users to effortlessly undo activities.
- Separation of Concerns: This improves code readability and streamlines the main loop by separating the parsing of the input from the execution of the command.
- Easier Testing: By allowing commands to be tested independently, the application's testability and dependability are increased.
In essence, the Command pattern keeps user-friendly, manageable, and scalable REPL programs.


## Singleton Pattern:
A class is guaranteed to have a single instance according to the Singleton pattern, which also offers a global point of access to it. This is very helpful for:

- Controlled Access: This guarantees restricted access to the single instance, which is essential for coordinating system-wide actions.
- Resource Management: Perfect for overseeing configurations or resources that are shared by the entire system.
- Consistency: As each code accesses a single instance, this ensures consistency for stateful information.


## Factory Method:
Although the Factory Method pattern specifies an interface for object creation, subclasses are free to modify the kind of objects that are created. It is advantageous because:

- Flexibility: The class has the option to provide subclasses control over object creation by delegating instantiation to them.
- Extensibility: Increases extensibility by allowing the addition of new product kinds without altering the code of the current factory.
- Decoupling: Encourages loose coupling by reducing the reliance between the application and concrete classes.


## Memento Pattern: 
In order to enable the item to be restored to its original state at a later time, the Memento pattern externalizes and records an object's internal state. Among its benefits are:

- Undo Functionality: Enables the state of an object to be rolled back to a prior state, making it easier to build undo procedures in applications.
- State preservation: Provides for the preservation and restoration of state without disclosing implementation specifics.
- Snapshot handling: helpful for saving copies of the states of applications that can be restored at a later time.


## Strategy Pattern: 
The Strategy pattern encapsulates, defines, and renders compatible a family of algorithms. As a result, the algorithm can change without affecting the clients that use it. Among its advantages are:

Flexibility: A major source of flexibility is the ability for clients to change algorithms (strategies) at runtime.
Isolation: Removes algorithm implementation specifics from the code that utilizes them.
Extension: The application is more extensible when new strategies are added without altering the context.

The HistoryCommand class acts as the context in the Strategy pattern analogy. It maintains a reference to one of the concrete strategies and delegates it to handle the request. The context is configured with a concrete strategy by the user's choice from the menu (load_history, save_history, clear_history, delete_history_record).
