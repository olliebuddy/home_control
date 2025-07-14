import requests
from django.shortcuts import render, redirect

BASE_URL = "http://homeassistant.local:8123/api"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyYTQyYWFjZGNlYzg0MWRkYjUwZDFiY2I2ODYzNTIzMiIsImlhdCI6MTc1MTA5NTQwNSwiZXhwIjoyMDY2NDU1NDA1fQ.bM6Pnqb-jt1Ee1lMV7CyeiJHCkCUkNMZMcQ9muTTDE4"
LIGHT_ENTITY_ID = "light.dining_lamp"
ROLLERCOASTER_ENTITY_ID = "rollercoaster_lights_power"
TESLA_ENTITY_ID = "sensor.tesla_wall_connector_session_energy"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

def toggle_light():
    url = f"{BASE_URL}/services/light/toggle"
    data = {"entity_id": LIGHT_ENTITY_ID}
    requests.post(url, headers=HEADERS, json=data)

def get_sensor_value(entity_id):
    url = f"{BASE_URL}/states/{entity_id}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        value = data.get("state")
        unit = data.get("attributes", {}).get("unit_of_measurement", "")
        return f"{value} {unit}"
    return "Unavailable"

def control_panel(request):
    if request.method == "POST":
        toggle_light()
        return redirect("dashboard")
    
    roller_power = get_sensor_value(ROLLERCOASTER_ENTITY_ID)
    tesla_power = get_sensor_value(TESLA_ENTITY_ID)

    context = {
        "roller_power": roller_power,
        "tesla_power": tesla_power
    }

    return render(request, "dashboard/control.html", context)

