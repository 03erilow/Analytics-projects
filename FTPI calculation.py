# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:47:22 2024

@author: ericl
"""

import pandas as pd
import numpy as np
from scipy.stats import zscore

# Training a model to fit weights in the offensive output-metric according to correlation to goals scored,
# and weights to defensive compactness-metric according to correlation to least goals allowed.
# Then we adjust the weights so that all metrcis are in proportion to each other by calculating z-scores.

def calculate_weights(data, metric_columns, target_column, normalize=True):
    """
    Calculates weights for metrics based on their correlation to a target. This is then done for both offensive
    output-metrics and for the compactness factor-metrics. 
    
    Parameters:
        data (pd.DataFrame): Dataset with metrics and target variable.
        metric_columns (list): List of metric column names.
        target_column (str): Name of the target column (e.g., goals scored or least goals allowed).
        normalize (bool): Whether to normalize using z-scores.
    
    Returns:
        dict: Dictionary of metrics with adjusted weights.
    """
    # Calculate correlations between each metric and the target
    correlations = {col: data[col].corr(data[target_column]) for col in metric_columns}
    
    # Convert correlations into weights (normalize to sum to 1 for interpretability)
    total_correlation = sum(abs(corr) for corr in correlations.values())
    initial_weights = {col: abs(corr) / total_correlation for col, corr in correlations.items()}
    
    # Adjust weights based on z-scores (if normalize=True)
    if normalize:
        z_scores = {col: zscore(data[col]) for col in metric_columns}
        weight_adjustments = {col: np.std(z_scores[col]) for col in metric_columns}
        
        adjusted_weights = {
            col: initial_weights[col] * weight_adjustments[col] 
            for col in metric_columns
        }
        
        # Normalize adjusted weights to sum to 1
        total_adjusted = sum(adjusted_weights.values())
        final_weights = {col: adjusted_weights[col] / total_adjusted for col in metric_columns}
    else:
        final_weights = initial_weights

    return final_weights

def calculate_ftpi(offensive_output, compactness_factor, field_tilt):
    """
    Calculate the Final Third Productivity Index (FTPI).

    Parameters:
        offensive_output (float): A measure of attacking effectiveness (e.g., xG per possession).
        compactness_factor (float): A measure of defensive difficulty imposed by the opponent.
        field_tilt (float): Proportion of attacking third activity vs. defensive third activity.

    Returns:
        float: The calculated FTPI score.
    """
    # FTPI formula: FTPI = Offensive Output/(Compactness Factor * Field Tilt)
    if compactness_factor == 0 or field_tilt == 0:  # Avoid division by zero
        raise ValueError("Compactness Factor and Field Tilt cannot be zero.")
    ftpi = offensive_output / (compactness_factor * field_tilt)
    return ftpi

def compute_offensive_output(offensive_metrics_dict):
    """
    Compute offensive output as a weighted sum of metrics.

    Parameters:
    - offensive_metrics_dict: A dictionary where keys are the offensive metric names (strings) and values are tuples:
                    (metric_value (float), weight (float)).

    Returns:
    - offensive_output: The weighted sum of the metrics.
    """
    # Ensure input is a dictionary
    if not isinstance(offensive_metrics_dict, dict):
        raise ValueError("metrics_dict must be a dictionary with metric names as keys and (value, weight) tuples as values.")

    # Compute the weighted sum of all metrics
    offensive_output = sum(value * weight for value, weight in offensive_metrics_dict.values())

    return offensive_output


def compute_compactness_factor(compactness_metrics_dict, opponent_field_tilt):
    """
    Compute Compactness Factor based on opponent defensive characteristics.

    Parameters:
    - compactness_metric_dict: A dictionary where keys are the compactness metric names (strings) and values are tuples:
                    (metric_value (float), weight (float)).

    Returns:
    - compactness_factor: The weighted sum of the metrics divided by opponent field tilt
    """
    # Compute the weighted sum of all metrics and divide by opponent field tilt
    compactness_factor = sum(value * weight for value, weight in compactness_metrics_dict.values())/opponent_field_tilt
    
    return compactness_factor

#%%
# Usage of the functions we have to calculate the final FTPI for a team or a match

# Dataset for a league, a single team, multiple matches or a single match
data = pd.read_csv("dataset.csv")

# Offensive output metrics
offensive_metrics = [] # all offensive metrics of your choice included in the dataset, manually inputed
offensive_weights = calculate_weights(data, offensive_metrics, 'goals_scored')

# Compactness factor metrics
compactness_metrics = [] # all compactness metrics of your choice included in the dataset, manually inputed
compactness_weights = calculate_weights(data, compactness_metrics, 'least_goals_allowed')

results = []

for _, row in data.iterrows():
    # Create the offensive metrics dictionary for the current row
    offensive_metrics_dict = {
        metric_name: (row[metric_name], offensive_weights[metric_name])
        for metric_name in offensive_metrics
    }

    # Create the compactness metrics dictionary for the current row
    compactness_metrics_dict = {
        metric_name: (row[metric_name], compactness_weights[metric_name])
        for metric_name in compactness_metrics
    }

    # Access field tilt and opponent field tilt for the current row
    field_tilt = row["field_tilt"]
    opponent_field_tilt = row["opponent_field_tilt"]

    # Compute offensive output, compactness factor and ftpi by calling our functions
    offensive_output = compute_offensive_output(offensive_metrics_dict)
    compactness_factor = compute_compactness_factor(compactness_metrics_dict, opponent_field_tilt)
    ftpi = calculate_ftpi(offensive_output, compactness_factor, field_tilt)

    # Store the result for this row
    results.append({"Compactness factor": compactness_factor, 
                    "Offensive output": offensive_output, 
                    "FTPI": ftpi})

# Convert results into a DataFrame
results_df = pd.DataFrame(results)

# Add the computed columns to the original dataset
final_data = pd.concat([data, results_df], axis=1)

# Export to Excel
final_data.to_excel("final_data.xlsx", index=False)

print("Data exported successfully to final_data.xlsx")


