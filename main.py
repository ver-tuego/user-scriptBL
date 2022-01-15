import vk_api
import re
import time
from threading import Thread
from vk_api.longpoll import VkLongPoll, VkEventType

try:
    from config import access_token, ignoreBan
except ImportError:
    exit('Необходимо проверить все нужные элементы в config.py')

if access_token == '':
    exit('Необходимо указать токен в "access_token" из config.py')

vk_session = vk_api.VkApi(token=access_token)
api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def getBanned(vk_session):
    result = vk_session.method("account.getBanned")
    if result['count'] == 0:
        return 1
    else:
        return result['items']

getTime = time.time() - 1
listBanned = getBanned(vk_session)

def Handler(event):

    global getTime, listBanned
    user_id = event.user_id

    print(f'#LOGS | {time.strftime("%m.%d %H:%M:%S")} | {user_id} | ', re.sub(r"\s", " ", event.text))

    if (time.time() - getTime) > 0:
        listBanned = getBanned(vk_session)
        getTime = time.time() + 30

    if event.peer_id > 2000000000 and listBanned != 1:
        if user_id in listBanned and user_id not in ignoreBan:
            vk_session.method("messages.delete", {"peer_id": event.peer_id,
                                                  "message_ids": event.message_id})

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        newEvent = Thread(target=Handler, args=(event,))
        newEvent.start()

