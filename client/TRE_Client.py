import Pyro5.api

users = [
    {"ID": 123456, "password": "a"}
]

class TRE_Client:
    def __init__(self):
        ns = Pyro5.api.locate_ns()
        self.server = Pyro5.api.Proxy("PYRONAME:tax.estimator")
        self.authenticated_user = None

        self.person_id = None
        self.TFN = None
        self.taxable_income = None
        self.tax_withheld = None
        self.has_private_health = False
        self.tax_refund = None
        self.net_income = None

    def authenticate_user(self, person_id, password):
        if len(person_id) != 6 or not person_id.isdigit():
            return False

        for user in users:
            if user["ID"] == int(person_id) and user["password"] == password:
                self.authenticated_user = int(person_id)
                self.person_id = int(person_id)
                return True
        return False

    def verify_tax_data(self):
        try:
            self.taxable_income = float(self.taxable_income)
            self.tax_withheld = float(self.tax_withheld)
            self.has_private_health = str(self.has_private_health).strip().lower() == "yes"
        except ValueError:
            print("Error: Invalid numerical values.")
            return False

        if not (self.taxable_income >= 0 and 0 <= self.tax_withheld < self.taxable_income):
            print("Error: Taxable income and tax withheld values are incorrect.")
            return False

        return True

    def get_tax_details(self):
        while True:
            try:
                self.taxable_income = float(input("Enter taxable income: "))
                self.tax_withheld = float(input("Enter tax withheld: "))
                self.has_private_health = input("Do you have private health insurance ('yes' or 'no')? ").strip().lower()

                if self.has_private_health not in ["yes", "no"]:
                    print("Error: Enter 'yes' or 'no'.")
                    continue

                self.has_private_health = self.has_private_health == "yes"

                if not self.verify_tax_data():
                    print("Invalid tax data. Please try again.")
                    continue

                break  # Exit loop on successful input

            except ValueError:
                print("Error: Please enter valid numerical values.")

    def request_estimate(self):
        if self.authenticated_user is None:
            return "Error: Not Authenticated"

        if (self.taxable_income is None or self.tax_withheld is None) and not self.TFN:
            self.get_tax_details()

        print("Calculating...")
        _, _, self.taxable_income, self.tax_withheld, self.net_income, self.tax_refund = (
            self.server.taxCalcAPI(self.person_id, self.TFN, self.taxable_income, self.tax_withheld, self.has_private_health)
        )

    def display_tax_return(self):
        if self.tax_refund is None:
            print("Error: No tax estimate available.")
            return

        if self.TFN:
            print(self.tax_refund)
        else:
            if self.tax_refund >= 0:
                print(f"\nOn your taxable income of ${self.taxable_income:,.2f}, you've paid ${self.tax_withheld:,.2f}.")
                print(f"Your return estimate is ${self.tax_refund:,.2f}.")
            else:
                owed_amount = abs(self.tax_refund)
                print(f"On your taxable income of ${self.taxable_income:,.2f}, you've paid ${self.tax_withheld:,.2f}.")
                print(f"You owe an additional ${owed_amount:,.2f}.")

    def user_prompted(self):
        while True:
            print("\nWelcome to the Personal Income Tax Return Estimator")
            print("Enter your User ID or 'Q' to quit")
            person_id = input("> ")
            if person_id.upper() == "Q":
                break
            password = input("Enter your Password\n> ")
            if not self.authenticate_user(person_id, password):
                print("Error: Invalid Credentials")
            else:
                print("Do you have a Tax File Number (TFN)?")
                if input("[Y]es - [N]o: ").upper() == "Y":
                    while True:
                        try:
                            if self.person_id != int(input("User ID: ")): raise TypeError
                            self.TFN = int(input("TFN: "))
                            break
                        except TypeError:
                            print("Error: Invalid Input")
                self.request_estimate()
                self.display_tax_return()
                break