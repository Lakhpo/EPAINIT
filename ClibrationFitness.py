import epyt
from epyt import epanet
import pandas as pd
import numpy as np

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
