import pandas as pd
from common import * 

#full_team = data[data['Team'].str.startswith(name)]
attr_cols =[str(i) for i in range(0,11)]

def tr_cols():
    return attr_cols

def get_features(team):
    t = team[['overall_rating','pos_index']].set_index(['pos_index'])
    return t.transpose()

def create_team(full_team):
    # if len(full_team[full_team['Position'].isin(['RB','RWB'])]) < 1 or len(full_team[full_team['Position'].isin(['LB','LWB'])]) < 1:
    #     pass#print(full_team['Team'])
    # weird = False
    # if len(full_team[full_team['Position'].isin(['GK'])]) < 1:
    #     weird = True
    #     print(full_team['Year'])

    
    pos_index = {0:[0],1:[1,2],2:[3],3:[4,6], 4:[5],5:[7],6:[8],7:[9],8:[10]}

    field_pos = {0:[['LB', 'LWB'],1], 1:[['CB'],2], 2:[['RB', 'RWB'],1], 3:[['CM'],2], 4: [['CAM', 'CDM'],1],5: [['LM', 'LW'],1], 6: [['CF', 'ST'],1], 7:[['RM', 'RW'],1], 8:[['GK'],1]}    

    alt_pos = {0:['RB','RWB','CB'],1:[['RB','LB']],2:['LB','LWB','CB'],3: ['CAM','CDM', 'LM', 'RM'], 4 : ['CM'], 5: ['RM','RW','CF','ST'], 6 : ['RM','LM'], 7 : ['LM','LW','ST','CF']}

    iter_count = 0
    df_start = pd.DataFrame()
    full_team_size = len(full_team)
    temp_team = full_team.sort_values(by = ['player_name','overall_rating']).drop_duplicates(subset = ['player_name'], keep = 'first').copy()
    
    find_alternate = False
    
    while field_pos:
        for key in list(field_pos.keys()):

            (positions, count) = field_pos[key]
            
            if find_alternate:
                positions = alt_pos[key]
                pos_players = temp_team[temp_team['position'].isin(positions)].sort_values(by = ['overall_rating'], ascending = False).head(count)
            else:
                pos_players = temp_team[temp_team['position'].isin(positions)].sort_values(by = ['overall_rating'], ascending = False).head(count)
                
            if len(pos_players) > 0:
                
                shirt_numbers = pos_index[key][:len(pos_players)]
                
                pos_players['pos_index'] = shirt_numbers
                pos_index[key] = pos_index[key][len(pos_players):]
                df_start = df_start.append(pos_players)
                temp_team = temp_team[~temp_team['player_name'].isin(pos_players['player_name'])]

                if len(pos_players)!=count:
                    missing_count = count - len(pos_players)
                    field_pos[key][1] = missing_count
                else:
                    del field_pos[key]
        find_alternate = True
        iter_count +=1

    return df_start

def get_fieldpos_data(years):
        
    d = create_match_data(years, create_team, get_features)
    return (d[attr_cols],d['Result'])

    #norm_tr_data = normalize(tr_data, x_norm_cols)
