from flask import Flask
from flask import send_file

tester = Flask(__name__)

@tester.route("/test", methods=['GET', 'POST'])
def index():
    response = 'default_response.xml'
    return send_file(response)

if __name__ == "__main__":
    tester.run(port=3333)
