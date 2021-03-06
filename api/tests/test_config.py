# pylint: disable=redefined-outer-name
import pytest
from api import config
from api.config import DataReadingError, DataValidationError


################################################################################
#                                 Testing logging
################################################################################
# _logger = config.get_logger(logger_name="test")

# def mock_debug():
#     _logger.warning("warning message")

# def mock_info():
#     _logger.info("warning message")

# def mock_warning():
#     _logger.warning("warning message")


# def test_logger_debug(caplog):
#     caplog.set_level(logging.DEBUG, logger="test")
#     mock_debug()
#     # print(caplog.text)
#     assert "warning message" in caplog.text


# def test_logger_info(caplog):
#     caplog.set_level(logging.INFO)
#     mock_info()
#     assert "warning message" in caplog.text


# def test_logger_warning(caplog):
#     caplog.set_level(logging.WARNING)
#     mock_warning()
#     assert "warning message" in caplog.text


################################################################################
#                                 Testing custom errors
################################################################################
def test_DataReadingError_without_message():
    with pytest.raises(DataReadingError) as excinfo:
        raise DataReadingError()
    assert str(excinfo.value) == "DataReadingError"


def test_DataReadingError_with_message():
    with pytest.raises(DataReadingError) as excinfo:
        raise DataReadingError("with message")
    assert str(excinfo.value) == "DataReadingError with message"


def test_DataValidationError_without_message():
    with pytest.raises(DataValidationError) as excinfo:
        raise DataValidationError()
    assert str(excinfo.value) == "DataValidationError"


def test_DataValidationError_with_message():
    with pytest.raises(DataValidationError) as excinfo:
        raise DataValidationError("with message")
    assert str(excinfo.value) == "DataValidationError with message"


################################################################################
#                                 Testing Configs
################################################################################
def test_production_config():
    _config = config.ProductionConfig
    assert not _config.TESTING
    assert not _config.DEBUG
    assert not _config.DEVELOPMENT
    assert _config.DB_NAME == "covid"


def test_development_config():
    _config = config.DevelopmentConfig
    assert _config.TESTING
    assert _config.DEBUG
    assert _config.DEVELOPMENT
    assert _config.DB_NAME == "covid-staging"


@pytest.fixture
def mock_staging_true(monkeypatch):
    monkeypatch.setenv("STAGING", "True")


@pytest.fixture
def mock_staging_false(monkeypatch):
    monkeypatch.setenv("STAGING", "False")


def mock_config():
    """get config, used for testing default config"""
    _config = config.get_config()

    if _config is None:
        raise EnvironmentError("_config environment is not set.")

    return _config


def test_default_config_production(mock_staging_false):
    # pylint: disable=W0612,W0613
    _config = mock_config()
    assert _config.__class__.__name__ == "ProductionConfig"


def test_default_config_development(mock_staging_true):
    # pylint: disable=W0612,W0613
    _config = mock_config()
    assert _config.__class__.__name__ == "DevelopmentConfig"
