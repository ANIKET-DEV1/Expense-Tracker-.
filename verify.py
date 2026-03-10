from datetime import datetime
from .new import Helper
from datetime import datetime,date
class operation():
    def __init__(self):
        self.db=Helper()
    
    def verify_expense_deatils(self, user_id, description, amount, edate, cName):
        try:
            amount=float(amount)
        except ValueError:
            return 2
        try:
            edate = datetime.strptime(edate, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return 4
        if cName is None:
            return 6
        if amount <= 0:
            return 2
        if not description.strip():
            return 3
        if edate > date.today():
                print("Expense date cannot be in the future")
                return 4
        try:
                category_id = self.db.Category_get_ID(cName, user_id)
                self.db.Add_Expense(user_id, description, amount, edate, category_id)
                return 1
        except Exception as e:
                return 5
            
    def viewExpense(self,userID):
        try:
            getrow=self.db.view_Expenses(userID)
            print("Fetching Data..")
            if getrow:
                print(f"\n\n{'='*32} EXPENSE LIST {'='*32}")
                print(f"{'ID':<5} {'Category':<15} {'Description':<25} {'Amount':>16} {2*' '} {'Date'}{2*' '}")
                print("-" * 80)
                a=0
                for row in getrow:
                    print(f"{row[0]:<5} {row[1]:<15} {row[2]:<25} {row[3]:>16.2f}₹ {2*' '}{row[4]}{2*' '}")
                total = sum(r[3] for r in getrow)
                print("-" * 80)
                print(f"{'Total':<65} {total:.2f}₹")
                print("-" * 80)                
            else:
                 print("Nothing to Show!....")   
        except Exception as e:
             print(e)
             

         
    def monthly_expemse(self,userID):
        choice = input("Press ENTER for current month or type 'custom': ")
        if choice == "":
            today = date.today()
            month = today.month
            year = today.year
        else:
            month = int(input("Month (1-12): "))
            year = int(input("Year (YYYY): "))
        try:

            rows=self.db.month_Expenses(userID,month,year)
            if rows:
                print(f"\n\n{'='*10} Monthly Report {'='*10}")
                print('-'*40)
                print(f"{'Categories':<15} {'Amount':>20}")
                print('-'*40)
                for r in rows:
                      print(f"{r[0]:<15} {r[1]:>20}₹")
                total = sum(r[1] for r in rows)
                print("-" * 40)
                print(f"{'Total':<30} {total:.2f}₹")
                print("-" * 40) 
            else:
                 print("\nNo data Found!")
                

        except Exception as e:
             print('Error:',e)


    def add_debt(self, user_id):
        person_name = input("Enter name of person: ").strip().capitalize()
        while True:
            try:
                amount = float(input("Amount: "))
                if amount <= 0:
                    print(" Amount must be greater than 0")
                    continue
                break
            except ValueError:
                print(" Enter a valid number")
        while True:
            debt_type = input("Lent or Borrowed: ").strip().lower()
            if debt_type in ("lent", "borrowed"):
                break
            print(" Enter only 'lent' or 'borrowed'")
        while True:
            debt_status = input("Pending or Paid: ").strip().lower()
            if debt_status in ("pending", "paid"):
                break
            print(" Enter only 'pending' or 'paid'")
        while True:
            date_input = input("Enter Date (YYYY-MM-DD): ").strip()
            try:
                debt_date = datetime.strptime(date_input, "%Y-%m-%d").date()
                break
            except ValueError:
                print(" Invalid date format")
        try:
            self.db.new_add_debt(
                user_id,
                person_name,
                amount,
                debt_type,
                debt_status,
                debt_date
            )
            print(" Debt added successfully")
        except Exception as e:
            print(" Database Error:", e)

                    
    def view_debt(self,userID):
        try:
            row=self.db.display_debt(userID)
            if row:
                print(f"\n\n{'='*34} DEBT LIST {'='*34}")
                print(f"{'ID':<5} {'Person':>15} {'Amount':>15} {'Debt Type':>15} {'Debt Status':>15} {2*' '} {'Date'}{2*' '}")
                print("-" * 80)
                for r in row:
                    print(f"{r[0]:<5} {r[1]:>15} {r[2]:>15.2f}₹ {r[3]:>15} {r[4]:>15} {2*' '} {r[5]}{2*' '}")
                total=sum(r[2] for r in row)
                print("-" * 80)
                print(f"{'Total':<60}{total:.2f}₹")
            else:
                 print('Nothing to display')
        except Exception as e:
             print('Error:',e) 
               
                     
        
    def Mark_debt(self, userID):
        try:
            debtId = int(input("Enter DebtID: "))

            debt = self.db.get_debt_by_id(debtId,userID) 
            if not  debt:
                print("DebtID not found")
                return

            print(
                f"Debt details:\n"
                f"DebtID: {debt[0]}\n"
                f"Person: {debt[1]}\n"
                f"Amount: {debt[2]}\n"
                f"Debt Type: {debt[3]}\n"
                f"Debt Status: {debt[4]}\n"
                f"Date: {debt[5]}"
            )
            if debt[4] == 'paid':
                print("It's already paid")
                return
            check = input("Mark this debt as PAID? (Y/N): ").strip().lower()
            if check == 'y':
                self.db.update_debt(debtId, userID)
                print("Debt marked as paid")
            else:
                print("Operation cancelled")

        except ValueError:
            print("Invalid DebtID")
        except Exception as e:
            print("mark_debt error:", e)
    
    def view_cate(self,userID):
        try:
            row=self.db.view_category(userID)
            if row:
                print(f"\nYour Categories:")
                for r in row:
                    print(r[0])
            else:
                print("No data Found! ")
        except Exception as e:
            print("view_Category:",e)
        
                    


                    



                        