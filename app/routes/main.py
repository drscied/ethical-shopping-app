from flask import Blueprint, render_template, request, jsonify
from ..models import Product, Company, ProductAlternative, RetailLocation
from ..extensions import db
import requests
import re

bp = Blueprint('main', __name__, url_prefix='')

def get_parent_company(brand_name):
    # Comprehensive mapping of brands to their parent companies
    company_hierarchy = {
        'pepsico': {
            'name': 'PepsiCo',
            'trump_support_score': 0.7,
            'alternatives': ['Late July', 'Kettle Brand', "Newman's Own"],
            'brands': [
                'pepsi', 'frito-lay', 'doritos', 'cheetos', 'lays', 'tostitos', 'fritos', 
                'mountain dew', 'gatorade', 'tropicana', 'quaker', 'aquafina', 'lipton',
                'ruffles', 'pepsi max', 'sierra mist', 'sunchips', 'sabra'
            ]
        },
        'coca-cola': {
            'name': 'Coca-Cola Company',
            'trump_support_score': 0.6,
            'alternatives': ['Zevia', 'Blue Sky', 'Jones Soda'],
            'brands': [
                'coke', 'sprite', 'fanta', 'dasani', 'minute maid', 'powerade',
                'vitaminwater', 'smartwater', 'honest tea', 'costa coffee',
                'simply orange', 'fairlife', 'peace tea'
            ]
        },
        'goya': {
            'name': 'Goya Foods',
            'trump_support_score': 0.9,
            'alternatives': ['Iberia', 'La Preferida', 'Trader Joes'],
            'brands': ['goya', 'good o', 'tropical']
        },
        'kellogg': {
            'name': "Kellogg's",
            'trump_support_score': 0.3,
            'alternatives': [],
            'brands': [
                'kelloggs', 'pringles', 'cheez-it', 'rice krispies', 'pop-tarts', 
                'eggo', 'nutri-grain', 'morningstar farms', 'special k', 'frosted flakes',
                'froot loops', 'corn flakes', 'apple jacks'
            ]
        },
        'general mills': {
            'name': 'General Mills',
            'trump_support_score': 0.4,
            'alternatives': [],
            'brands': [
                'cheerios', 'pillsbury', 'betty crocker', 'nature valley', 'yoplait',
                'häagen-dazs', 'old el paso', 'progresso', "annie's", 'cascadian farm',
                'lucky charms', 'trix', 'chex', 'cinnamon toast crunch'
            ]
        },
        'kraft heinz': {
            'name': 'Kraft Heinz',
            'trump_support_score': 0.6,
            'alternatives': ['Annie\'s', 'Field Roast', 'Follow Your Heart'],
            'brands': [
                'kraft', 'heinz', 'oscar mayer', 'philadelphia', 'velveeta', 'planters',
                'maxwell house', 'capri sun', 'kool-aid', 'jell-o', 'miracle whip',
                'crystal light', 'classico', 'ore-ida'
            ]
        },
        'nestle': {
            'name': 'Nestlé',
            'trump_support_score': 0.7,
            'alternatives': ['Endangered Species', 'Tony\'s Chocolonely', 'Theo Chocolate'],
            'brands': [
                'nestle', 'nescafe', 'nespresso', 'kitkat', 'gerber', 'perrier', 
                'san pellegrino', 'poland spring', 'stouffers', 'lean cuisine', 'hot pockets',
                'coffee mate', 'nesquik', 'butterfinger', 'crunch', 'purina', 'fancy feast'
            ]
        }
    }
    
    # Alternative brands with their political scores
    alternative_brands = {
        'late july': {'name': 'Late July Snacks', 'trump_support_score': 0.2},
        'kettle': {'name': 'Kettle Brand', 'trump_support_score': 0.3},
        'newmans own': {'name': "Newman's Own", 'trump_support_score': 0.1},
        'zevia': {'name': 'Zevia', 'trump_support_score': 0.2},
        'blue sky': {'name': 'Blue Sky Beverages', 'trump_support_score': 0.3},
        'boylan': {'name': 'Boylan Bottling', 'trump_support_score': 0.2},
        'jones': {'name': 'Jones Soda Co.', 'trump_support_score': 0.3},
        'iberia': {'name': 'Iberia Foods', 'trump_support_score': 0.4},
        'la preferida': {'name': 'La Preferida', 'trump_support_score': 0.3},
        'trader joes': {'name': 'Trader Joes', 'trump_support_score': 0.2},
        'annies': {'name': "Annie's Homegrown", 'trump_support_score': 0.2},
        'field roast': {'name': 'Field Roast', 'trump_support_score': 0.3},
        'follow your heart': {'name': 'Follow Your Heart', 'trump_support_score': 0.2},
        'endangered species': {'name': 'Endangered Species Chocolate', 'trump_support_score': 0.1},
        'tonys chocolonely': {'name': "Tony's Chocolonely", 'trump_support_score': 0.2},
        'theo chocolate': {'name': 'Theo Chocolate', 'trump_support_score': 0.3}
    }
    
    # Normalize brand name for matching
    brand_name = brand_name.lower().strip()
    
    # First check if this is a parent company name
    for company_key, company_data in company_hierarchy.items():
        if company_key in brand_name:
            return company_data
    
    # Then check if this is a brand owned by a parent company
    for company_data in company_hierarchy.values():
        for brand in company_data['brands']:
            if brand in brand_name or brand_name in brand:
                return company_data
    
    # Finally check alternative brands
    for alt_brand, alt_data in alternative_brands.items():
        if alt_brand in brand_name or brand_name in alt_brand:
            return alt_data
            
    return {'name': brand_name.title(), 'trump_support_score': 0.5, 'alternatives': []}

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/search', methods=['POST'])
def search():
    product_name = request.form.get('product_name')
    if not product_name:
        return jsonify({'error': 'Product name is required'}), 400
        
    # First try our database
    product = Product.query.filter(Product.name.ilike(f'%{product_name}%')).first()
    
    if not product:
        # Query OpenFoodFacts API
        search_url = f'https://world.openfoodfacts.org/cgi/search.pl?search_terms={product_name}&json=1'
        try:
            response = requests.get(search_url)
            data = response.json()
            
            if data['products']:
                product_data = data['products'][0]
                brand_name = product_data.get('brands', '').split(',')[0]
                
                # Get the parent company information
                company_data = get_parent_company(brand_name)
                if not company_data:
                    company_data = get_parent_company(product_name)  # Try with product name if brand not found
                
                # Create temporary company
                company = Company(
                    name=company_data['name'],
                    political_affiliation='Republican' if company_data['trump_support_score'] > 0.5 else 'Democrat',
                    trump_support_score=company_data['trump_support_score']
                )
                
                # Create temporary product
                product = Product(
                    name=product_data.get('product_name', product_name),
                    company=company,
                    category=product_data.get('categories', '').split(',')[0],
                    description=product_data.get('generic_name', ''),
                    image_url=product_data.get('image_url', '')
                )
            else:
                return jsonify({'error': 'Product not found'}), 404
                
        except requests.exceptions.RequestException:
            return jsonify({'error': 'Failed to fetch product information'}), 500
    
    company = product.company
    is_trump_supporter = company.trump_support_score > 0.5
    
    # Get alternative products if company supports Trump
    alternatives = []
    if is_trump_supporter:
        # Get predefined alternatives for the parent company
        company_data = get_parent_company(company.name)
        predefined_alternatives = company_data.get('alternatives', [])
        
        for alt_brand in predefined_alternatives:
            alt_company_data = get_parent_company(alt_brand)
            
            # Search OpenFoodFacts for this brand's products
            try:
                alt_search_url = f'https://world.openfoodfacts.org/cgi/search.pl?brands={alt_brand}&json=1'
                alt_response = requests.get(alt_search_url)
                alt_data = alt_response.json()
                
                if alt_data['products']:
                    alt_product_data = alt_data['products'][0]
                    
                    alternatives.append({
                        'product': {
                            'name': alt_product_data.get('product_name', f'{alt_brand} Alternative'),
                            'description': f'A better alternative from {alt_company_data["name"]}, a company that does not support the Trump administration.',
                            'image_url': alt_product_data.get('image_url', '')
                        },
                        'company': alt_company_data['name'],
                        'similarity_score': 0.9,
                        'retailers': [
                            {
                                'name': 'Amazon',
                                'price': 0.00,
                                'url': f"https://www.amazon.com/s?k={alt_brand.replace(' ', '+')}+{product.category.replace(' ', '+') if hasattr(product, 'category') and product.category else ''}",
                                'address': None
                            },
                            {
                                'name': 'Whole Foods',
                                'price': 0.00,
                                'url': None,
                                'address': 'Find at your local Whole Foods'
                            }
                        ]
                    })
            except:
                # If API fails, still add the brand as a suggestion
                alternatives.append({
                    'product': {
                        'name': f'{alt_brand} Products',
                        'description': f'Try products from {alt_company_data["name"]}, a company that does not support the Trump administration.',
                        'image_url': ''
                    },
                    'company': alt_company_data['name'],
                    'similarity_score': 0.9,
                    'retailers': [
                        {
                            'name': 'Amazon',
                            'price': 0.00,
                            'url': f"https://www.amazon.com/s?k={alt_brand.replace(' ', '+')}",
                            'address': None
                        }
                    ]
                })
    
    return jsonify({
        'product': {
            'name': product.name,
            'company': company.name,
            'is_trump_supporter': is_trump_supporter,
            'support_score': company.trump_support_score
        },
        'alternatives': alternatives
    })
