from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getTeams():

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t.*
        from lahmansbaseballdb.teams t 
        """

        cursor.execute(query, ())

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getYears(teamName):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """  select  a.`year` , a.playerID
from lahmansbaseballdb.appearances a , lahmansbaseballdb.teams t 
where t.name = %s
and t.ID = a.teamID  
            """

        cursor.execute(query, (teamName,))

        for row in cursor:
            result.append((row['year'], row['playerID']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesoEdges(y1,y2,t):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """  select count(a.playerID) as weight
from lahmansbaseballdb.appearances a , lahmansbaseballdb.appearances a2, lahmansbaseballdb.teams t, lahmansbaseballdb.teams t2  
where a.playerID = a2.playerID 
and a2.`year` = %s and a.`year` = %s
and t.`year` = a.`year` and t2.`year` = a2.`year`
and a.teamID = t.ID and a2.teamID = t2.ID 
and t.name = t2.name 
and t.name = %s
                """

        cursor.execute(query, (y1,y2,t,))

        for row in cursor:
            result.append(row['weight'])

        cursor.close()
        conn.close()
        return result
