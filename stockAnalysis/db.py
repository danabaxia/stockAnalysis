import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'trading'

TABLES = {}

TABLES['invest'] = (
    "CREATE TABLE invest ("
    "  invest_id INT NOT NULL AUTO_INCREMENT,"
    "  ticker varchar(14) NOT NULL,"
    "  principle double NOT NULL,"
    "  strategy varchar(14) NOT NULL,"
    "  status ENUM('running', 'complete') DEFAULT 'running',"
    "  goal double DEFAULT 0.05,"
    "  PRIMARY KEY (invest_id)"
    ") ENGINE=InnoDB")

TABLES['orders'] = (
    "CREATE TABLE orders ("
    "  order_id int NOT NULL AUTO_INCREMENT,"
    "  time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
    "  price double NOT NULL, "
    "  amount double NOT NULL,"
    "  type varchar(14) NOT NULL,"
    "  invest_id int,"
    "  PRIMARY KEY (order_id),"
    "  FOREIGN KEY (invest_id) REFERENCES invest(invest_id)"
    ") ENGINE=InnoDB")


data_invest= ('FB', 100, 'long',0.06)
data_order = (140.01, 100, 'buy', 1)

def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def create_tables(cursor):
    #check db if not exits, create one
    try:
        cursor.execute("USE {}".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(DB_NAME))
            mydb.database = DB_NAME
        else:
            print(err)
            exit(1)
    #create tables 
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exits.")
            else:
                print(err.msg)
        else:
            print("OK")

def insert_invest(cursor, data):
    add_order = ("INSERT INTO invest "
                 "(ticker, principle, strategy, goal) "
                 "VALUES (%s, %s, %s, %s)")
    #Insert new order
    cursor.execute(add_order,data)
    #commit data
    mydb.commit()

def insert_order(cursor, data):
    insert = ("INSERT INTO orders "
              "(price, amount, type, invest_id) "
              "VALUES (%s, %s, %s, %s)")
    #Insert new order
    cursor.execute(insert,data)
    #commit data
    mydb.commit()

def find_invest_byID(cursor, investID):
    #query = ('SELECT * FROM orders WHERE invest_id = ?')
    cursor.execute('SELECT * FROM orders WHERE invest_id = %s',(investID,))
    return cursor.fetchall()

####status: running, complete
def find_active_invest(cursor, status):
    cursor.execute ("SELECT * FROM invest WHERE status LIKE %s", (status,))
    return cursor.fetchall()

def find_invest_bySymbol(cursor, ticker):
    cursor.execute("SELECT * FROM invest WHERE ticker LIKE %s", (ticker,))
    return cursor.fetchall()

    
def show_invest_table(cursor):
    cursor.execute('SELECT * FROM invest')
    return cursor.fetchall()

def show_order_table(cursor):
    cursor.execute('SELECT * FROM orders')
    return cursor.fetchall()

if __name__ == "__main__":
    #connect to mysql server
    mydb = mysql.connector.connect(user='root', 
                                  password='Hjb1314$',
                                  host="localhost",
                                  database="trading"
                                  )
    cursor = mydb.cursor()
    create_tables(cursor)
    #insert an invest
    insert_invest(cursor, data_invest)
    #insert an order
    #insert_order( cursor, data_order)
    #print(find_invest(cursor, 1))
    #print(find_active_invest(cursor))
    #print(find_active_invest(cursor,'running'))
    #print(find_invest_bySymbol(cursor,'FB'))
    cursor.close()    
    mydb.close()
    

