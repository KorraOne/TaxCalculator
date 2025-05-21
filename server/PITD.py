import Pyro5.api

@Pyro5.api.expose
class PITD:
    def __init__(self):
        self.data = {}

    def add_user_data(self, person_id, TFN, incomes, withhelds):
        key = f"{person_id}-{TFN}"
        self.data[key] = {
            "person_id": person_id,
            "TFN": TFN,
            "incomes": incomes,
            "withheld": withhelds
        }

    def get_user_data(self, person_id, TFN):
        print("Received request from Server")
        return self.data.get(f"{person_id}-{TFN}", None)


def create_random_user_data():
    import random
    person_id = "123456"
    TFN = random.randint(10_000_000, 99_999_999)
    incomes = []
    withhelds = []
    fortnights = random.randint(1, 26)
    for _ in range(0, fortnights):
        incomes.append(round(random.uniform(200, 2000), 2))
        withhelds.append(round(incomes[-1] * 0.1, 2))

    return person_id, TFN, incomes, withhelds