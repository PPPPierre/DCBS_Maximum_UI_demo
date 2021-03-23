from SerialConnection import MyPort
from decimal import Decimal
from CRC16 import crc16Add
import Visualisation
from DataSave import save_data
import struct


class DataBase:
    def __init__(self):

        # serial connection
        self.port = MyPort(show_response=False)

        # Status
        self.b_DefautHard = -1
        self.b_DefautVbatt = -1
        self.b_SOH_EnCours = -1
        self.b_SOH_Fini = -1
        self.charge_End = -1
        self.err_list = []

        # Test Time
        self.testTime = -1
        self.liveTime = -1
        self.remainingTime = -1
        self.on_time = -1

        # Measurement
        self.voltage12 = -1
        self.voltage24 = -1
        self.current = -1
        self.capacity = -1
        self.t_data = []
        self.v_data = []
        self.i_data = []
        self.c_data = []

        # Charge Test
        self.I_seuil = -1
        self.time_seuil = -1
        self.targetVoltage = -1
        self.maxCurrent = -1
        self.endCurrent = -1

        # CCA Test

        self.Rinterne = -1

        # Load Test
        self.CCA_onCours = -1
        self.CCA = -1
        self.Load_second = -1

        # Load Test
        self.RC_current = 50
        self.RC_second = -1

    # Port check ######################################################################################################
    def is_port_on(self):
        port = self.port.get_port()
        if port:
            return 1
        else:
            return 0

    # Status check ####################################################################################################
    def check_status(self):
        print("checking status...")
        result = self.port.commute_read("ff03d1000002e8e9")
        is_OK = 1
        if result != "":
            self.b_DefautHard = int(result[6:8], 16) % 2
            self.b_DefautVbatt = int(result[6:8], 16) // 16 % 2
            self.b_SOH_EnCours = (int(result[10:12], 16)) % 2
            self.b_SOH_Fini = (int(result[10:12], 16) // 2) % 2
            if self.b_DefautHard == 1:
                print('Hard Error: lack of hardware!')
                self.err_list.append('Hard Error: lack of hardware!')
                self.hard_err()
                self.pwr_err()
                is_OK = 0
            if self.b_DefautVbatt == 1:
                print("Battery Error: please check the connection of the battery!")
                self.err_list.append("Battery connection error!")
                is_OK = 0
            if is_OK == 1:
                return True
        return False

    def is_defaut_hard(self):
        if self.b_DefautHard:
            return True
        return False

    def is_batt_connected(self):
        if not self.b_DefautVbatt:
            return True
        return False

    def hard_err(self):
        print("checking hard errors...")
        result_hard = self.port.commute_read("ff03d1010002b929")

    def pwr_err(self):
        print("checking power errors...")
        result_power = self.port.commute_read("ff03d10200010928")

    def init_settings(self):
        print("Initial application...")
        setting_list = [
            ['Options',
             'ff10d02000050a01000001010001000000913c',
             'ff10d02000052cde'],
            ['Dish scale',
             'FF 10 D0 21 00 08 10 00 00 00 00 83 C0 CA 3D 00 00 00 00 00 00 00 00 74 7E',
             'FF 10 D0 21 00 08 BC DB'],
            ['Test settings',
             'ff10d02400172e0a000000cdcccc3d000070410000c842cdcccc3d01010000000000004842000020420000a042f401237500000000e04e',
             'ff10d0240017ed12'],
            ['Hard reset',
             'FF 10 D0 2A 00 01 02 00 00 38 33',
             'FF 10 D0 2A 00 01 0D 1F'],
            ['Setting reset',
             'FF 10 D0 2A 00 01 02 01 00 39 A3',
             'FF 10 D0 2A 00 01 0D 1F'],
            ['Para reset',
             'FF 10 D0 2A 00 01 02 02 00 39 53',
             'FF 10 D0 2A 00 01 0D 1F']
        ]

        for name, command, response in setting_list:
            command = command.replace(' ', '').lower()
            result = self.port.commute(command)
            if result == response.replace(' ', '').lower():
                print(name + " setting finished!")
            else:
                is_OK = 0
                print(name + " setting fail!")
                print("Application initialing fail!")
                return False
        print("Application initialing success!")
        return True

    # Measurement #####################################################################################################
    def init_measure_data(self):
        print("Initial data of the measurement ...")
        self.voltage12 = 0
        self.voltage24 = 0
        self.current = 0
        self.capacity = 0
        self.t_data = []
        self.v_data = []
        self.i_data = []
        self.c_data = []
        self.liveTime = 0
        self.remainingTime = self.testTime
        self.on_time = 0

    def refresh_data(self, i_on=False, c_on=False):
        self.measure(i_on, c_on)
        self.liveTime = self.liveTime + 0.5
        self.remainingTime = self.remainingTime - 0.5
        if self.is_test_on_time():
            self.on_time = 1

    def measure(self, i_on=False, c_on=False):
        result = self.port.commute_read("ff03d105001078e5")
        if result:
            v12_hex = result[14: 22]
            v24_hex = result[22: 30]
            c_hex = result[30: 38]
            self.voltage12 = self.hex_to_float(v12_hex)
            self.voltage24 = self.hex_to_float(v24_hex)
            self.v_data.append(self.voltage12)
            if i_on:
                self.current = self.hex_to_float(c_hex)
                self.i_data.append(self.current)
            if c_on:
                self.capacity = Decimal(self.liveTime * 50 / 3600).quantize(Decimal('0.000'))
                self.c_data.append(self.capacity)
            self.t_data.append(self.liveTime)
            print("Measuring battery status: Voltage %.3f Current %.3f" % (self.voltage12, self.current))
            return True
        return False

    def battery_check(self):
        print("Checking battery polarity...")
        # Battery Polarity Check
        self.measure()
        if self.voltage12 < 1:
            print("Warning: Battery connection problem!")
            return False
        return True

    def is_test_on_time(self):
        return self.remainingTime <= 0

    # Charge Test #####################################################################################################
    def get_settings_from_charge_panel(self, voltage, maxCurrent, time_min, endCurrent):
        print("getting settings of the charge test ...")
        self.targetVoltage = voltage
        self.maxCurrent = maxCurrent
        self.testTime = time_min*60
        self.endCurrent = endCurrent

    def set_charge_settings(self):
        hex_Voltage = self.float_to_hex(self.targetVoltage)
        hex_maxCurrent = self.float_to_hex(self.maxCurrent)
        hex_endCurrent = self.float_to_hex(self.endCurrent)
        chargingTime = self.testTime
        hex_chargingTime = self.dec_to_long(chargingTime)
        self.I_seuil = 0
        self.time_seuil = 0
        if self.endCurrent != 0:
            self.I_seuil = 1
        if chargingTime != 0:
            self.time_seuil = 1
        flag1 = self.set_voltage_current(hex_Voltage, hex_maxCurrent)
        flag2 = self.set_seuils("0"+str(self.I_seuil), "0"+str(self.time_seuil), hex_endCurrent, hex_chargingTime)
        return flag1 & flag2

    def set_seuils(self, seuil_I="00", seuil_T="00", hex_endCurrent="00000000", hex_chargingTime="00000000"):
        command = crc16Add("ff10d030000a14" +
                           seuil_I + seuil_T + "0a00" +
                           hex_endCurrent + hex_chargingTime +
                           "0000000000000000")
        result = self.port.commute(command)
        # print(command)
        if result == "ff10d030000a6d1f":
            print("Setting limitations success!")
            return True
        else:
            print("Setting limitations fail!")
            return False

    def set_voltage_current(self, hex_V, hex_C):
        command = crc16Add("ff10d02f00050a0000" + hex_V + hex_C)
        result = self.port.commute(command)
        print(command)
        if result == "ff10d02f00051cdd":
            print("Setting voltage/current success!")
            return True
        else:
            print("Setting voltage/current fail!")
            return False

    def charge_start(self):
        print("Starting charge test...")
        if self.battery_check():
            self.init_measure_data()
            result = self.port.commute("ff10d10600010201002ecf")
            if result == "ff10d1060001cd2a":
                self.charge_End = 0
                print("Charge start!")
                return True
            else:
                print("Warning: Charge start fail!")
                return False

    def charge_stop(self):
        print("Stopping test...")
        result = self.port.commute("ff10d10600010200002f5f")
        if result == "ff10d1060001cd2a":
            print("Test stop!")
            return True
        else:
            print("Warning: Test stop fail!")
            return False

    def is_charge_finished(self):
        if self.I_seuil == 1:
            if (self.liveTime >= 10) & (self.current <= self.endCurrent):
                print("Current is below the limit.")
                return True
        return False

    # CCA test ########################################################################################################
    def init_CCA_test(self):
        print("initializing CCA test...")
        self.b_SOH_EnCours = -1
        self.b_SOH_Fini = -1
        self.Rinterne = -1
        result = self.port.commute("FF10D10D00010200002E24")
        if result == "ff10d10d0001bce8":
            print("CCA test init!")
            return True
        print("Warning: CCA test init fail!")
        return False

    def is_on_CCA(self):
        if self.b_SOH_EnCours == 1:
            return True
        else:
            return False

    def activate_CCA_test(self):
        print("activating CCA test...")
        result = self.port.commute("FF10D10C00010200002FF5")
        if result == "ff10d10c0001ed28":
            print("CCA test start!")
            return True
        print("Warning: CCA test start fail!")
        return False

    def start_CCA_test(self):
        if self.init_CCA_test():
            if self.activate_CCA_test():
                return True

    def get_CCA_result(self):
        result = self.port.commute_read("ff03d10e00040928")
        if result:
            self.b_SOH_EnCours = int(result[6:8], 16) % 2
            self.b_SOH_Fini = int(result[6:8], 16) // 2 % 2
            self.Rinterne = self.hex_to_float(result[14:22])
            if self.b_SOH_EnCours == 1:
                return 2
            if self.b_SOH_Fini == 1:
                return 1
            else:
                return 0
        return -1

    # Load test #######################################################################################################
    def load_test_status_check(self):
        command = 'ff03d108000928ec'
        result = self.port.commute(command)
        if result:
            status = int(result[6:8], 16) % 2
            if status:
                self.CCA_onCours = 1
            else:
                self.CCA_onCours = 0
            return True
        return False

    def get_settings_from_load_test_panel(self, CCA, second):
        self.CCA = CCA
        self.testTime = second
        self.Load_second = second

    def set_load_test_settings(self):
        CCA = self.CCA
        second = self.testTime
        hex_CCA = self.dec_to_word(CCA)
        hex_second = self.dec_to_word(second)
        # print(hex_CCA, hex_second)
        command = crc16Add("ff10d036000204" + hex_CCA + hex_second)
        result = self.port.commute(command)
        # print(command)
        if result == "ff10d03600028cd8":
            print("Setting success!")
            return True
        else:
            print("Setting fail!")
            return False

    def load_test_start(self):
        if self.battery_check():
            self.init_measure_data()
            if self.init_load_test():
                if self.activate_load_test():
                    return True

    def load_test_stop(self):
        print("Stopping test...")
        self.load_test_status_check()
        if self.CCA_onCours:
            result = self.port.commute("ff10d03600020400000000dabf")
            if result == "ff10d03600028cd8":
                print("Test stop!")
                return True
            else:
                print("Warning: Test stop fail!")
                return False

    def init_load_test(self):
        print("initializing Load test...")
        result = self.port.commute("ff10d10a00010200002f93")
        if result == "ff10d10a00010d29":
            print("Load test init!")
            return True
        print("Warning: Load test init fail!")
        return False

    def activate_load_test(self):
        print("activating Load test...")
        result = self.port.commute("ff10d10900010200002fa0")
        if result == "ff10d1090001fd29":
            print("Load test start!")
            return True
        print("Warning: Load test start fail!")
        return False

    # RC test #######################################################################################################
    def get_settings_from_RC_test_panel(self, second):
        self.testTime = second
        self.RC_second = second

    def set_RC_test_settings(self):
        current = self.RC_current
        second = self.testTime
        hex_current = self.dec_to_word(current)
        hex_second = self.dec_to_word(second)
        command = crc16Add("ff10d036000204" + hex_current + hex_second)
        result = self.port.commute(command)
        if result == "ff10d03600028cd8":
            print("Setting success!")
            return True
        else:
            print("Setting fail!")
            return False

    def RC_test_start(self):
        if self.battery_check():
            self.init_measure_data()
            if self.init_load_test():
                if self.activate_load_test():
                    return True

    def RC_test_stop(self):
        print("Stopping test...")
        result = self.port.commute("ff10d03600020400000000dabf")
        if result == "ff10d03600028cd8":
            print("Test stop!")
            return True
        else:
            print("Warning: Test stop fail!")
            return False

    def init_RC_test(self):
        print("initializing Load test...")
        result = self.port.commute("ff10d10a00010200002f93")
        if result == "ff10d10a00010d29":
            print("Load test init!")
            return True
        print("Warning: Load test init fail!")
        return False

    def activate_RC_test(self):
        print("activating Load test...")
        result = self.port.commute("ff10d10900010200002fa0")
        if result == "ff10d1090001fd29":
            print("Load test start!")
            return True
        print("Warning: Load test start fail!")
        return False

    # data transfer ###################################################################################################
    def hex_to_float(self, hex):
        hex_invert = ""
        for i in range(0, 4):
            hex_invert += hex[6-2*i:8-2*i]
        result_raw = struct.unpack('>f', bytes.fromhex(hex_invert))[0]
        result = Decimal(result_raw).quantize(Decimal('0.000'))
        return result

    def float_to_hex(self, f):
        hex_raw = str(hex(struct.unpack('>I', struct.pack('<f', f))[0])).replace("0x", '')
        if len(hex_raw) < 8:
            for i in range(0, 8 - len(hex_raw)):
                hex_raw = "0" + hex_raw
        return hex_raw

    def dec_to_word(self, dec):
        hex_invert = str(hex(int(dec))).replace("0x", '')
        if len(hex_invert) < 4:
            for i in range(0, 4 - len(hex_invert)):
                hex_invert = "0" + hex_invert
        hex_result = hex_invert[2:4] + hex_invert[0:2]
        return hex_result

    def dec_to_long(self, dec):
        hex_invert = str(hex(int(dec))).replace("0x", '')
        if len(hex_invert) < 8:
            for i in range(0, 8 - len(hex_invert)):
                hex_invert = "0" + hex_invert
        hex_result = ""
        for i in range(0, 4):
            hex_result += hex_invert[6-2*i:8-2*i]
        return hex_result

    # Visualisation ###################################################################################################
    def plot_measurement(self, title, type, mode='show', path=''):
        data2 = None
        legend = ""
        label = ""
        if type == 'v':
            pass
        if type == 'v+i':
            data2 = self.i_data
            legend = "Current"
            label = "Current (A)"
        if type == 'v+c':
            data2 = self.c_data
            legend = "Capacity"
            label = "Capacity (A·h)"
        Visualisation.img_plot(title, self.t_data, self.v_data, data2, legend, label, mode, path)

    # Data Saving #####################################################################################################
    def save_data(self, type, test):
        path = '0'
        if type == 'v+i':
            path = save_data(self.t_data, self.v_data, self.i_data, test, 'Current (A)')
        elif type == 'v+c':
            path = save_data(self.t_data, self.v_data, self.c_data, test, 'Capacity (A.h)')
        elif type == 'v':
            path = save_data(self.t_data, self.v_data, data2=None, test_name=test)
        return path


if __name__ == '__main__':
    data = DataBase()
    # data.measure()
    # data.status_check()
    # data.set_charge_settings()
