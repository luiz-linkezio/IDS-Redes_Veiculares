from joblib import load
from sklearn.svm import OneClassSVM
import can
import time
import subprocess
import numpy as np
import pandas as pd

def predict(model, message, model_name, timestamp):
    global benign_count
    global malicious_count

    df_message = pd.DataFrame()

    df_message["Rel Time"] = [(message.timestamp - timestamp)]
    df_message["DLC"] = [message.dlc]
    df_message["Arb ID"] = [message.arbitration_id]

    counter = 0
    for byte in message.data:
        df_message[f'Byte {counter}'] = [byte]
        counter += 1
        
    while counter < 4:
        df_message[f'Byte {counter}'] = 0
        counter += 1
    
    if model_name == "OCSVM":
        predict = model.predict(df_message)
        
        if predict == 1:
            benign_count += 1
            print(f"Mensagem BENIGNA: {message}")
        elif predict == -1:
            malicious_count += 1
            print(f"Mensagem MALICIOSA: {message}")
    
    print(100*malicious_count/(benign_count+malicious_count),"%")
    
    return message.timestamp

benign_count = 0
malicious_count = 0

ocsvm_model = load("/home/live/Documents/PET Luiz e Karen - Dupla 7/model_ocsvm.joblib")

with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

    messages = list()
    timestamp = 0
    while True:
        try:
            for message in bus:
                timestamp = predict(ocsvm_model, message, "OCSVM", timestamp)
                messages.append(message)

        except Exception as e:
            print('erro', e)
            
            subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
            subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
            
            bus.flush_tx_buffer()
