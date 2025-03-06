from flask import Blueprint, request, jsonify
from ..models import db, Company, PoliticalDonation, Product, RetailLocation
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/update-company-data', methods=['POST'])
def update_company_data():
    data = request.get_json()
    if not data or 'company_name' not in data:
        return jsonify({'error': 'Company name is required'}), 400
        
    company = Company.query.filter_by(name=data['company_name']).first()
    if not company:
        company = Company(name=data['company_name'])
        db.session.add(company)
    
    # Update company data
    if 'political_affiliation' in data:
        company.political_affiliation = data['political_affiliation']
    if 'trump_support_score' in data:
        company.trump_support_score = data['trump_support_score']
    
    company.last_updated = datetime.utcnow()
    
    # Add new donation if provided
    if 'donation' in data:
        donation = PoliticalDonation(
            company_id=company.id,
            amount=data['donation']['amount'],
            recipient=data['donation']['recipient'],
            date=datetime.fromisoformat(data['donation']['date']),
            source=data['donation']['source']
        )
        db.session.add(donation)
    
    db.session.commit()
    return jsonify({'message': 'Company data updated successfully'})

@bp.route('/report-finding', methods=['POST'])
def report_finding():
    data = request.get_json()
    if not data or 'company_name' not in data or 'evidence_url' not in data:
        return jsonify({'error': 'Company name and evidence URL are required'}), 400
    
    # Here you would implement verification logic and update the database
    # For now, we'll just store the report
    return jsonify({'message': 'Finding reported and pending verification'})

@bp.route('/update-prices', methods=['POST'])
def update_prices():
    data = request.get_json()
    if not data or 'product_id' not in data or 'prices' not in data:
        return jsonify({'error': 'Product ID and prices are required'}), 400
    
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Update retail locations with new prices
    for price_data in data['prices']:
        location = RetailLocation.query.filter_by(
            product_id=product.id,
            retailer_name=price_data['retailer']
        ).first()
        
        if location:
            location.price = price_data['price']
            location.availability = price_data['available']
            location.last_updated = datetime.utcnow()
    
    db.session.commit()
    return jsonify({'message': 'Prices updated successfully'})
