import requests
from datetime import datetime


class getScore:
    def __init__(self):
        self.apiKey="0j5QTKSXmQNwLylfz0MIuPVQZgD3"
        self.urlAllMatches="https://cricapi.com/api/matches/"
        self.urlMatchScore="https://cricapi.com/api/cricketScore/"
        self.uniqueMatchId=0;


    def getUniqueId(self,team):
        urlParameters={"apikey":self.apiKey}
        resp=requests.get(self.urlAllMatches,params=urlParameters)
        respDict=resp.json()
        ans=""
        for i in respDict['matches']:
            if(i['team-1'].lower()==team or i['team-2'].lower()==team):
                currentDate = datetime.today().strftime('%Y-%m-%d')
                if(currentDate== i['date'].split("T")[0]):
                    self.uniqueMatchId=i['unique_id']
            
                    
            if(self.uniqueMatchId!=0 and i['matchStarted']):
                ans+=(i['team-1'] +" vs "+i['team-2']+" "+i['type'])+"\n"
                ans+=("Toss won by: "+i['toss_winner_team'])+"\n"
                matchDetails=self.getScore(self.uniqueMatchId)
                if(matchDetails['stat']!=""):
                    ans+=(matchDetails['stat'])+"\n"
                ans+=("Score: "+matchDetails['score'])
                try:
                    ans+=("Match won by: "+ i['winner_team'])+"\n"
                except KeyError as e:
                    pass;
                return;
            else:
                ans=("No matches currently underway."+"\n")
                ans+="\n"
                ans+=self.prevSchedule(respDict,team)+"\n"
                ans+=self.nextSchedule(respDict,team)
                return ans;
            
    def prevSchedule(self,respDict,team):
        ans=""
        currentDate = datetime.today().strftime('%Y-%m-%d')
        for i in respDict['matches']:
            if(i['team-1'].lower()==team or i['team-2'].lower()==team):
                matchDate=i['date']
                if(matchDate<currentDate):
                    ans+=("Previous fixture was played on: "+matchDate.split("T")[0])+"\n"
                    matchDetails=self.getScore(i['unique_id'])
                    ans+=("Score: "+matchDetails['score'])+"\n"
                    ans+=("Match won by: "+ i['winner_team'])+"\n"
                    return ans
                
        ans+=("Previous match details unavailable.")+"\n"
        return ans
      
                
    def nextSchedule(self,respDict,team):
        ans=""
        currentDate = datetime.today().strftime('%Y-%m-%d')
        for i in respDict['matches']:
            if(i['team-1'].lower()==team or i['team-2'].lower()==team):
                matchDate=i['date']
                if(matchDate>currentDate):
                    ans+=("Next match is scheduled on: "+matchDate.split("T")[0])+"\n"
                    ans+=("Fixture: "+i['team-1']+ " vs "+i['team-2']+" "+i['type'])+"\n"
                    return ans

        ans+=("Upcoming fixtures unavailable.")+"\n"
        return ans
        

    
    def getScore(self,uniqueMatchId):
        urlParameters={"apikey":self.apiKey,"unique_id":uniqueMatchId}
        resp=requests.get(self.urlMatchScore,params=urlParameters)
        respDict=resp.json()
        try:
            matchDetails={"stat":respDict['stat'],"score":respDict['score']}
        except KeyError as e:
            matchdetails={}
        return matchDetails
        
