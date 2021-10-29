from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/data1.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Tabla(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nickname=db.Column(db.String(20), unique=True, nullable=False)
    contrasena=db.Column(db.String(80),nullable=False)
    nombres_usuario=db.Column(db.String(20))
    apellidos_usuario=db.Column(db.String(20))
    rol=db.Column(db.String(10))
    direccion_usuario=db.Column(db.String(20))
    email_usuario=db.Column(db.String(40))
    genero_usuario=db.Column(db.String(3))
    fecha_nacimiento=db.Column(db.String(8))

@app.route("/")
def vuelta():
    return render_template("login.html")

@app.route("/inicio")
def semivuelta():
    return render_template("navegacion.html")

@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=="POST":
        hashed_pw=generate_password_hash(request.form["password"], method="sha256")
        new_user=Tabla(nickname=request.form["username"], contrasena=hashed_pw,
                       nombres_usuario=request.form["nombres_u"], apellidos_usuario=request.form["apellidos_u"],
                        rol=request.form["rol"], direccion_usuario=request.form["direccion_u"],
                        email_usuario=request.form["email_u"], genero_usuario=request.form["genero_u"],
                        fecha_nacimiento=request.form["fecha_u"]
                       )
        
        db.session.add(new_user)
        db.session.commit()
        

        
        return redirect(url_for("semivuelta"))
    return render_template("registro_usuarios.html")
    
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        #consulta a ver si existe el usuario
            user=Tabla.query.filter_by(nickname=request.form["username"]).first()
            #consulta si la contraseña es correcta
            if user and check_password_hash(user.contrasena,request.form["password"]):
                return render_template("navegacion.html")
            return("credenciales invalidas")    
    return render_template("login.html")


@app.route('/edicion')
def edicion():
    mostrar=Tabla.query.all()
    return render_template("edicion_usuarios.html", show=mostrar)


@app.route('/delete/<id>')

def delete(id):
    task=Tabla.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for("semivuelta"))



@app.route("/edit_user")
def editar():
    return render_template("formedit.html")

@app.route("/submitform",methods=["POST"])
def implementar():
    lectura=Tabla.query.filter_by(nickname=request.form["username_e"]).first()
    lectura.nickname=request.form["username_e"]
    lectura.nombres_usuario=request.form["nombres_e"]
    lectura.apellidos_usuario=request.form["apellidos_e"]
    lectura.direccion_usuario=request.form["direccion_e"]
    lectura.email_usuario=request.form["email_e"]
    db.session.commit()
    return redirect(url_for("edicion"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
    
#i hope this works
#i hope this works
