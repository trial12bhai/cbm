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

