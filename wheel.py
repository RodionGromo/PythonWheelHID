import struct
import time
from adafruit_hid import find_device

def mapvalues(inp,input_max,input_min,out_min,out_max):
	return (x - input_min) * (out_max - out_min) // (input_max - input_min) + out_min

class gameWheel:
    #Emulating 8 buttons and 4 analog inputs
    def __init__(self,devices):
        #Find our wheel on hid's
        self._wheel = find_device(devices,usage_page=0x01,usage=0x05)
        #report[0] buttons 1-8
        #report[1] analog -127 to 127
        #report[2] analog -127 to 127
        #report[3] analog -127 to 127
        #report[4] analog -127 to 127
        self._report = bytearray(6)
        #save last report to not spam usb
        self._last_report = bytearray(6)
        #save stats before reporting
        self._buttons = 0
        self._analog1 = 0
        self._analog2 = 0
        self._analog3 = 0
        self._analog4 = 0

        #try to send initial report to see if HID device is ready
        #if not wait and retry
        try:
            self.reset_all()
        except OSError:
            time.sleep(1)
            self.reset_all()

    def press_buttons(self,buttons):
        for button in buttons:
            self._buttons |= self.isValidButton(button)
        self._send()

    def release_buttons(self, buttons):
        for button in buttons:
            self._buttons &= ~self.isValidButton(button)
        self._send()

    def release_all(self):
        self._buttons = 0
        self._analog1 = 0
        self._analog2 = 0
        self._analog3 = 0
        self._analog4 = 0
        self._send()

    def move_analogs(self,a1=None,a2=None,a3=None,a4=None):
        if a1 is not None:
            self._analog1 = self.isValidAnalog(a1)
        if a2 is not None:
            self._analog2 = self.isValidAnalog(a2)
        if a3 is not None:
            self._analog3 = self.isValidAnalog(a3)
        if a4 is not None:
            self._analog4 = self.isValidAnalog(a4)
        self._send()

    def reset_all(self):
        self._buttons = 0
        self._analog1 = 0
        self._analog2 = 0
        self._analog3 = 0
        self._analog4 = 0
        self._send(always=True)

    def _send(self,always=False):
        struct.pack_into("<bbbbb",self._report,0,self._buttons,self._analog1,self._analog2,self._analog3,self._analog4)
        
        if always or self._last_report != self._report:
            self._wheel.send_report(self._report)
            self._last_report[:] = self._report

    @staticmethod
    def isValidButton(button):
        if button in range(0,8):
            return 2 ** button
        else:
            raise ValueError("Invalid button")

    @staticmethod
    def isValidAnalog(analog):
        if analog in range(-127,128):
            return analog
        else:
            raise ValueError("Invalid analog value")
