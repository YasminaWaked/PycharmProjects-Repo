from flask import Flask, render_template, request
app = Flask(__name__)
import requests

API_KEY = 'REDACTED'
API_URL = ('https://api.openweathermap.org/data/2.5/weather?q={}&mode=json&units=metric&appid={}')

def query_api(city):
    print(API_URL.format(city, API_KEY))
    data = requests.get(API_URL.format(city, API_KEY)).json()
    return data

@app.route('/')
def index():
    resp = query_api('London')
    print(resp)
    city = resp['name']
    temp = resp['main']['temp']
    country = resp['sys']['country']
    weather = resp['weather'][0]['description']
    iconcode = resp['weather'][0]['icon']
    humidity = resp['main']['humidity']
    feels_like = resp['main']['feels_like']
    return render_template('index.html', city=city, temp=temp, country=country, weather=weather, iconcode=iconcode, humidity=humidity, feels_like=feels_like)

@app.route("/results", methods=['GET', 'POST'])
def result():
    input_city = request.form.get('city')
    resp = query_api(input_city)
    error = None
    if resp:
        if len(resp) <= 2:
            error = resp['message']
        else:
            temp = resp['main']['temp']
            city = resp['name']
            country = resp['sys']['country']
            weather = resp['weather'][0]['description']
            iconcode = resp['weather'][0]['icon']
            humidity = resp['main']['humidity']
            feels_like = resp['main']['feels_like']
            return render_template('index.html', city=city, temp=temp, country=country, weather=weather, iconcode=iconcode, humidity=humidity, feels_like=feels_like)
    return render_template('index.html', error=error)


if __name__ == '__main__':
    app.run(debug=True)
