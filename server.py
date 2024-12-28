from flask import Flask, render_template, request
from weather import get_current_weather
from waitress import serve
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    state = request.args.get('state', 'NA')
    country = request.args.get('country', 'US')
    unit = request.args.get('unit', 'imperial')  # Default to Fahrenheit if no unit is provided

    if not bool(city.strip()):
        city = "San Macos"  # Default city if input is empty

    try:
        weather_data = get_current_weather(city, unit, state, country)

        # Check if the response code is 200 (OK)
        if weather_data['cod'] != 200:
            return render_template('city-not-found.html', city=city, unit=unit, state=state, country=country)
        
        return render_template(
            'weather.html',
            title=weather_data["name"],
            status=weather_data["weather"][0]["description"].capitalize(),
            temp=f"{weather_data['main']['temp']:.1f}",
            feels_like=f"{weather_data['main']['feels_like']:.1f}",
            unit=unit,
            maxtemp = f"{weather_data['main']['temp_max']:.1f}",
            mintemp = f"{weather_data['main']['temp_min']:.1f}"
        )

    except requests.exceptions.RequestException as req_err:
        return render_template('error.html', message="Unable to connect to the weather service. Please check your internet connection.")
    except Exception as e:
        return render_template('error.html', message=f"An error occurred.")


if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['PORT'] = 8000
    serve(app, host="0.0.0.0", port=app.config['PORT'])
