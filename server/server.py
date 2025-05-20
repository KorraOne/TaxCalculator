import Pyro5.server
import Pyro5.api
from TaxEstimator import TaxEstimator

if __name__ == "__main__":
    daemon = Pyro5.server.Daemon()
    ns = Pyro5.api.locate_ns()
    uri = daemon.register(TaxEstimator)
    ns.register("tax.tax", uri)
    print("RMI Tax Estimator Server is Running. URI:", uri)
    daemon.requestLoop()