import serial.tools.list_ports
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation



def serial_ports():
    ports = list(serial.tools.list_ports.comports())
    for i, (port_no, description, address) in enumerate(ports):
        print(f"{i + 1}.device|---------------------------------------------------------")
        print(f"Port number: {port_no}\nDescription: {description}\nAddress: {address}")

    print()


def separator(incoming_data):

    if "essure" in incoming_data[0]:
        pressure.append(float(incoming_data[1]))
    elif "Temperature" in incoming_data[0]:
        temperature.append(float(incoming_data[1]))
    elif "altitude" in incoming_data[0]:
        altitude.append(float(incoming_data[1]))
    return pressure, temperature, altitude


def animate(i, dataList, serialPort):
    msg = str(serialPort.readline()).strip("b'  *CPam\\r\\n").split("=")
    print(msg)

    datalist_temp = separator(msg)[1][-50:]
    datalist_pressure = separator(msg)[0][-50:]
    datalist_alt = separator(msg)[2][-50:]

    ax_temp.clear()
    ax_temp.plot(datalist_temp)
    ax_temp.grid(True)
    ax_temp.set_ylim([-60, 120], auto=False)
    ax_temp.set_title("BMP_sensor_data")
    ax_temp.set_ylabel("Temp, °C")

    ax_pressure.clear()
    ax_pressure.grid(True)
    ax_pressure.plot(datalist_pressure)
    ax_pressure.set_ylim([97000, 98300])
    ax_pressure.set_ylabel("pressure, Pa")

    ax_alt.clear()
    ax_alt.grid(True)
    ax_alt.plot(datalist_alt)
    ax_alt.set_ylim(100, 500)
    ax_alt.set_ylabel("altitude, m")


pressure = []
temperature = []
altitude = []

datalist_temp = []
datalist_pressure = []
datalist_alt = []

serial_ports()

fig = plt.figure(figsize=(10, 8))
ax_temp = fig.add_subplot(311)
ax_pressure = fig.add_subplot(312)
ax_alt = fig.add_subplot(313)

serialPort = serial.Serial("COM4", 9600)
time.sleep(1)

# writer = matplotlib.animation.PillowWriter()

ani = animation.FuncAnimation(fig=fig,
                              func=animate,
                              frames=100,
                              fargs=((datalist_pressure, datalist_temp, datalist_alt), serialPort),
                              interval=100)

# ani.save("mymovie.gif", writer=writer)

plt.show()
serialPort.close()
