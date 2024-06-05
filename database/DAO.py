from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getYear():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select YEAR(s.`datetime`) as time 
                        from sighting s """
        cursor.execute(query)
        for row in cursor:
            result.append(row["time"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllShape(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.shape as shape 
                from sighting s 
                where YEAR(s.`datetime`)=%s"""
        cursor.execute(query, (year,))
        for row in cursor:
            result.append(row["shape"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s.id as state
from state s """
        cursor.execute(query)
        for row in cursor:
            result.append(row["state"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.state1 as n1, n.state2 as n2
from neighbor n """
        cursor.execute(query)
        for row in cursor:
            result.append((row["n1"], row["n2"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPesoArchi(n1, n2, year, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(s.id) as peso
                    from sighting s 
                    where (s.state  = %s or s.state=%s) 
                    and year(s.`datetime`) = %s   
                    and s.shape = %s"""
        cursor.execute(query, (n1, n2, year, shape,))
        for row in cursor:
            result.append(row["peso"])
        cursor.close()
        conn.close()
        return result

    def getDistance(self):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(s.id) as peso
                            from sighting s 
                            where (s.state  = %s or s.state=%s) 
                            and year(s.`datetime`) = %s   
                            and s.shape = %s"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["peso"])
        cursor.close()
        conn.close()
        return result
