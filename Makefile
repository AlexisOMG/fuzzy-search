.DEFAULT_GOAL = install

install:
	pip3 install wheel && \
	pip3 install setuptools && \
	pip3 install twine && \
	python3 setup.py bdist_wheel && \
	pip3 install dist/fuzzydeduplication-0.1.0-py3-none-any.whl

uninstall:
	pip3 uninstall -y dist/fuzzydeduplication-0.1.0-py3-none-any.whl && \
	rm -rf build/ dist/ fuzzydeduplication.egg-info/ 