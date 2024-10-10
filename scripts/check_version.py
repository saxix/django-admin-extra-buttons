# tired to have too many packaging errors
# small script to check the package is correctly installed
from pathlib import Path
from importlib.metadata import version

import toml
from admin_extra_buttons import VERSION

expected = toml.load((Path(__file__).parent.parent / 'pyproject.toml').open())['project']['version']
print("Expected version:", expected)
print("Metadata version:", version('django_admin_extra_buttons'))
print("Package version:", VERSION)
assert VERSION == expected
assert version('django_admin_extra_buttons') == expected
