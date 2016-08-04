from __future__ import print_function
from random import randint
import zipfile
import yaml
import re
import json
import logging
import datetime
from sys import argv


def get_all_matches_yaml_list():
    zf = zipfile.ZipFile('all.zip', 'r')
    return zf.namelist()


def read_file_in_zip(filename):
    zf = zipfile.ZipFile('all.zip', 'r')
    if filename in ("README.txt"):
        data = zf.read(filename)
        return data
    else:
        try:
            data = yaml.safe_load(zf.read(filename))
            return data
        except KeyError:
            print('ERROR: Did not find %s in zip file' % filename)
        else:
            print(filename, ':')
            print(repr(data))
        print


def get_city(filename):
    try:
        return read_file_in_zip(filename)["info"]["city"]
    except:
        pass


def give_delivery_info(runs_scored, delivery):
    for ball, ball_info in delivery.items():
        over_info = [ball] + [ball_info["runs"]["batsman"]] + \
                        [ball_info["runs"]["extras"]] + \
                        [ball_info["runs"]["total"]]
        over_info.append(runs_scored + ball_info["runs"]["total"])
        try:
            if ball_info["wicket"]:
                over_info += [1]
        except KeyError:
            over_info += [0]
        return over_info


def handle_ind_innings(city_coords, ind_innings):
    """
    the output is a list in the following format
    [[ first ball, batsman, extras, total this ball, total runs scored yet,
    if_wicket]
    [ second ball, batsman, extras, total this ball, total runs scored yet,
    if_wicket]
    ... and so on
    [ last ball, batsman, extras, total this ball, total runs scored yet,
    if_wicket]]
    """
    delivery_info_list = []
    runs_scored = 0
    for k, v in ind_innings.items():
        deliveries = v["deliveries"]
        for delivery in deliveries:
            delivery_info = give_delivery_info(runs_scored, delivery)
            runs_scored = delivery_info[4]
            delivery_info_list.append(city_coords + delivery_info)
    return delivery_info_list


def get_all_overs_data(filename):
    city_coords = get_lat_lng(get_city(filename))
    deliveries = []
    both_innings = read_file_in_zip(filename)["innings"]
    for ind_innings in both_innings:
        deliveries += handle_ind_innings(city_coords, ind_innings)
    return deliveries


def get_all_cricket_cities():
    return [get_city(filename) for filename in get_all_matches_yaml_list()]


def print_city_names():
    """
    there are around 3200 fields
    so take them batch by batch
    """
    for filename in get_all_matches_yaml_list()[2500:3500]:
        print(get_city(filename))


def get_relevant_data(line):
    date_match = re.search(r'(\d+\-\d+\-\d+)', line)
    if date_match:
        date_match_text = date_match.group(1)
        return date_match_text.replace("-", "")

    float_match = re.search(r'(\d+\.\d+)', line)
    if float_match:
        float_match_text = float_match.group(1)
        return float_match_text

    num_match = re.search(r'(\d+)', line)
    if num_match:
        num_match_text = num_match.group(1)
        return num_match_text


def get_lat_lng(city):
    with open("city_lat_lon.txt") as f:
        data = json.load(f)
        return data[city]


def create_xdata_ydata_per_over(file):
    zf = zipfile.ZipFile('all.zip', 'r')
    f = str(zf.read(file)).split("\\n")
    city_coordinates = get_lat_lng(get_city(file))
    dataset = [x for x in city_coordinates]
    for line in f:
        dataset.append(get_relevant_data(line))
    dataset = [float(x) for x in dataset if x is not None]
    return dataset


def get_dataset():
    for file in get_all_matches_yaml_list()[0:10]:
        if file != "README.txt":
            print(create_xdata_ydata_per_over(file))


def get_date():
    mylist = []
    today = datetime.date.today()
    mylist.append(today)
    return mylist[0]


if __name__ == "__main__":
    # see the args
    present_iter_lower = int(argv[1])
    present_iter_upper = int(argv[2])

    # logging
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] \
                                     [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.INFO)

    fileName = "logs/organise_retrieved_data_%s_%s"\
        % (get_date(), randint(0, 50))
    fileHandler = logging.FileHandler("{0}.log".format(fileName))
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.INFO)

    rootLogger.addHandler(fileHandler)

    for file_name in get_all_matches_yaml_list()[present_iter_lower:present_iter_upper]:
        if file_name != "README.txt":
            try:
                print(get_all_overs_data(file_name))
            except Exception as e:
                rootLogger.info(e)
                rootLogger.info("file not working: %s" % file_name)
