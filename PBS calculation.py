# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 17:06:21 2024

@author: ericl
"""
import pandas as pd

"""
Function to calculate the Press Breaking Score row by row in a dataset that contains all actions. 
The dataset should contain: number of opponents bypassed by the action, number of opponents within a given 
radius of the ball before and after the action, average distance to these opponents within this radius of 
the ball before and after the action, and finally the possession value change of the action (for example xT
or EPV). The function returns the three components that sum up to the PBS. The values of the components are 
then normalized so that they are relative to each other size wise. The PBS is then added to the provided
dataset and a new, updated dataset is returned.
"""

def calculate_pbs(row, radius=10, max_density_adjustment_factor=5):

    # Calculate Density Adjustment Factor (DAF)
    if row["opponents_after"] == 0:
        density_adjustment_factor = max_density_adjustment_factor
    else:
        density_adjustment_factor = row["opponents_before"] / row["opponents_after"]

    # Calculate Opponent Proximity Value (OPV)
    if row["opponents_after"] == 0:
        opv = radius - row["avg_distance_before"]
    else:
        opv = row["avg_distance_after"] - row["avg_distance_before"]

    # Calculate line_break_value * DAF
    line_break_value_daf = row["number_bypassed"] * density_adjustment_factor

    return line_break_value_daf, row["possession_value_change"], opv


# Load dataset
data = pd.read_csv("dataset.csv")

# Step 1: Compute individual components
components = data.apply(calculate_pbs, axis=1, result_type="expand")
components.columns = ["line_break_value_daf", "possession_value_change", "opv"]

# Step 2: Normalize components using z-scores
z_scores = (components - components.mean()) / components.std()
z_scores.columns = ["z_line_break_value_daf", "z_possession_value_change", "z_opv"]

# Step 3: Calculate normalized PBS
data["PBS"] = z_scores["z_line_break_value_daf"] + z_scores["z_possession_value_change"] + z_scores["z_opv"]

# Export updated dataset
data_with_pbs = pd.concat([data, z_scores], axis=1)
data_with_pbs.to_excel("final_data_with_normalized_pbs.xlsx", index=False)
print("Updated dataset exported to final_data_with_normalized_pbs.xlsx")
