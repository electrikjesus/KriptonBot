import json
import urllib2
import os
import time
import telegram

kripton_people = [
    'kadertarlan', 
    'yeliztaneroglu', 
    'ozcanesen', 
    'aybuke', 
    'gulsahkose'
    ]

bot = telegram.Bot(token='<<TOKEN>>')

while True:
    data = urllib2.urlopen('http://review.blissroms.com/changes/?n=25&O=81')
    json_text = data.read()
    json_text = json_text[5:] # trim

    latest_changes = json.loads(json_text)

    for patch in latest_changes:

        _number = str(patch['_number'])

        if patch['owner']['username'] in kripton_people and not os.path.exists("sentcommits/" + _number):

                message = 'Gonderen: ' + patch['owner']['username'] + \
                        '\n - Durum: ' + patch['status'] + \
                        '\n - Baslik: ' + patch['subject'] + \
                        '\n - Degisiklik: +' + str(patch['insertions']) + ' -' + str(patch['deletions']) + \
                        '\n - Baglanti: review.blissroms.com/#/c/' + _number

                subscribers = []
                for update in bot.getUpdates():
                    chat_id = update['message']['chat']['id']
                    if chat_id not in subscribers:
                        subscribers.append(chat_id)

                for chat_id in subscribers:
                    try:
                        bot.sendMessage(chat_id, message)
                    except:
                        pass

                open("sentcommits/" + _number, 'a').close() # touch sentcommits/id

    time.sleep(10)
