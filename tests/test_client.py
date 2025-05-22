import pytest
from client.TRE_Client import TRE_Client

mocked_users = [
    {"ID": 123456, "password": "pass123"}
]

@pytest.fixture()
def tre_client():
    return TRE_Client(mocked_users)

@pytest.mark.parametrize("person_id, password, expected_result", [
    ("123456", "pass123", True),
    ("123456", "Incorrect", False),
    ("12345", "pass123", False),
    ("12345", "Incorrect", False)
])
def test_authenticate_user(tre_client, person_id, password, expected_result):
    assert tre_client.authenticate_user(person_id, password) == expected_result

@pytest.mark.parametrize("income, withheld, expected", [
    (2000, 300, True),
    (5000, 1000, True),
    (2000, -100, False),
    (-100, 50, False),
    (2000, 2000, False),
    (3000, 3500, False)
])
def test_verify_tax_data(tre_client, income, withheld, expected):
    assert tre_client.verify_tax_data(income, withheld) == expected
