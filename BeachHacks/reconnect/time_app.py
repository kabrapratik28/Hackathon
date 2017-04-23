# -*- coding: utf-8 -*-
from flask import Flask, request
from flask_restful import Resource, Api
from flask import jsonify

app = Flask(__name__)
api = Api(app)

user_timings = {} #{'prat': set(9,10,14,15,16)} 
user_friends = {} #{'prat':['ab','cd']}

def get_over_lap_data(user_name,timings_data,friends_data):
    temp = list(timings_data)
    temp.sort()
    ans = [set() for i in range(24)]
    for each_time in range(len(temp)):
        for each_friend in friends_data:
            if (each_friend in user_timings) and (temp[each_time] in user_timings[each_friend]):
                ans[temp[each_time]].add(each_friend)
    results = []
    start = ans[0]
    start_pos = 0
    i = 0
    #print ans
    while (i<24):
        if ans[i]!=start:
            if len(start)>0:
                times = []
                if str(start_pos)==str(i-1):
                    times = [str(start_pos)]
                else:
                    times = [str(start_pos),str(i-1)]
                results.append([", ".join(list(start)),"-".join(times)])
            start_pos = i
            start = ans[i]
        i = i+1
    #last
    if len(start)>0:
                times = []
                if str(start_pos)==str(i-1):
                    times = [str(start_pos)]
                else:
                    times = [str(start_pos),str(i-1)]
                results.append([", ".join(list(start)),"-".join(times)])
    return results      

class GetTimeTable(Resource):
    def options (self):
        return {'Allow' : 'GET' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET,POST' }

    def get(self,user_name):
        if user_name in user_timings and user_name in user_friends:
            timings_data = user_timings[user_name]
            friends_data = user_friends[user_name]
            results = get_over_lap_data(user_name,timings_data,friends_data)
            return {'user_name':user_name,'timing':results}, 200, {'Access-Control-Allow-Origin':'*'}
        else:
            return {user_name:["User NOT exists or No Friends"]}, 200, {'Access-Control-Allow-Origin':'*'}

class AddTimeTable(Resource):
    def options (self):
        return {'Allow' : 'POST' }, 200, \
        { 'Access-Control-Allow-Origin': '*', \
          'Access-Control-Allow-Methods' : 'PUT,GET,POST' }

    def post(self):
        data = request.get_json(force=True)
        username = data['user_name']
        timings = data['timing']
        friends = data['friends']
        #split on comma
        friends = friends.split(",")
        user_friends[username] = friends
        p = set()
        for i in timings:
            p.add(i)
        user_timings[username] = p
        #print {'user_name':username,'timing':timings,'friends':friends}
        return {'user_name':username,'timing':timings,'friends':friends}, 200, {'Access-Control-Allow-Origin':'*'}
    
api.add_resource(AddTimeTable, '/reconnect')
api.add_resource(GetTimeTable, '/time/<string:user_name>')

if __name__ == '__main__':
    app.run(debug=True)