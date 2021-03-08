import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D22)
mcp = MCP.MCP3008(spi, cs)
channel = AnalogIn(mcp, MCP.P2)

v1 = channel.voltage
bar = (66.7*(v1-0.5))

switch = True
while (switch == True):
    print('Raw ADC Value: ', channel.value)
    print('ADC Voltage: ' + str(channel.voltage) + 'V')
    print('Pressure: ' + str(int(bar)) + 'bar')
    time.sleep(0.5)
    if switch == False:
        break
