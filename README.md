# IDS Redes Veiculares

Este repositóio foi criado com o objetivo de criar sistemas de detecção de intrusão (IDS) para redes veiculares, redes usando o protocolo CAN e redes usando o protocolo Ethernet, para estes IDSs serem testados em ambientes controlados e gerar resultados.

## Organização de Diretórios/Arquivos

O diretório:
 - `requirements` contém os requirimentos para rodar os códigos do projeto.
 - `CAN` contém todos os trabalhos realizados para rede CAN.
 - `Ethernet` contém todos os trabalhos realizados para rede Ethernet.
 - `CAN/data` ou `Ethernet/data` contém os dados coletados para o respectivo protocolo, que posteriormente foi usado para treinamento, validação e testes dos modelos de inteligência artificial.
 - `CAN/models` ou `Ethernet/models` contém os modelos treinados de inteligência artificial e seus respectivos scalers para o respectivo protocolo.
 - `CAN/Treinamento_do(s)_modelo(s)_de_IA.ipynb` ou `Ethernet/Treinamento_do(s)_modelo(s)_de_IA.ipynb` são arquivos júpiter com código em python responsável por treinar,validar e testar modelos de inteligência artificial para o respectivo protocolo.
 - `Ethernet/Tratamento_PCAPNG.py` é um arquivo python responsável por tratar os arquivos PCAPNG, basicamente faz uma limpeza e padronização dos dados.
 - `CAN/Gerador_de_mensagens_aleatorias.py` é um arquivo python responsável por gerar mensagens CAN aleatórias.
 - `CAN/Tratamento_CSV_Python_CAN.py` é um arquivo python responsável por tratar mensagens CAN de um arquivo CSV, basicamente faz uma limpeza e padronização dos dados.
 - `CAN/Scripts para o Barramento` é uma pasta que contém scripts para coletar(`Coletor_de_mensagens.py`) mensagens CAN, atacar(`Ataques.py`) um barramento CAN e fazer o deploy do IDS(`IDS.py`) em um barramento físico CAN reais(ainda que em ambiente controlado).
