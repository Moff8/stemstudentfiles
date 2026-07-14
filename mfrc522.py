'''
Prerequisites
Enable I2C on Raspberry Pi via raspi-config > Interface Options > I2C
Install dependent tools:
sudo apt update && sudo apt install python3-smbus i2c-tools

Verify the connection: run i2cdetect -y 1, you should see the device address 0x28 (default address of WS1850S) in the output.
Example 1: Python (smbus2 + MFRC522 I2C implementation)
Install smbus2:
pip3 install smbus2

Example code for reading card UID
'''


import smbus2
import time

# WS1850S default I2C address
WS1850S_ADDR = 0x28
# MFRC522 register definitions
REG_COMMAND = 0x01
REG_COM_IRQ = 0x04
REG_FIFO_DATA = 0x09
REG_FIFO_LEVEL = 0x0A
REG_BIT_FRAMING = 0x0D
REG_MODE = 0x11
REG_TX_CONTROL = 0x14
REG_TX_ASK = 0x15
REG_CRC_RESULT_H = 0x21
REG_CRC_RESULT_L = 0x22

class WS1850S:
    def __init__(self, bus=1):
        self.bus = smbus2.SMBus(bus)
        self.addr = WS1850S_ADDR
        self._init_chip()

    def _write_reg(self, reg, value):
        self.bus.write_byte_data(self.addr, reg, value)

    def _read_reg(self, reg):
        return self.bus.read_byte_data(self.addr, reg)

    def _set_bitmask(self, reg, mask):
        tmp = self._read_reg(reg)
        self._write_reg(reg, tmp | mask)

    def _clear_bitmask(self, reg, mask):
        tmp = self._read_reg(reg)
        self._write_reg(reg, tmp & (~mask))

    def _init_chip(self):
        self._write_reg(REG_COMMAND, 0x0F)  # Soft reset
        time.sleep(0.1)
        self._write_reg(REG_MODE, 0x3D)
        self._write_reg(0x2A, 0x8F)
        self._write_reg(0x2B, 0x3F)
        self._write_reg(0x2D, 0x1E)
        self._write_reg(REG_TX_ASK, 0x40)
        self.antenna_on()

    def antenna_on(self):
        if not (self._read_reg(REG_TX_CONTROL) & 0x03):
            self._set_bitmask(REG_TX_CONTROL, 0x03)

    def _send_command(self, cmd, data):
        self._write_reg(REG_COMMAND, 0x00)  # Idle
        self._write_reg(REG_COM_IRQ, 0x7F)  # Clear interrupts
        self._write_reg(REG_FIFO_LEVEL, 0x80)  # Flush FIFO
        for byte in data:
            self._write_reg(REG_FIFO_DATA, byte)
        self._write_reg(REG_COMMAND, cmd)
        if cmd == 0x0C:  # Transceive command
            self._set_bitmask(REG_BIT_FRAMING, 0x80)
        timeout = 1000
        while True:
            irq = self._read_reg(REG_COM_IRQ)
            if irq & 0x01:
                return None
            if irq & 0x20 or timeout <= 0:
                break
            timeout -= 1
            time.sleep(0.001)
        self._clear_bitmask(REG_BIT_FRAMING, 0x80)
        if timeout <= 0:
            return None
        count = self._read_reg(REG_FIFO_LEVEL)
        return [self._read_reg(REG_FIFO_DATA) for _ in range(count)]

    def is_new_card_present(self):
        self._write_reg(REG_BIT_FRAMING, 0x07)
        res = self._send_command(0x0C, [0x26])
        return res is not None and len(res) >= 2

    def read_card_uid(self):
        self._write_reg(REG_BIT_FRAMING, 0x00)
        res = self._send_command(0x0C, [0x93, 0x20])
        if res is None or len(res) < 5:
            return None
        return res[:4]

if __name__ == "__main__":
    rfid = WS1850S()
    print("WS1850S initialized, waiting for card...")
    while True:
        if rfid.is_new_card_present():
            uid = rfid.read_card_uid()
            if uid:
                print(f"Card UID: {' '.join([f'{b:02X}' for b in uid])}")
            time.sleep(0.5)
        time.sleep(0.1)
