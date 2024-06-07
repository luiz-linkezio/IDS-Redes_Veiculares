from joblib import load
from keras.models import load_model
#from sklearn.svm import OneClassSVM
import can
import subprocess
import numpy as np
import pandas as pd

def create_slicing_windows(data, labels=None, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step):
        a = data[i:(i + time_step)]

        X.append(a)

        if labels:
            Y.append(labels[i + time_step])

    return np.array(X), np.array(Y)

def df_construct(messages, timestamp, scaler=None):

    if isinstance(messages, list) == False:
        messages = [messages]

    df_message = pd.DataFrame()
    for message in messages:

        df_message["Rel Time"] = [(message.timestamp - timestamp)]
        timestamp = message.timestamp
        df_message["DLC"] = [message.dlc]
        df_message["Arb ID"] = [message.arbitration_id]

        counter = 0
        for byte in message.data:
            df_message[f'Byte {counter}'] = [byte]
            counter += 1
            
        while counter < 4:
            df_message[f'Byte {counter}'] = -1
            counter += 1

    if scaler:
        df_message_scaled = pd.DataFrame(scaler.transform(df_message), columns=df_message.columns, index=df_message.index)
        return df_message_scaled
    else:
        return df_message

def predict(message, timestamp, model, model_name, scaler=None, window_size=None, threshold=None):

    df_message = df_construct(message, timestamp, scaler)

    if window_size is not None:
        message_window, _ = create_slicing_windows(df_message, None, window_size)

    if model_name == "OCSVM":
        predict = model.predict(df_message)
        
        if predict == 1:
            print(f"Mensagem BENIGNA: {message}")
        elif predict == -1:
            print(f"Mensagem MALICIOSA: {message}")


    elif model_name == "LSTM":
        predict = model.predict(message_window)

        if predict > threshold:
            print(f"Janela BENIGNA de tamanho: {window_size}")
        elif predict < threshold:
            print(f"Janela MALICIOSA de tamanho: {window_size}")


ocsvm_model = load("/home/live/Documents/PET Luiz e Karen - Dupla 7/model_ocsvm.joblib")

lstm_model = load_model("/home/live/Documents/PET Luiz e Karen - Dupla 7/xxxxxxxxxxxx")
lstm_windows_size = 150
lstm_scaler = load("/home/live/Documents/PET Luiz e Karen - Dupla 7/xxxxxxxxxxxxxx")
lstm_theshold = 0

with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

    count = 0
    timestamp = 0
    lstm_messages_list = list()
    while True:
        try:
            message = bus.recv()


            predict(message, timestamp, ocsvm_model, "OCSVM")


            lstm_messages_list.append(message)
            count += 1
            if count == lstm_windows_size:
                predict(lstm_messages_list, timestamp, lstm_model, "LSTM", lstm_scaler, lstm_windows_size, lstm_theshold)

            timestamp = message.timestamp

        except Exception as e:
            print("Erro:", e)
            
            subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
            subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
            
            bus.flush_tx_buffer()