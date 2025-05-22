# creates server, creates TaxEstimator

import Pyro5.server
import Pyro5.api
from TaxEstimator import TaxEstimator

if __name__ == "__main__":
    try:
        IP = input("Enter IP address: ")
        daemon = Pyro5.server.Daemon(host="IP")
        ns = Pyro5.api.locate_ns(host=IP)
        uri = daemon.register(TaxEstimator)
        ns.register("tax.estimator", uri)
        print("RMI Tax Estimator Server is Running. URI:", uri)
        daemon.requestLoop()
    except:
        print("Server failed to start.")