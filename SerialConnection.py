#! /usr/bin/env python
import serial
import time


class MyPort:
    def __init__(self, portName="/dev/ttyACM0", baudRate=57600, parity='N', show_response=False):
        self.ComPort = portName
        self.BaudRate = baudRate
        self.Parity = parity
        self.show = show_response
        try:
            self.serial = serial.Serial(port=self.ComPort,
                                        baudrate=self.BaudRate,
                                        bytesize=8,
                                        parity=self.Parity,
                                        stopbits=1,
                                        timeout=5)
        except Exception:
            self.serial = None
        else:
            print("Port:", self.serial)
            if self.serial.isOpen():
                print("Open success")
            else:
                print("Open failed")

    def get_port(self):
        return self.serial

    def commute(self, input=""):
        if self.show:
            print("Send: " + input)
        time.sleep(0.01)
        for i in range(0, 11):
            myinput = bytes.fromhex(input)
            try:
                self.serial.write(myinput)
            except OSError:
                return ''
            else:
                time.sleep(0.01)
                count = self.serial.inWaiting()
                if self.show:
                    print("Receive", count, "Words")
                if count > 0:
                    myoutput = self.serial.read(count)
                    if self.show:
                        print("Response:", myoutput.hex())
                    return myoutput.hex()
        print("Warning: Cannot receive any response!")
        return ''

    def commute_read(self, input=""):
        result = self.commute(input)
        if (result[0:5] == "ff03") | (len(result) == 10 + 4*int(input[8:12], 16)):
            return result
        print("Warning: Reading error!")
        return ""

    def commute_write(self):
        pass


if __name__ == '__main__':
    port = MyPort()
    a = port.commute_read("ff03d105001078e5")
    print("a:", a)
'''
    t1 = threading.Thread(target=receive, name="Receive")
    t2 = threading.Thread(target=send, name="Send")
    t2.start()
    t1.start()
'''
