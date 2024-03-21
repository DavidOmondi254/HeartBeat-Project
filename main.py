import smbus
import time
import matplotlib.pyplot as plt

# Initialize I2C bus and register addresses
bus = smbus.SMBus(1)
address = 0x57
register = 0x00

# Initialize variables
data = []
timestamps = []

# Set up plot
fig, ax = plt.subplots()
line, = ax.plot(timestamps, data)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Pulse (BPM)')

# Read and process data from pulse sensor
while True:
    try:
        # Read data from pulse sensor
        raw_data = bus.read_i2c_block_data(address, register)

        # Combine data bytes to form 16-bit integer value
        value = (raw_data[0] << 8) | raw_data[1]

        # Calculate pulse rate in BPM
        if value > 0:
            bpm = 60 / (value / 1000)

            # Add new data to arrays
            data.append(bpm)
            timestamps.append(time.time())

            # Update line data in plot
            line.set_xdata(timestamps)
            line.set_ydata(data)

            # Rescale axes and redraw plot
            ax.relim()
            ax.autoscale_view(True, True, True)
            fig.canvas.draw()
            fig.canvas.flush_events()

            # Print BPM value
            print(f"Pulse: {bpm} BPM")

    except KeyboardInterrupt:
        # Close I2C bus and exit program
        bus.close()
        plt.close()
        print("Program terminated by user.")
        break

