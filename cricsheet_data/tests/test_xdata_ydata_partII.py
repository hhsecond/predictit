from organise_retrieved_data import get_relevant_data, \
                get_lat_lng

from nose.tools import nottest


def test_get_relevant_data_date():
    res = get_relevant_data("  created: 2016-06-30")
    assert res == "20160630"

def test_get_relevant_data_float():
    res = get_relevant_data("  data_version: 0.7")
    assert res == "0.7"

def test_get_relevant_data_num():
    res = get_relevant_data("              batsman: 2")
    assert res == "2"

def test_get_lat_lng():
    res = get_lat_lng("Chelmsford")
    assert res == [51.7355868, 0.4685497]
