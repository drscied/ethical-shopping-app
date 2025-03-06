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
    if os.getenv('DATABASE_URL'):
        # Production database URL from environment variable
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace('postgres://', 'postgresql://')
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
