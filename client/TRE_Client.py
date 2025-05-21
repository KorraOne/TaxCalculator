import Pyro5.api
from usersData import users

class TRE_Client:
    """
    A client for interacting with the Tax Return Estimator server.
    Handles authentication, tax details inputs, and displaying results.
    """
    def __init__(self):
        """Initialises attributes."""
        self.server = None

        self.authenticated_user = None
        self.person_id = None
        self.TFN = None
        self.biweekly_income = []
        self.biweekly_withheld = []
        self.taxable_income = None
        self.tax_withheld = None
        self.has_private_health = False
        self.tax_refund = None
        self.net_income = None

    def connect(self):
        """Connects to TaxEstimator server."""
        ns = Pyro5.api.locate_ns()
        self.server = Pyro5.api.Proxy("PYRONAME:tax.estimator")

    def authenticate_user(self, person_id, password):
        """Authenticates user via ID and Password.
        Changes state of class to be authenticated.
        Args:
            person_id (str): User ID string (6-digits).
            password (str): User password.
        Returns:
            bool: True if authentication successful."""
        if len(person_id) != 6 or not person_id.isdigit():
            return False

        for user in users:
            if user["ID"] == int(person_id) and user["password"] == password:
                self.authenticated_user = int(person_id)
                self.person_id = int(person_id)
                return True
        return False

    def verify_tax_data(self, income, withheld):
        """Verifies inputted data is valid.
        Args:
            income (float): Single fortnight taxable income.
            withheld (float): Single fortnight withheld tax.
        Returns:
            bool: True if values are valid."""
        try:
            self.biweekly_income.append(float(income))
            self.biweekly_withheld.append(float(withheld))
            self.has_private_health = str(self.has_private_health).strip().lower() == "yes"
        except ValueError:
            print("Error: Invalid numerical values.")
            return False

        if not (income >= 0 and 0 <= withheld < income):
            print("Error: Taxable income and tax withheld values are incorrect.")
            return False

        return True

    def get_tax_details(self):
        """Prompts user for details and stores them."""
        while True:
            self.has_private_health = input("Do you have private health insurance ('yes' or 'no')? ").strip().lower()
            if self.has_private_health in ["yes", "no", "y", "n"]:
                self.has_private_health = self.has_private_health == "yes"
                break
            print("Error: Enter 'yes' or 'no'.")

        amountFortnights = int_input("How many fortnights of data? (max of 26)\n> ", "Error: Enter a valid number.")
        for fortnight in range(0, min(amountFortnights, 26)):
            while True:
                print("For Fortnight", fortnight + 1)
                income = int_input("Enter taxable income: ", "Error: Enter a valid income amount.")
                withheld = int_input("Enter tax withheld: ", "Error: Enter a valid withheld amount.")
                if not self.verify_tax_data(income, withheld):
                    print("Invalid tax data. Please try again.")
                    continue
                break

    def request_estimate(self):
        """Calls servers calculation functions. Stores result."""
        if self.authenticated_user is None:
            return "Error: Not Authenticated"

        if (self.biweekly_income == [] or self.biweekly_withheld == []) and not self.TFN:
            self.get_tax_details()

        print("Calculating...")
        _, _, self.taxable_income, self.tax_withheld, self.net_income, self.tax_refund = (
            self.server.taxCalcAPI(self.person_id, self.TFN, self.biweekly_income, self.biweekly_withheld, self.has_private_health)
        )

    def display_tax_return(self):
        """Displays Tax Return Estimate in readable format."""
        if self.tax_refund is None:
            print("Error: No tax estimate available.")
            return

        print(f"\nOn your taxable income of ${self.taxable_income:,.2f}, you've paid ${self.tax_withheld:,.2f}.")
        if self.tax_refund >= 0:
            print(f"Your return estimate is ${self.tax_refund:,.2f}.")
        else:
            owed_amount = abs(self.tax_refund)
            print(f"You owe an additional ${owed_amount:,.2f}.")
        print(f"Resulting in your net income of ${self.net_income:,.3f}.")


    def user_prompted(self):
        """Main user interface structure."""
        print("\nWelcome to the Personal Income Tax Return Estimator")
        person_id = input("Enter your User ID or 'Q' to quit: ")
        if person_id.upper() == "Q":
            return
        password = input("Enter your Password\n> ")

        if not self.authenticate_user(person_id, password):
            print("Error: Invalid Credentials")
            return

        print("Do you have a Tax File Number (TFN)?")
        if input("[Y]es - [N]o: ").upper() == "Y":
            entered_id = int_input("User ID: ", "Error: Enter a valid User ID.")
            if self.person_id != entered_id:
                print("Error: Incorrect User ID.")
                return
            self.TFN = int_input("TFN: ", "Error: Enter a valid TFN.")
        else:
            if self.person_id != int_input("User ID: ", "Error: Enter a valid User ID."):
                print("Error: Incorrect User ID.")
                return
        self.request_estimate()
        self.display_tax_return()


def int_input(prompt, error_message) -> int:
    """Re-prompts until valid int is inputted.
    Args:
        prompt (str): Prompt displayed to user.
        error_message (str): Error message after invalid input.
    Returns:
        int: Users valid input.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print(error_message)