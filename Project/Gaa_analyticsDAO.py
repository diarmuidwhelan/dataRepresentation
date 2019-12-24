# DAO that facilitates interaction with MYSQL database

import mysql.connector
import dbconfigtemplate as cfg # import configurations
import pandas as pd
class Gaa_analyticsDAO:
    db=""
    def connectToDB(self):
        self.db = mysql.connector.connect(
            host=       cfg.mysql['host'],
            user=       cfg.mysql['user'],
            password=   cfg.mysql['password'],
            database=   cfg.mysql['database'],
            buffered=True
        )
    def __init__(self): 
        self.connectToDB()
     
    
    def getCursor(self):
        if not self.db.is_connected():
            self.connectToDB()
            
        return self.db.cursor()
    
            
    def create(self, values):
        cursor = self.getCursor()
        
        sql="insert into gaa_analytics.match_info ('game_id','team','team_name', 'venue', 'date','competition','round','player','player_name') values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, values)
        self.db.commit()
        lastRowId=cursor.lastrowid
        cursor.close
        return lastRowId

    def getAll(self):
        cursor = self.getCursor()
        sql="select * from gaa_analytics.match_info"
        cursor.execute(sql)
        results = cursor.fetchall()
        returnArray = []
     #  print(results)
        for result in results:
           # print(result)
            returnArray.append(self.convertToDictionary(result))
        cursor.close
        return returnArray

    def getAllViz(self):
        cursor = self.getCursor()
        sql="select  PLAYER_NAME,TEAM_NAME,COUNT(ACTION) AS ACTIONS,COUNT(DISTINCT GAMEID) AS MATCHES,SUM(CASE WHEN ED.ACTION IN ('INT','B','TU','TS','C') THEN 1 ELSE 0 END)/(COUNT(DISTINCT GAMEID)) AS WORKRATE_PER_GAME,SUM(CASE WHEN ED.ACTION IN ('KO REC') THEN 1 ELSE 0 END)/(COUNT(DISTINCT GAMEID)) AS KO_RET_PER_GAME,((SUM(CASE WHEN ED.ACTION IN ('TS','TU') THEN 1 ELSE 0 END))/(COUNT(DISTINCT GAMEID))) AS TACKLES_PER_GAME,(( SUM(CASE WHEN ED.ACTION IN ('SPT','FPT','FPM','SPM','SG','SGM','PM','PG') THEN 1 ELSE 0 END))/(COUNT(DISTINCT GAMEID))) AS SHOTS_PER_GAME,( SUM(CASE WHEN ED.ACTION IN ('SAVE')THEN 1 ELSE 0 END))/(COUNT(DISTINCT GAMEID)) AS SAVES_PER_GAME,SUM(EXP_PTS)/(COUNT(DISTINCT GAMEID)) AS EXP_PTS_PER_GAME,SUM(CASE WHEN ED.ACTION IN ('SPT','FPT') THEN 1 WHEN ED.ACTION IN ('SG','PG')THEN 3 ELSE 0 END)/(COUNT(DISTINCT GAMEID)) AS PTS_PER_GAME,SUM(EXP_PTS) AS EXP_PTS,SUM(CASE WHEN ED.ACTION IN ('TS') THEN 1 ELSE 0 END) AS SUCCESSFUL_TACKLES,SUM(CASE WHEN ED.ACTION IN ('TU') THEN 1 ELSE 0 END) AS UNSUCCESSFUL_TACKLES,SUM(CASE WHEN ED.ACTION IN ('SAVE') THEN 1 ELSE 0 END) AS SAVES,SUM(CASE WHEN ED.ACTION IN ('TS') THEN 1 ELSE 0 END)/SUM(CASE WHEN ED.ACTION IN ('TU','TS') THEN 1 ELSE 0 END) AS TACKLE_SUCCESS, SUM(CASE WHEN ED.ACTION IN ('SPT','FPT') THEN 1 WHEN ED.ACTION IN ('SG','PG')THEN 3 ELSE 0 END) - SUM(Exp_Pts) AS SHOT_EFFICIENCY, (SUM(CASE WHEN ED.ACTION IN ('SPT','FPT') THEN 1 WHEN ED.ACTION IN ('SG','PG')THEN 3 ELSE 0 END) - SUM(Exp_Pts))/ (SUM(CASE WHEN ED.ACTION IN ('SPT','FPT','FPM','SPM','SG','SGM','PM','PG') THEN 1 ELSE 0 END)) AS SHOT_EFFICIENCY_PER_SHOT, (SUM(CASE WHEN ED.ACTION IN ('SPT','FPT') THEN 1 WHEN ED.ACTION IN ('SG','PG')THEN 3 ELSE 0 END))/ (SUM(CASE WHEN ED.ACTION IN ('SPT','FPT','FPM','SPM','SG','SGM','PM','PG') THEN 1 ELSE 0 END)) AS PTS_PER_SHOT,SUM(EXP_PTS)/ (SUM(CASE WHEN ED.ACTION IN ('SPT','FPT','FPM','SPM','SG','SGM','PM','PG')THEN 1 ELSE 0 END)) AS EXP_PTS_PER_SHOT, SUM(CASE WHEN ED.ACTION IN ('SPT','FPT','FPM','SPM','SG','SGM','PM','PG') THEN 1 ELSE 0 END) AS TOTAL_SHOTS,SUM(CASE WHEN ED.ACTION IN ('SPT','FPT') THEN 1 WHEN ED.ACTION IN ('SG','PG')THEN 3 ELSE 0 END) AS TOTAL_SCORES,SUM(CASE WHEN ED.ACTION IN ('INT','B','TU','TS','C') THEN 1 ELSE 0 END) AS WORKRATE from (select distinct * from gaa_analytics.match_info) mi LEFT join gaa_analytics.event_data ed on mi.game_id=ed.gameID and mi.player=ed.player and mi.team_name=ed.team GROUP BY 1,2"
        cursor.execute(sql)
        results = pd.DataFrame(cursor.fetchall())
        #print(results)
        cursor.close
        return results

    def findByID(self, id):
        cursor = self.getCursor()
        sql="select * from gaa_analytics.match_info where game_id = %s"
        values = (id,)

        cursor.execute(sql, values)
        results = cursor.fetchall()
        returnArray = []
     #  print(results)
        for result in results:
            print(result)
            returnArray.append(self.convertToDictionary(result))
        cursor.close
        return returnArray

    def update(self, values):
        cursor = self.getCursor()
        sql="update gaa_analytics.match_info set game_id=%s,team=%s,team_name=%s, venue=%s, date=%s,competition=%s,round=%s,player=%s,player_name=%s"
        cursor.execute(sql, values)
        self.db.commit()
        cursor.close()

    def delete(self, id):
        cursor = self.getCursor()
        sql="delete from gaa_analytics.match_info where game_id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.db.commit()
        cursor.close()

    def convertToDictionary(self, result):
        colnames=['game_id','team','team_name', 'venue', 'date','competition','round','player','player_name']
        item = {}
        
        if result:
            for i, colName in enumerate(colnames):
                value = result[i]
                item[colName] = value
        
        return item

    
        
Gaa_analyticsDAO = Gaa_analyticsDAO()