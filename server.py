from flask import Flask, request, jsonify
from flask.views import MethodView
from db import User, Ad, Session
from schema import validate_create_user, validate_create_ad

app = Flask('server')


class UserView(MethodView):

    def get(self):
        pass

    def post(self):
        json_data = validate_create_user(request.json)        
        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            session.commit()
            return jsonify(
                {
                    'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email
                    #'creation_time': new_user.creation_time.isoformat()
                }
            )

    def patch(self):
        pass

    def delete(self):
        pass


class AdsView(MethodView):

    def get(self, ad_id: int):
        pass

    def post(self):
        json_data = request.json
        with Session() as session:
            new_ad = Ad(**json_data)
            session.add(new_ad)
            session.commit()
            return jsonify(
                {
                    'id': new_ad.id,
                    'title': new_ad.title,
                    #'creation_time': new_ad.creation_time.isoformat()
                }
            )

    def patch(self, ad_id: int):
        pass

    def delete(self, ad_id: int):
        pass



app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_with_id'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UserView.as_view('users_post'), methods=['POST'])
app.add_url_rule('/ads/<int:ad_id>', view_func=AdsView.as_view('ad_with_id'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/ads/', view_func=AdsView.as_view('users_ads'), methods=['POST'])

app.run(port=5000)
