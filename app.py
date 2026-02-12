import requests
from flask import Flask, render_template, request
from forms import RectangleForm
from forms import WeatherReport
app = Flask(__name__)
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'

@app.route('/')  # this runs home
def home():
    return render_template("index.html")
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/rectangle', methods=['GET', 'POST'])
def rectangle():
    form = RectangleForm() # creating a RectangleForm object
    area = None
    perimeter = None

    if form.validate_on_submit():
        length = form.length.data
        width = form.width.data

        if form.area.data: # if area submit field is clicked
            area = length * width
        elif form.perimeter.data:
            perimeter = 2 * (length + width)

    return render_template("rectangle.html",
                           form=form, area=area, perimeter=perimeter)


@app.route('/weather', methods=['GET', 'POST'])
def weather():
    form = WeatherReport()

    weather_data = None
    error = None

    if form.validate_on_submit():
        city = form.city.data.strip()

        # 1) City -> (lat, lon) using Nominatim
        geo_url = "https://nominatim.openstreetmap.org/search"
        geo_params = {"q": city, "format": "json", "limit": 1}
        geo_headers = {"User-Agent": "ASE-Flask-Student-Project (school use)"}

        geo_resp = requests.get(geo_url, params=geo_params, headers=geo_headers, timeout=10)
        geo_results = geo_resp.json()

        if not geo_results:
            error = "City not found. Please try another spelling."
            return render_template("weather.html", form=form, weather_data=weather_data, error=error)

        lat = float(geo_results[0]["lat"])
        lon = float(geo_results[0]["lon"])

        # 2) (lat, lon) -> current weather using Open-Meteo
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current_weather": True
        }

        w_resp = requests.get(weather_url, params=weather_params, timeout=10)
        w_json = w_resp.json()

        if "current_weather" not in w_json:
            error = "Weather data is unavailable right now. Try again later."
        else:
            cw = w_json["current_weather"]
            weather_data = {
                "city": city,
                "temperature": cw.get("temperature"),
                "windspeed": cw.get("windspeed"),
                "winddirection": cw.get("winddirection"),
                "time": cw.get("time")
            }

    return render_template("weather.html", form=form, weather_data=weather_data, error=error)



if __name__ == '__main__':
    app.run(debug=True, port=5001)