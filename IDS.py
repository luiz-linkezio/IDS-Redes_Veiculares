from joblib import load
from keras.models import load_model
#from sklearn.svm import OneClassSVM
import can
import subprocess
import numpy as np
import pandas as pd

def gerar_lotes(dados, tamanho_lote):
    for i in range(0, len(dados), tamanho_lote):
        lote = dados[i:i + tamanho_lote]
        yield lote

def create_slicing_windows(data, time_step=1):
    X = []
    for c in range(1):
        a = data[c:(c + time_step)]
        X.append(a)
    return np.array(X)

def df_construct(messages, timestamp, scaler=None):

    if isinstance(messages, list) == False:
        messages = [messages]

    df_message = pd.DataFrame()
    for message in messages:
        
        counter = 0
        byte_list = list()
        for byte in message.data:
            byte_list.append(byte)
            counter += 1
            
        while counter < 4:
            byte_list.append(-1)
            counter += 1
        
        df_message = df_message._append({'Timestamp': (message.timestamp - timestamp), 'DLC': message.dlc,'Arb ID': message.arbitration_id,'Byte 0': byte_list[0],'Byte 1':byte_list[1],'Byte 2':byte_list[2],'Byte 3':byte_list[3]}, ignore_index=True)
        timestamp = message.timestamp

    if scaler:
        df_message_scaled = pd.DataFrame(scaler.transform(df_message), columns=df_message.columns, index=df_message.index)
        return df_message_scaled
    else:
        return df_message

def predict(message, timestamp, model, model_name, scaler=None, window_size=None, threshold=None):
	global benign_count
	global malicious_count
	
	df_message = df_construct(message, timestamp, scaler)
	if window_size is not None:
		message_window = create_slicing_windows(df_message, window_size)
	
	if model_name == "OCSVM":
		predict = model.predict(df_message)
		if predict == 1:
			print(f"Mensagem BENIGNA: {message}")
		elif predict == -1:
			print(f"Mensagem MALICIOSA: {message}")

	elif model_name == "LSTMns":
		predict = model.predict(message_window)
		
		reconstruction_error = np.mean(np.square(message_window - predict), axis=(1, 2))
		
		print(reconstruction_error)
		if reconstruction_error < threshold:
			print(f"Janela BENIGNA de tamanho: {window_size}")
			benign_count += 1
		elif reconstruction_error > threshold:
			malicious_count += 1
			print(f"Janela MALICIOSA de tamanho: {window_size}")
		print(f"Benignas: {benign_count}, Maliciosas: {malicious_count}")

	elif model_name == "LSTMs":
		predict = model.predict(message_window)
		print(predict)
		if predict > 0:
			benign_count += 1
			print(f"Janela BENIGNA de tamanho: {window_size}")
		elif predict <= 0:
			malicious_count += 1
			print(f"Janela MALICIOSA de tamanho: {window_size}")


#ocsvm_model = load("/home/live/Documents/PET Luiz e Karen - Dupla 7/model_ocsvm.joblib")

lstm_model = load_model("/home/petdupla7/Desktop/PET/models/model0_LSTM_ns_bc_ws150_t0,04415.keras")
#lstm_model = load_model("/home/petdupla7/Desktop/PET/models/model0_LSTM_s_bc_ws150.keras")
lstm_windows_size = 150
lstm_scaler = load("/home/petdupla7/Desktop/PET/models/scalers/scaler_model0_LSTM_ns_bc_ws150_t0,04415")
#lstm_scaler = load("/home/petdupla7/Desktop/PET/models/scalers/scaler_model0_LSTM_s_bc_ws150")
lstm_theshold = 0.12
print(f"Threshold: {lstm_theshold}")

benign_count = 0
malicious_count = 0
with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

    count = 0
    timestamp = 0
    lstm_messages_list = list()
    while True:
        try:
            message = bus.recv()


            #predict(message, timestamp, ocsvm_model, "OCSVM")


            lstm_messages_list.append(message)
            count += 1
            if count == lstm_windows_size:
                predict(lstm_messages_list, timestamp, lstm_model, "LSTMns", lstm_scaler, lstm_windows_size, lstm_theshold)
                count = 0
                lstm_messages_list = list()

            timestamp = message.timestamp

        except Exception as e:
            print("Erro:", e)
            
            subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
            subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
            
            bus.flush_tx_buffer()
