# tired to have too many packaging errors
# small script to check the package is correctly installed
from importlib.metadata import version
from pathlib import Path

import toml

from admin_extra_buttons import VERSION

expected = toml.load((Path(__file__).parent.parent / "pyproject.toml").open())["project"]["version"]
assert expected == VERSION
assert version("django_admin_extra_buttons") == expected
