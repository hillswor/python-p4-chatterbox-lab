from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)


@app.route("/messages", methods=["GET", "POST"])
def messages():
    if request.method == "GET":
        messages_serialized = [
            message.to_dict()
            for message in Message.query.order_by(Message.created_at.asc()).all()
        ]

        if not messages:
            response = make_response(jsonify([]), 404)

        else:
            response = make_response(jsonify(messages_serialized), 200)

            return response

    elif request.method == "POST":
        message = Message(
            body=request.json["body"],
            username=request.json["username"],
        )

        db.session.add(message)
        db.session.commit()

        response = make_response(jsonify(message.to_dict()), 201)

        return response


@app.route("/messages/<int:id>", methods=["GET", "PATCH", "DELETE"])
def messages_by_id(id):
    message = Message.query.get(id)

    if request.method == "GET":
        if not message:
            response = make_response(jsonify({}), 404)

            return response

        else:
            response = make_response(jsonify(message.to_dict()), 200)

            return response

    elif request.method == "PATCH":
        if not message:
            response = make_response(jsonify({}), 404)

            return response

        else:
            message = Message(**request.json)
            db.session.add(message)
            db.session.commit()

            response = make_response(jsonify(message.to_dict()), 201)

            return response

    elif request.method == "DELETE":
        if not message:
            response = make_response(jsonify({}), 404)

            return response

        else:
            db.session.delete(message)
            db.session.commit()

            response = make_response(jsonify({}), 204)

            return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
