from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

class Plays(Resource):
    def get(self):
        data = pd.read_csv('plays.csv')  # read local CSV
        data = data.to_dict()  # convert dataframe to dict
        return {'data': data}, 200  # return data and 200 OK

    def post(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('play_number', required=True)  # add args
        parser.add_argument('quarter', required=True)  # add args
        parser.add_argument('start_time', required=True)  # add args
        parser.add_argument('end_time', required=True)  # add args
        parser.add_argument('home', required=True)
        parser.add_argument('away', required=True)
        parser.add_argument('participating_players',required=False, action='append')
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('plays.csv')

        if args['play_number'] in list(data['play_number']):
            return {
                'message': f"'{args['play_number']}' already exists."
            }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'play_number': [args['play_number']],
                'quarter': [args['quarter']],
                'start_time': [args['start_time']],
                'end_time': [args['end_time']],
                'home': [args['home']],
                'away': [args['away']],
                'participating_players': [args['participating_players']]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('plays.csv', index=False)  # save back to CSV
            return {'data': data.to_dict()}, 200  # return data with 200 OK


    def put(self):  
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('play_number', required=True)  # add args
        parser.add_argument('player', required=True)
        args = parser.parse_args()  # parse arguments to dictionary

        # read our CSV
        data = pd.read_csv('plays.csv')
        print(list(data['play_number']))

        if int(args['play_number']) in list(data['play_number']):
            # evaluate strings of lists to lists !!! never put something like this in prod
            data['participating_players'] = data['participating_players'].apply(
                lambda x: ast.literal_eval(x)
            )
            # select our user
            play_data = data[data['play_number'] == args['play_number']]

            # update user's locations
            if len(play_data['participating_players']) == 0:
                play_data['participating_players'] = args['player']
            else:
                play_data['participating_players'] = play_data['participating_players'].values[0] \
                    .append(args['player'])
            
            
            # save back to CSV
            data.to_csv('plays.csv', index=False)
            # return data and 200 OK
            return {'data': data.to_dict()}, 200

        else:
            # otherwise the userId does not exist
            return {
                'message': f"'{args['play_number']}'  not found."
            }, 404

                    
# class Players(Resource):
#     def get(self):
#         data = pd.read_csv('players.csv')  # read local CSV
#         return {'data': data.to_dict()}, 200  # return data dict and 200 OK
    
#     def post(self):
#         parser = reqparse.RequestParser()  # initialize parser
#         parser.add_argument('number', required=True, type=int)  # add args
#         parser.add_argument('name', required=True)
#         args = parser.parse_args()  # parse arguments to dictionary
        
#         # read our CSV
#         data = pd.read_csv('players.csv')
    
#         # check if location already exists
#         if args['number'] in list(data['number']):
#             # if locationId already exists, return 401 unauthorized
#             return {
#                 'message': f"'{args['number']}' already exists."
#             }, 409
#         else:
#             # otherwise, we can add the new location record
#             # create new dataframe containing new values
#             new_data = pd.DataFrame({
#                 'number': [args['number']],
#                 'name': [args['name']]
#             })
#             # add the newly provided values
#             data = data.append(new_data, ignore_index=True)
#             data.to_csv('players.csv', index=False)  # save back to CSV
#             return {'data': data.to_dict()}, 200  # return data with 200 OK
    
    


api.add_resource(Plays, '/plays')  # add endpoints
#api.add_resource(Players, '/players')

if __name__ == '__main__':
    app.run()  # run our Flask app