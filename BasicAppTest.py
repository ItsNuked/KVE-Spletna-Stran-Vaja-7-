from flask import Flask

BasicAppTest = Flask(__name__)

@BasicAppTest.route('/hello/')
def hello_world():
    return "Hello world! Stran deluje."

if __name__ == '__main__':
    BasicAppTest.run(debug=True)
