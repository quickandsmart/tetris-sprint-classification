from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/classify_sprint',methods=['GET','POST'])
def classify_sprint():
    user = request.form['user']


    util.request_sprint_data(user)


    response = jsonify({
        'player': user,
        'sprint_type': util.classify_sprint(user),
        'replay': util.get_replay()
    })
    response.headers.add('Access-Control-Allow-Origin','*')

    return response


if __name__ == "__main__":
    util.load_saved_artifacts()
    print("Starting Python Flash Server for Tetrio sprint classification...")
    app.run()