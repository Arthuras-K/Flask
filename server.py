from flask import Flask, request, jsonify
from flask.views import MethodView
from db import User, Ad, Session
from schema import validate_create_user, validate_create_ad
from errors import HttpError
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt


app = Flask('server')
bcrypt = Bcrypt(app)

# Специальный декоратор для обратки ошибки и красивого вывода
@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response

def get_user(user_id: int, session: Session):
    user = session.query(User).get(user_id)
    if user is None:
        raise HttpError(404, 'user not found')
    return user

def get_ad(ad_id: int, session: Session):
    ad = session.query(Ad).get(ad_id)
    if ad is None:
        raise HttpError(404, 'ad not found')
    return ad


class UsersView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            return jsonify(
                {
                    'id': user.id,
                    'username': user.username,
                    'creation_time': user.creation_time.isoformat(),
                }
            )

    def post(self):
        json_data = validate_create_user(request.json)     
        json_data['password'] = bcrypt.generate_password_hash(json_data['password'].encode()).decode()

        with Session() as session:
            new_user = User(**json_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'user already existrs')
            return jsonify(
                {
                    'id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email,
                    'creation_time': new_user.creation_time.isoformat()
                }
            )

    def patch(self, user_id: int):
        json_data = request.json
        with Session() as session:
            user = get_user(user_id, session)
            for field, value in json_data.items():
                setattr(user, field, value)
            session.add(user)
            session.commit()
            return jsonify({'status': 'succes patch'})

    def delete(self, user_id: int):
        with Session() as session:
            user = get_user(user_id, session)
            # token = check_auth(session)
            # if token.user_id != user.id:
            #     raise HttpError(403, "user has no access")
            session.delete(user)          
            session.commit()
            return jsonify({'status': 'succes delete'})


class AdsView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify(
                {
                    'id': ad.id,
                    'title': ad.title,
                    'description': ad.description,
                }
            )

    def post(self):
        json_data = validate_create_ad(request.json)  
        json_data = request.json
        with Session() as session:
            new_ad = Ad(**json_data)
            session.add(new_ad)
            session.commit()
            return jsonify(
                {
                    'id': new_ad.id,
                    'title': new_ad.title,
                    'creation_time': new_ad.creation_time.isoformat()
                }
            )

    def patch(self, ad_id: int):
        json_data = request.json
        with Session() as session:
            ad = get_ad(ad_id, session)
            for field, value in json_data.items():
                setattr(ad, field, value)
            session.add(ad)
            session.commit()
            return jsonify({'status': 'succes patch'})

    def delete(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            session.delete(ad)          
            session.commit()
            return jsonify({'status': 'succes delete'})


app.add_url_rule('/users/<int:user_id>', view_func=UsersView.as_view('users_with_id'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/users/', view_func=UsersView.as_view('users_post'), methods=['POST'])
app.add_url_rule('/ads/<int:ad_id>', view_func=AdsView.as_view('ad_with_id'), methods=['GET', 'PATCH', 'DELETE'])
app.add_url_rule('/ads/', view_func=AdsView.as_view('users_ads'), methods=['POST'])

app.run(port=5000)
