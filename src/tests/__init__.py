import pytest

# registers helper/convenience functions with pytest to support writing diff/error information to stdout and stderr
pytest.register_assert_rewrite("tests.support")
