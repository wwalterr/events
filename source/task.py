from time import sleep


import schedule


from cache import client


from threading import Thread


from ast import literal_eval


def request(data):
    print(data)


def channel_webhook(message):
    data = literal_eval(message.get('data', {}).decode('utf-8'))

    schedule.every(data.get('seconds')).seconds.do(lambda: request(data))


def start_schedule():
    while True:
        schedule.run_pending()

        sleep(1)


def start_message(pubsub):
    while True:
        message = pubsub.get_message()

        if message:
            print(message)


def start_task():
    print(' * Task start')

    Thread(target=start_schedule, name='Schedule').start()

    pubsub = client.pubsub()

    pubsub.subscribe(**{'webhook': channel_webhook})

    Thread(target=start_message, name='Message', args=(pubsub,)).start()
