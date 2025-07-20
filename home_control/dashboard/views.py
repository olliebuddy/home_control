import requests
from django.shortcuts import render, redirect

BASE_URL = "http://homeassistant.local:8123/api"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyYTQyYWFjZGNlYzg0MWRkYjUwZDFiY2I2ODYzNTIzMiIsImlhdCI6MTc1MTA5NTQwNSwiZXhwIjoyMDY2NDU1NDA1fQ.bM6Pnqb-jt1Ee1lMV7CyeiJHCkCUkNMZMcQ9muTTDE4"
DINNINGLIGHT_ENTITY_ID = "light.dining_lamp"
ROLLERCOASTER_ENTITY_ID = "sensor.rollercoaster_lights_power"
TESLA_SESSION_ENTITY_ID = "sensor.tesla_wall_connector_session_energy"
TESLA_ENERGY_ENTITY_ID = "sensor.tesla_wall_connector_energy"
BEDSIDELAMP_ENTITY_ID = "light.bedside_lamp"
CUPBOARDLIGHTS_ENTITY_ID = "light.cupboard_lights"
SOLAR_TODAY_ENTITY_ID = "sensor.solis_energy_today"
COFFEE_ENTITY_ID = "switch.pc191ha_4_socket_1"
COFFEEMACHINE_ENERGY_ENTITY_ID = "sensor.pc191ha_4_power"
WASHING_MACHINE_ENTITY_ID = "sensor.washer_current_status"
WASHING_MACHINE_STATUS_ENTITY_ID = "number.washer_delayed_end"
KITCHEN_SOCKET_ENTITY_ID = "switch.kitchen_bench_socket"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json",
}

def toggle_light():
    url = f"{BASE_URL}/services/light/toggle"
    data = {"entity_id": DINNINGLIGHT_ENTITY_ID}
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

def set_sensor_value(entity_id, value):
    url = f"{BASE_URL}/services/number/set_value"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "entity_id": entity_id,
        "value": value
    }
    response = requests.post(url, headers=headers, json=data)
    return response.ok

def toggle_specific_light(entity_id):
    url = f"{BASE_URL}/services/light/toggle"
    data = {"entity_id": entity_id}
    requests.post(url, headers=HEADERS, json=data)

def toggle_switch(entity_id):
    url = f"{BASE_URL}/services/switch/toggle"
    data = {"entity_id": entity_id}
    requests.post(url, headers=HEADERS, json=data)

def control_panel(request):
    if request.method == "POST":
        if "toggle_dining_lamp" in request.POST:
            toggle_light()
        elif "toggle_kitchen_bench" in request.POST:
            toggle_switch(KITCHEN_SOCKET_ENTITY_ID)
        elif "toggle_bedside_lamp" in request.POST:
            toggle_specific_light(BEDSIDELAMP_ENTITY_ID)
        elif "toggle_cupboard_lights" in request.POST:
            toggle_specific_light(CUPBOARDLIGHTS_ENTITY_ID)
        elif "toggle_coffee_machine" in request.POST:
            toggle_switch(COFFEE_ENTITY_ID)
        
        return redirect("dashboard")
    
    roller_power = get_sensor_value(ROLLERCOASTER_ENTITY_ID)
    tesla_power = get_sensor_value(TESLA_SESSION_ENTITY_ID)
    tesla_energy = get_sensor_value(TESLA_ENERGY_ENTITY_ID)
    solar_today = get_sensor_value(SOLAR_TODAY_ENTITY_ID)
    coffee_energy = get_sensor_value(COFFEEMACHINE_ENERGY_ENTITY_ID)
    washing_status =  get_sensor_value(WASHING_MACHINE_ENTITY_ID)
    washing_machine_delay = get_sensor_value(WASHING_MACHINE_STATUS_ENTITY_ID)
    
    context = {
        "roller_power": roller_power,
        "tesla_power": tesla_power,
        "tesla_energy": tesla_energy,
        "solar_today": solar_today,
        "coffee_energy": coffee_energy,
        "washing_status": washing_status,
        "washing_machine_delay": washing_machine_delay, 
    }

    return render(request, "dashboard/control.html", context)

def set_washing_machine_delay(request):
    if request.method == "POST":
        delay = request.POST.get("washing_delay")
        if delay:
            try:
                delay = int(delay)
                set_sensor_value(WASHING_MACHINE_STATUS_ENTITY_ID, delay)
            except ValueError:
                pass 
    return redirect("dashboard")