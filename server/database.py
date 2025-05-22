from PITD import PITD, create_random_user_data
import Pyro5.api, Pyro5.server

if __name__ == "__main__":
    database = PITD()
    database.add_user_data("123456", "12345678", [200, 200, 300], [40, 40, 50])
    database.add_user_data("111111", "11111111", [5000, 4000, 7990], [300, 200, 5000])
    database.add_user_data("654321", "98765432", *create_random_user_data())

    try:
        IP = input("Enter IP address: ")
        daemon = Pyro5.server.Daemon(host=IP)
        ns = Pyro5.api.locate_ns(host=IP)
        uri = daemon.register(database)
        ns.register("tax.database", uri)
        print("Database Server is running...")
        daemon.requestLoop()
    except:
        print("Database Server failed to start.")