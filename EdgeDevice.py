

from paho.mqtt import client as mqtt

clientId = "fc-edge"
broker = 'broker.hivemq.com'
topic1 = "/traffic/lane1"
topic2= "/traffic/lane2"
port = 1883




def connect():
    def on_connect(client,userdata, flags, rc):
        if rc == 0:
            print("Success")
        else:
            print("Fail ", rc)

    client = mqtt.Client(clientId)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def subscribe(client: mqtt):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic1)
    client.subscribe(topic2)
    client.on_message = on_message


def run():
    client = connect()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()