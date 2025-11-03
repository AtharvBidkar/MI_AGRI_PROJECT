from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

# Load datasets
crop_df = pd.read_csv('crop_master_organic.csv')
location_df = pd.read_csv('location_table_cleaned.csv')

# Your OpenWeatherMap API key
API_KEY = "e9d5e3b92ecf1f26b5f2742d202d1de6"

# Helper function to fetch weather
def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        temp = data['main']['temp']
        return round(temp, 1)
    except:
        return None

@app.route("/get_path", methods=["POST"])
def get_path():
    data = request.json
    state = data["state"]
    district = data["district"]
    city = data["city"]
    crop = data["crop"]

    temperature = get_weather(city)

    crop_info = crop_df[crop_df['crop'].str.lower() == crop.lower()]
    if crop_info.empty:
        return jsonify({"error": "Crop not found"}), 404

    crop_data = crop_info.iloc[0]

    result = {
        "✅ Crop": crop.title(),
        "📍 Location": f"{district}, {state}",
        "🌱 Sowing Season": crop_data['sowing_season'],
        "🌡️ Ideal Temperature": f"{crop_data['temp_min']}–{crop_data['temp_max']} °C",
        "📊 Current Temperature": f"{temperature} °C" if temperature else "Not available",
        "🧪 Soil Type": crop_data['soil'],
        "💧 Watering": crop_data['watering'],
        "🌿 Fertilizers": crop_data['fertilizers'],
        "🛡️ Pest Management": crop_data['pest_control'],
        "🕒 Harvest": crop_data['harvest_time'],
        "📈 Growth Stages": crop_data['growth_stages'],
        "🌡️ Note": "Current temperature doesn't match ideal range" if temperature and not (crop_data['temp_min'] <= temperature <= crop_data['temp_max']) else "Temperature is suitable"
    }

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
