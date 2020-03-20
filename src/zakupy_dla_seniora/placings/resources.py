from flask_restful import Resource, reqparse
from zakupy_dla_seniora.placings.models import Placings
from zakupy_dla_seniora.sms_handler.dialog_functions import placing_creation_message

register_parser = reqparse.RequestParser()
register_parser.add_argument('user_id', help='This field cannot be blank', required=True)
register_parser.add_argument('message_id', help='This field cannot be blank', required=True)


class PlacingCreation(Resource):
    def post(self):
        data = register_parser.parse_args()
        new_placing = Placings(
            user_id=data['user_id'],
            message_id=data['message_id'],
        )
        new_placing.save()

<<<<<<< HEAD
        return placing_creation_message(user_id = new_placing.user_id, message_id = new_placing.message_id)


class PlacingEnding(Resource):
    def post(self):
        data = register_parser.parse_args()
        edited_placing = Placings(
            user_id=data['user_id'],
            message_id=data['message_id'],
            placing_status = "waiting for ending approval"
        )

        edited_placing.save()
=======
        return placing_creation_message(user_id=new_placing.user_id, message_id=new_placing.message_id)
>>>>>>> eb2c3fee6deedbac128dea82b1d30a68937af6ea
