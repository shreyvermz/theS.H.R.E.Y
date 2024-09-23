import pandas as pd 
import numpy as np
#player stats from 1998-2022

# ADD A KEY TO CHANGE ABBREVIATIONS TO FULL NAMES AND FULL NAMES TO ABBREVIATIONS

# CREATE BENCHMARK VARIABLES TO TRACK TURNING POINTS THAT CAN BE USED
# TO SCORE EACH CATEGORY. 

#  S.      H.     R.             E.          Y.
#  SCORING. HELP. REASONABILITY. EFFICIENCY. YEARLY_OUTLOOK.

# EACH CATEGORY WILL BE SCORED AND GIVEN A RATING
# FIND A WAY TO COMBINE SCORE RATINGS IN THE END TO PRODUCE A PLAYER'S SHREY

# downloaded spreadsheet holding info from nba finals, we can use that when implementing yearly outlook and maybe even reasonability
scoring_grade = 0
help_grade = 0
position = ''
ppg = 0 
status = None # holds role that we made in the help section
won_title = False # hold false unless yearly outlook returns otherwise
stats = pd.read_csv('NBA_Player_Stats_2.csv')
team_stats = pd.read_csv('NBA_Team_Stats.csv')
yearly_results = pd.read_excel('NBA Finals and MVP.xlsx')
###################################################################################
def how_many_averaged_more(stat_name, stat, season): # gives us the number of players who averaged more of a given stat
                                                     # getter function
    # see how many averaged more points
    if str(stat_name) == 'PTS':
        # find how many averaged more 
        more = stats.loc[(stats['PTS'] > stat) &
                         (stats['Season'] == str(season)), 'Player'].count()
        
        return more 
    
     # see how many averaged more assists  
    elif stat_name == 'AST':
        
        more = stats.loc[(stats['AST'] > stat) &
                         (stats['Season'] == str(season)), 'Player'].count()
        
        return more
        
    elif stat_name == 'TRB':
        
        more = stats.loc[(stats['TRB'] > stat) &
                         (stats['Season'] == str(season)), 'Player'].count()
        
        return more
        
    elif stat_name == 'BLK':
        
        more = stats.loc[(stats['BLK'] > stat) &
                         (stats['Season'] == str(season)), 'Player'].count()
        
        return more 
        
    elif stat_name == 'STL':
    
        more = stats.loc[(stats['STL'] > stat) &
                         (stats['Season'] == str(season)), 'Player'].count()
        
        return more 
    
    elif stat_name == 'MP':
    
        more = stats.loc[(stats['MP'] > stat) &
                         (stats['Season'] == str(season)), 'Player'].count()
        
        return more 
    
    else:
        return 'Not a valid entry'
###################################################################################
def scoring(name, season): # find out how many players averaged more points after we get ppg
                           # split into positions, as ppg, apg, rpg have different tiers for different positions
                           # first score is a result of ppg and their corresponding scoring tier (see tier setter function for details)
                           # score is then scaled depending on where in the nba player ranked in ppg
                           # only the top 10 scorers are able to get this second scaling added (works to keep top achievers of this stat exclusive)
    
    global ppg
    global position
    global status
    global scoring_grade
    
    # makes sure passed in info can be used
    if not stats[(stats['Player'] == str(name)) & (stats['Season'] == str(season))].empty:
        # getting players positions for stats like assists, rebounds, blocks
        position = stats.loc[(stats['Player'] == str(name)) &
                             (stats['Season'] == str(season)), 'Pos'].values
        
        # holds the ppg even across other teams
        ppg = round(stats.loc[(stats['Player'] == str(name)) &
                              (stats['Season'] == str(season)), 'PTS'].values.mean(), 2)
        
        # holds the teams the player played with across the season
        teams = stats.loc[(stats['Player'] == str(name)) &
                          (stats['Season'] == str(season)) &
                          (stats['Tm'] != 'TOT'), 'Tm'].values
        # TOT is total, not Toronto. We dont want the combined portion for now 
        filtered_teams = teams[teams != 'TOT']
        
        # calls function to see how many averaged more 
        better = how_many_averaged_more('PTS', ppg, season)
        
        # calls function to see what the average across all players in the league that season was 
        avg = season_average('PTS', season)
        # places scorer in their scoring tier, the lower tier the better
        tier_holder = tier_setter('PTS', ppg, position)
        # base scoring grade, before any qualifying tier scalers are applied
        scoring_score1 = round(ppg * tier_holder, 2)
        # only applies if player was a top 10 average scorer
        if (better < 10):
            if (better == 9):
                scoring_scaler = 1.05
            elif (better == 8):
                scoring_scaler = 1.1
            elif (better == 7):
                scoring_scaler = 1.15
            elif (better == 6):
                scoring_scaler = 1.2
            elif (better == 5):
                scoring_scaler = 1.25
            elif (better == 4):
                scoring_scaler = 1.28
            elif (better == 3):
                scoring_scaler = 1.3
            elif (better == 2):
                scoring_scaler = 1.33
            elif (better == 1):
                scoring_scaler = 1.35
            elif (better == 0):
                scoring_scaler = 1.5
            # applies scaler to final score if in the top 10 average scorers  
            scoring_grade = round(scoring_score1 * scoring_scaler, 2)
        
        else:
            # if not in the top 10
            scoring_grade = scoring_score1
            
        
        # statement returned after info found
        return '\n' + str(name) + ' averaged ' + str(ppg) + ' points per game while playing for ' + str(filtered_teams) +\
            '\nThe average across all players (at least 10 minutes per game) was ' + str(avg) +\
            '. ' + str(better) + ' players averaged more points. Based on these stats,' +\
                ' their scoring grade was ' + str(scoring_grade) + '.'
        
    
    else:
        # in case info is not found
        return 'Player or season not found in database.'
