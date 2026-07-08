import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
# 2. Cargamos las variables de entorno del archivo .env
load_dotenv()

app = Flask(__name__)

# 3. Traemos la URI desde el entorno. 
# Colocamos una cadena vacía o un valor por defecto por si se olvida configurar la variable.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:@localhost/mi_base_datos')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
DEBUG = os.environ.get("DEBUG", "TRUE") == "TRUE"

# --- MODELO DE SQLALCHEMY ---
class Ubicacion(db.Model):
    __tablename__ = 'ubicaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float, nullable=True)
    altitude = db.Column(db.Float, nullable=True)
    speed = db.Column(db.Float, nullable=True)
    heading = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "accuracy": self.accuracy,
            "altitude": self.altitude,
            "speed": self.speed,
            "heading": self.heading,
            "timestamp": self.timestamp.isoformat()
        }

@app.route("/api/ubicacion", methods=["POST"])
def guardar_ubicacion():
    # Obtener los datos JSON enviados en la petición
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    
    try:
        # Convertir el string de timestamp (ISO 8601) a un objeto datetime de Python
        # Si falla o no viene, usamos la hora actual
        ts_str = data.get("timestamp")
        if ts_str:
            # Reemplazamos la 'Z' si viene de Flutter/Dart para que Python lo procese fácil
            ts_str = ts_str.replace("Z", "")
            timestamp_dt = datetime.fromisoformat(ts_str)
        else:
            timestamp_dt = datetime.utcnow()

        # Crear la nueva instancia del modelo
        nueva_ubicacion = Ubicacion(
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            accuracy=data.get("accuracy"),
            altitude=data.get("altitude"),
            speed=data.get("speed"),
            heading=data.get("heading"),
            timestamp=timestamp_dt
        )
        
        # Guardar en la base de datos
        db.session.add(nueva_ubicacion)
        db.session.commit()
        
        # Retornar estatus 200 con un mensaje de éxito
        return jsonify({"message": "Ubicación guardada con éxito", "id": nueva_ubicacion.id}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al guardar: {str(e)}"}), 500


if __name__ == "__main__":
    # Crear las tablas automáticamente si no existen (útil para desarrollo)
    with app.app_context():
        db.create_all()
        
    print(f"running debug as {DEBUG}")
    app.run(debug=DEBUG)
