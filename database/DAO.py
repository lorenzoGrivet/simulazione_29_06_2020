from database.DB_connect import DBConnect
from model.match import Match


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getMesiDAO():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=False)
        query = """select distinct month (m.`Date`)
                    from premierleague.matches m 
                    order by month ( m.`Date` )"""

        cursor.execute(query, ())

        for a in cursor:
            result.append(a[0])

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getNodi(mese):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """		select m.MatchID ,m.TeamHomeID ,m.TeamAwayID , t.Name nomeHome,t2.Name nomeAway
                        from premierleague.matches m ,premierleague.teams t, premierleague.teams t2  
                        where month (m.`Date`)=%s
                        and m.TeamHomeID =t.TeamID 
                        and m.TeamAwayID = t2.TeamID """

        cursor.execute(query, (mese,))

        for a in cursor:
            result.append(Match(**a))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(mese,minuti):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=False)
        query = """select a1.MatchID, a2.MatchID, count(a1.PlayerID)
                    from 
                    (select a.PlayerID ,a.MatchID
                    from premierleague.actions a ,premierleague.matches m 
                    where a.TimePlayed > %s
                    and m.MatchID=a.MatchID
                    and month (m.`Date`)=%s ) a1, 
                    (select a.PlayerID ,a.MatchID
                    from premierleague.actions a ,premierleague.matches m 
                    where a.TimePlayed > %s
                    and m.MatchID=a.MatchID
                    and month (m.`Date`)=%s ) a2
                    where a1.PlayerID = a2.PlayerID
                    and a1.MatchID < a2.MatchID
                    group by a1.MatchID, a2.MatchID"""

        cursor.execute(query, (minuti,mese,minuti,mese,))

        for a in cursor:
            result.append(a)

        cursor.close()
        conn.close()
        return result

