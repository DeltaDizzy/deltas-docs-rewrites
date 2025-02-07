# Overview

!!! note
    This site discusses command-based programming as defined by WPILib 2023-2025 (Commands v2 with Triggers and Command Factories). When Coroutines/Continuations (Commands v3) are merged into main (NET 2027) they may be added to these docs.

The WPILib commands framework approaches multitasking by dividing code into 3 categories:

- Subsystems
    - Classes that contain actuator objects (motor controllers, servos, solenoids, etc.) and inherit from the `Subsystem` interface.
- Commands
    - Objects that call methods defined in Subsystems (and/or normal classes) or use their state directly via lambda captures to perform one or more actions.
- Classes
    - Normal objects, not subject to any of the semantics or requirements of Subsystems or Commands, can represent non-actuating hardware (e.g. vision management), state, or anything the user wants.

## Requirements

A core principle of Command-Based is that only one command should have access to a given subsystem at any moment, to avoid competition for hardware resources. This is enforced by command requirements. If a command requires a subsystem that is already "in use", one of the commands will be cancelled (depending on the existing command's `InterruptionBehavior`).

