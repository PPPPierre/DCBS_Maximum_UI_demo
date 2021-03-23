import binascii
import crcmod


# CRC16-MODBUS
def crc16Add(read):
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "")
    readcrcout = hex(crc16(binascii.unhexlify(data)))
    str_list = list(readcrcout)
    # print(str_list)
    if len(str_list) == 5:
        str_list.insert(2, '0')  # 位数不足补0
    crc_data = "".join(str_list)
    # print(crc_data)
    read = read.strip() + crc_data[4:] + crc_data[2:4]
    # print('CRC16:', crc_data[4:] + ' ' + crc_data[2:4])
    # print('Modbus_CRC16:>>>', read)
    return read


if __name__ == '__main__':
    crc16Add("ff10d02f00050a0000000060410000f041")
