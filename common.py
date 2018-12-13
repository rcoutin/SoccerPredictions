import pandas as pd

norm_team_name = {}
norm_team_name['Man Utd'] = 'Manchester United'
norm_team_name['Man United'] = 'Manchester United'
norm_team_name['Manchester Utd'] = 'Manchester United'
norm_team_name['QPR'] = 'Queens Park Rangers'
norm_team_name['Newcastle'] = 'Newcastle United'
norm_team_name['Newcastle Utd'] = 'Newcastle United'
norm_team_name['Huddersfield'] = 'Huddersfield Town'
norm_team_name['Wolves'] = 'Wolverhampton Wanderers'
norm_team_name['Cardiff'] = 'Cardiff City'
norm_team_name['Leicester'] = 'Leicester City'
norm_team_name['Spurs'] = 'Tottenham Hotspur'
norm_team_name['West Ham'] = 'West Ham United'
norm_team_name['Brighton'] = 'Brighton & Hove Albion'
norm_team_name['Man City'] = 'Manchester City'
norm_team_name['West Brom'] = 'West Bromwich Albion'
norm_team_name['Bournemouth'] = 'Bournemouth'
norm_team_name['Stoke'] = 'Stoke City'
norm_team_name['Swansea'] = 'Swansea City'
norm_team_name['Hull'] = 'Hull City'
norm_team_name['Norwich'] = 'Norwich City'


def update_form(team_form,home_team_name, away_team_name, result):
        if result == 1:
            team_form[home_team_name] += 2
            team_form[away_team_name] -= 2
        elif result == 3:
            team_form[home_team_name] -= 3
            team_form[away_team_name] += 3
        else:
            team_form[home_team_name] -= 1
            team_form[away_team_name] += 1

def norm_team_names(team_info):
    """Normalize team names based on this mapping"""

    for key,value in norm_team_name.items():
        team_info.loc[lambda df: df['HomeTeam'] == key, 'HomeTeam'] = value
        team_info.loc[lambda df: df['AwayTeam'] == key, 'AwayTeam'] = value
    
    return team_info

def get_player_attribute_data(year):
        
    import sqlite3 as db 
    conn = db.connect('soccer/database.sqlite')

    query_str = """select  p.player_name,pa2.* from player_attributes pa2, player p where p.player_api_id = pa2.player_api_id and
    (pa2.player_api_id, pa2.date) in (
    select z.player_api_id, z.date from (
    select pa.player_api_id, pa.date, min(abs(strftime('%%s',pa.date) - strftime('%%s','%(year)s-09-01 00:00:00'))) from player_attributes pa, player p 
                                    where pa.player_api_id = p.player_api_id
                                    and strftime('%%s',pa.date) > strftime('%%s','2014-05-14 00:00:00') 
                                    and pa.date like '%(year)s%%'
                                    group by pa.player_api_id ) z )"""%{'year':year}
    
    all_player_attrs = pd.read_sql_query(query_str,conn)
    return all_player_attrs

def get_fixtures(year):

    if int(year) == 2018:
        f = pd.read_csv('epl18fixtures.csv')
    else:
        f = pd.read_csv('epl-results-19932018/EPL_Set.csv')
    f = f.replace(norm_team_name)
    
    return f[f['Season'].str.startswith(year)]



def get_player_attr_pos(year):
    """JOIN player attribute data with player position data based on PLAYER_NAME """
    data_year = {'2016':'epl2016_fifa17.csv','2017':'epl2017_fifa18.csv','2018':'epl2018_fifa19.csv'}
    if int(year) > 2015:
        
        return pd.read_csv(data_year[str(year)], dtype = {'overall_rating':float} ).replace(norm_team_name)

    else:
        player_position_data = pd.read_csv('player_pos.csv', dtype = {'overall_rating':float} )
        player_position_data = player_position_data[player_position_data['Year'] == int(year) + 1]

        player_attribute_data  = get_player_attribute_data(year)

        joined = player_attribute_data.merge(player_position_data,on = "player_name" , how='inner')
        return joined.replace(norm_team_name)

def get_all_team_data(year,create_team,get_features):
    """Given a year, create teams for all teams that played in the EPL in that year
    1) Create Team 2) Configure their attributes """
    data = {}

    joined_data = get_player_attr_pos(year)
    fixtures = get_fixtures(year)
    teams = fixtures['HomeTeam'].unique() #get all unique teams

    for team_name in teams:
     
        d = joined_data[joined_data['team'] == team_name.strip()]
        if d.empty:
            print(team_name,year)
        starting_team = create_team(joined_data[joined_data['team'] == team_name.strip()])
        features = get_features(starting_team)
        data[team_name] = (starting_team, features)
    return data

def get_teams_feature_diff(i,row,home_attrs,away_attrs,team_form):
    attrs = {}
   
    for key in home_attrs.keys():
        attrs[str(key)] = float(home_attrs[key]) - float(away_attrs[key])
        #attrs['a_'+str(key)] = 
        
    # attrs['h_form'] = team_form[row['HomeTeam']]
    # attrs['a_form'] = team_form[row['AwayTeam']]
    attrs['Home_Team'] = row['HomeTeam']
    attrs['Away_Team'] = row['AwayTeam']
    
    if str(row['FTHG']).strip() == "":
        attrs['Result'] == 4
    else:
        attrs['Result'] = 1 if row['FTHG'] - row['FTAG'] > 0  else (3 if row['FTHG'] - row['FTAG'] < 0 else 2)
    attrs['Game_Week'] = (i//10) + 1
    # norm_attrs['FTHG'] = row['FTHG']
    # norm_attrs['FTAG'] = row['FTAG']
   
                                        
    update_form(team_form,row['HomeTeam'],row['AwayTeam'],attrs['Result'])
    
    norm_df = pd.DataFrame(attrs, index = [str(i)])
    
    return norm_df 

    
def create_match_data(years,create_team,get_features):
    
    full_res_df = pd.DataFrame()
    
    for year in years:
        
        team_store = get_all_team_data(year,create_team,get_features)
        i = 0
        res_df = pd.DataFrame()
        f = get_fixtures(year)
        #f = f[~f['FTHG'].isnull()]
    
        team_form = {name:60 for name in f['HomeTeam'].unique()}
        
        for key,row in f.iterrows():
            home = row['HomeTeam']
            away = row['AwayTeam']

            home_attrs = team_store[home][1]
            away_attrs = team_store[away][1]

            res_df = res_df.append(get_teams_feature_diff(i,row,home_attrs,away_attrs,team_form))

            i = i + 1
        
        full_res_df = full_res_df.append(res_df)

    # full_res_df['h_form'] = full_res_df['h_form']/100
    # full_res_df['a_form'] = full_res_df['a_form']/100

    return full_res_df

    
def 