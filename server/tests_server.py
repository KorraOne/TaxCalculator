import pytest
from TaxEstimator import TaxEstimator

@pytest.fixture
def tax_estimator():
    return TaxEstimator()

@pytest.mark.parametrize("taxable_income, expected_tax", [
    [10_000, 0],
    [18_200, 0],
    [30_000, 2_242],
    [45_000, 5_092],
    [60_000, 9_967],
    [120_000, 29_467],
    [150_000, 40_567],
    [180_000, 51_667],
    [200_000, 60_667]
])
def test_calculate_income_tax(tax_estimator, taxable_income, expected_tax):
    assert tax_estimator.calculate_income_tax(taxable_income) == pytest.approx(expected_tax, 0.001)

@pytest.mark.parametrize("taxable_income, expected_tax", [
    [50_000, 1_000],
    [100_000, 2_000],
])
def test_calculate_medicare_levy(tax_estimator, taxable_income, expected_tax):
    assert tax_estimator.calculate_medicare_levy(taxable_income) == expected_tax

@pytest.mark.parametrize("taxable_income, has_private_health, expected_tax", [
    [85_000, True, 0],
    [95_000, False, 950],
    [110_000, False, 1_375],
    [145_000, False, 2_175]
])
def test_calculate_medicare_surcharge(tax_estimator, taxable_income, has_private_health, expected_tax):
    assert tax_estimator.calculate_medicare_levy_surcharge(taxable_income, has_private_health) == expected_tax