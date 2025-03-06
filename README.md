# Ethical Shopping Assistant

An AI-powered app that helps consumers make informed purchasing decisions based on companies' political affiliations, focusing on identifying companies that support the Trump administration and providing ethical alternatives.

## Features

- Product search functionality using OpenFoodFacts API
- Company political alignment scoring system
- Alternative product recommendations
- Comprehensive brand hierarchy mapping
- Dynamic product information display

## Tech Stack

- Backend: Flask (Python)
- Database: PostgreSQL (Production) / SQLite (Development)
- Frontend: HTML, JavaScript, Tailwind CSS
- External API: OpenFoodFacts

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   SECRET_KEY=your_secret_key
   ```
5. Initialize the database:
   ```bash
   python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
   ```
6. Seed sample data:
   ```bash
   python seed_data.py
   ```
7. Run the development server:
   ```bash
   flask run
   ```

## Deployment

This application is configured for deployment on Render.com:

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn "app:create_app()"`
4. Add environment variables:
   - `SECRET_KEY`: Your secret key
   - `DATABASE_URL`: Your PostgreSQL database URL (Render will provide this if you create a PostgreSQL database)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License
