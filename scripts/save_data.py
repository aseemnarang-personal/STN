import os, inspect, json

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script directory
path += '/../data/'


os.chdir(path)

with open('yelp_academic_dataset_business.json', 'rb') as f:
    data = f.readlines()

data = map(lambda x: x.rstrip(), data)

business_list = [x for x in [json.loads(line) for line in data] if x['city'] == 'Edinburgh']

print 'Done!'

with open('edinburgh.json', 'wb') as outfile:
    json.dump(business_list, outfile)
