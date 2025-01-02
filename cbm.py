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

# Function to update the plot on Streamlit
def update_plot():
    # Create the plot in Streamlit
    st.write("### Sensor Data")
    
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))
    
    # Plot Velocity data
    ax[0].plot(sensor_data['time'], sensor_data['velx'], label='Velocity X')
    ax[0].set_title('Velocity vs Time')
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Velocity (scaled)')
    ax[0].legend()

    # Uncomment and plot Acceleration data if available
    # ax[1].plot(sensor_data['time'], sensor_data['accx'], label='Acceleration X')
    # ax[1].set_title('Acceleration vs Time')
    # ax[1].set_xlabel('Time')
    # ax[1].set_ylabel('Acceleration (scaled)')
    # ax[1].legend()

    st.pyplot(fig)

    # After the plot is shown, close it to avoid too many open figures
    plt.close(fig)

# Initialize the MQTT client
client = paho.Client("123")  # Use a simple, unique client ID
client.tls_set(certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED)
client.username_pw_set("test", "12345")

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("3f4b987c21d74a5a87e6bdc7411d5651.s1.eu.hivemq.cloud", 8883)

# Start the MQTT loop in the background
client.loop_start()

# Streamlit app interface
st.title("Real-time Sensor Data Visualization")