class getPlayer:
    def __init__(self,name,formt):
        self.urlPlayerFinder="https://cricapi.com/api/playerFinder"
        self.apiKey="0j5QTKSXmQNwLylfz0MIuPVQZgD3"
        self.urlPlayerStats="https://cricapi.com/api/playerStats"
        self.name=name
        self.formt=formt
        self.ans=""
        
        
    def getPlayerStats(self):
        urlParameters={"name":self.name,"apikey":self.apiKey}
        resp=requests.get(self.urlPlayerFinder,params=urlParameters)
        respDict=resp.json()
        try:
            player=respDict['data'][0];
            playerId=player['pid']
            urlParameters={"pid":playerId,"apikey":self.apiKey}
            resp=requests.get(self.urlPlayerStats,params=urlParameters)
            respDict=resp.json()
            ans=""
            ans+=respDict['fullName']+","+respDict['country']+"\n"+respDict['battingStyle']+","+respDict['bowlingStyle']+"\n"+"\n"
            
            
            ans+="Batting:"+"\n"
            ans+=("Matches:"+respDict["data"]["batting"][self.formt]["Mat"]+"\n")
            ans+=("Runs:"+respDict["data"]["batting"][self.formt]["Runs"]+"\n")
            ans+=("Strike rate:"+respDict["data"]["batting"][self.formt]["SR"]+"\n")
            ans+=("Average:"+respDict["data"]["batting"][self.formt]["Ave"]+"\n")
            ans+=("Highest score:"+respDict["data"]["batting"][self.formt]["HS"]+"\n")
            ans+=("100s:"+respDict["data"]["batting"][self.formt]["100"]+"\n")
            ans+=("50s:"+respDict["data"]["batting"][self.formt]["50"]+"\n"+"\n")
            
            
            ans+=("Bowling:")+"\n"
            ans+=("Matches:"+respDict["data"]["bowling"][self.formt]["Mat"])+"\n"
            ans+=("Wickets:"+respDict["data"]["bowling"][self.formt]["Wkts"])+"\n"
            ans+=("Economy:"+respDict["data"]["bowling"][self.formt]["Econ"])+"\n"
            ans+=("Average:"+respDict["data"]["bowling"][self.formt]["Ave"])+"\n"
            ans+=("Runs:"+respDict["data"]["bowling"][self.formt]["Runs"])+"\n"
            ans+=("5Ws:"+respDict["data"]["bowling"][self.formt]["5w"])+"\n"+"\n"
            return ans
        except Exception as e:
            #print("Error retrieving player data.")
            ans=""
            return ans
    
                

if __name__ == "__main__":
    import telebot
    bot = telebot.TeleBot("1829051285:AAFGpWtkRDHpq5E__5eqjvAMs42C3M1YKZw")

    @bot.message_handler(commands=['help'])
    def send_welcome(message):
            bot.reply_to(message, "Hi and thank you for using CricBot. Using CricBot is extremely simple:\nTo retrieve player statistics type /playerstats.\nTo retrieve match statistics type /matchstats.\nHave fun!")



    
    @bot.message_handler(commands=['playerstats'])
    def send_welcome(message):
            bot.reply_to(message, "Enter the player name (first name<space>last name) and format(tests/T20Is/ODIs)")
            @bot.message_handler(func=lambda message: True)
            def getstats(message):
                try:
                    playerNamefirst=message.text.split(" ")[0]
                    playerNamelast=message.text.split(" ")[1]
                    formt=message.text.split(" ")[2]
                    playerName=playerNamefirst+" "+playerNamelast
                    playerObj=getPlayer(playerName,formt)
                    stats=playerObj.getPlayerStats()
                    if(stats!=""):
                        bot.reply_to(message,"Here you go:\n"+stats)
                    else:
                        bot.reply_to(message,"Requested data unavailable.")
                    bot.reply_to(message,"Type /help at anytime for a quick tutorial.")
                except Exception as e:
                    bot.reply_to(message,"Invalid format.")
                    bot.reply_to(message,"Type /help at anytime for a quick tutorial.")
                    


    @bot.message_handler(commands=['matchstats'])
    def send_welcome(message):
            bot.reply_to(message, "Enter a team name.")
            @bot.message_handler(func=lambda message: True)
            def getstats(message):
                team=message.text.lower()
                matchObj=getScore()
                stats=matchObj.getUniqueId(team)
                bot.reply_to(message,"Here you go:\n"+stats)
                bot.reply_to(message,"Type /help at anytime for a quick tutorial.")    
    
    bot.polling()







    
##    name=input("Enter the players full name:")
##    formt=input("Enter the format(tests/T20Is/ODIs):")
##    playerObj=getPlayer(name,formt)
##    print("")
##    message=playerObj.getPlayerStats()
##    print(message)





    
