import Pyro5.api

users = [
    {"ID": 123456, "password": "ADMIN"}
]

@Pyro5.api.locate_ns
class TRE_Client:
    def __init__(self):
        self.server = Pyro5.api.Proxy("PYRONAME:tax.estimator")
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
        if taxable_income >= 0 and 0 <= tax_withheld < taxable_income:
            return {"taxable_income":taxable_income,
                    "tax_withheld": tax_withheld,
                    "has_private_health": has_private_health}
        return None


    def request_estimate(self):
        taxable_income, tax_withheld, has_private_health = self.get_tax_details()
        if self.authenticated_user is None:
            return "Error: Not Authenticated"

        if self.verify_tax_data(taxable_income, tax_withheld, has_private_health) is None:
            return "Error: Invalid tax data"

        tax_refund = self.server.estimate_tax_return(taxable_income, tax_withheld, has_private_health)
        return tax_refund

    def get_tax_details(self):
        taxable_income = input("taxable income: ")
        tax_withheld = input("tax withheld: ")
        has_private_health = input("private health (Bool): ")

        return taxable_income, tax_withheld, has_private_health

    def user_prompted(self):
        while True:
            print("Welcome to the Personal Income Tax Return Estimator")
            print("Enter your User ID or 'Q' to quit")
            person_id = input("> ")
            if person_id.upper() == "Q":
                break
            password = input("Enter your Password\n> ")
            if self.authenticate_user(person_id, password):
                print("Do you have a Tax File Number (TFN)?")
                command = input("[Y]es - [N]o").upper()
                match command:
                    case "Y":
                        print("Error: Not Implemented in Phase 1")
                    case "N":
                        self.request_estimate()