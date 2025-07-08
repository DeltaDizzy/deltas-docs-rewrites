# Logging Data

## Units

Keeping track of units is one of the most critical tasks when doing System Identification. At all times, you *must* be aware of:

- The units your sensor reports in
- The units your motor controller needs setpoints in
- The units of the control gains

If the units do not match, some amount of manual dimensional analysis will be required to convert them.

## What to Log

SysId requires three different datasets for each motor that will be characterized:

1. Position
2. Velocity
3. *Output* Voltage (not battery/bus voltage)

## Choosing a Logger

SysId will only accept WPILib DataLogs (.wpilog files), but there are many ways to create them.

* Logging to NetworkTables and using `DataLogManager` to clone it to a DataLog
* Epilogue using a File backend
* DogLog (3rd-party library)
* Vendor logging solutions such as CTRE's `SignalLogger` or the `URCL` REV logger

When determining which logging solution to use, measurement timing is the primary consideration. The quality of the fit depends primarily on the level of timing jitter (or the amount that the time between measurements changes randomly during the test duration), though making the actual interval length itself smaller can also improve accuracy. Most timing jitter is caused by the Java Garbage Collector on the SystemCore, and so a low-hanging fruit for data improvement is to move to a lower-jitter collection method such as direct CAN timestamp measurements offtered by CTRE's `SignalLogger` or `URCL` for REV devices.

Any of these should work perfectly fine, but consult the documentation for each to learn how to use it. The remainder of this page will assume you are using WPILib logging.

## How to Log

!!! note For a full example project, see the SysIdRoutine example ([Java](https://github.com/wpilibsuite/allwpilib/tree/main/wpilibjExamples/src/main/java/edu/wpi/first/wpilibj/examples/sysidroutine), [C++](https://github.com/wpilibsuite/allwpilib/tree/main/wpilibcExamples/src/main/cpp/examples/SysIdRoutine), [Python](https://github.com/robotpy/examples/tree/main/SysId))

WPILib provides the `SysIdRoutine` class for creating and automating SysId tests to streamline data collection for teams. The API is designed with the Command-Based paradigm in mind, as it is used by the majority of FRC teams. The underlying `SysIdRoutineLog` recording API is usable in Non-Command codebases but will not be detailed here.

### SysIdRoutine

The intended usecase of `SysIdRoutine` is for one instance to be constructed in each subsystem. This instance must be provided with the test config (the Quasistatic test's voltage ramp rate, the Dynamic test's step voltage, and optionally a timeout) and a Mechanism object containing callbacks for driving the mechanism's motors and recording the test data as well as an instance of the subsystem object. If you do not understand Lambda Expressions or the concept of Callbacks, or just need a refresher, read the [Treating Functions as Data](https://docs.wpilib.org/en/stable/docs/software/basic-programming/functions-as-data.html) article.

The drive callback only needs to take the provided voltage object and use the voltage to set the motor output.

The data logging callback requires you to specify the name the motor will be logged under, as well as the values you wish to record. The API supports many quantities, but Voltage, Position, and Velocity are the important ones for System Identification purposes. angular and linear position, velocity, and acceleration are distinct entities, so make sure you are using the correct `Measure` 

!!! note All datapoints must be passed to the API using unit-safe types (`Measure` in Java, an mp-units quantity in C++). Some motor APIs return data natively using unit-safe values, but the majority do not, so you will need to construct them using the motor data before or while calling the log methods!

```java
SysIdRoutine routine = new SysIdRoutine(
    // no arguments means to use the defaults (1V / Second ramp rate, 7V step foltage, 10 second timeout).
    new SysIdRoutine.Config(
        Volts.of(0.5).Per(Second), // 0.5V / sec ramp rate
        Volts.of(4), // 4V step voltage
        Seconds.of(4) // 4 second timeout
    ), 
    new SysIdRoutine.Mechanism(
        // you can use a method reference for this, but if you understand lambda expressions it is easiest to use them instead.
        volts -> {
            motor.setVoltage(volts.magnitude());
        },

        log -> {
            // comment this
            log.motor("shooter-wheel")
                .voltage(Volts.of(motor.getVoltage()))
                .position(Rotations.of(motor.getPosition()))
                .velocity(Rotations.per(Second).of(motor.getVelocity()));
        }
    )
);
```

## Extracting Logs

After recording your log, you must extract it from the SystemCore. WPILib logging will leave a .wpilog on the SystemCore, which can be downloaded remotely using `DataLogTool`. If a USB flash drive was plugged into the SystemCore and had sufficient free space, the log will have been recorded to it, so unplugging the drive and copying the file onto your computer is also possible.

After the log file is in hand, open the SysId application and proceed to [Loading Data](loading-data.md).