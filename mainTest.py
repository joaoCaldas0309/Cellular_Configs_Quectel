import argparse
import time
from tqdm import tqdm

class FakeSerial:
    def __init__(self, *args, **kwargs):
        print("Conectado a uma porta COM virtual.")

    def write(self, command):
        # Simula o envio de comando para a porta
        time.sleep(0.5)

    @property
    def in_waiting(self):
        return True

    def readline(self):
        return b"Resposta simulada do dispositivo."

def handle_status(ser):
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

def handle_reboot(ser):
    commands = [b"REBOOT1", b"REBOOT2", b"REBOOT3"]
    with tqdm(total=len(commands), desc="Executando REBOOT", leave=True, ncols=80, ascii=True) as progress_bar:
        for command in commands:
            ser.write(command)
            time.sleep(1)  # Simulando tempo entre cada comando de reboot
            progress_bar.update(1)

def handle_info(ser):
    commands = [b"INFO1", b"INFO2", b"INFO3"]
    responses = []
    with tqdm(total=len(commands), desc="Executando INFO", leave=True, ncols=80, ascii=True) as progress_bar:
        for command in commands:
            ser.write(command)
            if ser.in_waiting:
                response = ser.readline().decode().strip()
                responses.append(response)
            time.sleep(1)  # Tempo de espera entre comandos
            progress_bar.update(1)
    tqdm.write("\nInformações recebidas: " + str(responses))

def main():
    parser = argparse.ArgumentParser(description="Script de simulação para comunicação com porta COM.")
    parser.add_argument("port", help="Porta COM simulada ou real.")
    parser.add_argument("command", help="Comando a ser enviado ('STATUS', 'REBOOT', 'INFO', etc.).")

    args = parser.parse_args()
    ser = FakeSerial()

    command = args.command.strip().upper()
    if command == "STATUS":
        handle_status(ser)
    elif command == "REBOOT":
        handle_reboot(ser)
    elif command == "INFO":
        handle_info(ser)
    else:
        print(f"Comando '{args.command}' não reconhecido.")

if __name__ == "__main__":
    main()
