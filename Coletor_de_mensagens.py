import can
import subprocess
import os
import csv

# Abra o arquivo CSV para escrita
with open('mensagens_can.csv', 'w', newline='') as csvfile:
    fieldnames = ['Timestamp', 'ID', 'Data']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Escreva os cabeçalhos do CSV
    writer.writeheader()

    # Inicialize a conexão CAN
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:
        messages = list()
        timestamp = 0

        # Loop infinito para receber mensagens e escrever no CSV
        while True:
            try:
                #for message in bus:
                    # Adicione a mensagem à lista
                #    messages.append(message)

                    # Escreva a mensagem no arquivo CSV
                #    writer.writerow({'Timestamp': message.timestamp, 'ID': message.arbitration_id, 'Data': message.data})

                message = bus.recv()

                messages.append(message)

                # Escreva a mensagem no arquivo CSV
                writer.writerow({'Timestamp': message.timestamp, 'ID': message.arbitration_id, 'Data': message.data})

            except Exception as e:
                print('erro', e)
                
                # Reinicie a conexão CAN
                subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                
                # Limpe o buffer de transmissão do barramento CAN
                bus.flush_tx_buffer()