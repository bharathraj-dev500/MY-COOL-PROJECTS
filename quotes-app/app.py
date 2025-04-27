from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

quotes = [
    "The best way to get started is to quit talking and begin doing.",
    "Don't let yesterday take up too much of today.",
    "Success is not in what you have, but who you are.",
    "Dream bigger. Do bigger."
]

@app.route('/')
def home():
    quote = random.choice(quotes)
    return render_template('index.html', quote=quote)

@app.route('/new_quote', methods=['GET'])
def new_quote():
    quote = random.choice(quotes)
    return jsonify(quote=quote)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
