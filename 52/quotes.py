import json
from flask import Flask, jsonify, abort, request

app = Flask(__name__)

quotes = [
    {
        "id": 1,
        "quote": "I'm gonna make him an offer he can't refuse.",
        "movie": "The Godfather",
    },
    {
        "id": 2,
        "quote": "Get to the choppa!",
        "movie": "Predator",
    },
    {
        "id": 3,
        "quote": "Nobody's gonna hurt anybody. We're gonna be like three little Fonzies here.",  # noqa E501
        "movie": "Pulp Fiction",
    },
]


def _get_quote(qid):
    """Recommended helper"""
    for quote in quotes:
        if quote.get("id") == qid:
            return quote
    else:
        abort(404)


def _quote_exists(existing_quote):
    """Recommended helper"""
    for quote in quotes:
        if quote.get("quote") == existing_quote:
            return True
    else:
        return False


@app.route("/api/quotes", methods=["GET"])
def get_quotes():
    return jsonify({"quotes": quotes})


@app.route("/api/quotes/<int:qid>", methods=["GET"])
def get_quote(qid):
    return jsonify({"quotes": [_get_quote(qid)]})


@app.route("/api/quotes", methods=["POST"])
def create_quote():
    data = request.get_json()
    quote = data.get("quote")
    movie = data.get("movie")
    if _quote_exists(quote):
        abort(400)
    if not quote or not movie:
        abort(400)
    incr_idx = max([q.get("id") for q in quotes]) + 1
    new_quote = {"id": incr_idx, "quote": quote, "movie": movie}
    quotes.append(new_quote)
    data = dict(quote=new_quote)
    return jsonify(data), 201


@app.route("/api/quotes/<int:qid>", methods=["PUT"])
def update_quote(qid):
    data = request.get_json()
    quote = data.get("quote")
    movie = data.get("movie")
    old_quote = _get_quote(qid)
    if _quote_exists(quote):
        data = dict(quote=old_quote)
        return jsonify(data)
    elif not quote or not movie:
        abort(400)
    else:
        for q in quotes:
            if q["id"] == qid:
                q["quote"] = quote
                q["movie"] = movie
                data = {"quote": q}
                return jsonify(data)


@app.route("/api/quotes/<int:qid>", methods=["DELETE"])
def delete_quote(qid):
    get_quote(qid)
    for i, q in enumerate(quotes):
        if q["id"] == qid:
            quotes.remove(q)
    return jsonify({}), 204


if __name__ == "__main__":
    app.run()
