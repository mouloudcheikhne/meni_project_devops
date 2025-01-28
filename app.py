import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Meni_project_devops.sqlite3'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Maximum file size 16MB
db = SQLAlchemy(app)
app.secret_key = "mini_project_devops"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Users model
class Users(db.Model):
    __tablename__ = 'users'
    def __init__(self, nom, prenom, password, tel, rol='user'):
        self.nom = nom
        self.prenom = prenom
        self.password = password
        self.tel = tel
        self.rol = rol
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(70))
    prenom = db.Column(db.String(70))
    rol = db.Column(db.String(70), default='user')
    tel = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))

# Payement model
class Payement(db.Model):
    __tablename__ = 'Payement'
    def __init__(self, id_client, code_etudient, image, nivaux, annee, mois):
        self.id_client = id_client
        self.code_etudient = code_etudient
        self.image = image
        self.nivaux = nivaux
        self.annee = annee
        self.mois = mois

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_client = db.Column(db.Integer, db.ForeignKey('users.id'))
    code_etudient = db.Column(db.String(200))
    image = db.Column(db.String(255))
    nivaux = db.Column(db.String(200))
    annee = db.Column(db.String(200))
    mois = db.Column(db.String(200))
    validation = db.Column(db.String(200), default='no')
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/regester', methods=['GET', 'POST'])
def regester():
    if request.method == 'GET':
        return render_template('regester.html')
    else:
        nom = request.form['nom']
        prenom = request.form['prenom']
        tel = request.form['tel']
        password = request.form['password']
        user = Users(nom=nom, prenom=prenom, tel=tel, password=password)
        db.session.add(user)
        db.session.commit()
        return nom

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        tel = request.form['tel']
        password = request.form['password']
        user = Users.query.filter_by(tel=tel, password=password).first()
        if user:
            if user.rol == "user":
                session['user'] = user.tel
                return session['user']
            else:
                session['admin'] = user.tel
                return session['admin']
        else:
            return "no"
@app.route('/payement', methods=['GET', 'POST'])
def payement():
    if 'user' in session:
        if request.method == "GET":
            return render_template('form_payement.html')
        else:
            code_etudient = request.form['code_etudient']
            image = request.files['image']
            nivaux = request.form['nivaux']
            annee = request.form['annee']
            mois = request.form['mois']

            # Check if image is valid and allowed
            if image and allowed_file(image.filename):
                # Secure the filename and save it
                filename = secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(filepath)

                # Retrieve the current user's ID
                client=session['user']
                user = Users.query.filter_by(tel=client).first()
                if user:
                    
                    id_client = user.id

                    # Create a new payement record with the image filename
                    payement = Payement(
                        id_client=id_client,
                        code_etudient=code_etudient,
                        image=filename,  # Store the filename, not the file object
                        nivaux=nivaux,
                        annee=annee,
                        mois=mois
                    )

                    # Add to the database and commit
                    db.session.add(payement)
                    db.session.commit()

                    return "Payment added successfully!"
                else:
                    return session['user']
            else:
                return "Invalid image format."
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))    

# Create all tables if they don't exist yet
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
