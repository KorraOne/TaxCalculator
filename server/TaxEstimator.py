import Pyro5.api

@Pyro5.api.expose
class TaxEstimator:
    """A tax estimate that calculates income tax, medicare levy,
    and medicare levy surcharge based on taxable income and private
    health status.
    """
    def __init__(self):
        """Initalises tax brackets used for income tax calculation.
        Stores database name for connection."""
        self.income_tax_brackets = [
            {"min": 0, "max": 18_200, "rate": 0},
            {"min": 18_201, "max": 45_000, "rate": 0.19},
            {"min": 45_001, "max": 120_000, "rate": 0.325},
            {"min": 120_001, "max": 180_000, "rate": 0.37},
            {"min": 180_001, "max": float("inf"), "rate": 0.45}
        ]
        self.database_name = "tax.database"

    def _calculate_income_tax(self, taxable_income):
        """Calculates income tax based on the provided taxable income.
        Args:
             taxable_income (float): The total taxable income.
        Returns:
            float: The total income tax owed.
        """
        tax = 0
        for bracket in self.income_tax_brackets:
            if taxable_income > bracket["max"]:
                tax += (bracket["max"] - bracket["min"]) * bracket["rate"]
            else:
                tax += (taxable_income - bracket["min"]) * bracket["rate"]
                break
        return tax

    def _calculate_medicare_levy(self, taxable_income):
        """Calculates the medicare levy based on taxable income.
        Args:
             taxable_income (float): The total taxable income.
        Returns:
            float: The medicare levy amount.
        """
        return taxable_income * 0.02

    def _calculate_medicare_levy_surcharge(self, taxable_income, has_private_health):
        """Calculates Medicare levy surcharge based on income level and
        private health status.
        Args:
             taxable_income (float): The total taxable income.
             has_private_health (bool): True or False if user has private health.
        Returns:
            float: the Medicare levy surcharge amount.
        """
        if has_private_health:
            return 0

        if taxable_income > 140_000:
            return taxable_income * 0.015
        elif taxable_income > 105_000:
            return taxable_income * 0.0125
        elif taxable_income > 90_000:
            return taxable_income * 0.01
        return 0

    def _estimate_tax_return(self, taxable_income, tax_withheld, has_private_health):
        """Estimates tax return based on total taxable income and tax withheld.
        Args:
             taxable_income (float): The total taxable income.
             tax_withheld (float): The amount of tax withheld.
             has_private_health (bool): True or False if user has private health.
        Returns:
            float: The estimated tax refund or amount owned (if negative).
        """
        income_tax = self._calculate_income_tax(taxable_income)
        medicare_levy_tax = self._calculate_medicare_levy(taxable_income)
        medicare_levy_surcharge = self._calculate_medicare_levy_surcharge(taxable_income, has_private_health)

        total_tax = income_tax + medicare_levy_tax + medicare_levy_surcharge
        tax_refund = tax_withheld - total_tax
        return tax_refund

    def displayBiweeklyDataLog(self, income:list[int], withheld:list[int]):
        """Displays a formatted log of biweekly income and tax withheld.
        Args:
            income (list[int]): List of taxable income for each fortnight.
            withheld (list[int]): List of tax withheld amounts per fortnight.
        """
        print("\n=== Biweekly Tax Data Log ===")
        for i in range(len(income)):
               print(f"Fortnight {i + 1}: Taxable Income = ${income[i]:,}, Tax Withheld = ${withheld[i]:,}")

        print("\nEnd of Clients Biweekly tax data log.")

    def calcAnnual(self, data:list[int]):
        """Sums biweekly financial data.
        Args:
            data (list[int]): List of financial values.
        Returns:
            int: Total annual value."""
        total = 0
        for num in data:
            total += num
        return total

    def connectPITD(self):
        try:
            ns = Pyro5.api.locate_ns()
            return Pyro5.api.Proxy(ns.lookup(self.database_name))
        except:
            return "Error: Could not reach Database"

    def calcFromPITDData(self, person_id, TFN):
        database = self.connectPITD()
        if database == "Error: Could not reach Database":
            return database

        user_data = database.get_user_data(person_id, TFN)

        total_income = self.calcAnnual(user_data["incomes"])
        total_withheld = self.calcAnnual(user_data["withheld"])
        return total_income, total_withheld

    def taxCalcAPI(self, person_id, TFN, income, withheld, has_private_health):
        """Calculates taxable income, tax, withheld, and estimated tax return for given input.
        Args:
            person_id (int): The ID of the user.
            TFN: (int | None): Tax File Number if available.
            income (list[int]): List of taxable incomes.
            withheld (list[int]): List of withheld tax.
            has_private_health (bool): True or False if user has private health.
        Returns:
            tuple: Contains person_id, TFN status, taxable income, tax withheld, net income, and tax refund."""
        taxable_income = self.calcAnnual(income)
        tax_withheld = self.calcAnnual(withheld)


        if not TFN:
            self.displayBiweeklyDataLog(income, withheld)
            tax_refund = self._estimate_tax_return(taxable_income, tax_withheld, has_private_health)
            net_income = taxable_income + tax_refund - tax_withheld

            hasTFN = True if TFN else False
            return person_id, hasTFN, taxable_income, tax_withheld, net_income, tax_refund
        else:
            taxable_income, tax_withheld = self.calcFromPITDData(person_id, TFN)
            tax_refund = self._estimate_tax_return(taxable_income, tax_withheld, has_private_health)
            net_income = taxable_income + tax_refund - tax_withheld
            return person_id, TFN, taxable_income, tax_withheld, net_income, tax_refund