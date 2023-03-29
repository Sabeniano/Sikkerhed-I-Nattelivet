import folium
import threading
from models import Bruger
from mqtt import mqtt_listener
from flask import Flask, g, render_template, request, url_for, redirect, session

#Starter mqtt som lytter på gps_data_topic
thread = threading.Thread(target=mqtt_listener())
thread.start()

app = Flask(__name__)
app.secret_key = 'SDSDSHFT23213213FDSFSDF'

#Funktion der starter hver gang der er en HTTP request
@app.before_request
def before_request():
    if 'brugernavn' in session:
        # Bruger er allerede logget ind, loader bruger objekt til user som kan bruges til view
        user = Bruger.find_by_username(session['brugernavn'])
        if user:
            g.user = user

@app.route("/")
def index():
     return render_template('index.html')

@app.route("/index", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        brugernavn = request.form.get('brugernavn')
        kode = request.form.get('kode')

        bruger = Bruger.find_by_username(brugernavn)
        if bruger and bruger.kode == kode:
            session['brugernavn'] = bruger.brugernavn
            return redirect(url_for('profil'))
        else:
            return render_template('index.html', error='Invalid username or password') #TODO ERROR
    else:
        return render_template('index.html')

#TODO opret
@app.route("/registrer", methods=['GET', 'POST'])
def registrer():
    if request.method == 'POST':
        brugernavn = request.form.get('brugernavn')
        kode = request.form.get('kode')
    else:
        return render_template('index.html')

@app.route("/profil")
def profil():
    if g.user:
        return render_template('profil.html', user = g.user)
    else:
        return redirect(url_for('index'))

#https://young-frog-3.telebit.io/lokation/55.69178/12.55388
@app.route("/lokation/")
@app.route("/lokation/<float:latitude>/<float:longitude>")
def lokation(latitude=None, longitude=None):
    if latitude is None or longitude is None:
        latitude, longitude = 55.69178, 12.55388
        m = folium.Map(location=[latitude, longitude], zoom_start=13)
        return render_template('lokation.html', map=m._repr_html_())
    
    m = folium.Map(location=[latitude, longitude], zoom_start=13)
    folium.Marker(location=[latitude, longitude], popup='Lokation').add_to(m)
    return render_template('lokation.html', map=m._repr_html_())

# TODO ALLE LOKATIONER
@app.route("/kort")
def kort():
    return render_template('kort.html')

@app.route("/logout")
def logout():
    session.pop('brugernavn', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()