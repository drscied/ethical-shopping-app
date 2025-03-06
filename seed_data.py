from app import create_app, db
from app.models import Company, Product, ProductAlternative, RetailLocation
from datetime import datetime

def seed_data():
    app = create_app()
    with app.app_context():
        # Create companies
        goya = Company(
            name='Goya Foods',
            political_affiliation='Republican',
            trump_support_score=0.9,
            last_updated=datetime.utcnow()
        )
        
        eden = Company(
            name='Eden Foods',
            political_affiliation='Neutral',
            trump_support_score=0.2,
            last_updated=datetime.utcnow()
        )
        
        db.session.add_all([goya, eden])
        db.session.commit()
        
        # Create products
        goya_beans = Product(
            name='Goya Black Beans',
            company_id=goya.id,
            category='Canned Goods',
            description='Premium black beans',
            image_url='https://example.com/goya-beans.jpg'
        )
        
        eden_beans = Product(
            name='Eden Organic Black Beans',
            company_id=eden.id,
            category='Canned Goods',
            description='Organic black beans, sustainably farmed',
            image_url='https://example.com/eden-beans.jpg'
        )
        
        db.session.add_all([goya_beans, eden_beans])
        db.session.commit()
        
        # Create alternative product relationship
        alt = ProductAlternative(
            product_id=goya_beans.id,
            alternative_product_id=eden_beans.id,
            similarity_score=0.95,
            price_comparison={
                'average_price_difference': -0.50,
                'sustainability_score': 0.9
            }
        )
        
        db.session.add(alt)
        db.session.commit()
        
        # Add retail locations
        locations = [
            RetailLocation(
                product_id=eden_beans.id,
                retailer_name='Whole Foods',
                price=2.49,
                availability=True,
                location_type='physical',
                address='123 Market St, San Francisco, CA'
            ),
            RetailLocation(
                product_id=eden_beans.id,
                retailer_name='Amazon',
                price=1.99,
                availability=True,
                location_type='online',
                url='https://amazon.com/eden-beans'
            )
        ]
        
        db.session.add_all(locations)
        db.session.commit()
        
        print('Sample data has been seeded!')
