import serial
import time
import board
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import matplotlib.pyplot as plt

# set up the LCD display
lcd_columns = 16
lcd_rows = 2
i2c = board.I2C()
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# set up the serial connection to the Arduino
ser = serial.Serial('COM3', 9600)

# set up the graph
plt.ion()
fig, ax = plt.subplots()
xs = []
ys = []

# loop to read and display heart rate data
while True:
    # read the heart rate data from the Arduino
    data = ser.readline().decode().strip()
    
    try:
        # convert the heart rate data to an integer
        heart_rate = int(data)
        
        # display the heart rate on the LCD display
        lcd.clear()
        lcd.message = "Heart Rate:\n" + str(heart_rate)
        
        # update the graph with the new heart rate data
        xs.append(time.time())
        ys.append(heart_rate)
        ax.clear()
        ax.plot(xs, ys)
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Heart Rate (BPM)')
        plt.draw()
        plt.pause(0.01)
        
    except ValueError:
        # if the heart rate data couldn't be converted to an integer, ignore it
        pass