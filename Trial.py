from flask import Flask
from flask_ask import Ask, statement, question, session
from zomato import Zomato
import json
from unidecode import unidecode

app = Flask(__name__)
ask = Ask(app, "/zomato")
z = Zomato("309e354eabc5cf4d7ea8eddef054c677")
id=0
restaurant_names=[]
details = []
cuisine = []
cost = []
rating = []

def get_categories():
    data=z.parse("categories","")
    print data
    data_json= json.loads(data)
    l=[]
    for x in data_json['categories']:
        l.append(unidecode(x[u'categories'][u'name'])+"....")
    l=' '.join([i for i in l])
    l = l.replace('&','and')
    return l

def get_collections(cid):
    data=z.parse("collections","city_id={}".format(cid))
    print data
    data_json= json.loads(data)
    l=[]
    for x in data_json['collections']:
        l.append(unidecode(x[u'collection'][u'title'])+"....")
    l=' '.join([i for i in l])
    l = l.replace('&amp;','')
    l = l.replace('caf&eacute;s','cafe')
    l = l.replace('&#039;','')
    return l

def get_restaurant(id,type):
    data = z.parse("location_details","entity_id={}".format(id)+","+"entity_type={}".format(type))
    data=json.loads(data)

    global restaurant_names 
    global details
    global cuisine
    global cost 
    restaurant_names = []
    details = []
    cuisine = []
    cost = []
    for i in range(10):
        if data["best_rated_restaurant"][i]["restaurant"]["name"]:
            restaurant_names.append(unidecode(data["best_rated_restaurant"][i]["restaurant"]["name"]).lower())
            details.append(unidecode(data["best_rated_restaurant"][i]["restaurant"]["location"]["locality"]))
            cuisine.append(unidecode(data["best_rated_restaurant"][i]["restaurant"]["cuisines"]))
            cost.append(data["best_rated_restaurant"][i]["restaurant"]["average_cost_for_two"])
            rt =str(data["best_rated_restaurant"][i]["restaurant"]["user_rating"]["aggregate_rating"]).replace('.',' point ')
            rating.append(rt)
    r=' '.join([i.replace('&','and')+"...." for i in restaurant_names])
    print details
    return r

def get_locationdetails(loc):
    data=z.parse("locations","query={}".format(loc))
    print data
    data_json= json.loads(data)

    l=[]
    for x in data_json["location_suggestions"]:
        global id 
        id = x[u'entity_id']
        type = x[u'entity_type']
    print type
    print "entity_id={}".format(id)
    s= get_restaurant(id,type)
    return s

@app.route('/')
def homepage():
    return "hi there, how ya doin?"

@ask.launch
def start_skill():
    welcome_message = 'Hello there, How may I assist you?'
    return question(welcome_message)

@ask.intent("AMAZON.YesIntent")
def share_headlines():
    s = get_categories()
    message = "The available categories are {}".format(s)
    return statement(message)

@ask.intent("WhereIntent")
def askLocation():
    q = "What is your location?"
    return question(q)

@ask.intent("LocationIntent")
def get_Location(Location):
    loc = get_locationdetails(Location)
    return statement("The restaurants are {}".format(loc))

@ask.intent("CollectionIntent")
def share_collections():
    s = get_collections(id)
    message = "{}".format(s)
    return statement(message)



''''@ask.intent("CategoryIntent")
def share_categories():
    s = get_categories()
    message = "The available categories are {}".format(s)
    return statement(message)'''

@ask.intent("RestaurantIntent")
def share_detail_restaurants(Restaurant):
    global restaurant_names
    global details
    global cuisine
    detail_dict = {}
    cuisine_dict = {}
    cost_dict = {}
    rating_dict = {}
    for i in range(len(restaurant_names)):
        detail_dict[restaurant_names[i]]=details[i]
        cuisine_dict[restaurant_names[i]]=cuisine[i]
        cost_dict[restaurant_names[i]]=cost[i]
        rating_dict[restaurant_names[i]]=rating[i]
    print rating_dict[Restaurant.lower()]
    print detail_dict[unidecode(Restaurant.lower())]
    print cuisine_dict[unidecode(Restaurant.lower())]
    print cost_dict[unidecode(Restaurant.lower())]
    return statement("It is rated {}".format(rating_dict[unidecode(Restaurant.lower())])+".... by users .. and is located in {}".format(detail_dict[unidecode(Restaurant.lower())])+"..... It serves {}".format(cuisine_dict[unidecode(Restaurant.lower())])+"..... cuisine .. and the average cost for two people is {}".format(cost_dict[unidecode(Restaurant.lower())]))



@ask.intent("AMAZON.NoIntent")
def no_intent():
    bye_text = 'Maybe next time then, Bye'
    return statement(bye_text)

if __name__ == '__main__':
    app.run(debug=True)