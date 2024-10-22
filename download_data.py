import requests

csv_url = 'https://docs.google.com/spreadsheets/d/16bEpYUm1Z2FpAjQOAQi8JEC3tRvOoAJZgV005v6RuEw/gviz/tq?tqx=out:csv'

# Realiza la solicitud GET para descargar el CSV
response = requests.get(csv_url)

# Verifica si la solicitud fue exitosa
if response.status_code == 200:
    # Guarda el contenido en un archivo CSV
    with open('intiuv_data.csv', 'wb') as f:
        f.write(response.content)
    print("Archivo CSV descargado exitosamente.")
else:
    print(f"Error al descargar el archivo: {response.status_code}")