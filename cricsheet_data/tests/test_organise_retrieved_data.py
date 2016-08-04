from organise_retrieved_data import get_all_matches_yaml_list, \
                read_file_in_zip, get_all_cricket_cities, \
                get_all_overs_data, give_delivery_info, \
                handle_ind_innings
import json
import pprint

from nose.tools import nottest

pp = pprint.PrettyPrinter(indent=2)


def test_get_all_matches_yaml_list():
    res = get_all_matches_yaml_list()
    assert len(res) == 3181


def test_read_file_in_zip():
    res = read_file_in_zip("913629.yaml")
    print(res)
    assert res["info"]["city"] == "London"


def test_read_file_in_zip_readme():
    res = read_file_in_zip("README.txt")
    print(res)
    assert len(res) == 198740


def test_read_file_in_zip2():
    res = read_file_in_zip("913629.yaml")
    pp.pprint(res)
    assert res["info"]["city"] == "London"


@nottest
def test_get_all_cricket_cities():
    res = get_all_cricket_cities()
    print(res)
    assert res == 1


def test_get_all_over():
    res = get_all_overs_data("913629.yaml")
    print(res)
    assert len(res) == 505


def test_give_delivery_info():
    res = give_delivery_info(10, {0.1: {
        'batsman': 'MDKJ Perera','bowler': 'DJ Willey',
        'non_striker': 'MD Gunathilaka',
        'runs': { 'batsman': 1,'extras': 0,'total': 1}}})
    print(res)
    assert res == [0.1, 1, 0, 1, 11, 0]


def test_give_delivery_info_wicket():
    res = give_delivery_info(13, {1.3: {
        'batsman': 'MD Gunathilaka','bowler': 'CR '
        'Woakes','non_striker': 'MDKJ'
                        'Perera',
         'runs': {'batsman': 0,
                   'extras': 0,
                   'total': 0},
         'wicket': {'fielders': [ 'JM '
                    'Bairstow'],
         'kind': 'run '
                 'out',
          'player_out': 'MDKJ '
                        'Perera'}}})
    print(res)
    assert res == [1.3, 0, 0, 0, 13, 1]


def test_handle_ind_innings():
    res = handle_ind_innings([1,2], {'1st innings': {'deliveries':
                                            [{0.1: {'batsman': 'MDKJ Perera',
                                              'bowler': 'DJ Willey',
                                              'non_striker': 'MD Gunathilaka',
                                              'runs': { 'batsman': 1,
                                                        'extras': 0,
                                                        'total': 1}}},
                                     {0.2: {'batsman': 'MD Gunathilaka',
                                              'bowler': 'DJ Willey',
                                              'non_striker': 'MDKJ Perera',
                                              'runs': {'batsman': 2,
                                                        'extras': 0,
                                                        'total': 2}}}]}})
    pp.pprint(res)
    assert res == [[1, 2, 0.1, 1, 0, 1, 1, 0], [1, 2, 0.2, 2, 0, 2, 3, 0]]
