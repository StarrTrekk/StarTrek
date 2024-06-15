from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from geopy.geocoders import Nominatim

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
db = SQLAlchemy(app)
geolocator = Nominatim(user_agent="myapp")

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Location {self.id} ({self.latitude}, {self.longitude})>'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/locate', methods=['POST'])
def locate():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    location = Location(latitude=latitude, longitude=longitude)
    db.session.add(location)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/follow')
def follow():
    locations = Location.query.order_by(Location.id.desc()).limit(10).all()
    return jsonify([{'latitude': location.latitude, 'longitude': location.longitude} for location in locations])

if __name__ == '__main__':
    #db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
