from database.DB_connect import DBConnect



class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.GeneID as id, Chromosome as cromosoma
                    from genes_small.genes g 
                    where g.Essential = 'Essential' """

        cursor.execute(query, ())

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

