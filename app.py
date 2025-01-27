from flask import Flask, render_template, redirect, request, url_for,session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Meni_project_devops.sqlite3'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)
app.secret_key="mini_project_devops"
class Users(db.Model):
    __tablename__ = 'users'
    def __init__(self,nom,prenom,password,tel,rol='user'):
        self.nom=nom
        self.prenom=prenom
        self.password=password
        self.tel=tel
        self.rol=rol
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(70))
    prenom = db.Column(db.String(70))
    rol = db.Column(db.String(70),default='user')
    tel = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

class Payement(db.Model):
    __tablename__ = 'Payement'
    def __init__(self,id_client,code_etudient,image,nivaux,annee):
        self.id_client=id_client
        self.code_etudient=code_etudient
        self.image=image
        self.nivaux=nivaux
        self.annee=annee
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    id_client=db.Column(db.Integer,db.ForeignKey('users.id'))
    code_etudient=db.Column(db.String(200))
    image=db.Column(db.String(255))
    nivaux=db.Column(db.String(200))
    annee=db.Column(db.String(200))
    
        


@app.route("/")
def hello():
    return "hhhh"
    
    # return render_template("login.html")
@app.route('/regester',methods=['GET','POST'])
def regester():
    if request.method=='GET':
        return render_template('regester.html')
    else:
        nom=request.form['nom']
        prenom=request.form['prenom']
        tel=request.form['tel']
        password=request.form['password']
        user=Users(nom=nom,prenom=prenom,tel=tel,password=password)
        db.session.add(user)
        db.session.commit()
        return nom
    
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        tel=request.form['tel']
        password=request.form['password']
        user=Users.query.filter_by(tel=tel,password=password).first()
        if user:
            return "nsr"
        else:
            return "no"
        

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=10000, debug=True)