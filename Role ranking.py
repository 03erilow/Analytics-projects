# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 12:12:42 2024

@author: ericl
"""
import pandas as pd
from scipy.stats import zscore

# Dataset for your league
df_outfield = pd.read_excel('Liga F.xlsx')  
df_gk = pd.read_excel('Liga F GK.xlsx')

# Define the weights for different roles
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

# Normalize the dataset using z-scores
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

# Function to calculate the weighted role score
def calculate_role_score(df, role_weights):
    total_weight = sum(role_weights.values())
    if not (0.99 <= total_weight <= 1.01):
        raise ValueError("Role weights must sum to 1.")
    
    relevant_columns = list(role_weights.keys())
    missing_columns = [col for col in relevant_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in dataset: {missing_columns}")
    
    role_score = (
        df[relevant_columns]
        .multiply(list(role_weights.values()), axis=1)
        .sum(axis=1)
    )
    return role_score

# List of columns to add
additional_columns = ["Nation", "Pos", "Squad", "Age", "Born", "Mins"]

# Process outfield players
df_outfield_normalized = normalize_data(df_outfield, roles_outfield)
role_scores_outfield = {}
for role_name, role_weights in roles_outfield.items():
    try:
        role_scores_outfield[role_name] = calculate_role_score(df_outfield_normalized, role_weights)
    except ValueError as e:
        print(f"Error calculating {role_name} score: {e}")
        role_scores_outfield[role_name] = None

# Create a dataset for outfield role scores
role_scores_outfield_df = pd.DataFrame(role_scores_outfield)
role_scores_outfield_df.insert(0, "Player", df_outfield["Player"])  # Add player names

# Add additional columns to outfield dataset
for col in additional_columns:
    if col in df_outfield.columns:  # Ensure the column exists in the original dataset
        role_scores_outfield_df[col] = df_outfield[col]

# Reorder columns in new outfield dataframe
columns_order = ["Player"] + additional_columns + [col for col in role_scores_outfield_df.columns if col not in ["Player"] + additional_columns]
role_scores_outfield_df = role_scores_outfield_df[columns_order]

# Process goalkeepers
df_gk_normalized = normalize_data(df_gk, roles_gk)
role_scores_gk = {}
for role_name, role_weights in roles_gk.items():
    try:
        role_scores_gk[role_name] = calculate_role_score(df_gk_normalized, role_weights)
    except ValueError as e:
        print(f"Error calculating {role_name} score: {e}")
        role_scores_gk[role_name] = None

# Create a dataset for GK role scores
role_scores_gk_df = pd.DataFrame(role_scores_gk)
role_scores_gk_df.insert(0, "Player", df_gk["Player"])  # Add player names

# Add additional columns to GK dataset
for col in additional_columns:
    if col in df_gk.columns:  # Ensure the column exists in the original dataset
        role_scores_gk_df[col] = df_gk[col]
        
# Reorder columns to GK dataset
columns_order = ["Player"] + additional_columns + [col for col in role_scores_gk_df.columns if col not in ["Player"] + additional_columns]
role_scores_gk_df = role_scores_gk_df[columns_order]

# Dataframe to Excel
role_scores_outfield_df.to_excel("Role_scores_outfield_liga_f_details.xlsx")
role_scores_gk_df.to_excel("Role_scores_gk_liga_f_details.xlsx")