############################################################################################################## 
def help(name, season): # get a help scaler as a result of POINTS RATIO / STOCKS SCALER /  REASONABILITY FUNCTION OUTPUT
                        # assists and rebounds are given tiers and applied to the help scaler
                        # taking into account rebounding, assists, and defensive contributions in order to determine a players impact on their team
                        # we take defensive efficiency into account to assign roles to a player
                        # still need to figure out where to use roles. Could be part of the text based answer
    
    global ppg
    global position
    global status
    global help_grade
    
    # look if it exists
    if not stats[(stats['Player'] == str(name)) & (stats['Season'] == str(season))].empty:
        # format date so we can access other database
        season_formatted = convert_date(season)
        # get their team names
        teams = stats.loc[(stats['Player'] == str(name)) &
                          (stats['Season'] == str(season)) &
                          (stats['Tm'] != 'TOT'), 'Tm'].values
        # iterate through because some play for multiple teams
        for i in teams:
            # change format to send to database
            team_full_name = abbreviation_to_name(i)
            # send the team name to yearly outlook to check if a chip was won 
            won_title = yearly_outlook(team_full_name, season)
            # get teams stats for the year
            # if not team_stats[(team_stats['Team'] == str(team_full_name)) & (team_stats['Year'] == str(season_formatted))].empty:
            
            this_teams_pts = team_stats.loc[(team_stats['Team'] == str(team_full_name)) &
                                            (team_stats['Year'] == str(season_formatted)), 'Pts'].values
                
            # show teams points
            print('\nWhile ' + str(name) + ' played for ' + str(team_full_name) + ', the team averaged ' + str(this_teams_pts) + ' points per game.')
            # calculates the ratio for the points scored and team scored
            ratio = ppg / this_teams_pts
            # stocks (steals and blocks) in order to provide to the HELP SCALER
            stocks_holder, stocks_tier_holder = get_stocks(name, season)
            # constant scaler that gives most of the basis for the help score (PORTION OF POINTS, ERA OF TIME PLAYED, DEFENSIVE IMPACT THROUGH STOCKS)
            HELP_SCALER = (ratio + 1) * reasonability(name, season) * stocks_tier_holder
            # rounding 
            team_ratio = np.round((ratio * 100), 2)
            # --------------------------------------------------------------
            # now lets start accounting for assists
            
            # tracks assists per game
            apg = round(stats.loc[(stats['Player'] == str(name)) &
                              (stats['Season'] == str(season)), 'AST'].values.mean(), 2)
            
            # gets position of the player so we can make tiers, its global so we can access it in other function/later on
            position = stats.loc[(stats['Player'] == str(name)) &
                                 (stats['Season'] == str(season)), 'Pos'].values[0]
            # place player into tier depending on their assist numbers
            assists_tier = tier_setter('AST', apg, position)
            # show how many averaged more, just like scoring
            better_apg = how_many_averaged_more('AST', apg, season)
            # calculates part of the final help score
            help_score_assists = HELP_SCALER * assists_tier
            
            # now account for rebounds 
            
            rpg = round(stats.loc[(stats['Player'] == str(name)) &
                              (stats['Season'] == str(season)), 'TRB'].values.mean(), 2)
            # place player into tier depending on their assist numbers
            rebounds_tier = tier_setter('TRB', rpg, position)
            # show how many averaged more, just like scoring
            better_rpg = how_many_averaged_more('TRB', apg, season)
            # calculates part of the final help score
            help_score_rebounds = rebounds_tier * HELP_SCALER
            help_grade = help_score_assists + help_score_rebounds
            # getting defensive efficiency of team to place into impact category
            team_defense_eff = team_stats.loc[(team_stats['Team'] == str(team_full_name)) &
                                            (team_stats['Year'] == str(season_formatted)), 'Deff'].values
            
            # time to set status, a global varibale we declared
            # criteria for Giver, subject to change
            if ((team_ratio > 22) & (team_defense_eff > 1) & (5 <= help_grade < 10)):

                status = 'Giver'
            # criteria for Winner, is basically the best category to be placed into (good defense lowers help score needed to qualify)
            elif ((team_ratio > 20) & (team_defense_eff < -0.5) & (help_grade > 6.0)) or ((team_ratio > 24) & (help_grade >= 10.0)): 
                
                status = 'Winner'
            # criteria for Complimentary player   
            elif (team_ratio < 20) & ((team_defense_eff < -5) or (help_grade >= 6.5)):
                
                status = 'Complimentary'
            # anything else will be a taker -> TEST THIS AND ADJUST CATEGORIES IF MORE ACCURATE PLACEMENTS NEEDED  
            else:
                
                status = 'Taker'
            
            # statements to the console 
            print('His team had a defensive efficiency of ' + str(team_defense_eff) + ' helped by his ' + str(stocks_holder) + ' stocks per game, scaling his help score by ' + str(stocks_tier_holder))
            print('Percent of teams points accounted for: ' + str(team_ratio) + '%. His corresponding help scaler is: ' + str(HELP_SCALER))
            print('He averaged ' + str(apg) + ' assists per game as a ' + str(position) + ', and has placed into tier ' + str(assists_tier) + ' for his position.')
            print('He averaged ' + str(rpg) + ' rebounds per game as a ' + str(position) + ', and has placed into tier ' + str(rebounds_tier) + ' for his position.')
            print(str(better_apg) + ' players averaged more assists in ' + str(season) + '.')
            print(str(better_rpg) + ' players averaged more rebounds in ' + str(season) + '.')
            print('The total help score so far is ' + str(np.round(help_grade, 2)))
            if (won_title == True):
                print(str(name) + ' won a title this season, so his role will change from ' + str(status) + ' to Winner.')
                status = 'Winner'
            else:
                print(str(name) + ' played the role of ' + str(status) + ' for ' + str(team_full_name))
            # print('This player won a title this season: ' + str(won_title))
            
            
            
            # add descriptions and criteria that outlines why the player was given the role they were given
            print('Would you like to see more information regarding the players role?\n')
            role_choice = input('Please enter \'Yes\' or \'No\' or \'ALL\' to see a description for all 4 roles: ')
            if role_choice == 'Yes':
                role = status
                print(role_descriptor(role))
            elif role_choice == 'No':
                pass
            elif role_choice == 'ALL':
                role = 'ALL'
                print(role_descriptor(role))
            else:
                print('\nNot a valid input.\n')
                 
            return 'This concludes the help section. Reasonability was factored in the process of calculating the final help score.\n'
              
