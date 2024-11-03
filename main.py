import argparse
import serial
import time
from tqdm import tqdm

class fakeSerial:
    def __init__(self, *args, **kwargs):
        print("Connected with COM port")
    
    def write(self, command):
        print(f"Sended command: {command.decode()}")

    @property
    def in_waiting(self):
        return True
    
    def readline(self):
        return b"Device simulated response"
    
def condition_ARGENTINA(ser):
    commands = [b"STATUS1", b"STATUS2", b"STATUS3"]
    responses = []
    # Barra de progresso configurada para uma única linha
    with tqdm(total=len(commands), desc="Executando STATUS", leave=True, ncols=80, ascii=True) as progress_bar:
        for command in commands:
            ser.write(command)
            if ser.in_waiting:
                response = ser.readline().decode().strip()
                responses.append(response)
            time.sleep(1)  # Tempo de espera entre comandos
            progress_bar.update(1)  # Atualiza a barra após cada comando
    tqdm.write("\nRespostas do dispositivo: " + str(responses))
        

def condition_BRAZIL(ser):
    ser.write(b"BRAZIL_Device")
    time.sleep(1)

    print(f'$ALL CONFIGS DEFAULT\n\r')
    time.sleep(1)
    print('$CELLULAR APN NAME 0 quectel.br\n\r')
    time.sleep(1)
    print("$CELLULAR APN USER 0\n\r")
    time.sleep(1) 
    print('$CELLULAR APN PASSWORD 0\n\r')
    time.sleep(1) 
    print('$CELLULAR APN CONTEXT_TYPE 0 IPv4\n\r')
    time.sleep(1)
    print('$CELLULAR APN AUTH_METHOD 0 NONE\n\r')
    time.sleep(1)
    print('$CELLULAR CONFIGS SAVE\n\r')
    time.sleep(1)
    print('$ALL CONFIGS SAVE\n\r')
    time.sleep(1)
    print('$CELLULAR CONFIGS STATUS\n\r')
    time.sleep(1)
    


def condition_INFO(ser):
    if ser.in_waiting:
        response = ser.readline().decode().strip()
        print(f"Resposta do dispositivo: {response}")
    else:
        print("Nenhuma resposta recebida.")

def main ():

    parser = argparse.ArgumentParser(description= "Script for communication with COM port")
    parser.add_argument("port", help="Especify COM port where the device is connected")
    parser.add_argument("command", help="Command to be sended for the device")

    args = parser.parse_args()
    ser = fakeSerial()

    command = args.command.strip().upper()
    if command == "ARGENTINA":
        condition_ARGENTINA(ser)
    elif command == "BRAZIL":
        condition_BRAZIL(ser)
    elif command == "TESTE":
        condition_INFO(ser)
    else:
        print("error")

if __name__ == '__main__':
    main()