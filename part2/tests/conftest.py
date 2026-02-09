import warnings
# This setsup pytest file

def pytest_configure():
    warnings.filterwarnings(
        "ignore",
        category=DeprecationWarning,
        message=r".*jsonschema\.RefResolver.*"
    )
