# Manual System Identification with R

Prerequisites:
- [R Installation](https://www.r-project.org/)
- The RStudio IDE (used by this tutorial) or PyCharm with the R extension (they have UI elements that make the workflow MUCH easier and so few professionals use R without them)

## Data Collection

To fully sample the state-space of the mechanism, we will need to observe a steady output ramp *and* its response to step-changes in output. It is recommended to either run two tests (one with a steady ramp from 0 output and one with a single large step output) or a combined "stairstep" test (multiple small steps that combined form the shape of a ramp). Implementing these tests on your robot and recording the Data is left as an exercise for the reader, but WPILib's `SysIdRoutine` class and DataLogTool's ability to export specific DataLog entries as a CSV are both very useful here.

!!! note
    If you are logging data using CTR Electronics' `SignalLogger`, be sure to convert the .hoot to .wpilog with Tuner X (Windows/MacOS) or the Owlet command-line tool (Windows/MacOS/Linux). **Do not use AdvantageScope to export, as it only records value changes and will thus deform the log.**

## Using R

Upon installing and opening RStudio, you should be greeted by this screen:

![RStudio Home Screen](media/manual-id/rstudio/rstudio-home.png)

Load the CSV file with `data <- read.csv(filePath)`, where `filePath` is the absolute path to the csv file enclosed in double quotes.

[image]

Because each record is logged at a slightly different time, each row will only contain one of the values we want, so we will need to group the rows. Before we do this, we want to separate the data into the quasistatic and dynamic portions, to avoid overlaying them.

