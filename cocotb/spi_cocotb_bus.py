"""Driver for Serially Peripheral Interface"""

import cocotb
from cocotb.triggers import RisingEdge, ReadOnly, Lock, FallingEdge, Timer
from cocotb_bus.drivers import BusDriver
from cocotb.result import ReturnValue
from cocotb.binary import BinaryValue
from cocotb.types import Logic

#import array
#import numpy

class SPIProtocolError(Exception):
    pass

class SPI(BusDriver):
    """Serially Peripheral Interface Bus Driver
    """
    
    _signals = ["SPI_clk",  # Output; SPI clock, active during transactions only
                "SPI_csb",  # Output; SPI chip-select bar
                "SPI_copi", # Output; SPI data controller-out-peripheral-in
                "SPI_cipo", # Input; SPI data controller-in-peripheral-out
                "SPI_CPOL", # Output; SPI configuration input defining clock polarity
                "SPI_CPHA" # Output; SPI configuration input defining active clock phase 
                ]

    def __init__(self, entity, name, clock, **kwargs):
        BusDriver.__init__(self, entity, name, clock, **kwargs)

        self.cpol = 0
        self.cpha = 0
        self.clock_ratio = 2
        self.data = Logic(0)
        # Drive some sensible defaults (setimmediatevalue to avoid x asserts)
        self.bus.SPI_csb.setimmediatevalue(1)
        #self.bus.SPI_CPOL.setimmediatevalue(self.cpol)
        #self.bus.SPI_CPHA.setimmediatevalue(self.cpha)
        self.bus.SPI_clk.setimmediatevalue(0)

    def toggle_spi_clk(self):
        if self.bus.SPI_clk.value == 1:
            self.bus.SPI_clk.value = 0
        else:
            self.bus.SPI_clk.value = 1
    async def set_cpol(self, cpol):
        self.cpol = cpol

        await RisingEdge(self.clock)
        self.bus.SPI_CPOL.value = self.cpol
        self.bus.SPI_clk.value = self.cpol

    async def set_cpha(self, cpha):
        self.cpha = cpha

        await RisingEdge(self.clock)
        self.bus.SPI_CPHA.value = self.cpha

    async def send_data(self, data, length):
        self.data = data
        for i in range(length):
            #print(hex(self.data))
            await RisingEdge(self.clock)
            if i == 0:
                self.bus.SPI_csb.value = 0
            else:
                self.toggle_spi_clk()
                if self.cpha == 1:
                    self.data = (self.data << 1) | self.bus.SPI_cipo.value

            if self.cpha == 0:
                self.bus.SPI_copi.value = (self.data >> (length -1)) & 0x1
                #print("Data: " + hex(self.data))
                #print("COPI: " + str(self.bus.SPI_copi.value))
                #print("MSB: " + hex(self.data >> (length -1)))
                self.data = (self.data << 1) & 0xFF

            await RisingEdge(self.clock)
            self.toggle_spi_clk()
            if self.cpha == 0:
                pass
                #self.data = (self.data << 1) | self.bus.SPI_cipo.value
                try:
                    self.data =  self.data | self.bus.SPI_cipo.value
                except:
                    pass
                else:
                    pass
            else:
                self.bus.SPI_copi.value = (data >> (length -1)) & 0x1

        await RisingEdge(self.clock)
        self.toggle_spi_clk()
        if self.cpha == 1:
            self.data = (self.data << 1) | self.bus.SPI_cipo.value
        await RisingEdge(self.clock)
        self.bus.SPI_csb.value = 1
