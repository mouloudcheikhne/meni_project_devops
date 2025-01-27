from flask import Flask, render_template, redirect, request, url_for,session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Meni_project_devops.sqlite3'
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "hhhh"

# with app.app_context():
#     db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=10000, debug=True)