# tired to have too many packaging errors
# small script to check the package is correctly installed
from pathlib import Path
from importlib.metadata import version

import toml
from admin_extra_buttons import VERSION

expected = toml.load(Path('pyproject.toml').open())['project']['version']
assert VERSION == expected
assert version('django_admin_extra_buttons') == expected
print(VERSION)
