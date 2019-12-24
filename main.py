import json
import vk_api
import requests
import random
import pprint
import io
import sys

from vk_api import VkUpload
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


def loadInfo():
    arr = []
    with open("logs.txt", "r") as file:
        lines = file.readlines()
        for i in lines:
            arr.append(i.rstrip("\n").split("-"))
    return arr


def saveInfo(data):
    with open("logs.txt", "w+") as file:
        for i in data:
            file.write(i[0] + "-" + i[1] + "\n")


def generateNames():
    result = [["Александр"], ["Егор"], ["Сергей"], ["Николай"], ["Эрнест"], ["Максим"]]

    names = ["Александр", "Егор", "Сергей", "Николай", "Эрнест", "Максим"]

    for i in range(len(result)):
        
        toAdd = random.choice(names)
        
        while toAdd == result[i][0]:
            if (len(names) == 1):
                generateNames()
                break
            toAdd = random.choice(names)

        result[i].append(toAdd)
        names.remove(toAdd)

    return result

result = generateNames()
print("Done!")

mode = ""

for i in range(len(sys.argv)):
    if (i == 1):
        mode = sys.argv[i]

if (mode == "save"): saveInfo(result)
elif (mode == "load"): result = loadInfo()

API_KEY = "05b0d6177e4c408d5c33f30a6a579c8b3e15b8d1df8e9cf7aafbd08898c06d06228a686d36142277cd2a2"

PUBLIC_ID = 190162848

vk_session = vk_api.VkApi(token = API_KEY)
vk_session._auth_token()

vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, PUBLIC_ID)

while True:
    try:
        for event in longpoll.listen():
            print("here is new event - " + str(event.type))
            if (event.type == VkBotEventType.MESSAGE_TYPING_STATE):
                vk.messages.send(peer_id = event.object.from_id, message = "Печатаешь? Печатай давай.", random_id = get_random_id())
            elif (event.type == VkBotEventType.MESSAGE_NEW):
                name = vk.users.get(user_ids = (event.object.from_id))[0]["first_name"]
                if ("получить" in event.object.text.lower()):
                    print(name)
                    for i in result:
                        if (i[0] == name):
                            vk.messages.send(peer_id = event.object.from_id, message = "Тебе выпал " + i[1] + ".", random_id = get_random_id())
    except:
        print("i've got exception... keep working.")