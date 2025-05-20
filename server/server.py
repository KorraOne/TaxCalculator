import Pyro5.server
from TaxEstimator import TaxEstimator

if __name__ == "__main__":
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(TaxEstimator)
    print("RMI Tax Estimator Server is Running. URI:", uri)
    daemon.requestLoop()