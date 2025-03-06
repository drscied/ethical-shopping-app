from flask import Flask
from dotenv import load_dotenv
import os
from .extensions import db, migrate

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    
    # Ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Configure database based on environment
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        # Handle Render's "postgres://" vs "postgresql://" difference
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        # Development SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'ethical_shopping.db')
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .routes import main, api
    app.register_blueprint(main.bp)
    app.register_blueprint(api.bp)
    
    return app
