import espnff, pandas as pd, matplotlib.pyplot as plt, numpy as np
from espnff import League

def power_graphs(league_id=None, year=None, espn_s2=None, swid=None, latestWeek=17):
    if league_id == None:
        raise Exception('Must enter league ID...Exiting')
    elif year == None:
        raise Exception('Must enter league year...Exiting')
    
    league = League(league_id, year, espn_s2, swid)

    wks = []
    twks = []
    trks=[]

    def find_index(df, column, find_term):
        df = df[column][df.index[df[column] == find_term]]
        return(df.index[0])



    for i in range(0,latestWeek):
        w = i + 1
        wk = league.power_rankings(week=w)
        wk = pd.DataFrame(wk,columns=['Score','Team'])
        wks.append(wk)

    wk = wks
    wks = []

    for i in range(len(wk)):
        t = []
        s = []
        for x in range(len(wk[i])):
            tb = str(wk[i]['Team'][x])
            tb = str(tb)[5:(len(tb)-1)]
            t.append(tb)
            s.append(float(wk[i]['Score'][x]))
        ts = pd.DataFrame(
            {'Team':t,
             'Score':s
             })
        wks.append(ts)

    for i in range(len(wks)):
        wks[i].sort_values('Team',inplace=True)
        wks[i].reset_index(drop=True,inplace=True)

    wksTeam = []


    for i in range(len(wks)):
        place = [i+1]
        place.extend(list(wks[i]['Score']))
        wksTeam.append(place)

    c = ['Week']
    c.extend(sorted(t))

##Change this to fit your league's team names
    color_dict = {'Team1':'#00e9ff'
                  ,'Team2':'#0083ff'
                  ,"Team3":'#2e00ff'
                  ,'Team4':'#981E32'
                  ,'Team5':'#521f6d'
                  ,'Team6':'#d8ff00'
                  ,"Team7":'#002C5F'
                  ,'Team8':'#ffa100'
                  ,'Team9':'#6d571f'
                  ,'Team10':'#ff0000'
                  ,'Team11':'#46b230'
                  ,'Team12':'#00ff11'
                  }

    for i in range(len(sorted(t))):
        color_dict[t[i]] = color_dict['Team' + str(i+1)]

    tpd = pd.DataFrame(data=wksTeam,columns=c)
    tpd.to_csv('wk' + str(len(wksTeam)) + ' power scores.csv',index=False)
    tpd = pd.read_csv('wk' + str(len(wksTeam)) + ' power scores.csv',index_col='Week')

                 
    for i in range(len(wks)):
        test = wks[i].sort_values('Score',ascending=False)
        twks.append(test.reset_index(drop=True))


    for x in range(len(twks)):
        place = [x + 1]
        for i in range(len(sorted(t))):
            place.append(find_index(twks[x],'Team',sorted(t)[i])+1)
        trks.append(place)

    ranks = pd.DataFrame(data=trks,columns=c)
    ranks.to_csv('wk' + str(len(wksTeam)) + ' power rankings.csv',index=False)
    ranks = pd.read_csv('wk' + str(len(wksTeam)) + ' power rankings.csv',index_col='Week')

    lines = tpd.plot.line(title='Power Rankings',table=True, use_index=False,color=[color_dict.get(x, '#333333') for x in ranks.columns])
    plt.axes().get_xaxis().set_visible(False)
    plt.legend(bbox_to_anchor=(1.25,1),loc='upper right',borderaxespad=0.)
    plt.plot(marker='o')

    plt.subplots_adjust(0.13,0.36,0.81,0.96,0.2,0.2)

    lines = ranks.plot.line(title='Power Score',table=True, use_index=False,color=[color_dict.get(x, '#333333') for x in ranks.columns]).invert_yaxis()    
    plt.axes().get_xaxis().set_visible(False)
    plt.legend(bbox_to_anchor=(1.25,1),loc='upper right',borderaxespad=0.)
    plt.plot(marker='o')

    plt.subplots_adjust(0.13,0.36,0.81,0.96,0.2,0.2)

    plt.show()
