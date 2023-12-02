import requests
import json
import paho.mqtt.client as mqtt

def get_machine_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Ошибка при получении данных с {url}")
        return None

def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

def connect_mqtt():
    client = mqtt.Client(client_id="any")
    client.username_pw_set("admin1", "@dmIN")
    client.on_message = on_message
    client.connect("82.146.60.95", 1883)
    client.subscribe("sens/t")
    client.subscribe("sens/h")
    client.loop_start()
    return client

def display_data():
    lab_machine_url = "https://cnc.kovalev.team/get/3"
    lab_machine_data = get_machine_data(lab_machine_url)

    if lab_machine_data:
        print("Данные лабораторного станка:")
        print(f"Режим канала: {lab_machine_data['data'][1][1][3][1]}")
        print(f"Программа управления первого канала: {lab_machine_data['data'][1][1][5][1]}")
        print(f"Процент выполнения программы: {lab_machine_data['data'][1][1][6][1]}")
    
    milling_machine_url = "https://cnc.kovalev.team/get/5"
    milling_machine_data = get_machine_data(milling_machine_url)

    if milling_machine_data:
        print("\nДанные фрезерного станка:")
        print(f"Статус канала: {milling_machine_data['data'][1][1][2][1]}")

    mqtt_client = connect_mqtt()

    mqtt_client.loop_stop()
    mqtt_client.disconnect()

display_data()
