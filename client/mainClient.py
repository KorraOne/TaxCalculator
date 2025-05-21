# main file for creating a client
# creates a client, connects to server, and starts client prompts

from TRE_Client import TRE_Client
from usersData import users

if __name__ == "__main__":
    client = TRE_Client(users)
    client.connect()
    client.user_prompted()