##################################################################################################################      
# look at eras the player played in and return a corresponding scaler for reasonability
def reasonability(name, season): # smallest operation of the S.H.R.E.Y. process
                                 # is mostly used as a complimentary function to HELP
                                 # takes the era a player scored in and scales their scoring feats to match the style of play
                                 # PRE 2004-05 / 2004-2012 / 2012 - 2014 / 2014+
                                                            #smallest era
    
    global ppg
    global position
    global status

    # check if player and season exists in database
    if not stats[(stats['Player'] == str(name)) & (stats['Season'] == str(season))].empty:
        
        # for every year before the up tempo era
        if (season < '2004-05'):
            # biggest scaling since scoring was the most scarce here
            if (ppg < 10):
                return 1
            elif (10 <= ppg < 15):
                return 1.05
            elif (15 <= ppg < 20):
                return 1.15
            elif (20 <= ppg < 25):
                return 1.3
            elif (25 <= ppg < 30):
                return 1.5
            else:
                return 2
            # scaling gets smaller as players become better at scoring 
        elif ('2004-05' <= season < '2016-17'):
            
            if (ppg < 15):
                return 1
            elif (15 <= ppg < 20):
                return 1.05
            elif (20 <= ppg < 25):
                return 1.15
            elif (25 <= ppg < 30):
                return 1.3
            else:
                return 1.7   
            
            
        elif (season >= '2016-17'):
            
            if (ppg < 20):
                return 1
            elif (20 <= ppg < 25):
                return 1.05
            elif (25 <= ppg < 30):
                return 1.15
            else:
                return 1.3
            
        else:
            return 'Inputted season did not correlate to an era'
        
##################################################################################################################

