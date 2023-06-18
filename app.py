from flask import Flask, render_template, request, redirect, url_for, session, flash
from views.VistaUtente import vistaUtente
from models.giornalista import Giornalista
from models.notiziaTestuale import NotiziaTestuale
from views.VistaPredefinita import vistaPredefinita
from views.VistaAmministratore import vistaAmministratore

app = Flask(__name__)
# La secretkey serve per l'application, potremmo metterla nelle variabili di .env volendo
app.secret_key = 'mysupersecretkey'

# Per comodità setto anche come index, ma qui ci andrà ovviamente un redirect alla landing page
@app.route("/")
def landingPage():
    return render_template("landingPage.html")


# http://localhost:5000/login/
# @app.route -> login
app.add_url_rule('/login', view_func=vistaPredefinita.as_view('login',1), methods=['GET','POST'])
# @app.route -> registerGiornalista
app.add_url_rule('/registerGiornalista', view_func=vistaPredefinita.as_view('registerGiornalista',3), methods=['GET', 'POST'])
# @app.route -> registerUtente
app.add_url_rule('/registerUtente', view_func=vistaPredefinita.as_view('registerUtente',2), methods=['GET', 'POST'])
# @app.route -> notizia
app.add_url_rule('/notizia', view_func=vistaUtente.as_view('notizia',1), methods=['GET', 'POST'])
# @app.route -> notiziaTesto
app.add_url_rule('/notiziaTesto', view_func=vistaUtente.as_view('notiziaTesto',2), methods=['GET', 'POST'])
# @app.route -> notiziaTesto/segnalaNotizia
app.add_url_rule('/notiziaTesto/segnalaNotizia', view_func=vistaUtente.as_view('notiziaTesto/segnalaNotizia',6), methods=['GET', 'POST'])
# @app.route -> notiziaImmagine
app.add_url_rule('/notiziaImmagine', view_func=vistaUtente.as_view('notiziaImmagine',3), methods=['GET', 'POST'])
# @app.route -> notiziaImmagine/segnalaNotizia
app.add_url_rule('/notiziaImmagine/segnalaNotizia', view_func=vistaUtente.as_view('notiziaImmagine/segnalaNotizia',6), methods=['GET', 'POST'])
# @app.route -> notiziaAudio
app.add_url_rule('/notiziaAudio', view_func=vistaUtente.as_view('notiziaAudio',4), methods=['GET', 'POST'])
# @app.route -> notiziaAudio
app.add_url_rule('/notiziaAudio/segnalaNotizia', view_func=vistaUtente.as_view('notiziaAudio/segnalaNotizia',6), methods=['GET', 'POST'])
# @app.route -> notiziaVidio
app.add_url_rule('/notiziaVideo', view_func=vistaUtente.as_view('notiziaVideo',5), methods=['GET', 'POST'])
# @app.route -> notiziaVideo
app.add_url_rule('/notiziaVideo/segnalaNotizia', view_func=vistaUtente.as_view('notiziaVideo/segnalaNotizia',6), methods=['GET', 'POST'])
# @app.route -> amministratore
app.add_url_rule('/amministratore', view_func = vistaAmministratore.as_view('amministratore'), methods=['GET', 'POST'])



@app.route('/login/logout')
def logout():
    # elimino la sessione
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('isUtente', None)
    session.pop('isGiornalista', None)
    session.pop('admin',None)
    return render_template('login.html',msglogout=1)

# Per gli error code di flask
# https://flask.palletsprojects.com/en/1.0.x/patterns/errorpages/
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404Error.html'), 404

# Per la pagina di contatto
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)