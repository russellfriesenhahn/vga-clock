py3/bin/activate:
	virtualenv --system-site-packages -p python3 py3

py3/bin/cocotb-config: py3/bin/activate
	. py3/bin/activate; \
	pip3 install numpy; \
	pip3 install cocotb; \
	pip3 install cocotb-bus; \
	pip3 install pytest; \
	deactivate

ENV_PRODUCTS=py3/bin/cocotb-config
env: $(ENV_PRODUCTS)

sim: design_init
	cd sim/cocotb_sim; make

clean:
	rm -rf modules/cocotb
	rm -rf py3
	cd sim/cocotb_sim; make clean
