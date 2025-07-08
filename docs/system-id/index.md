# System Identification

!!! warning
    Familiarity with and some level of intuition for PID Controllers, DC Motor Feedforwad, and Dimensional Analysis are assumed in this section. Without them, you *will* be confused and lost.

## What is System Identification?

Feedforwards require a mathematical model of a system, which in FRC generally boils down to 3-4 constant gains: Ks, Kv, and Ka. This model can also be used to estimate optimal PID gains. The goal of System Identification is to estimate these gains.

For FRC robots, [Recalc](https://reca.lc) can provide good estimates of Kg, Kv, and Ka, which should act as your starting point. Ks can then be detemined empirically. If you want to squeeze the most performance possible out of your mechanisms, however, tests of your mechanism will be required to determine (or *identify*) the true gains.

DC Motors are very linear, so with some tricks the gains can be found with a relatively straightforward least-squares linear regression. To ensure accurate gain estimates, a good sampling of the "state-space" (or set of all possible states, such as all posible position-velocity pairs for an elevator or arm or turret) of the mechanism is needed. In practice, this means performing specific tests and analyzing the resultant data to perform the fit. 

To help teams do this quickly and without needing as much experience, WPILib provides a robot-side API and analysis tool under the name "SysId". SysId can allow feedforward and PID gains to be found simply, but debugging issues will require familiarity with the concepts and modern FRC tools such as AdvantageScope.

!!! note
    SysId's feedback gains are optimal for the provided model, but unmodeled effects, lower quality data, and measurement latency may require tweaking the gains. More controllable systems will always work better "out of the box".
    
SysId is not a silver bullet, and more experienced users can obtain the gains even faster without it, but for the middle ground it can greatly enhance controls workflows. It is up to teams if they want to dedicate the time to proper System Identification, as even very non-optimal gains can compensate for many issues and win events.

## SysId
The SysId tool performs two functions, the feedforward regression and running an LQR (Linear-Quadratic Regulator). LQR is a method of finding optimum Kp and Kd gains given a system model defined by the feedforward gains. Critically, this means the LQR can be used with gains from *any* source, and SysId is equipped with a "theoretical mode" to allow arbitrary gains (such as those obtained from Recalc) to be fed to the LQR.

## Table of Contents

- [Manual System Idenification](../system-id/manual-id)
- Using SysId
    - [Logging Data](sysid/logging-data.md)
    - [Loading Data](sysid/loading-data.md)
    - [Viewing Diagnostics](sysid/diagnostics.md)
    - [Analyzing Data](sysid/analyzing-data.md)
    - [Common Errors and Troubleshooting](sysid/troubleshooting.md)