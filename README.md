# ckanext-ed

[![image](https://travis-ci.org/ViderumGlobal/ckanext-ed.svg?branch=master)](https://travis-ci.org/ViderumGlobal/ckanext-ed)

## Requirements

For example, you might want to mention here which versions of CKAN this
extension works with.

## Installation

To install ckanext-ed:

1.  Activate your CKAN virtual environment, for example:

```
. /usr/lib/ckan/default/bin/activate
```

2.  Install the ckanext-ed Python package into your virtual
    environment:

```
pip install ckanext-ed
```

3.  Add `ed` to the `ckan.plugins` setting in your CKAN config
    file (by default the config file is located at
    `/etc/ckan/default/production.ini`).

4.  Restart CKAN. For example if you've deployed CKAN with Apache on
    Ubuntu:

```
sudo service apache2 reload
```

# Config Settings

Document any optional config settings here. For example:

```
# The minimum number of hours to wait before re-checking a resource
# (optional, default: 24).
ckanext.ed.some_setting = some_default_value
```

## Development Installation

To install ckanext-ed for development, activate your CKAN
virtualenv and do:

```
git clone https://github.com/viderumglobal/ckanext-ed.git
cd ckanext-ed
python setup.py develop
pip install -r dev-requirements.txt
```

## Running the Tests

To run the tests, do:

```
nosetests --nologcapture --with-pylons=test.ini
```

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (`pip install coverage`) then
    run:

```
nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.ed --cover-inclusive --cover-erase --cover-tests
```

## Registering ckanext-ed on PyPI

ckanext-ed should be availabe on PyPI as
<https://pypi.python.org/pypi/ckanext-ed>. If that link doesn't
work, then you can register the project on PyPI for the first time by
following these steps:

1.  Create a source distribution of the project:

```
python setup.py sdist
```

2.  Register the project:

```
python setup.py register
```

3.  Upload the source distribution to PyPI:

```
python setup.py sdist upload
```

4.  Tag the first rel
