# Django Admin Extra Buttons

Django application that allows easy creation of wizards, actions and/or links to external resources
as well as api only views.

# Project Agent Instructions

## Environment

- Python 3.12+
- Django >= 4.2
- Testing: pytest + django-webtest + coverage
- Linting: ruff

## Commands
```bash
# Quick test
pytest tests/

# Format code
ruff format src/

# Code conventions compliance e
tox

```
## Development guidelines

- Never commit without asking


## Code Style

- No comments unless explicitly requested
- Follow existing code patterns in the codebase -
- Use mypy type checking and verify with `tox -e mypy`
- Update documentation in `docs`

## Testing

- Test files in `tests/test_*.py`
- Use pytest fixtures from `conftest.py`
- Django test app at `tests/demoapp/`
- Do NOT modify existing tests

## Project Structure

- Source code: `src/admin_extra_buttons/`
- Tests: `tests/`
- Demo app: `tests/demoapp/`
- Documentation: `docs/src/api/`
