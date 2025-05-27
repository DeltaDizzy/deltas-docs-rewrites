# Logging Data

## Units

Keeping track of units is one of the most critical tasks when doing System Identification. At all times, you *must* be aware of:

- The units your sensor reports in
- The units your motor controller needs setpoints in
- The units of the control gains

If the units do not match, some amount of manual dimensional analysis will be required to convert them.

## Choosing a Logger

SysId will only accept WPILib DataLogs (.wpilog files), but there are many ways to create them.

* Logging to NetworkTables and using `DataLogManager` to clone it to a DataLog
* Epilogue using a File backend
* DogLog (3rd-party library)
* Vendor logging solutions such as CTRE's `SignalLogger` or the `URCL` REV logger

When determining which logging solution to use, measurement timing is the primary consideration. The quality of the fit depends primarily on the level of timing jitter (or the amount that the time between measurements changes randomly during the test duration), though making the actual interval length itself smaller can also improve accuracy. Most timing jitter is caused by the Java Garbage Collector on the RoboRIO, and so a low-hanging fruit for data improvement is to move to a lower-jitter collection method such as direct CAN timestamp measurements offtered by CTRE's `SignalLogger` or `URCL` for REV devices.

Any of these should work perfectly fine, but consult the documentation for each to learn how to use it.

## What to Log

SysId requires three different datasets for each motor that will be characterized:

1. Position
2. Velocity
3. *Output* Voltage