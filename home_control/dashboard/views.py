import requests
from django.shortcuts import render, redirect
from datetime import datetime, time

BASE_URL = "http://homeassistant.local:8123/api"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyYTQyYWFjZGNlYzg0MWRkYjUwZDFiY2I2ODYzNTIzMiIsImlhdCI6MTc1MTA5NTQwNSwiZXhwIjoyMDY2NDU1NDA1fQ.bM6Pnqb-jt1Ee1lMV7CyeiJHCkCUkNMZMcQ9muTTDE4"
DINNINGLIGHT_ENTITY_ID = "light.dining_lamp"
ROLLERCOASTER_SENSOR_ENTITY_ID = "sensor.rollercoaster_lights_power"
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
SPALIGHT_ENTITY_ID = "light.sibp601x_light"
SPA_PUMP1_ENTITY_ID = "fan.sibp601x_pump_1"
SPA_PUMP2_ENTITY_ID = "fan.sibp601x_pump_2"
HOME_SERVER_ENTITY_ID = "switch.pc191ha_3_socket_1"
HOME_SERVER_POWER_SENSOR_ID = "sensor.pc191ha_3_power"
ROLLER_COASTER_LIGHTS_ENTITY_ID = "switch.rollercoaster_lights_socket_1"
SOILSDCPOWER_PV1_ENTITY_ID = "sensor.solis_dc_power_pv1"
SOILSDCPOWER_PV2_ENTITY_ID = "sensor.solis_dc_power_pv2"
LOW_COST_START_ENTITY_ID = "input_datetime.low_cost_start"
LOW_COST_END_ENTITY_ID = "input_datetime.low_cost_end"
GARAGE_DOOR_ENTITY_ID = "switch.garage_door_socket"

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
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    data = {"entity_id": entity_id}
    requests.post(url, headers=headers, json=data)

def toggle_fan(entity_id):
    url = f"{BASE_URL}/services/fan/toggle"
    data = {"entity_id": entity_id}
    requests.post(url, headers=HEADERS, json=data)

