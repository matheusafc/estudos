from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def consultar_cambio(coin_origin, coin_destination):
    url = f"https://economia.awesomeapi.com.br/json/last/{coin_origin}-{coin_destination}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        rate_cambio = data.get(f"{coin_origin}{coin_destination}", {}).get("bid")
        if rate_cambio:
            return float(rate_cambio)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/converter', methods=['POST'])
def converter():
    value = request.form.get('value')
    if value:
        try:
            value = float(value)
        except ValueError:
            return "Valor inválido, por favor insira um número válido."
    else:
        return "Valor não fornecido."

    coin_origin = request.form.get('coin_origin', '').upper()
    coin_destination = request.form.get('coin_destination', '').upper()

    if not coin_origin or not coin_destination:
        return "Por favor, preencha todos os campos de moeda."

    taxa = consultar_cambio(coin_origin, coin_destination)
    
    if taxa is not None:
        conversion_value = value * taxa
        return render_template('resultado.html', conversion_value=conversion_value, coin_origin=coin_origin, coin_destination=coin_destination, taxa=taxa)
    else:
        return "Erro ao consultar a taxa de câmbio. Verifique as moedas e tente novamente mais tarde."

if __name__ == "__main__":
    app.run(debug=True)
