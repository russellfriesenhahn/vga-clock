# Simple tests for an adder module
import cocotb
from cocotb.triggers import *
from cocotb.clock import Clock
import random
import numpy
import sys
from spi_cocotb_bus import SPI

SKIP_ALL = False

CLK_PERIOD_NS = 10
async def setup_dut(dut):
    await cocotb.start(Clock(dut.Clk, CLK_PERIOD_NS, units='ns').start())

@cocotb.test(skip = (SKIP_ALL))
async def vga_clock_test0(dut):
    """
    """
    await cocotb.start(Clock(dut.clk, CLK_PERIOD_NS, units='ns').start())
    await cocotb.start(Clock(dut.CSPI_sys_clk, 30, units='ns').start())
    spi = SPI(dut, "", dut.CSPI_sys_clk)
    dut.reset_n.value = 0
    await RisingEdge(dut.CSPI_sys_clk)
    await RisingEdge(dut.CSPI_sys_clk)
    await RisingEdge(dut.CSPI_sys_clk)
    dut.adj_sec.value = 0
    dut.adj_min.value = 0
    dut.adj_hrs.value = 0
    dut.reset_n.value = 1
    

    await spi.send_data(0x02,8)
    await spi.send_data(0x01,8)
    await spi.send_data(0x00,8)
    await RisingEdge(dut.CSPI_sys_clk)
    await RisingEdge(dut.CSPI_sys_clk)
    await RisingEdge(dut.CSPI_sys_clk)
    await spi.send_data(0x02,8)
    await spi.send_data(0x00,8)
    await spi.send_data(0x0E,8)

    await spi.send_data(0x02,8)
    await spi.send_data(0x00,8)
    await spi.send_data(0x08,8)

    await spi.send_data(0x02,8)
    await spi.send_data(0x05,8)
    await spi.send_data(0x34,8)

    await spi.send_data(0x02,8)
    await spi.send_data(0x06,8)
    await spi.send_data(0x12,8)

    await spi.send_data(0x02,8)
    await spi.send_data(0x07,8)
    await spi.send_data(0x08,8)

    await spi.send_data(0x02,8)
    await spi.send_data(0x00,8)
    await spi.send_data(0x01,8)
    #await spi.send_data(0xDE,8)
    await RisingEdge(dut.CSPI_sys_clk)
    await RisingEdge(dut.CSPI_sys_clk)
    await RisingEdge(dut.CSPI_sys_clk)
    print(hex(spi.data))
    #assert spi.data == 0xA5, "Readback data does not match"

    