def efficiency(name, season): # main comparison stat will be eFG
                              # probably the most in depth efficiency analysis we can get
                              # a stat made up randomly won't be as effective
                              # simple function not due to ineffectiveness, but rather overeffectiveness of the eFG stat
                              # for now is mostly text based, not much to do with eFG besides show it 
                              # main goal is to provide context for the stat and why it matters depending on the era of the player chosen
    global ppg
    global position
    global status
    
    if not stats[(stats['Player'] == str(name)) & (stats['Season'] == str(season))].empty:
        
        efieldgoal = round(stats.loc[(stats['Player'] == str(name)) &
                                      (stats['Season'] == str(season)), 'eFG%'].values.mean(), 2)
        efieldgoal = round((efieldgoal * 100), 2)
        
        # efieldgoal = round(stats.loc[(stats['Player'] == str(name)) &
        #                               (stats['Season'] == str(season)), 'eFG%'].values.mean(), 2)
        # for every year before the up tempo era
        if (season < '2004-05'):
            
            if (efieldgoal < 38):
                eff_description = str(name) + ' played before the craze of the Seven Seconds or Less ' +\
                                                'tempo of offense introduced by Mike D\'antoni in 2004-2005. 3 pointers ' +\
                                                'were not nearly as prevalent as they are today, and ' + str(name) +\
                                                ' struggled with scoring the ball efficiently during an era with a lack of ' +\
                                                'offensive creativity with an eFG of ' + str(efieldgoal) + '%. Perhaps the embrace ' +\
                                                'of the three point shot would have boded well for ' + str(name) + '\'s playstyle.'
                                                
                return eff_description
            elif (38 <= efieldgoal < 44):
                eff_description = str(name) + ' played before the craze of the Seven Seconds or Less ' +\
                                              'tempo of offense introduced by Mike D\'antoni in 2004-2005. 3 pointers ' +\
                                              'were not nearly as prevalent as they are today, and ' + str(name) +\
                                              ' showed adequate aptitude in scoring the ball with an eFG of ' + str(efieldgoal) + '%.'
                                                
                return eff_description
            elif (44 <= efieldgoal < 50):
                eff_description = str(name) + ' played before the craze of the Seven Seconds or Less ' +\
                                                'tempo of offense introduced by Mike D\'antoni in 2004-2005. 3 pointers ' +\
                                                'were not nearly as prevalent as they are today, yet ' + str(name) +\
                                                ' showed no issues with scoring the ball efficiently within the era\'s playstyle, boasting an ' +\
                                                'eFG of ' + str(efieldgoal) + '%.'
                return eff_description
            else:
                eff_description = str(name) + ' played before the craze of the Seven Seconds or Less' +\
                                                'tempo of offense introduced by Mike D\'antoni. 3 pointers ' +\
                                                'were not nearly as prevalent as they are today, and the overall pace of the game '+\
                                                'would be almost unrecognizable today. \nHowever ' + str(name) +\
                                                ' displayed masterful control over the slower paced and minimally spaced ' +\
                                                'offensive tendencies of pre-modern teams, as their eFG was at a whopping' + str(efieldgoal) +\
                                                '%.'
                return eff_description
            
        elif ('2004-05' <= season < '2016-17'):
            
            if (efieldgoal < 40):
                eff_description = str(name) + ' played at the cusp of our modern age of offense, beginning in 2004. Mike D\'antoni famously ' +\
                                              'urged the Phoenix Suns to play a style of offense that lived by the rule: Seven Seconds or Less. ' +\
                                              'This ushering of up tempo offense made scoring easier around the league, and the age of virtually unstoppable ' +\
                                              'offense was born. \nHowever, ' + str(name) + ' was the furthest thing from unstoppable, as their eFG was an abysmal ' +\
                                            + str(efieldgoal) + '%.'
                                            
                return eff_description
            elif (40 <= efieldgoal < 47):
                eff_description = str(name) + ' played at the cusp of our modern age of offense, beginning in 2004. Mike D\'antoni famously ' +\
                                              'urged the Phoenix Suns to play a style of offense that lived by the rule: Seven Seconds or Less. ' +\
                                              'This ushering of up tempo offense made scoring easier around the league, and the age of virtually unstoppable ' +\
                                              'offense was born. \n' + str(name) + ' was serviceable in this era, and shot reasonably average at an eFG of ' +\
                                            + str(efieldgoal) + '%.'
                return eff_description
            elif (47 <= efieldgoal < 52):
                eff_description = str(name) + ' played at the cusp of our modern age of offense, beginning in 2004. Mike D\'antoni famously ' +\
                                              'urged the Phoenix Suns to play a style of offense that lived by the rule: Seven Seconds or Less. ' +\
                                              'This ushering of up tempo offense made scoring easier around the league, and the age of virtually unstoppable ' +\
                                              'offense was born. \n' + str(name) + ' took advantage of this faster style of play, and contributed an eFG of ' +\
                                               str(efieldgoal) + '%.' 
                return eff_description
            else:
                eff_description = str(name) + ' played at the cusp of our modern age of offense, beginning in 2004. Mike D\'antoni famously ' +\
                                              'urged the Phoenix Suns to play a style of offense that lived by the rule: Seven Seconds or Less. ' +\
                                              'This ushering of up tempo offense made scoring easier around the league, and the age of virtually unstoppable ' +\
                                              'offense was born. \nThis new style of play was ideal for ' + str(name) + ', as the combination of an optimal ' +\
                                              'shot diet along with shot-making skills, they imposed an eFG of ' + str(efieldgoal) + '%.'
                return eff_description
            
            
        elif (season >= '2016-17'):
            
            
            if (efieldgoal < 45):
                eff_description = str(name) + ' was a participant in the beginning of the most electric era of offensive basketball. The' +\
                                              ' emergence of Stephen Curry and his one-man revolution in the league resulted in an era dominated' +\
                                              ' by the three pointer. Efficiency skyrocketed in this age, as analytics deemed three pointers as the' +\
                                              ' best use of an offense\'s possessions, denoted by a Houston Rockets team that took almost half of their' +\
                                              ' shots from three point range. \n' + str(name) + ' struggled with the lightning fast pace of the game' +\
                                              ' and posted an eFG of ' + str(efieldgoal) + '%.'
                return eff_description
            elif (45 <= efieldgoal < 50):
                eff_description = str(name) + ' was a participant in the beginning of the most electric era of offensive basketball. The' +\
                                              ' emergence of Stephen Curry and his one-man revolution in the league resulted in an era dominated' +\
                                              ' by the three pointer. Efficiency skyrocketed in this age, as analytics deemed three pointers as the' +\
                                              ' best use of an offense\'s possessions, denoted by a Houston Rockets team that took almost half of their' +\
                                              ' shots from three point range. \n' + str(name) + ' proved a viable scoring option for this fast paced era,' +\
                                              ' with an eFG of ' + str(efieldgoal) + '%.'
                return eff_description
            elif (50 <= efieldgoal < 55):
                eff_description = str(name) + ' was a participant in the beginning of the most electric era of offensive basketball. The' +\
                                              ' emergence of Stephen Curry and his one-man revolution in the league resulted in an era dominated' +\
                                              ' by the three pointer. Efficiency skyrocketed in this age, as analytics deemed three pointers as the' +\
                                              ' best use of an offense\'s possessions, denoted by a Houston Rockets team that took almost half of their' +\
                                              ' shots from three point range. \n' + str(name) + ' was a seamless fit into this evolved playstyle,' +\
                                              ' using the increased space on the floor and shot oppurtunities to merit an eFG at ' + str(efieldgoal) + '%.' 
                return eff_description
            else:
                eff_description = str(name) + ' was a participant in the beginning of the most electric era of offensive basketball. The' +\
                                              ' emergence of Stephen Curry and his one-man revolution in the league resulted in an era dominated' +\
                                              ' by the three pointer. Efficiency skyrocketed in this age, as analytics deemed three pointers as the' +\
                                              ' best use of an offense\'s possessions, denoted by a Houston Rockets team that took almost half of their' +\
                                              ' shots from three point range. \n' + str(name) + ' was one of the most efficient scorers in the league during' +\
                                              ' the ' + str(season) + ' season. By keeping their eFG at ' + str(efieldgoal) + '%, they were able to add' +\
                                              ' value to their team while earning them extra possessions with smarter shots, constituting the makings' +\
                                              ' of a winning player.'
                return eff_description
        else:
            return 'Inputted season did not correlate to an era'
###################################################################################################################

def yearly_outlook(team, season): # Might need to bring in third database showing the league winners
                                  # how much weight does winning a championship add to a player?
                                  # and how do we split the credit with a championship when considering a role player vs a star?
                                  # MVPs dont hold too much weight in my eyes because voter fatigue affected certain players disproportionately
                                  # called in the process of help, used implicitly like tier setter 
    global won_title    
                              
    # case handling for lakers and clippers because their abbreviation transformation was different
    if team == 'L.A.Lakers':
        temp_team = 'Lakers'
    elif team == 'L.A.Clippers':
        temp_team = 'Clippers'
    else:
        temp_team = team
        
    # storing a temp year value we can use in 3rd database  
    temp_season = season[:4]
    
    
    # accessing name of the winner of the league in the given year
    winner_this_year = yearly_results.loc[yearly_results['Year'] == int(temp_season), 'NBA Champion'].values
    
    # print(winner_this_year)    
    # if the team name and winner this year have the same name
    if str(temp_team) in str(winner_this_year):
        won_title = True
    else:
        won_title = False
    
    # return whether or not the player won a title this year
    return won_title
    
    
    
