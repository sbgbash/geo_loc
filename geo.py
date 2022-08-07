# A program to find the closest building withing a 10000 meter radius of computer
import overpy
import geopy.distance
import geocoder


def main():
    # get current location of computer
    loc = get_location()
    # convert into string format
    loc_str = f'{str(loc[0])}, {str(loc[1])}'
  
    # establish the API
    api = overpy.Overpass()

    # use API to query openStreetMaps 
    try:
        result = api.query(f"""[out:json][timeout:25];(nwr["building"="yes"]
            (around: 10000, {loc_str}););
            out body;>;out skel qt;""")
    except overpy.exception.OverpassGatewayTimeout:
        print("OSM Server load too high - please try again later")
   
    # create dict to store builduing name and distance/location
    data = {}
    
    # iterate through way objects if there is a building grab name/coordinates
    for way in result.ways:
        if way.tags.get('name', 'n/a') != 'n/a':
            lat_lon = (f'{round(way.nodes[0].lat, 5)}, {round(way.nodes[0].lon, 5)}')
            data.update({way.tags.get('name', 'n/a'): [round(geopy.distance.geodesic( \
                loc, lat_lon).miles, 2), lat_lon]})

    # print out closest building
    for k, v in data.items():
        print(f'Building: {k}, distance: {v[0]} miles, loc: {v[1]}')

# function to get current computer location using IP
def get_location():
    g = geocoder.ip('me')
    return g.latlng

main()