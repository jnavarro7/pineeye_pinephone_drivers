import smbus
import time
import os
import curses
import sys

# from amg8833_registers import * #Registers can be stored in a different file and imported here.

# Sensor is in I2C channel 3
i2c_ch = 2

# AMG8233 address on the I2C bus
i2c_address = 0x68

# Register addresses
pixeltest = 0x80  # Register used for debug lines.

row1 = [0x80, 0x82, 0x84, 0x86, 0x88, 0x8A, 0x8C, 0x8E]
row2 = [0x90, 0x92, 0x94, 0x96, 0x98, 0x9A, 0x9C, 0x9E]
row3 = [0xA0, 0xA2, 0xA4, 0xA6, 0xA8, 0xAA, 0xAC, 0xAE]
row4 = [0xB0, 0xB2, 0xB4, 0xB6, 0xB8, 0xBA, 0xBC, 0xBE]
row5 = [0xC0, 0xC2, 0xC4, 0xC6, 0xC8, 0xCA, 0xCC, 0xCE]
row6 = [0xD0, 0xD2, 0xD4, 0xD6, 0xD8, 0xDA, 0xDC, 0xDE]
row7 = [0xA0, 0xE2, 0xE4, 0xE6, 0xE8, 0xEA, 0xEC, 0xEE]
row8 = [0xF0, 0xF2, 0xF4, 0xF6, 0xF8, 0xFA, 0xFC, 0xFE]

rows = [row1, row2, row3, row4, row5, row6, row7, row8]

print("Initializing the I2C Bus")
bus = smbus.SMBus(i2c_ch)
time.sleep(1)


def debug_test():
    val = bus.read_i2c_block_data(i2c_address, pixeltest, 1)
    print("Test Value:", val)
    val = bus.read_byte_data(i2c_address, pixeltest)
    print(val)


def readpixels():
    # Read the Pixel 1 register (1 bytes)
    for i in pixel:
        val = bus.read_i2c_block_data(i2c_address, i)
        print("Value:", val)
        time.sleep(0.001)


def color_select(tempround):
    if tempround <= 22.0:
        return "\x1b[6;37;44m"
    elif tempround > 22.0 and tempround <= 24.0:
        return "\x1b[6;37;42m"
    elif tempround > 24.0 and tempround <= 36.0:
        return "\x1b[6;30;43m"
    elif tempround >= 36.0:
        return "\x1b[6;37;41m"
    else:
        return "\x1b[6;37;40m"


def readrows():
    for i in rows:
        for j in i:
            val = bus.read_byte_data(i2c_address, j)  # Read pixels from AMG8833 sensor
            valstr = str(val)  # Convert "val" to string
            dec = int(valstr, 16)  # Convert Hexadecimal to decimal
            temp = dec * 0.25  # Convert to Celcius degress
            if temp >= 59:
                temp -= 29
            else:
                temp -= 10  # Adjust
            tempround = round(temp, 1)  # Round temperature to a single decimal point
            # 			tempround -= 5 			#Adjust
            # print(tempround,end = " ")
            strtempround = str(tempround)  # Convert tempround to string
            # print('\x1b[6;37;44m' + strtempround + '\x1b[0m',end = " ")
            color = ""
            color = color_select(
                tempround
            )  # Function to assign a color depending on the temperature
            print(color + strtempround + "\x1b[0m", end=" ")
            time.sleep(0.001)
        print()


os.system("clear")
while True:
    readrows()
    time.sleep(0.1)
    os.system("clear")