###################################################################################################################
def abbreviation_to_name(abbrev):
    # hardcode the direct correlations
    if abbrev == 'VAN':
        return 'Vancouver'
    elif abbrev == 'SAC':
        return 'Sacramento'
    elif abbrev == 'CHI':
        return 'Chicago'
    elif abbrev == 'TOR':
        return 'Toronto'
    elif abbrev == 'SAS':
        return 'San Antonio'
    elif abbrev == 'DEN':
        return 'Denver'
    elif abbrev == 'MIL':
        return 'Milwaukee'
    elif abbrev == 'CLE':
        return 'Cleveland'
    elif abbrev == 'ATL':
        return 'Atlanta'
    elif abbrev == 'POR':
        return 'Portland'
    elif abbrev == 'BOS':
        return 'Boston'
    elif abbrev == 'UTA':
        return 'Utah'
    elif abbrev == 'ORL':
        return 'Orlando'
    elif abbrev == 'DAL':
        return 'Dallas'
    elif abbrev == 'SEA':
        return 'Seattle'
    elif abbrev == 'GSW':
        return 'Golden State'
    elif abbrev == 'CHH':
        return 'Charlotte'
    elif abbrev == 'MIA':
        return 'Miami'
    elif abbrev == 'LAC':
        return 'L.A.Clippers'
    elif abbrev == 'PHI':
        return 'Philadelphia'
    elif abbrev == 'LAL':
        return 'L.A.Lakers'
    elif abbrev == 'NJN':
        return 'New Jersey'
    elif abbrev == 'IND':
        return 'Indiana'
    elif abbrev == 'NYK':
        return 'New York'
    elif abbrev == 'PHO':
        return 'Phoenix'
    elif abbrev == 'HOU':
        return 'Houston'
    elif abbrev == 'MIN':
        return 'Minnesota'
    elif abbrev == 'WAS':
        return 'Washington'
    elif abbrev == 'DET':
        return 'Detroit'
    elif abbrev == 'MEM':
        return 'Memphis'
    elif abbrev == 'NOH':
        return 'New Orleans'
    elif abbrev == 'CHA':
        return 'Charlotte'
    elif abbrev == 'NOK':
        return 'New Orleans'
    elif abbrev == 'OKC':
        return 'Oklahoma City'
    elif abbrev == 'BRK':
        return 'Brooklyn'
    elif abbrev == 'NOP':
        return 'New Orleans'
    elif abbrev == 'CHO':
        return 'Charlotte'
    elif abbrev == 'TOT':
        return 'got total. we dont want it'
    else:
        return 'Not a valid abbreviation'
######################################################################################
def season_average(stat_name, year):
    
    if stat_name == 'PTS':
        # checks ppg of all players over 10 mpg to not skew the data 
        return round(stats.loc[(stats['Season'] == str(year)) &
                               (stats['MP'] >= 10), 'PTS'].values.mean(), 2)
    
    # add the rest as we go 
####################################################################################### 
def get_stocks(name, season):
    # find blocks stats in season
    blockspg = round(stats.loc[(stats['Player'] == str(name)) &
                              (stats['Season'] == str(season)), 'BLK'].values.mean(), 2)
    # find steals stats in season
    stealspg = round(stats.loc[(stats['Player'] == str(name)) &
                              (stats['Season'] == str(season)), 'STL'].values.mean(), 2)
    # combine steals and blocks to get stocks
    stockspg = round((blockspg + stealspg), 2)
    # add scaling to the stocks
    if (2 <= stockspg < 3):
        stocks_tier = 1.1
    elif (3 <= stockspg < 4):
        stocks_tier = 1.15
    elif (4 <= stockspg < 5):
        stocks_tier = 1.5
    elif (stockspg >= 5):
        stocks_tier = 2
    else:
        stocks_tier = 1
    # use the stocks stat in order to gauge contribution to team defense
    return stockspg, stocks_tier
 ####################################################################################        
def tier_setter(stat_name, stat, position): # ppg doesnt need to be split up among positions
                                            # apg and rpg need their own categories 
                                            # someone like russell westbrook and jokic need to be regarded as the positional anomalies they are
                                            # most likely wont need to split up the rest, stocks make sure guard and big defense are regarded differently
    # tier setting for points
    if stat_name == 'PTS':
        
        if 0 <= stat < 10:
            tier = 1
        elif 10 <= stat < 15:
            tier = 2 
        elif 15 <= stat < 17:
            tier = 3
        elif 17 <= stat < 20:
            tier = 4
        elif 20 <= stat < 23:
            tier = 5
        elif 23 <= stat < 26:
            tier = 6
        elif 26 <= stat < 29:
            tier = 7
        elif 29 <= stat < 30:
            tier = 8
        elif 30 <= stat < 32:
            tier = 9
        elif stat >= 32:
            tier = 10
        else:
            return 'Not a valid stat line'     
        
        return tier
    # tier setting for assists
    elif stat_name == 'AST':
        # point guards
        if str(position) == 'PG':
            
            if 5 <= stat < 7:
                tier = 2
            elif 7 < stat < 10:
                tier = 3
            elif stat >= 10:
                tier = 4
            else:
                tier = 1
        # shooting guards
        elif str(position) == 'SG':
            
            if 4 <= stat < 6:
                tier = 2
            elif 6 <= stat < 8:
                tier = 3
            elif stat >= 8:
                tier = 4
            else:
                tier = 1
        # small forwards
        elif str(position) == 'SF':
            
            if 3 <= stat < 4:
                tier = 2
            elif 4 <= stat < 6:
                tier = 3
            elif stat >= 6:
                tier = 4
            else:
                tier = 1
        # power forwards        
        elif str(position) == 'PF':
            
            if 1 <= stat < 3:
                tier = 2
            elif 3 <= stat < 5:
                tier = 3
            elif stat >= 5:
                tier = 4
            else:
                tier = 1
        # centers        
        elif str(position) == 'C':
            
            if 0.5 <= stat < 2:
                tier = 2
            elif 2 <= stat < 4:
                tier = 3
            elif stat >= 4:
                tier = 4
            else:
                tier = 1        
        else:
            return 'Unable to map players position'
        # give back the tier when done 
    
    elif stat_name == 'TRB':
        
        if str(position) == 'PG':
            
            if 3 <= stat < 5:
                tier = 2
            elif 5 <= stat < 7:
                tier = 3
            elif stat >= 7:
                tier = 4
            else:
                tier = 1
        # shooting guards
        elif str(position) == 'SG':
            
            if 3 <= stat < 5:
                tier = 2
            elif 5 <= stat < 7:
                tier = 3
            elif stat >= 7:
                tier = 4
            else:
                tier = 1
        # small forwards
        elif str(position) == 'SF':
            
            if 4 <= stat < 5.5:
                tier = 2
            elif 5.5 <= stat < 7.5:
                tier = 3
            elif stat >= 7.5:
                tier = 4
            else:
                tier = 1
        # power forwards        
        elif str(position) == 'PF':
            
            if 4 <= stat < 6:
                tier = 2
            elif 6 <= stat < 8.5:
                tier = 3
            elif stat >= 8.5:
                tier = 4
            else:
                tier = 1
        # centers        
        elif str(position) == 'C':
            
            if 5 <= stat < 7:
                tier = 2
            elif 7 <= stat < 10:
                tier = 3
            elif stat >= 10:
                tier = 4
            else:
                tier = 1        
        else:
            return 'Unable to map players position'
        # give back the tier when done 
        
        
    return tier
    
 #############################################################   
