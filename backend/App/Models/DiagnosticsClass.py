from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

class Diagnostics(object):
    #Ping React frontend to ensure "reactivity" (lol)
    async staticmethod def PingFrontend:
        return True #Placeholder

    #Ping MongoDB to make sure data is able to both be accessed and logged from frontend
    async staticmethod def PingBackend:
        return True #Placeholder

    #Combine both pings and execute as one function, above functions should be run explicitly by admins, while this should be
    #on a general health page
    async staticmethod def RoundTripPing:
        return True #Placeholder

    #Should the pings be successful this will be run to check if server performance is degraded or up to par
    async staticmethod def DataRecollectionTest:
        return 0.00

    pass


