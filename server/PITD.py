import Pyro5.api

@Pyro5.api.expose
class PITD:
    def __init__(self):
        self.data = []

    def add_user_data(self, person_id, TFN, incomes:list[int], withhelds:list[int]):
        user_data = {
                    "person_id": person_id,
                    "TFN": TFN,
                    "incomes": incomes,
                    "withheld": withhelds
                     }
        self.data.append(user_data)

    def get_user_data(self, person_id, TFN):
        for user_data in self.data:
            if user_data["person_id"] == person_id and user_data["TFN"] == TFN:
                return user_data
        return None


def create_random_user_data():
    import random
    person_id = "123456"
    TFN = random.randint(10_000_000, 99_999_999)
    incomes = []
    withhelds = []
    fortnights = random.randint(1, 26)
    for _ in range(0, fortnights):
        incomes.append(round(random.randint(200, 2000), 2))
        withhelds.append(round(incomes[-1] * 0.1, 2))

    return person_id, TFN, incomes, withhelds