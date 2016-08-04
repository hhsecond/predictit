import requests, json, time


def get_cities():
    with open("countries.txt") as f:
        return [x.rstrip() for x in f.readlines()]

def query_google(city):
    response  = requests.get("http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % city)
    if response.status_code == 200:
        json_response = json.loads(response.text)
    return json_response

def get_lat_lon_from(response):
    results =  response["results"][0]
    for key, value in results.items():
        if key == "geometry":
            geometry = value
            if geometry["location_type"] == "APPROXIMATE":
                lat = geometry['location']['lat']
                lng = geometry['location']['lng']
                return (lat, lng)

def city_lat_lon():
    city_lat_lon_dict = {}
    for city in get_cities():
        response = query_google(city)
        time.sleep(3)
        print("%s: %s" % (city, get_lat_lon_from(response)))
        city_lat_lon_dict[city] = get_lat_lon_from(response)

    with open("city_lat_lon.txt", "w") as f:
        json.dump(city_lat_lon_dict, f)

if __name__ == "__main__":
    city_lat_lon()
