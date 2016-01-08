# vim: noexpandtab:syntax=make
CWD	=$(shell pwd)
PYTHON =python3
PYTHON2=python2
PYTHON3=python3
PYTHON2_LIB_DIR ="/usr/lib/python2.7/dist-packages"
PYTHON3_LIB_DIR ="/usr/lib/python3/dist-packages"
PYTHON2_MODULE_NAME=libsousou
PYTHON3_MODULE_NAME=libsousou


clean:
	find . | grep -E "(__pycache__|\.pyc$\)" | xargs rm -rf
	rm -rf dist build
	rm -rf *.egg-info
	rm -rf ../*.orig.tar.gz
	rm -rf *.egg-info


install-development-deps:
	pip3 install coverage nose pylint sphinx sphinxcontrib-napoleon==0.2.11\
		sphinx_rtd_theme==0.1.6 nose-cov

links:
	make purge
	ln -s $(CWD)/$(PYTHON2_MODULE_NAME) $(PYTHON2_LIB_DIR)/$(PYTHON2_MODULE_NAME)
	ln -s $(CWD)/$(PYTHON3_MODULE_NAME) $(PYTHON3_LIB_DIR)/$(PYTHON3_MODULE_NAME)


purge:
	rm -rf $(PYTHON2_LIB_DIR)/$(PYTHON2_MODULE_NAME)
	rm -rf $(PYTHON3_LIB_DIR)/$(PYTHON3_MODULE_NAME)
