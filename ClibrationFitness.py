import epyt
from epyt import epanet
import pandas as pd
import numpy as np
import math


d = epanet("C:/Users/chase/Documents/GitHub/EPAINIT/2_Loop_Problem.inp")
df = pd.read_csv(
    "C:/Users/chase/Documents/GitHub/EPAINIT/Example files/2-loop-problem/2loop pressure.txt",
    sep="\t",
    header=3,
)

print(type(df))

num_Node = d.getNodeCount()
num_Junctions = d.getNodeJunctionCount()
indexid = {}

# Create two tables one with the Node Index another with the node ID.
# ACE: Check this to make sure indenting is correct
for i in range(0, num_Node):
    Index = 0
    if d.getNodeType(i) == "JUNCTION":
        NameID = d.getNodeNameID(i)
        indexid[NameID] = i


assert len(indexid) == num_Junctions

# using pandas import Tab seperated values
# Why pandas over simple csv? Because there is a possibility that we may have to handle .dat files and sometimes even excel files for user convience.
df = pd.read_csv(
    "C:/Users/chase/Documents/Time Series Practice.txt",
    sep="\t",
    header=1,
)
# Get the Indexs where each node begins and ends"

# Get the amount of colums in your csc
CalNodeIndexs = np.array([])
Size = df.shape[0]  # Number of rows in the data set

# Check if the content of the node row is has a string in it and that string isn't Nan
for i in range(1, Size):
    if type(df.iloc[i, 0]) == str and df.iloc[i, 0] != "nan":
        CalNodeIndexs = np.append(CalNodeIndexs, [i])

# Create a dictionary containing times and pressures for a given node, then assign that dictionary to
CalDict = {}
numcalnode = CalNodeIndexs.size
for i in range(0, numcalnode):
    flexDict = {}
    # For the last one just go to the end of the data set
    Startingpoint = CalNodeIndexs[i]
    Startingpoint = int(Startingpoint)
    if i < numcalnode - 1:
        StopingPoint = CalNodeIndexs[i + 1]
        StopingPoint = int(StopingPoint)
    else:
        StopingPoint = Size
    # Create a nested dictionary for with times [j,1] and indipendent variable (usually pressure) [j,2] and save to larger dictionary under node name [Index,0]
    for j in range(Startingpoint, StopingPoint):
        flexDict[df.iloc[j, 1]] = df.iloc[j, 2]
    SpefNodeIndex = CalNodeIndexs[i]
    SpefNodeIndex = int(SpefNodeIndex)
    CalDict[df.iloc[SpefNodeIndex, 0]] = flexDict
# Now that the observed data is created we need to get the simulated data.
# Initualize simulation and go step by step to create a similar dict for the simulated data.
d.openHydraulicAnalysis()
d.initializeHydraulicAnalysis()

d.getComputedTimeSeries()
Length_of_Analysis = 24  # I need to see if i can call this directly using the api
Simulationdict = {}
for name in indexid:
    Simulationdict[name] = {}

for i in range(Length_of_Analysis + 1):
    time = i
    # For node in Node name
    for name in indexid:
        flexDict = {}
        # Get corrosponding NodeID
        id = indexid[name]
        # Get pressure using Node ID
        Value = d.getNodePressure(id)
        flexDict[i] = Value
        # Create Dict with Time and pressure and add it to the Node Dict using Node name
        Simulationdict[name][time] = Value
    d.nextHydraulicAnalysisStep()
    d.runHydraulicAnalysis()

# Now we have both dictionaries YIPEEE

# in the oveserved data, call the same observed data
for name in CalDict:
    for time in CalDict[name]:
        Value1 = CalDict[name][time]
        Value2 = Simulationdict[name][time]
