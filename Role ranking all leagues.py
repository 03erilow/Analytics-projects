# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 16:21:46 2024

@author: ericl
"""

import pandas as pd
from scipy.stats import zscore

# Calculate adjustment factors for each league
def calculate_adjustment_factors(data, baseline_league):
    """
    Calculate adjustment factors for every metric in the dataset based on the baseline league.

    Args:
        data (pd.DataFrame): The dataset containing all leagues and metrics.
        baseline_league (str): The name of the baseline league (e.g., 'Mean' or 'UWCL').

    Returns:
        dict: A dictionary of dictionaries containing adjustment factors for each metric across leagues.
    """
    metrics = [col for col in data.columns if col not in ["Player", "League", "Pos", "Squad", "Nation", "Age", "Born", "Mins"]]
    adjustment_factors = {}

    # Calculate means for each metric in the baseline league
    baseline_means = data[data["League"] == baseline_league][metrics].iloc[0]

    for league in data["League"].unique():
        if league == baseline_league:
            continue
        
        league_means = data[data["League"] == league][metrics].iloc[0] 

        # Compute adjustment factors for the current league
        league_adjustments = {
            metric: baseline_means[metric] / league_means[metric] if league_means[metric] != 0 else 1
            for metric in metrics
        }
        
        # Store the adjustment factors for this league
        adjustment_factors[league] = league_adjustments

    return adjustment_factors

# Calculate the role score for every player with adjustment factors for each league
def calculate_role_score_with_adjustments(df, roles, adjustment_factors, baseline_league="Mean"):
    """
    Calculate role scores for all players in the DataFrame while incorporating league-specific adjustment factors for metrics.
    
    Parameters:
        df (pd.DataFrame): The normalized player dataset.
        roles (dict): Dictionary defining roles and their associated metrics with weights.
        adjustment_factors (dict of dict): Nested dictionary with league-specific adjustment factors for each metric.
        baseline_league (str): The baseline league name (default: "UWCL").
        
    Returns:
        pd.DataFrame: DataFrame with additional columns for each role score, reordered with metadata first.
    """
    # Create a copy to avoid modifying the original data
    role_scores = df.copy()

    # Check if the "League" column exists
    if "League" not in df.columns:
        raise ValueError("DataFrame must contain a 'League' column to apply league-specific adjustments.")

    # Iterate over each role and calculate the role score
    for role_name, metrics_weights in roles.items():
        # Initialize the role score column
        role_scores[role_name] = 0

        for metric, weight in metrics_weights.items():
            # Adjust metrics using league-specific adjustment factors
            adjusted_metric_values = df.apply(
                lambda row: row[metric] * adjustment_factors.get(row["League"], {}).get(metric, 1),
                axis=1
            )
            # Accumulate the weighted, adjusted metric values into the role score
            role_scores[role_name] += adjusted_metric_values * weight

    # Reorder columns: keep metadata columns first, followed by role scores
    metadata_columns = ["Player", "Nation", "Age", "Mins", "League", "Squad", "Pos"]
    role_columns = [col for col in role_scores.columns if col not in metadata_columns]
    role_scores = role_scores[metadata_columns + role_columns]

    return role_scores

# Normalize the dataset using z-scores so that all metrics are comparable to each other in size
def normalize_data(df, roles):
    # Identify all relevant columns for all roles
    relevant_columns = set()
    for role_weights in roles.values():
        relevant_columns.update(role_weights.keys())
        
    # Convert set to list for indexing
    relevant_columns = list(relevant_columns)
    
    # Ensure all relevant columns are in the dataset
    missing_columns = [col for col in relevant_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns for normalization: {missing_columns}")
    
    # Apply z-score normalization to relevant columns
    normalized_df = df.copy()
    normalized_df[relevant_columns] = df[relevant_columns].apply(zscore, axis=0, nan_policy='omit')
    return normalized_df

# Usage

# Load the player-level dataset
outfield_player_data = pd.read_excel("Outfield player data.xlsx")
gk_player_data = pd.read_excel("GK player data.xlsx")

# Load the league-level metrics dataset. Should contain league level averages for every metric used
df_league_metrics = pd.read_excel("Average league data.xlsx")

# Define the baseline league
baseline_league = "Mean"

# Define the roles dictionary (use your predefined roles dictionary here)
roles_outfield = {
    "Ball playing CB": {
        "CmpLong%": 0.2,
        "Passes_to_final_third": 0.2,
        "Progressive_passes": 0.2,
        "Cmp_passes": 0.2,
        "Aerial_duel_win%": 0.1,
        "TklWin%": 0.1
    },
    "Defensive CB": {
        "Recoveries": 0.2, # Def duels
        "Blocks_passes": 0.15, # Def duels
        "Blocks_shots": 0.1, # Def duels
        "Fouls": 0.2,
        "Aerial_duel_win%": 0.15,
        "TklWin%": 0.1,
        "Interceptions": 0.1
    },
    "Wide CB": {
        "Recoveries": 0.2,
        "Blocks_passes": 0.1,
        "Blocks_shots": 0.05,
        "Progressive_passes": 0.15,
        "Progressive_carries": 0.1,
        "Fouls": 0.1,
        "CmpShort%": 0.2,
        "CmpLong%": 0.1
    },
    "Attacking FB": {
        "Passes_to_final_third": 0.25,
        "Progressive_carries": 0.2, 
        "Recoveries": 0.15,
        "xA": 0.1,
        "Crs": 0.05,
        "PPA": 0.05,
        "CPA": 0.05,
        "Succ_TO%": 0.1,
        "SCA": 0.05
    },
    "Inverted FB": {
        "AttPass": 0.35,
        "Progressive_passes": 0.2, 
        "Recoveries": 0.1,
        "TklWin%": 0.1,
        "Interceptions": 0.1,
        "AttShort": 0.15,
    },
    "Possession enabler": {
        "AttShort": 0.3,
        "CmpShort%": 0.25, 
        "Pass%": 0.2,
        "AttPass": 0.15,
        "Fouls": 0.1,
    },
    "Defensive CM": {
        "Recoveries": 0.2, # Def duels
        "Blocks_passes": 0.1, # Def duels
        "Blocks_shots": 0.05, # Def duels
        "Fouls": 0.15,
        "Aerial_duel_win%": 0.1,
        "TklWin%": 0.1,
        "Interceptions": 0.2,
        "Pass%": 0.1,
    },
    "Number 6": {
        "Recoveries": 0.2, # Def duels
        "Blocks_passes": 0.05, # Def duels
        "Blocks_shots": 0.05, # Def duels
        "CmpShort%": 0.25,
        "AttShort": 0.2,
        "Dribblers_tackled": 0.05,
        "Interceptions": 0.1,
        "Fouls": 0.1,
    },
    "Deep lying playmaker": {
        "Passes_to_final_third": 0.25,
        "Progressive_passes": 0.25,
        "Key_passes": 0.15,
        "CmpMid%": 0.15,
        "CmpMid": 0.1,
        "Recoveries": 0.05,
        "TklWin%": 0.025,
        "Interceptions": 0.025,
    },
    "Progressive midfielder": {
        "Passes_to_final_third": 0.2,
        "Progressive_passes": 0.225,
        "Progressive_carries": 0.125,
        "Recieved_passes": 0.15,
        "SCA": 0.2,
        "PPA": 0.1,
    },
    "Box to box midfielder": {
        "Passes_to_final_third": 0.1,
        "Mins": 0.1,
        "Progressive_carries": 0.2,
        "Recoveries": 0.1, # Def duels
        "Blocks_passes": 0.05, # Def duels
        "Blocks_shots": 0.05, # Def duels
        "Interceptions": 0.15,
        "TklWin%": 0.05,
        "PPA": 0.15,
        "Key_passes": 0.05,
    },
    "Advanced playmaker": {
        "Key_passes": 0.25,
        "SCA": 0.25,
        "Passes_to_final_third": 0.20,
        "PPA": 0.15,
        "xA": 0.15
    },
    "Classic CAM": {
        "Key_passes": 0.2,
        "PPA": 0.1,
        "SCA": 0.1,
        "CPA": 0.1,
        "Succ_TO%": 0.1,
        "xA": 0.15, 
        "npxG": 0.1, 
        "Gls": 0.05,
        "Sh": 0.05,
        "SoT": 0.05,
    },
    "Wide CAM": {
        "Key_passes": 0.2,
        "PPA": 0.1,
        "SCA": 0.1,
        "CPA": 0.15,
        "Succ_TO%": 0.1,
        "xA": 0.15, 
        "Crs_PA": 0.15, 
        "Touches_Att pen": 0.05,
    },
    "Second striker": {
        "npxG": 0.2,
        "Touches_Att pen": 0.2,
        "Gls": 0.15,
        "xA": 0.15,
        "Succ_TO%": 0.1,
        "G/Sh": 0.1, 
        "Progressive_carries": 0.1, 
    },
    "Playmaking winger": {
        "Key_passes": 0.2,
        "PPA": 0.1,
        "Passes_to_final_third": 0.1,
        "Progressive_passes": 0.1,
        "Ast": 0.1,
        "xA": 0.1,
        "SCA": 0.1,
        "GCA": 0.15, 
        "Progressive_carries": 0.05, 
    },
    "Inverted winger": {
        "Sh": 0.25,
        "npxG": 0.15,
        "Touches_Att pen": 0.15,
        "Succ_TO%": 0.15,
        "Key_passes": 0.15,
        "Crs_PA": 0.15,
    },
    "Traditional winger": {
        "Key_passes": 0.2,
        "Succ_TO%": 0.175,
        "Crs_PA": 0.15,
        "SCA": 0.15,
        "xA": 0.15,
        "Progressive_carries": 0.075,
        "Sh": 0.1
    },
    "Inside forward": {
        "Touches_Att pen": 0.2,
        "npxG": 0.2,
        "Gls": 0.15,
        "G/Sh": 0.1,
        "xA": 0.15,
        "Progressive_carries": 0.1,
        "Sh": 0.1
    },
    "Deep lying striker": {
        "Key_passes": 0.2,
        "npxG": 0.2,
        "Gls": 0.2,
        "G/Sh": 0.1,
        "Ast": 0.1,
        "Progressive_carries": 0.1,
        "Recieved_passes": 0.1
    },
    "Target striker": {
        "Touches_Att pen": 0.25,
        "npxG": 0.225,
        "Gls": 0.1,
        "G/Sh": 0.05,
        "Aerial_duel_win%": 0.225,
        "SoT": 0.15,
    },
    "Playmaking striker": {
        "Key_passes": 0.2,
        "PPA": 0.2,
        "Passes_to_final_third": 0.1,
        "xA": 0.1,
        "Progressive_passes": 0.1,
        "Sh": 0.15,
        "Gls": 0.05,
        "npxG": 0.1
    },
    "Link-up striker": {
        "CmpShort%": 0.2,
        "AttShort": 0.1,
        "Recieved_passes": 0.2,
        "Key_passes": 0.15,
        "PPA": 0.1,
        "Sh": 0.1,
        "Gls": 0.05,
        "npxG": 0.1
    },
}
roles_gk = {"Shot stopping distributor": {
    
    "PSxG+/-": 0.25,
    "CmpShort": 0.2,
    "Launch_pass%": 0.2,
    "CmpLong%": 0.2,
    "Save%": 0.15,
    }
}

# Calculate adjustment factors for each league and each metric
adjustment_factors = calculate_adjustment_factors(df_league_metrics, baseline_league)

print(adjustment_factors)

# Normalize player data
normalized_outfield_data = normalize_data(outfield_player_data, roles_outfield)
normalized_gk_data = normalize_data(gk_player_data, roles_gk)

# Calculate role scores with adjustment factors for every player in the normalized player data
outfield_role_scores = calculate_role_score_with_adjustments(normalized_outfield_data, roles_outfield, adjustment_factors, baseline_league)
gk_role_scores = calculate_role_score_with_adjustments(normalized_gk_data, roles_gk, adjustment_factors, baseline_league)

# Save the results to a new Excel file
outfield_role_scores.to_excel("outfield_role_scores_with_adjustments.xlsx", index=False)
gk_role_scores.to_excel("gk_role_scores_with_adjustments.xlsx", index=False)