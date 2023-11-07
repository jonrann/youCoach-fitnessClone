# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'root', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = False)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query:str, data:dict=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
     
                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                # UPDATE/DELETE queries will return the NUMBER OF ROWS affected and/or TRUE/FALSE if the query was successful
                elif query.lower().find("update") >= 0 or query.lower().find("delete") >= 0:
                    self.connection.commit()
                    affected_rows = cursor.rowcount
                    if affected_rows > 0:
                        print(f"Query successful: {affected_rows} rows affected.")
                    else:
                        print("Query executed successfully but no rows were affected.")
                    return affected_rows > 0
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)