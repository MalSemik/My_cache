import pytest
from time import sleep
from my_cache.lesson_classes_cache import DictCache, PickleCache
from unittest.mock import patch
import os


@pytest.fixture()
def cache():
    return DictCache()


# @pytest.fixture()
# def p_cache():
#     return PickleCache()


def test_simple(cache):
    assert cache.cached_get("http://worldtimeapi.org/api/timezone/Europe/Warsaw").status_code == 200


def test_cache_return(cache):
    assert cache.cached_get("http://worldtimeapi.org/api/timezone/Europe").from_cache is False
    assert cache.cached_get("http://worldtimeapi.org/api/timezone/Europe").from_cache is True


def test_cache_expire(cache):
    assert cache.cached_get("http://worldtimeapi.org/api/timezone/Africa", 0.5).from_cache is False
    sleep(1.0)  # TODO: mock time to avoid sleepig
    assert cache.cached_get("http://worldtimeapi.org/api/timezone/Africa").from_cache is False


def test_cache_cleaning(cache):
    cache.cached_get("http://worldtimeapi.org/api/timezone/Europe/Rome", 0.5)
    sleep(1.0)
    cache.cached_get("http://worldtimeapi.org/api/timezone/America/New_York", 0.5)
    assert "http://worldtimeapi.org/api/timezone/Europe/Rome" not in cache.cache


def test_cache_return_mocks(cache):
    with patch("requests.get") as mock_requests:
        url = "https://google.com"
        cache.cached_get(url)
        cache.cached_get(url)
        assert mock_requests.called == 1


def test_pickle_cache(tmp_path):
    path = os.path.join(str(tmp_path), '.cache')
    p_cache = PickleCache(filename=path)
    assert p_cache.cached_get("http://worldtimeapi.org/api/timezone/Europe/Warsaw").status_code == 200


def test_reading_from_pickled_file(tmp_path):
    path = os.path.join(str(tmp_path), 'f1')
    p_cache_1 = PickleCache(filename=path)
    p_cache_1.cached_get("http://worldtimeapi.org/api/timezone/Europe/Rome")
    p_cache_2 = PickleCache(filename=path)
    assert p_cache_2.cached_get("http://worldtimeapi.org/api/timezone/Europe/Rome").from_cache is True

# def test_mocking():
#     with patch("requests.get") as mock_requests:
#         mock_requests.return_value = "rafał"
#         co = cached_get("ww.dupa.com")
#         assert co[0] == "rafał"
