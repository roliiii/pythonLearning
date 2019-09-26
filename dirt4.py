import requests
import json
from enum import Enum

class EventType(Enum):
    DiRT_DAILY_LIVE = "DiRT DAILY LIVE"
    OWNERS_CLUB = "THE OWNERS’ CLUB / DELTA DAILY"

class Dirt4RankUtil:
    def __init__(self, gamerMode: bool):
        self.session = requests.Session() 
        self.session.put(r"""https://www.dirt4game.com/api/profile/set-handling""",{"isAltHandling":gamerMode})

    def __getUrl(self, eventId, page = 1):
        return r"""https://www.dirt4game.com/api/leaderboard/event/"""+str(eventId)+"""/stage/1/page/"""+str(page)+r"""?assists=0&controls=0&orderByTotal=true&pageSize=100&platform=0&players=0"""
    
    def __getEventData(self, eventId, page = 1):
        data = self.session.get(self.__getUrl(eventId, page))
        return data.json()

    def __getEventId(self, eventType: EventType):
        data = self.session.get(r"""https://www.dirt4game.com/api/event/summary/?altHandling=false""")
        respJson = data.json()
        actEventTypeData = [x for x in respJson["eventTypes"] if x["name"] == eventType.value]

        return actEventTypeData[0]["events"][0]["eventId"]

    def getRank(self, eventType: EventType, userName: str):
        eventId = self.__getEventId(eventType)
        parsedData = self.__getEventData(eventId)

        for i in range(1,parsedData["PageCount"] + 1):
            if(i != 1):
                parsedData = __getEventData(session, eventId, i)
            for item in parsedData["Entries"]:
                if item["Name"] == userName:
                    return(str(item["Rank"]) + "/" + str(len(parsedData["Entries"])))
            return "--/--"

if __name__ == "__main__":
    dirt = Dirt4RankUtil(False)
    print(EventType.DiRT_DAILY_LIVE.value + ": " + dirt.getRank(EventType.DiRT_DAILY_LIVE,"Fluffy"))
    print(EventType.OWNERS_CLUB.value + ": " + dirt.getRank(EventType.OWNERS_CLUB,"Fluffy"))