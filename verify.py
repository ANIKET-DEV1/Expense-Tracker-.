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
        return True
            

    def add_debt(self, user_id,person_name, amount, debt_type, debt_status, date_input):
            try:
                amount = float(amount)
            except ValueError:
                return 2
            try:
                date_input = datetime.strptime(date_input, '%Y-%m-%d').date()
            except (ValueError, TypeError):
                return 4
            
            if debt_type is None or debt_status is None:
                return 5
            if amount <= 0:
                return 2
            if date_input > date.today():
                 return 6
            if not person_name.strip():
                return 3

        
                    


                    



                        