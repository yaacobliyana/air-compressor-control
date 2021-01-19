import board
import digitalio
import busio

print("Hello blinka!")

pin = digitalio.DigitalInOut(board.D4)
print("digital IO ok!")

i2c = busio.I2C(board.SCL, board.SDA)
print("i2c ok!")

spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
print("SPI ok!")

print("done!")
