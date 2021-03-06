# mono_test.py Demo program for nano_gui on an SSD1306 OLED display.

# The MIT License (MIT)
#
# Copyright (c) 2018 Peter Hinch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x32-spi-oled-display
# https://www.proto-pic.co.uk/monochrome-128x32-oled-graphic-display.html

# V0.31 9th Sep 2018

import utime
import uos
from ssd1306_setup import WIDTH, HEIGHT, setup
from writer import Writer, CWriter
from nanogui import Label, Meter, refresh

# Fonts
import courier20 as fixed
import font6 as small
import arial10


def fields(use_spi=False, soft=True):
    ssd = setup(use_spi, soft)  # Create a display instance
    Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = Writer(ssd, fixed, verbose=False)
    wri.set_clip(False, False, False)
    textfield = Label(wri, 0, 2, wri.stringlen('longer'))
    numfield = Label(wri, 25, 2, wri.stringlen('99.99'), bdcolor=None)
    countfield = Label(wri, 0, 90, wri.stringlen('1'))
    n = 1
    for s in ('short', 'longer', '1', ''):
        textfield.value(s)
        numfield.value('{:5.2f}'.format(int.from_bytes(uos.urandom(2),'little')/1000))
        countfield.value('{:1d}'.format(n))
        n += 1
        refresh(ssd)
        utime.sleep(2)
    textfield.value('Done', True)
    refresh(ssd)

def multi_fields(use_spi=False, soft=True):
    ssd = setup(use_spi, soft)  # Create a display instance
    Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = Writer(ssd, small, verbose=False)
    wri.set_clip(False, False, False)

    nfields = []
    dy = small.height() + 6
    y = 2
    col = 15
    width = wri.stringlen('99.99')
    for txt in ('X:', 'Y:', 'Z:'):
        Label(wri, y, 0, txt)
        nfields.append(Label(wri, y, col, width, bdcolor=None))  # Draw border
        y += dy

    for _ in range(10):
        for field in nfields:
            value = int.from_bytes(uos.urandom(3),'little')/167772
            field.value('{:5.2f}'.format(value))
        refresh(ssd)
        utime.sleep(1)
    Label(wri, 0, 64, ' DONE ', True)
    refresh(ssd)

def meter(use_spi=False, soft=True):
    ssd = setup(use_spi, soft)
    wri = Writer(ssd, arial10, verbose=False)
    ssd.fill(0)
    refresh(ssd)
    m0 = Meter(wri, 5, 2, height = 50, divisions = 4, legends=('0.0', '0.5', '1.0'))
    m1 = Meter(wri, 5, 44, height = 50, divisions = 4, legends=('-1', '0', '+1'))
    m2 = Meter(wri, 5, 86, height = 50, divisions = 4, legends=('-1', '0', '+1'))
    steps = 10
    for n in range(steps + 1):
        m0.value(int.from_bytes(uos.urandom(3),'little')/16777216)
        m1.value(n/steps)
        m2.value(1 - n/steps)
        refresh(ssd)
        utime.sleep(1)


tstr = '''Test assumes a 128*64 (w*h) display. Edit WIDTH and HEIGHT in ssd1306_setup.py for others.
Device pinouts are comments in ssd1306_setup.py.
All tests take two boolean args:
use_spi = False. Set True for SPI connected device
soft=True set False to use hardware I2C/SPI. Hardware I2C option currently fails with official SSD1306 driver.

Available tests:
fields() Label test with dynamic data.
multi_fields() More Labels.
meter() Demo of Meter object.
'''

print(tstr)
