import inspect, os
import json
from math import sin, cos, sqrt, atan2, radians

# Put all datasets in 'path-to-repo/data' directory please
path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
path += '/../data/'


os.chdir(path)

with open('yelp_academic_dataset_business.json', 'rb') as f:
    data = f.readlines()

data = map(lambda x: x.rstrip(), data)

business_list = [x for x in [json.loads(line) for line in data] if x['city'] == 'Edinburgh']

# Num of Edinburgh businesses = roughly 3500
# print len(business_list)


def calc_distance(business1, business2):
    # Gets the distance between 2 businesses
    # business1, business2 of type dict()

    R = 6373.0

    lat1 = radians(business1['latitude'])
    lon1 = radians(business1['longitude'])
    lat2 = radians(business2['latitude'])
    lon2 = radians(business2['longitude'])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def get_graph():

    # threshold --> the radius of our unit circle
    threshold = 0.3

    # Our graph
    G = dict()

    for (business1, business2) in [ (x, y) for x in business_list for y in business_list if x != y ]:

        distance = calc_distance(business1, business2)

        # Add them to the graph if they're closer than 2 * threshold (in km)
        if distance <= 2 * threshold:
            b1_id = business1['business_id']
            b2_id = business2['business_id']
            if b1_id in G:
                G[b1_id].append(b2_id)
            else:
                G[b1_id] = [b2_id]

    return G



if __name__ == '__main__':

    G = get_graph()

    total_connections = 0
    for key, val in G.iteritems():
        total_connections += len(val)

    # Undirect the edges
    total_connections /= 2

    print 'Number of keys --> '
    print len(G.keys())

    print 'Total connections -->'
    print total_connections

