import paho.mqtt.client as paho
import ssl
import streamlit as st
import matplotlib.pyplot as plt
from collections import deque
import numpy as np
import warnings

# Suppress the missing ScriptRunContext warning
warnings.filterwarnings("ignore", message="missing ScriptRunContext! This warning can be ignored when running in bare mode")

# Constants for scaling
scalev = 409.6  # Velocity scale factor
scaleg = 2367.13  # Acceleration scale factor

# Initialize global variables for storing data
sensor_data = {
    'time': deque(maxlen=100),  # To store time values (timestamps)
    'velx': deque(maxlen=100),  # To store velocity X values
}

# Callback function when connected to MQTT broker
def on_connect(client, userdata, flags, rc):
    print(f'Connected to MQTT broker with code {rc}')
    client.subscribe('#', qos=0)  # Subscribe to all topics

# Callback function when a message is received
def on_message(client, userdata, message):
    payload = message.payload
    buffer = bytearray(payload)

    # Extract sensor data (for demonstration, we assume specific byte positions)
    int_velx = buffer[5:7]

    # Convert bytes to integers and scale
    velxconvert_int = int.from_bytes(int_velx, byteorder='big', signed=False) / scalev

    # Add the received data to the global list (using time as a simple counter here)
    sensor_data['time'].append(len(sensor_data['time']) + 1)  # Simulating time as a counter
    sensor_data['velx'].append(velxconvert_int)

    # Update the Streamlit plot
    update_plot()

