# Manual System Identification

The goal of manual characterization is to, as quickly and simply as possible, get reasonably accurate values of the four feedforward gains (Ks, Kv, Ka, Kg) and two feedback gains (Kp and Kd).

The procedure does differ based on mechanism, so each major type will be discussed separately.

!!! warning
    All tuning procedures discussed below will require the use of data logging and plotting in either a vendor's hardware client (e.g. Phoenix Tuner X, REV Hardware Client, etc.) or AdvantageScope. Make sure you are familiar with data logging and one or more of these tools before continuing.

!!! note
    When units are described below, "output unit" refers to the unit that your eventual controller will output. In most cases this will be Voltage or Duty Cycle (Percent Output), but can be any unit (such as Chassis Speeds in Swerve Drive robot velocity controllers). "input unit" refers to the units of the setpoint being fed into the feedforward or the error (usually derived from a sensor or input device) fed into a feedback controller.

## Feedforward

### Simple Motor

Simple Motor systems are those that are driven by one motor (or multiple in one gearbox) and either only depend on velocity (such as flywheels) or those that are not affected by gravity (such as drive steer motors and turrets).

Ks has units of \[output\]. Gradually increase output until the mechanism just barely starts to move, overcoming static friction. The output just before motion begins is Ks. **[ADD ASCOPE GRAPH]**

Kv and Ka can be found with [Recalc](https://reca.lc).



### Elevator

The addition of gravity complicates things, making Kg and Ks somewhat interconnected. The units of Kg, like Ks, are \[output\]. The output that *almost* allows an elevator to move upwards is Kg + Ks, and the output that *almost* allows it to move down is Kg − Ks. Slowly increase output until the carriage begins to move upwards (output_{up}), and then decrease output until the carriage begins to move down (output_{down}).
**[ADD SCOPE GRAPH]**

Kg = (output_{up} + output_{down}) / 2

Ks = (output_{up} − output_{down}) / 2

Kv and Ka can be found with [Recalc](https://reca.lc) or by manual estimation. If the units of Ka are \\frac{V}{m²}


### Single Jointed Arm

Arms have another special factor, which is that the influence of gravity actually changes based on the angle of the arm. This means that when at angles other than horizontal, Kg will have to be scaled down by a factor of cos(angle) and that for the purposes of this analysis, an angle of 0 *must* be horizontal.

The procedure is identical to tuning feedforward on an elevator except for minding the angle. An offset must be applied to the angle both when calculating Kg and when using the feedforward in code to ensure that 0 = horizontal.

### Tweaking/Troubleshooting

If your mechanism is not tracking setpoints as well as you would like, there are some steps that can be taken to easily address them:

* If the steady−state velocity of the system is too low, increase Kv.
* A quick and dirty Kv can be calculated as max output / max velocity.

### Manually Determining Kv and Ka

If you want to empirically determine values for Kv and Ka (such as to verify Recalc's numbers are in the right ballpark) it becomes much more complex. Kv on flywheels can be estimated easily (slope of (0 speed, Ks) and (free speed, max output)) but otherwise a linear regression akin to SysId will be required. **This is considered an advanced topic. If you just want gains fast, use Recalc.** It is recommended to use R (a statistics/data visualization-oriented language), though Python/Jupyter Notebooks can also work well. See the [System Identification with R](system-id-r.md) tutorial for more information. 

## Feedback

Once feedforward gains have been found, there are two main options for finding Kp and Kd:

1. Use [SysId's theoretical mode](sysid/theoretical−mode.md) with Kv, Ka, the maximum allowed output, and an error tolerance to estimate Kp and Kd.
2. Manually tune Kp and Kd (the focus of this section).

### Manual

1. Increase Kp until the system begins oscillating around the setpoint.
2. If the mechanism only relies on velocity (e.g. flywheels), decrease Kp until the oscillation stops. If it also relies on position, increase Kd until the oscillation stops, reducing Kp if necessary.