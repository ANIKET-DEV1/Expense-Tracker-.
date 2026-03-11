import pymysql as sql
from werkzeug.security import check_password_hash,generate_password_hash
class Helper:
    def __init__(self):
        print("Connecting to database...")
        self.db = sql.connect(
            host="localhost",
            user="root",
            passwd="Awesome123.",
            database="ExpenseTracker"
        )
    

        queries = [
           """CREATE TABLE IF NOT EXISTS users(
    userID INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL unique,
    email VARCHAR(100) not null unique,
    password varchar(255) not null,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);""",

            """CREATE TABLE IF NOT EXISTS category(
                cID INT AUTO_INCREMENT PRIMARY KEY,
                userID INT NOT NULL,
                cName VARCHAR(100) NOT NULL,
                UNIQUE(userID, cName),
                FOREIGN KEY(userID) REFERENCES users(userID)
                ON DELETE CASCADE
            )""",

            """CREATE TABLE IF NOT EXISTS expenses(
                expenseID INT AUTO_INCREMENT PRIMARY KEY,
                userID INT NOT NULL,
                cID INT NOT NULL,
                description VARCHAR(255),
                amount DECIMAL(10,2) NOT NULL,
                expenseDate DATE NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(userID) REFERENCES users(userID) ON DELETE CASCADE,
                FOREIGN KEY(cID) REFERENCES category(cID) ON DELETE CASCADE
            )""",

            """CREATE TABLE IF NOT EXISTS debt(
                debtID INT AUTO_INCREMENT PRIMARY KEY,
                userID INT NOT NULL,
                PersonName VARCHAR(50) NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                debtType ENUM('lent','borrowed') NOT NULL,
                debtStatus ENUM('pending','paid') DEFAULT 'pending',
                debtDate DATE NOT NULL,
                FOREIGN KEY(userID) REFERENCES users(userID) ON DELETE CASCADE
            )"""
        ]

        cur = self.db.cursor()
        for q in queries:
            cur.execute(q)
        cur.close()
        print('Connected!')

    def insert_user(self, username, email, password): 
        try:
            cur = self.db.cursor()
            query="Select * from users where username=%s or email=%s"
            cur.execute(query, (username, email))
            if cur.fetchone():
                return 2
            query = "INSERT INTO users(username, email, password) VALUES (%s, %s, %s)"
            password = generate_password_hash(password)
            cur.execute(query, (username, email, password))
            self.db.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return False
        finally:
            cur.close()

    def select_user(self,Tablename):
        print("Select called")   
        try:
            cur = self.db.cursor()
            query = "Select * from %s"
            cur.execute(query, (Tablename))
            self.db.commit()
            
        except Exception as e:
            print("Error:", e)
        finally:
            cur.close()
    
    def Auth(self,username,password) -> int:  
        try:
            cur = self.db.cursor()
            query = "Select userID,password from users where username=%s "
            cur.execute(query,username)
            result = cur.fetchone()
            if result:
                userID=result[0]
                stored_password=result[1]
                if check_password_hash(stored_password, password): 
                    return userID  
            return 0
        except Exception as e:
            print("Error:", e)
            return 0
        finally:
            cur.close()

    def insert_catogory(self,userID, cName): 
        try:
            cur = self.db.cursor()

            raw_categories = self.Category_exist(userID)
            existing_names = [row[0] for row in raw_categories]
            if cName in existing_names:
                return 0
            query = "INSERT INTO category(userID,cName) VALUES (%s,%s)"
            cur.execute(query, (userID,cName))
            self.db.commit()
            return True
        except Exception as e:
            print("Error:", e)
            return 2
        finally:
            cur.close() 

    def Category_exist(self,userID) :  
        try:
            cur = self.db.cursor()
            query = "SELECT cName FROM category WHERE userID=%s"
            cur.execute(query, (userID,))  # 1. Execute first!
            result = cur.fetchall()
            return result
        except Exception as e:
            print("Error:", e)
            return []
        finally:
            cur.close() 
    
    def Add_Expense(self,userID,description,Amount,expenseDate,cID) -> int:  
        try:
            cur = self.db.cursor()
            print("Adding...")
            query = "INSERT INTO expenses(userID,cID,description,Amount,expenseDate) VALUES (%s,%s,%s,%s,%s)"
            cur.execute(query, (userID,cID,description,Amount,expenseDate))
            self.db.commit()
            print(f"Expense added successfully!")
            return 1
        except Exception as e:
            print("Error:", e)
            return 0
        finally:
            cur.close()

    # def get_userID(self,username):
    #     try:
    #         cur = self.db.cursor()
    #         query = "Select * from users where username=%s"
    #         cur.execute(query,(username))
    #         for row in cur:
    #             return row[0]
    #         return 0
    #     except Exception as e:
    #         print("Error:", e)
    #     finally:
    #         cur.close() 
    
    def Category_get_ID(self,name,user_id):
        try:
            cur = self.db.cursor()
            query = "Select * from category where cName=%s and userID=%s "
            cur.execute(query,(name,user_id))
            for row in cur:
                return row[0]
            return 0
        except Exception as e:
            print("Error:", e)
            return 0
        finally:
            cur.close() 
        
    def view_Expenses(self,userID):
        try: 
            query='''Select e.expenseID,c.cName,e.description,e.Amount,e.expenseDate from expenses e
                    inner join category c
                    on e.cID=c.cID
                    where e.userID=%s
                    order by expenseDate'''
            cur=self.db.cursor()
            cur.execute(query,(userID))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print('Error',e)
            return 
        finally:
            cur.close()

    def month_Expenses(self,userID,month,year):
        try: 
            query='''Select c.cName,sum(e.Amount) as total_amount from expenses e
                    inner join category c
                    on e.cID=c.cID
                    where e.userID=%s
                    AND YEAR(e.expenseDate) = %s
                    AND MONTH(e.expenseDate) = %s
                    GROUP BY c.cName
                    ORDER BY total_amount DESC'''
            cur=self.db.cursor()
            cur.execute(query,(userID,year,month))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print('Error',e)
            return 
        finally:
            cur.close()
        
    def new_add_debt(self,userID,PersonName,amount,debtType,debtStatus,DebtDate):
        try:
            cur=self.db.cursor()
            query="INSERT INTO debt(userID,PersonName,amount,debtType,debtStatus,DebtDate) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(query,(userID,PersonName,amount,debtType,debtStatus,DebtDate))
            self.db.commit()
        except Exception as e:
            print('new: ',e)
            return 
        finally:
            cur.close()
    
    def display_debt(self,userID):
        try:
            cur=self.db.cursor()
            query='''Select debtID,PersonName,amount,debtType,debtStatus,DebtDate from debt where userID=%s'''
            cur.execute(query,(userID))
            row=cur.fetchall()
            return row
        except Exception as e:
            print('new: ',e)
            return 
        finally:
            cur.close()

    def update_debt(self,debtID,userID):
        try:
            cur=self.db.cursor()
            query = """
            UPDATE debt
            SET debtStatus = 'paid'
            WHERE userID = %s
             AND debtID = %s
             AND debtStatus = 'pending'
            """
            cur.execute(query, (userID, debtID))
            self.db.commit()
            if cur.rowcount == 0:
                print("No row updated (already paid or not found)")
            else:
                print("Debt updated successfully")
        except Exception as e:
            print("upadate debt error:",e)
            return
        finally:
            cur.close()

    def get_debt_by_id(self, debtId, userID):
        cur = self.db.cursor()
        query = """
            SELECT debtID, PersonName, amount, debtType, debtStatus, DebtDate
            FROM debt
            WHERE debtID = %s AND userID = %s
        """
        cur.execute(query, (debtId, userID))
        result = cur.fetchone()
        cur.close()
        return result
    
    def view_category(self,userID):
        cur = self.db.cursor()
        query="""
            Select cName from category 
            where userID=%s
                """
        cur.execute(query,(userID))
        result=cur.fetchall()
        cur.close()
        return result
