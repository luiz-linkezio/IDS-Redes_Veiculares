import os
import csv
import random

# Função para gerar um valor aleatório dentro de um range
def generate_random_value(start, end, decimal_places=0):
    return round(random.uniform(start, end), decimal_places)

# Função para gerar uma linha de dados aleatórios
def generate_random_row():
    return [
        generate_random_value(0, 1, 10),  # float entre 0 e 1 com até 10 casas decimais
        random.randint(1, 4),             # inteiro entre 1 e 4
        random.randint(0, 255),           # inteiros entre 0 e 255
        random.randint(0, 255),           # inteiros entre 0 e 255
        random.randint(0, 255),           # inteiros entre 0 e 255
        random.randint(0, 255),           # inteiros entre 0 e 255
        random.randint(0, 255)            # inteiros entre 0 e 255
    ]

# Função para determinar o nome do arquivo de saída
def determine_output_file():
    base_name = "dados_aleatorios"
    file_extension = ".csv"
    directory = "data/ataques/"
    counter = 0

    while True:
        file_name = f"{base_name}_{counter}{file_extension}"
        if not os.path.exists(os.path.join(directory, file_name)):
            break
        counter += 1

    return os.path.join(directory, file_name)

# Número de linhas a serem geradas
num_rows = 50000

# Nome do arquivo CSV de saída
output_file = determine_output_file()

# Cabeçalho do CSV
header = ["Rel Time", "DLC", "Arb ID", "Byte 0", "Byte 1", "Byte 2", "Byte 3"]

# Geração dos dados aleatórios e escrita no arquivo CSV
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)  # Escreve o cabeçalho
    for _ in range(num_rows):
        writer.writerow(generate_random_row())

print(f"Dados gerados e salvos em '{output_file}'")
