# Team attribute based data creation pipeline
import pandas as pd
from common import * 
from preprocess import *
#from models import *

home_adv_factor = 1
num_top_players_for_attribute = 4

#All the attributes to consider for training"

attr_cols = ['crossing', 'finishing', 'heading_accuracy','short_passing', 'volleys', 'dribbling', 'free_kick_accuracy',
       'long_passing', 'ball_control', 'acceleration', 'sprint_speed',
       'agility', 'reactions', 'balance', 'shot_power', 'jumping', 'stamina',
       'strength', 'long_shots', 'aggression', 'interceptions',
       'vision', 'penalties', 'marking', 'standing_tackle', 'sliding_tackle',
       'gk_positioning','gk_reflexes']

x_norm_cols = [ "%s_%s"%(c,attr)  for c in ['h','a'] for attr in attr_cols if attr!='form']


def tr_cols():
    return attr_cols

def create_team(data):
    """For this approach construct the full team directly """
    return data

def get_features(team):
    agg_attrs = {}
    team_attrs = team[attr_cols]
    for key in team_attrs.keys():
            #print(team.sort_values(by = [key], ascending = False)[key].head(2 if key.startswith('gk') else 4))
            agg_attrs[key] = team.sort_values(by = [key], ascending = False)[key].head(1 if key.startswith('gk') else 4).mean()
        
    agg_attrs_df = pd.DataFrame([agg_attrs])
    return agg_attrs_df

# Get fixtures is common

### get all team data is common

def get_feats_data(years):
        
    d = create_match_data(years, create_team, get_features)

    s = stdize(d, [ pre + attr for pre in ['h_','a_'] for attr in attr_cols])
    diffs = diff_attrs(s,attr_cols)
    return (diffs[attr_cols],d['Result'])

    #norm_tr_data = normalize(tr_data, x_norm_cols)

get_feats_data(['2014'])