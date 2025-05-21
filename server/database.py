from PITD import PITD, create_random_user_data
import Pyro5

if __name__ == "__main__":
    database = PITD()
    database.add_user_data("123456", "12345678", [200, 200, 300], [40, 40, 50])
    database.add_user_data(*create_random_user_data())
    database.add_user_data(*create_random_user_data())

    try:
        daemon = Pyro5.server.Daemon()
        ns = Pyro5.api.locate_ns()
        uri = daemon.register(database)
        ns.register("tax.database", uri)

        print(database.data)
        print("Database Server is running...")
        daemon.requestLoop()
    except:
        print("Database Server failed to start.")