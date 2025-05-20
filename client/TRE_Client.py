import Pyro5.api

users = [
    {"ID": 123456, "password": "a"}
]

class TRE_Client:
    def __init__(self):
        ns = Pyro5.api.locate_ns()
        self.server = Pyro5.api.Proxy("PYRONAME:tax.tax")
        self.authenticated_user = None

    def authenticate_user(self, person_id, password):
        # short circuit case for optimisation
        if len(person_id) != 6 or not person_id.isdigit():
            return False

        # checks if user exists and if password matches
        for user in users:
            if user["ID"] == int(person_id) and user["password"] == password:
                self.authenticated_user = int(person_id)
                return True
        return False

    def verify_tax_data(self, taxable_income, tax_withheld, has_private_health):
        try:
            taxable_income = float(taxable_income)
            tax_withheld = float(tax_withheld)
            has_private_health = str(has_private_health).strip().lower() == "yes"
        except ValueError:
            print("valueError, 31")
            return None

        if taxable_income >= 0 and 0 <= tax_withheld < taxable_income:
            print("Returns")
            return taxable_income, tax_withheld, has_private_health
        print("Error, 40")
        return None


    def request_estimate(self):
        taxable_income, tax_withheld, has_private_health = self.get_tax_details()
        if self.authenticated_user is None:
            return "Error: Not Authenticated"

        taxable_income, tax_withheld, has_private_health = self.verify_tax_data(taxable_income, tax_withheld, has_private_health)
        if (taxable_income or tax_withheld or has_private_health) is None:
            return "Error: Invalid tax data"

        tax_refund = self.server.estimate_tax_return(taxable_income, tax_withheld, has_private_health)
        return tax_refund

    def get_tax_details(self):
        taxable_income = input("taxable income: ")
        tax_withheld = input("tax withheld: ")
        has_private_health = input("private health, 'yes' or 'no': ")

        return taxable_income, tax_withheld, has_private_health

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
                command = input("[Y]es - [N]o: ").upper()
                match command:
                    case "Y":
                        print("Error: Not Implemented in Phase 1")
                    case "N":
                        reply = self.request_estimate()
                        print(reply)