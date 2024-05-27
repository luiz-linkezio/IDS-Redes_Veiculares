from joblib import load
from sklearn.svm import OneClassSVM
import can
import time
import subprocess
import numpy as np
import pandas as pd

def predict(model, message, model_name):

    df_message = pd.DataFrame()

    df_message["Rel Time"] = message.timestamp
    df_message["Arb ID"] = message.arbitration_id
    df_message["DLC"] = message.dlc

    counter = 0
    for byte in message.data:
        df_message[f'Byte {counter}'] = byte
        counter += 1
    
    if model_name == "OCSVM":
        predict = model.predict(df_message)
        
        if predict == 1:
            print(f"Mensagem BENIGNA: {message}")
        elif predict == -1:
            print(f"Mensagem MALICIOSA: {message}")



ocsvm_model = load("models/model_ocsvm.joblib")
print(ocsvm_model)

with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

    messages = list()
    while True:
        try:
            for message in bus:
                predict(ocsvm_model, message, "OCSVM")
                messages.append(message)

        except Exception as e:
            print('erro', e)
            
            subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
            subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
            
            bus.flush_tx_buffer()