def convert_date(date):
    # split our existing date
    year, month = date.split('-')
    # store next year
    next_year = int(year) + 1
    # return new format
    return f"{year}-{next_year}"
    
##########################################################
def role_descriptor(role): # give a menu dropdown that shares criteria and aptitudes of each role criteria
                           # complimenter, giver, winner, and taker
    
    if role == 'Giver':
        
        giver_desc = '\nThe Giver is a player who, more often than not, has to compensate for their teams shortcomings on the offensive or defensive ' +\
                'end by scoring a high volume of their teams points and taking control of the game. Due to this offensive workload, a Giver ' +\
                'most likely has less defensive responsibility, and this player may not be the first choice you have when implementing a defensive lineup. ' +\
                'These players are, more often than not, heliocentric players who may be featured like a workhorse running back. Think of players such as ' +\
                'Luka Doncic, James Harden, Stephen Curry after Kevin Durant left him, and the list goes on. The prevalence of this archetype displays their effectiveness, ' +\
                'while many analysts may argue this playstyle is not conducive to a winning team. \n' +\
                'The criteria for this role were curated with this offensive/defensive dichotomy in mind, as the first qualification is accounting for at least (22%) of your teams points. ' +\
                'The next moniker of a Giver is having a lackluster defense. While the team defense may not be be entirely indicative of a players performance on that side of the ball, ' +\
                'having a high offensive usage paired with an underperforming defense does not typically correlate to a positive defensive impact. \n' +\
                'Keeping this in mind, the next criteria that must be met is a team defensive efficiency exceeding 1 for that season. ' +\
                'The last indicator of a Giver is that they contribute to the game in ways other than their scoring, like finding teammates or seeking out rebounds. \n' +\
                'Keeping this in mind, the player must have a help score between 5 and 10 in order to ensure impact in other aspects of the game. Any help score over 10 ' +\
                'begins to compensate for a player\'s defensive shortcomings and consequentally alters their role assignment. \n'
                
        return giver_desc
    
    elif role == 'Taker':
        
        taker_desc =  '\nThe Taker is the lowest tier of roles a player can be assigned in this portion of our analysis. A Taker fails to meet the criteria of the other 3 categories, ' +\
                'and is stuck in role-assigned purgatory. This player is unable to post a positive measureable impact on, not only the scoring end, but in complimentary ' +\
                'offensive endeavors like rebounds and assists, resulting in a help score too low for assignment to any of the other 3 roles. Players in this category may provide one essential ' +\
                'skill at a high level, such as shooting or rebounding, but they fail to impact the game in a variety of ways besides that. Their defensive impact isn\'t enough to merit a more ' +\
                'favorable evaluation. Many players who are signed to be shooters for a team will fall into this category. Being a shooter is one of the most demanded ' +\
                'commodities in our league, so many teams employ statistically handicapping players with the exception that they provide the most important skill set in the league. \n'
                
        return taker_desc
    
    elif role == 'Winner':
        # make sure to add portion that automatically makes player a Winner for the season if they won a chip
        winner_desc =  '\nThe Winner is the type of player that is most advantageous to have in a championship run according to this program\'s analysis. A Winner is a player who may not bear as heavy of ' +\
                'an offensive workload as a heliocentric role  akin to certain Givers, but that is because their team holds a favorable defensive efficiency while feauturing them as one of ' +\
                'the teams top scorers. Many players who fit in this category were former Givers, but the want for winning often outweighs the oppurtunity for stardom. ' +\
                'Players with fragile egos regarding how they are perceived by fans may be reluctant to allow themselves to take less of an offensive burden to qualify for this role, ' +\
                'as most conventional and popular statistics make it hard for common fans to pinpoint their impact. Though good defense is important, it is not the true measure that seperates ' +\
                'the Giver from the Winner. The true testament to what makes a Winner so great is the ability to make their defensive presence viable in a well-running defensive scheme ' +\
                'while maintaining the bulk of their offensive impact. \n' +\
                'Keeping this in mind, the first criteria that must be met is at least (20%) of their team\'s points resulting from them.\n' +\
                'Now that we ensured this player is still a high-level contributor on the scoring end, we must account for other ways they can impact ' +\
                'the game offensively. \n' +\
                'To make sure this player has accounted for extra-cirricular offensive impact, the second criteria that must be met is a help score exceeding 6. \n' +\
                'The offensive excellency of a Winner is impressive, but what is even more impressive is how their team is able to package this aptitude with an efficient defense. ' +\
                'An efficient defense with a high quality offensive contributor is often a positive reflection of the players making up the lineup. This means each player contributes to ' +\
                'a net positive basketball group, and has curated a formula that this analysis has concluded as the epitome of winning basketball. \n' +\
                'To account for this balanced style of basketball in our criteria, a team must have a defensive efficiency lower than -0.5. \n' +\
                'There is a way for a player to circumvent the previous criteria: to brute force their way to becoming a winning basketball player. ' +\
                'In this analysis, defensive success is the best compliment to good offense. However, there are certain players who are statistical anomalies when ' +\
                'it concerns the offensive side of the ball. I think the only rival to a complimentary defense is unstoppable offense. Defense is less of a factor ' +\
                'when a player wreaks enough havoc to continue tipping the scales in their team\'s favor. \n' +\
                'To account for these \'force of nature\' offensive players, that are seemingly becoming more common in conjunction to the rise ' +\
                'of offensive efficiency, additional criteria, including a player scoring (24%) of their teams respective points and maintaining a ' +\
                'help score of 10 or more, were added that can bolster a player\'s status straight to Winner. \n' +\
                'Lastly, using the Championships and MVP database, we can force every player who has won a championship for each season as a Winner. \n'
                
        return winner_desc
    
    elif role == 'Complimentary':
        # < 20, less than -5, more than or equal to 6.5
        compliment_desc = '\nThe Complimentary role was made with the blue-collar, defensively inclined, and master-of-intangibles in mind. Getting a player that ' +\
                'can shoulder the offensive work and be competent defensively is the gold standard for winning, however it is these Complimentary ' +\
                'players that truly oil the machine. Competency is the bare minimum, however these are the players that allow the Winners to ' +\
                'be comfotable with being adequate, as the Winners know their Compliments will be making up for everything around the edges. ' +\
                'A Complimentor, many times, is indicative of a team with multiple star-level players. The presence of other stars allows players, who ' +\
                'would otherwise put up more eye-popping numbers, to slump into a role more conducive to winning, therefore becoming a compliment to ' +\
                'those around him. For example, Chris Paul has mostly played the role of a Giver and Winner through a career punctuated by efficient scoring ' +\
                'and unparalleled passing chops. However, after growing older and into a less prominent scoring role with teams like the Suns or now the Spurs, ' +\
                'Chris Paul has slid himself into the role of a Complimentary player, taking what his years give him and conforming his playstyle to highlight his teammates. ' +\
                'Considering the lower offensive usage that befits those placed in this role, the first criteria makes sure the player has accounted for less than (20%) of his team\'s points. \n' +\
                'Once we are sure we have a low scoring player, we must pinpoint significant impact in other areas of the game. \n' +\
                'We do this by considering two more criteria: a team having a defensive efficiency under -5 and a player having a help score over 6.5. ' +\
                'Only one of these need to be true in conjunction with the low scoring criteria for a player to be placed into this category. \n' +\
                'Most players in the league will fall into the Complimentary and the Taker categories. Often times the difference between making yourself known ' +\
                'as a winning or losing player is dictated by the team you are surrounded by and how you are able to conform to their strengths and weaknesses. ' +\
                'Many Takers will have been Complimentary at worst on good teams, and many of those who are Complimentary would be slunk into the spot of Taker on a worse team. \n'
                
        return compliment_desc 
    
    elif role == 'ALL':
        all_desc = '\nThe Giver is a player who, more often than not, has to compensate for their teams shortcomings on the offensive or defensive ' +\
                'end by scoring a high volume of their teams points and taking control of the game. Due to this offensive workload, a Giver ' +\
                'most likely has less defensive responsibility, and this player may not be the first choice you have when implementing a defensive lineup. ' +\
                'These players are, more often than not, heliocentric players who may be featured like a workhorse running back. Think of players such as ' +\
                'Luka Doncic, James Harden, Stephen Curry after Kevin Durant left him, and the list goes on. The prevalence of this archetype displays their effectiveness, ' +\
                'while many analysts may argue this playstyle is not conducive to a winning team. \n' +\
                'The criteria for this role were curated with this offensive/defensive dichotomy in mind, as the first qualification is accounting for at least (22%) of your teams points. ' +\
                'The next moniker of a Giver is having a lackluster defense. While the team defense may not be be entirely indicative of a players performance on that side of the ball, ' +\
                'having a high offensive usage paired with an underperforming defense does not typically correlate to a positive defensive impact. \n' +\
                'Keeping this in mind, the next criteria that must be met is a team defensive efficiency exceeding 1 for that season. ' +\
                'The last indicator of a Giver is that they contribute to the game in ways other than their scoring, like finding teammates or seeking out rebounds. \n' +\
                'Keeping this in mind, the player must have a help score between 5 and 10 in order to ensure impact in other aspects of the game. Any help score over 10 ' +\
                'begins to compensate for a player\'s defensive shortcomings and consequentally alters their role assignment. \n' +\
                '\nThe Taker is the lowest tier of roles a player can be assigned in this portion of our analysis. A Taker fails to meet the criteria of the other 3 categories, ' +\
                'and is stuck in role-assigned purgatory. This player is unable to post a positive measureable impact on, not only the scoring end, but in complimentary ' +\
                'offensive endeavors like rebounds and assists, resulting in a help score too low for assignment to any of the other 3 roles. Players in this category may provide one essential ' +\
                'skill at a high level, such as shooting or rebounding, but they fail to impact the game in a variety of ways besides that. Their defensive impact isn\'t enough to merit a more ' +\
                'favorable evaluation. Many players who are signed to be shooters for a team will fall into this category. Being a shooter is one of the most demanded ' +\
                'commodities in our league, so many teams employ statistically handicapping players with the exception that they provide the most important skill set in the league. \n' +\
                '\nThe Complimentary role was made with the blue-collar, defensively inclined, and master-of-intangibles in mind. Getting a player that ' +\
                'can shoulder the offensive work and be competent defensively is the gold standard for winning, however it is these Complimentary ' +\
                'players that truly oil the machine. Competency is the bare minimum, however these are the players that allow the Winners to ' +\
                'be comfotable with being adequate, as the Winners know their Compliments will be making up for everything around the edges. ' +\
                'A Complimentor, many times, is indicative of a team with multiple star-level players. The presence of other stars allows players, who ' +\
                'would otherwise put up more eye-popping numbers, to slump into a role more conducive to winning, therefore becoming a compliment to ' +\
                'those around him. For example, Chris Paul has mostly played the role of a Giver and Winner through a career punctuated by efficient scoring ' +\
                'and unparalleled passing chops. However, after growing older and into a less prominent scoring role with teams like the Suns or now the Spurs, ' +\
                'Chris Paul has slid himself into the role of a Complimentary player, taking what his years give him and conforming his playstyle to highlight his teammates. \n' +\
                'Considering the lower offensive usage that befits those placed in this role, the first criteria makes sure the player has accounted for less than (20%) of his team\'s points. \n' +\
                'Once we are sure we have a low scoring player, we must pinpoint significant impact in other areas of the game. \n' +\
                'We do this by considering two more criteria: a team having a defensive efficiency under -5 and a player having a help score over 6.5. ' +\
                'Only one of these need to be true in conjunction with the low scoring criteria for a player to be placed into this category. \n' +\
                'Most players in the league will fall into the Complimentary and the Taker categories. Often times the difference between making yourself known ' +\
                'as a winning or losing player is dictated by the team you are surrounded by and how you are able to conform to their strengths and weaknesses. ' +\
                'Many Takers will have been Complimentary at worst on good teams, and many of those who are Complimentary would be slunk into the spot of Taker on a worse team. \n' +\
                '\nThe Winner is the type of player that is most advantageous to have in a championship run according to this program\'s analysis. A Winner is a player who may not bear as heavy of ' +\
                'an offensive workload as a heliocentric role  akin to certain Givers, but that is because their team holds a favorable defensive efficiency while feauturing them as one of ' +\
                'the teams top scorers. Many players who fit in this category were former Givers, but the want for winning often outweighs the oppurtunity for stardom. ' +\
                'Players with fragile egos regarding how they are perceived by fans may be reluctant to allow themselves to take less of an offensive burden to qualify for this role, ' +\
                'as most conventional and popular statistics make it hard for common fans to pinpoint their impact. Though good defense is important, it is not the true measure that seperates ' +\
                'the Giver from the Winner. The true testament to what makes a Winner so great is the ability to make their defensive presence viable in a well-running defensive scheme ' +\
                'while maintaining the bulk of their offensive impact. \n' +\
                'Keeping this in mind, the first criteria that must be met is at least (20%) of their team\'s points resulting from them.\n' +\
                'Now that we ensured this player is still a high-level contributor on the scoring end, we must account for other ways they can impact ' +\
                'the game offensively. \n' +\
                'To make sure this player has accounted for extra-cirricular offensive impact, the second criteria that must be met is a help score exceeding 6. \n' +\
                'The offensive excellency of a Winner is impressive, but what is even more impressive is how their team is able to package this aptitude with an efficient defense. ' +\
                'An efficient defense with a high quality offensive contributor is often a positive reflection of the players making up the lineup. This means each player contributes to ' +\
                'a net positive basketball group, and has curated a formula that this analysis has concluded as the epitome of winning basketball. \n' +\
                'To account for this balanced style of basketball in our criteria, a team must have a defensive efficiency lower than -0.5. \n' +\
                'There is a way for a player to circumvent the previous criteria: to brute force their way to becoming a winning basketball player. ' +\
                'In this analysis, defensive success is the best compliment to good offense. However, there are certain players who are statistical anomalies when ' +\
                'it concerns the offensive side of the ball. I think the only rival to a complimentary defense is unstoppable offense. Defense is less of a factor ' +\
                'when a player wreaks enough havoc to continue tipping the scales in their team\'s favor. \n' +\
                'To account for these \'force of nature\' offensive players, that are seemingly becoming more common in conjunction to the rise ' +\
                'of offensive efficiency, additional criteria, including a player scoring (24%) of their teams respective points and maintaining a ' +\
                'help score of 10 or more, were added that can bolster a player\'s status straight to Winner. \n' +\
                'Lastly, using the Championships and MVP database, we can force every player who has won a championship for each season as a Winner. \n'
                
        return all_desc
                
                
    else:
        return 'No valid role assigned.'
    
    
###########################################################
def the_process(player_name, season):
    
    global scoring_grade
    global help_grade
    
    print(scoring(player_name, season))
    print('\nThis concludes the Scoring analysis.\n')
    print('#########################################')
    print(help(player_name, player_season))
    print('#########################################\n')
    print(efficiency(player_name, player_season))
    print('\nThis concludes the Efficiency analysis.\n')
    print('##########################################')
    print(str(player_name) + ' finished with a scoring grade of ' + str(scoring_grade) + ' and a help score of ' + str(help_grade) + '.\n')
    # print('This player won a title this season: ' + str(won_title) + '.\n')
    # check yearly outlook we have to incorporate third database, which we will connect by sending the string name of a team to it
    # for example, easiest would be to send the city name, but then Lakers and Clippers would be compromised (maybe make an exception case for them)
#####################################################################################################################################

player_name = input('Enter the name of a player to analyze with S.H.R.E.Y.: ')
player_season = input('Enter the year you would like to view (format as YYYY-YY): ') 
the_process(player_name, player_season)

