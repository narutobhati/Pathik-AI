from flask import Flask
from config import Config
from extensions import db
from models.campaign import Campaign
from extensions import db, migrate

from routes.campaigns import campaigns_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(campaigns_bp, url_prefix="/api/campaigns")

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
