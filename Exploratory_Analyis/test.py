import sqlite3 as db 
import pandas as pd
conn = db.connect('soccer/database.sqlite')

def create_teams(name, year):


all_players_info = pd.read_sql_query("""select  p.player_name,pa2.* from player_attributes pa2, player p where p.player_api_id = pa2.player_api_id and
(pa2.player_api_id, pa2.date) in (
select z.player_api_id, z.date from (
select pa.player_api_id, pa.date, min(abs(strftime('%s',pa.date) - strftime('%s','2014-09-01 00:00:00'))) from player_attributes pa, player p 
                                where pa.player_api_id = p.player_api_id
                                and strftime('%s',pa.date) > strftime('%s','2014-05-14 00:00:00') 
                                and pa.date like '2014%'
                                group by pa.player_api_id ) z )""",conn)

# date_info = pd.read_sql_query("""select pa.player_api_id, pa.date, min(abs(strftime('%s',pa.date) - strftime('%s','2014-09-01 00:00:00'))) from player_attributes pa, player p 
#                                 where pa.player_api_id = p.player_api_id
#                                 and strftime('%s',pa.date) > strftime('%s','2014-05-14 00:00:00') 
#                                 and pa.date like '2014%'
#                                 group by pa.player_api_id""",conn)

#all_players_info = pd.read_sql_query('select p.player_name,pa.* from player_attributes pa, player p where pa.player_api_id = p.player_api_id and pa.date like "2014-09-18%"',conn)

ptm = pd.read_csv('statbunker-football-stats/Player Stats 2014-15.csv')
ptm = ptm[(ptm['Type Of Goal'] == 'Player') & (ptm['League'] == 'Premier League')]

#caller.set_index('key').join(other.set_index('key'))
joined = all_players_info.set_index('player_name').join(ptm.set_index('Player'), how='inner')

pos_sel = {'Defender': 4, 'Midfielder': 3, 'Forward': 3, 'Goalkeeper':1}

everton = joined[joined['Team'] == 'Everton']

team_agg = {}
team_name = 'Everton'
for key,value in pos_sel.items():

    grp = everton[everton['Position'] == key ].groupby(['Position'])['overall_rating'].nlargest(value)
    avg = grp.mean()
    team_agg[key] = avg

print(team_agg)
# print(ptm)

# ap_set = set(all_players_info['player_name'].values)
# ptm_set = set(ptm['Player'].values)

# inter = ap_set.intersection(ptm_set)
# #print('John Terry' in inter)
# #print(len(inter))
# print(ptm_set.difference(inter))
# print(len(ptm_set.difference(inter)))

#all_players_info['player_name']
#print(ptm)
#print(joined['Team'])

#print(ptm)

#print(all_players_info)





# print(pa.columns)
# print(pa)

# player = pd.read_sql_query('select * from player where player_api_id = "505942"',conn)
# # c = conn.cursor()
# # # c.execute('select * from player_attributes where player_api_id =?',('505942'))
# # #c.execute('select * from player_attributes ')
# # c.execute("SELECT name FROM sqlite_master WHERE type='player_attributes';")
# # d = c.fetchall()
# # # print(d)
# # print(player.columns)
# # print(player)

# # team = pd.read_sql_query('select * from team where team_ = "505942"',conn)
