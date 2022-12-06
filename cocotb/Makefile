TOPLEVEL_LANG ?= verilog

ifneq ($(TOPLEVEL_LANG),verilog)
all:
	@echo "Skipping; this example does not support VHDL at the top-level"
clean::

else

PWD=$(shell pwd)
TOPDIR=$(PWD)/..
PYTHONPATH := ./model:$(PYTHONPATH)

export PYTHONPATH

SIM ?= icarus

#not sure if only icarus include is by -I ...
ifeq ($(SIM),icarus)
COMPILE_ARGS+=-I$(TOPDIR)/rtl/ -I$(TOPDIR)/cocotb/
else
COMPILE_ARGS+=+incdir+$(TOPDIR)/hdl/
endif

#DUT
VERILOG_SOURCES = $(TOPDIR)/rtl/vga_clock.v $(TOPDIR)/rtl/spi1.v $(TOPDIR)/rtl/cmdProc.v
VERILOG_SOURCES += $(TOPDIR)/rtl/button_pulse.v $(TOPDIR)/rtl/VgaSyncGen.v
VERILOG_SOURCES += $(TOPDIR)/rtl/fontROM.v $(TOPDIR)/rtl/digit.v

#Test Bench
VERILOG_SOURCES += $(TOPDIR)/cocotb/vga_clock_cocotb.v

TOPLEVEL = vga_clock_cocotb 

#GPI_IMPL := vpi

export TOPLEVEL_LANG
#TOPLEVEL := stc0_core_cocotb 
MODULE=vga_clock_tests

PLUSARGS = '-lxt2'
include $(shell cocotb-config --makefiles)/Makefile.sim

endif