def control_panel(request):
    if request.method == "POST":
        if "dining_lamp_on" in request.POST:
            turn_on(DINNINGLIGHT_ENTITY_ID)
        elif "dining_lamp_off" in request.POST:
            turn_off(DINNINGLIGHT_ENTITY_ID)
        elif "kitchen_bench_on" in request.POST:
            turn_on(KITCHEN_SOCKET_ENTITY_ID, domain="switch")
        elif "kitchen_bench_off" in request.POST:
            turn_off(KITCHEN_SOCKET_ENTITY_ID, domain="switch")
        elif "bedside_lamp_on" in request.POST:
            turn_on(BEDSIDELAMP_ENTITY_ID)
        elif "bedside_lamp_off" in request.POST:
            turn_off(BEDSIDELAMP_ENTITY_ID)
        elif "cupboard_lights_on" in request.POST:
            turn_on(CUPBOARDLIGHTS_ENTITY_ID)
        elif "cupboard_lights_off" in request.POST:
            turn_off(CUPBOARDLIGHTS_ENTITY_ID)
        elif "coffee_machine_on" in request.POST:
            turn_on(COFFEE_ENTITY_ID, domain="switch")
        elif "coffee_machine_off" in request.POST:
            turn_off(COFFEE_ENTITY_ID, domain="switch")
        elif"spa_light_on" in request.POST:
            turn_on(SPALIGHT_ENTITY_ID)
        elif "spa_light_off" in request.POST:
            turn_off(SPALIGHT_ENTITY_ID)
        elif "spa_pump_1_on" in request.POST:
            turn_on(SPA_PUMP1_ENTITY_ID, domain="fan")
        elif "spa_pump_1_off" in request.POST:
            turn_off(SPA_PUMP1_ENTITY_ID, domain="fan")
        elif "spa_pump_2_on" in request.POST:
            turn_on(SPA_PUMP2_ENTITY_ID, domain="fan")
        elif "spa_pump_2_off" in request.POST:
            turn_off(SPA_PUMP2_ENTITY_ID, domain="fan")
        elif "home_server_on" in request.POST:
            turn_on(HOME_SERVER_ENTITY_ID, domain="switch")
        elif "home_server_off" in request.POST:
            turn_off(HOME_SERVER_ENTITY_ID, domain="switch")
        elif "roller_coaster_lights_on" in request.POST:
            turn_on(ROLLER_COASTER_LIGHTS_ENTITY_ID, domain="switch")
        elif "roller_coaster_lights_off" in request.POST:
            turn_off(ROLLER_COASTER_LIGHTS_ENTITY_ID, domain="switch")
        elif "garage_door_on" in request.POST:
            turn_on(GARAGE_DOOR_ENTITY_ID, domain="switch")
        elif "garage_door_off" in request.POST:
            turn_off(GARAGE_DOOR_ENTITY_ID, domain="switch")
        return redirect("dashboard")

   
    roller_power = get_sensor_value(ROLLERCOASTER_SENSOR_ENTITY_ID)
    tesla_power = get_sensor_value(TESLA_SESSION_ENTITY_ID)
    tesla_energy = get_sensor_value(TESLA_ENERGY_ENTITY_ID)
    solar_today = get_sensor_value(SOLAR_TODAY_ENTITY_ID)
    soils_power_pv1 = get_sensor_value(SOILSDCPOWER_PV1_ENTITY_ID)
    soils_power_pv2 = get_sensor_value(SOILSDCPOWER_PV2_ENTITY_ID)
    coffee_energy = get_sensor_value(COFFEEMACHINE_ENERGY_ENTITY_ID)
    washing_status =  get_sensor_value(WASHING_MACHINE_ENTITY_ID)
    washing_machine_delay = get_sensor_value(WASHING_MACHINE_STATUS_ENTITY_ID)
    home_server_power = get_sensor_value(HOME_SERVER_POWER_SENSOR_ID)
    low_cost_start = get_sensor_value(LOW_COST_START_ENTITY_ID).split()[0]
    low_cost_end = get_sensor_value(LOW_COST_END_ENTITY_ID).split()[0]

    try:
     low_cost_start = low_cost_start_raw.split()[0] if ":" in low_cost_start_raw else None
     low_cost_end = low_cost_end_raw.split()[0] if ":" in low_cost_end_raw else None
    except Exception:
      low_cost_start = None
      low_cost_end = None

    devices = {
    "dining_lamp": {
        "state": get_sensor_value(DINNINGLIGHT_ENTITY_ID).split()[0],
        "watts": 12
    },
    "bedside_lamp": {
        "state": get_sensor_value(BEDSIDELAMP_ENTITY_ID).split()[0],
        "watts": 12
    },
    "cupboard_lights": {
        "state": get_sensor_value(CUPBOARDLIGHTS_ENTITY_ID).split()[0],
        "watts": 10
    },
    "kitchen_bench": {
        "state": get_sensor_value(KITCHEN_SOCKET_ENTITY_ID).split()[0],
        "watts": 5
    }
}


    for dev in devices.values():
       if dev["state"] != "on":
        dev["watts"] = 0
    
    
    context = {
        "roller_power": roller_power,
        "tesla_power": tesla_power,
        "tesla_energy": tesla_energy,
        "solar_today": solar_today,
        "soils_power_pv1": soils_power_pv1,
        "soils_power_pv2": soils_power_pv2,
        "coffee_energy": coffee_energy,
        "washing_status": washing_status,
        "washing_machine_delay": washing_machine_delay,
        "home_server_power": home_server_power,
        "devices": devices, 
        "low_cost_start": low_cost_start,
        "low_cost_end": low_cost_end,
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

def set_low_cost_time(request):
    if request.method == "POST":
        start_time = request.POST.get("low_cost_start")
        end_time = request.POST.get("low_cost_end")
        if start_time and end_time:
            # Call Home Assistant API to set both times
            requests.post(
                f"{BASE_URL}/services/input_datetime/set_datetime",
                headers=HEADERS,
                json={"entity_id": LOW_COST_START_ENTITY_ID, "time": start_time}
            )
            requests.post(
                f"{BASE_URL}/services/input_datetime/set_datetime",
                headers=HEADERS,
                json={"entity_id": LOW_COST_END_ENTITY_ID, "time": end_time}
            )
    return redirect("dashboard")

def turn_on(entity_id, domain="light"):
    url = f"{BASE_URL}/services/{domain}/turn_on"
    data = {"entity_id": entity_id}
    requests.post(url, headers=HEADERS, json=data)

def turn_off(entity_id, domain="light"):
    url = f"{BASE_URL}/services/{domain}/turn_off"
    data = {"entity_id": entity_id}
    requests.post(url, headers=HEADERS, json=data)

