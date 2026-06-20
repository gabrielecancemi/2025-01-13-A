from database.DB_connect import DBConnect
from model.classification import Classification
from model.gene import Gene
from model.interaction import Interaction


class DAO():

    @staticmethod
    def get_localizations():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(localization) from classification c order by c.Localization desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["localization"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_classifications(loc):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select c.*, g.Essential  from classification c, genes g where g.GeneID  = c.GeneID
                    and c.localization = %s"""
            cursor.execute(query, (loc,))

            for row in cursor:
                result.append(Classification(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_interactions(idC, loc):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select i.GeneID1 as id1, i.GeneID2 as id2 from classification c , interactions i, classification c2 
                        where c.GeneID = i.GeneID1 and c2.GeneID = i.GeneID2 
                        and c.Localization = c2.Localization and c.Localization = %s and i.GeneID1 != i.GeneID2"""
            cursor.execute(query, (loc,))

            for row in cursor:
                result.append((idC[row["id1"]], idC[row["id2"]]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_chromosomes():
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select g.GeneID , g.Chromosome from genes g"""
            cursor.execute(query)

            for row in cursor:
                result[row["GeneID"]] = row["Chromosome"]

            cursor.close()
            cnx.close()
        return result
