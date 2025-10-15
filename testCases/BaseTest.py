import pytest
@pytest.mark.usefixtures("setup_and_teardown", "log_on_failure","page")
class BaseTest:
    pass