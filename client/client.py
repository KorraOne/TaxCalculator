import Pyro5.api

@Pyro5.api.expose
class TaxEstimator:
    def __init__(self):
        self.income_tax_brackets = [
            {"min": 0, "max": 18_200, "rate": 0},
            {"min": 18_201, "max": 45_000, "rate": 0.19},
            {"min": 45_001, "max": 120_000, "rate": 0.325},
            {"min": 120_001, "max": 180_000, "rate": 0.37},
            {"min": 180_001, "max": 1_000_000, "rate": 0.45}
        ]

    def calculate_income_tax(self, taxable_income):
        tax = 0
        for bracket in self.income_tax_brackets:
            if taxable_income > bracket["max"]:
                tax = (taxable_income - bracket["min"]) * bracket["rate"]
            else: break
        return tax

    def calculate_medicare_levy(self, taxable_income):
        return taxable_income * 0.02

    def calculate_medicare_levy_surcharge(self, taxable_income, has_private_health):
        if has_private_health:
            return 0

        if taxable_income > 140_000:
            return taxable_income * 0.015
        elif taxable_income > 105_000:
            return taxable_income * 0.0125
        elif taxable_income > 90_000:
            taxable_income * 0.01
        return 0

    def estimate_tax_return(self, taxable_income, tax_withheld, net_income, has_private_health):
        income_tax = self.calculate_income_tax(taxable_income)
        medicare_levy_tax = self.calculate_medicare_levy(taxable_income)
        medicare_levy_surcharge = self.calculate_medicare_levy_surcharge(taxable_income, has_private_health)

        total_tax = income_tax + medicare_levy_tax + medicare_levy_surcharge
        tax_refund = tax_withheld - total_tax
        return tax_refund

daemon = Pyro5.server.Daemon()
uri = daemon.register(TaxEstimator)
print("RMI Tax Estimator Server is Running. URI:", uri)
daemon.requestLoop()

