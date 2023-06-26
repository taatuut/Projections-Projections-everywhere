
import pandas as pd

ods_file = pd.read_excel(r'data/2022-08 Actuele kernnetpunten Rijksdriehoeksmeting.ods')
ods_file.to_csv (r'data/input.csv', index = None, header=True, sep=';')