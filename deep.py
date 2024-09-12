import requests

api_key = '841257ff-931d-41c0-89c1-2deb59a12473'  # Tu clave de API
response = requests.post(
    'https://api.deepai.org/api/text-generator',
    data={'text': 'dame informacion de Peru'},
    headers={'api-key': api_key}
)

if response.status_code == 200:
    print(response.json())  # Imprime la respuesta JSON
else:
    print(f"Error: {response.status_code} - {response.text}")
