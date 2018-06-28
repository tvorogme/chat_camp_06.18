from flask import Flask, request, render_template
import grequests

app = Flask(__name__)

ip_range = ["172.6.0.{}".format(str(i)) for i in range(255)]

messages = []


@app.route('/send')
def send_message():
    if 'message' in request.args:
        answers = []
        for ip in ip_range:
            answers.append(grequests.get("http://{}:9090/receive?message={}".format(ip,
                                        request.args['message']),
                                         timeout=0.1))
        grequests.map(answers)
    return "Sended"


@app.route('/receive')
def receive():
    if 'message' in request.args:
        messages.append(request.args['message'])
        return 'Ok!'
    else:
        return 'Not ok'


@app.route('/chat')
def chat():
    return " ".join(messages)


@app.route('/')
def index():
    return render_template("index.html")

app.run(host="0.0.0.0", port=9090, debug=True, threaded=True)
