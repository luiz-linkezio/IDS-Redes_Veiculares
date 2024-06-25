import csv
import os


diretorio_script = os.path.dirname(__file__)



# Descompactando
if os.path.isfile(os.path.join(diretorio_script, "data/dados.zip")) == True:
    import zipfile
    with zipfile.ZipFile(os.path.join(diretorio_script, "data/dados.zip"), "r") as zip_ref:
        zip_ref.extractall(os.path.join(diretorio_script, "data/"))



for pasta in os.listdir(os.path.join(diretorio_script, "data")):

    if pasta == "dados.zip":
        continue

    print(f"Verificando a pasta: {pasta}")

    for file in os.listdir(os.path.join(diretorio_script, f"data/{pasta}")):

        lista_zipada = list()

        print(f"Tratando o arquivo: {file}")

        timestamp_list = list()
        id_list = list()
        dlc_list = list()
        relative_time_list = list()
        byte_0_list = list()
        byte_1_list = list()
        byte_2_list = list()
        byte_3_list = list()

        with open(os.path.join(diretorio_script, f"data/{pasta}/{file}"), mode='r', errors="ignore") as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv)
            primeira_vez = True
            timestamp_anterior = 0
            primeiro_timestamp = True

            for linha in leitor_csv:

                if len(linha) < 3 or primeira_vez == True:
                    primeira_vez = False
                    continue

                if primeiro_timestamp == True:
                    primeiro_timestamp = False
                    timestamp_list.append(float(0))
                else:
                    timestamp_list.append(float(linha[0]) - timestamp_anterior)

                timestamp_anterior = float(linha[0])

                id_list.append(linha[1])

                dlc = len(eval(linha[2]))
                dlc_list.append(dlc)

                if dlc >= 1:
                    byte_0_list.append(eval(linha[2])[0])
                else:
                    byte_0_list.append(-1)
                if dlc >= 2:
                    byte_1_list.append(eval(linha[2])[1])
                else:
                    byte_1_list.append(-1)
                if dlc >= 3:
                    byte_2_list.append(eval(linha[2])[2])
                else:
                    byte_2_list.append(-1)
                if dlc >= 4:
                    byte_3_list.append(eval(linha[2])[3])
                else:
                    byte_3_list.append(-1)

        lista_zipada.extend(list(zip(timestamp_list, dlc_list, id_list, byte_0_list, byte_1_list, byte_2_list, byte_3_list)))

        lista_zipada.insert(0, ["Timestamp", "DLC", "Arb ID", "Byte 0", "Byte 1", "Byte 2", "Byte 3"])

        with open(os.path.join(diretorio_script, f"data/{pasta}/{file}"), mode="w", newline="") as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv)
            for elemento in lista_zipada:
                escritor_csv.writerow(elemento)

        print(f"Arquivo {file} tratado com sucesso.")

print("Todos os arquivos foram tratados com sucesso.")