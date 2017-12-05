from zomato import Zomato
import json

z = Zomato("309e354eabc5cf4d7ea8eddef054c677")
# A call to categories endpoint from zomato API.

# A call to restaurants endppoint from zomato 
# API with required parameters res_id
#z.parse("restaurant","res_id=16774318")


data=z.parse("locations","query=mumbai")
print data
data_json= json.loads(data)

l=[]
for x in data_json["location_suggestions"]:
	id = x[u'entity_id']
	type = x[u'entity_type']
print type
print "entity_id={}".format(id)
data = z.parse("location_details","entity_id={}".format(id)+","+"entity_type={}".format(type))
data=json.loads(data)

l=[]
for i in range(10):
	if data["best_rated_restaurant"][i]["restaurant"]["name"]:
		l.append(data["best_rated_restaurant"][i]["restaurant"]["name"])
