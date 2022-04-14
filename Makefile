BUILDDIR=${PWD}/~build

.mkbuilddir:
	@mkdir -p ${BUILDDIR}

help:
	echo

demo:
	cd tests && ./manage.py migrate
	cd tests && ./manage.py runserver

develop:
	python3 -m venv .venv
	.venv/bin/pip install -U pip setuptools
	.venv/bin/pip install -e .[dev,test,docs]

clean:
	# cleaning
	@rm -fr dist '~build' .pytest_cache .coverage src/admin_extra_buttons.egg-info
	@find . -name __pycache__ -o -name .eggs | xargs rm -rf
	@find . -name "*.py?" -o -name ".DS_Store" -o -name "*.orig" -o -name "*.min.min.js" -o -name "*.min.min.css" -prune | xargs rm -rf

fullclean:
	@rm -rf .tox .cache
	$(MAKE) clean

lint:
	@flake8 src/
	@isort -c src/

release:
	tox
	rm -fr dist/
	./setup.py sdist
	twine upload dist/

coverage:
	tox -e d40-py39 -- --create-db --cov-report=xml --cov-report=term --junitxml=pytest.xml

docs: .mkbuilddir
	@sh docs/to_gif.sh docs/images
	@mkdir -p ${BUILDDIR}/docs
	mkdocs build


.PHONY: build docs


