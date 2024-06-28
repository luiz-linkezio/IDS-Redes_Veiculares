import pyshark
import csv
import re

def extrair_audio_data(aaf_text):
    start_index = aaf_text.find("Audio Data [truncated]:") + len("Audio Data [truncated]:")
    end_index = aaf_text.find("Sample Chunk 0")
    audio_data = aaf_text[start_index:end_index].strip().replace("\n", "").replace(" ", "")
    
    audio_data = limpar_ansi(audio_data)

    # Dividir o audio_data em segmentos de 4 caracteres
    audio_chunks = [int(audio_data[i:i+4], 16) for i in range(0, len(audio_data), 4)]
    audio_chunks = audio_chunks[:-1]

    return audio_chunks

def limpar_ansi(texto):
    return re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', texto)

# Substitua 'seu_arquivo.pcapng' pelo caminho do seu arquivo PCAPNG, só fazer com cada arquivo
captura = pyshark.FileCapture('Ethernet\data\Ataques\Transmit Timestamp Jitter 2024_6_26-18h_53m_22s\TSNBox_192.168.41.151_4455.pcapng')

# Lista para armazenar os dados dos pacotes
pacote_dados = []

# Itera sobre os pacotes e extrai as informações relevantes
c = 0
timestamp_anterior = None

for pacote in captura:
    if hasattr(pacote, 'aaf'):
        c += 1
        print(f"{c}º pacote")
        audio_chunks = extrair_audio_data(str(pacote.aaf))

        timestamp_atual = pacote.sniff_time
        if timestamp_anterior is None:
            diferenca_tempo = 0
        else:
            diferenca_tempo = (timestamp_atual - timestamp_anterior).total_seconds()
        timestamp_anterior = timestamp_atual

        pacote_info = {
            'Rel Time': diferenca_tempo,
            'Length': pacote.length,
        }

        for i, chunk in enumerate(audio_chunks):
            pacote_info[f'Data_{i+1}'] = chunk

        pacote_dados.append(pacote_info)

# Libera os recursos quando terminar
captura.close()

# Escreve os dados dos pacotes em um arquivo CSV
with open('pacotes.csv', mode='w', newline='') as file:
    # Criar os nomes das colunas dinamicamente
    fieldnames = ['Rel Time', 'Length'] + [f'Data_{i+1}' for i in range(53)]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(pacote_dados)

print("Dados dos pacotes foram salvos em 'pacotes.csv'.")