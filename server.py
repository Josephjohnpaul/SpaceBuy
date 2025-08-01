#!/usr/bin/env python3
"""
SpaceBuy Web Server - Flask Backend API
Serves the HTML/CSS/JS frontend and provides API endpoints
"""

from flask import Flask, jsonify, request, send_from_directory, send_file
import os
import json
import uuid
from datetime import datetime
import random

# Import existing modules
from data import get_products, get_planets, get_space_agencies, get_planet_exclusive_products
from ai_pricing import get_ai_pricing, generate_product_description
from utils import calculate_delivery_cost, format_price, generate_tracking_number, calculate_estimated_delivery_time
import web_db_utils as db_utils

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'space-buy-secret-key')

# Ensure static directory exists
os.makedirs('static', exist_ok=True)

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_file('static/index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files (CSS, JS, images)"""
    return send_from_directory('static', filename)

# API Routes
@app.route('/api/products')
def api_products():
    """Get all products"""
    try:
        products = get_products()
        return jsonify(products)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/planets')
def api_planets():
    """Get all planets"""
    try:
        planets = get_planets()
        return jsonify(planets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/agencies')
def api_agencies():
    """Get all space agencies"""
    try:
        agencies = get_space_agencies()
        return jsonify(agencies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/exclusive-products')
def api_exclusive_products():
    """Get planet exclusive products"""
    try:
        exclusive = get_planet_exclusive_products()
        return jsonify(exclusive)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle user login/registration"""
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        planet_pref = data.get('planet_pref')
        
        if not name or not email:
            return jsonify({'error': 'Name and email are required'}), 400
        
        # Create or get user
        user_data = db_utils.create_user(name, email, planet_pref)
        if user_data:
            return jsonify(user_data)
        else:
            return jsonify({'error': 'Login failed'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def api_create_order():
    """Create a new order"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        product_name = data.get('product_name')
        destination_planet = data.get('destination_planet')
        total_price_inr = data.get('total_price_inr')
        space_agency = data.get('space_agency')
        is_exclusive = data.get('is_exclusive', False)
        
        if not all([user_id, product_name, destination_planet, total_price_inr, space_agency]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Generate tracking number and delivery time
        tracking_number = generate_tracking_number()
        
        if is_exclusive:
            estimated_delivery_time = "Same day"
            base_price_usd = total_price_inr / 83  # Convert back to USD
            delivery_cost_usd = 0.0
        else:
            planets = get_planets()
            planet_info = planets.get(destination_planet)
            if planet_info:
                estimated_delivery_time = calculate_estimated_delivery_time(planet_info)
                base_price_usd = (total_price_inr / 83) * 0.2  # Estimate base price
                delivery_cost_usd = (total_price_inr / 83) * 0.8  # Rest is delivery
            else:
                estimated_delivery_time = "Unknown"
                base_price_usd = total_price_inr / 83
                delivery_cost_usd = 0.0
        
        # Create order in database
        order_id = db_utils.create_order(
            user_id=user_id,
            product_name=product_name,
            product_category="General",  # Could be improved
            destination_planet=destination_planet,
            base_price_usd=base_price_usd,
            delivery_cost_usd=delivery_cost_usd,
            total_price_inr=total_price_inr,
            space_agency=space_agency,
            estimated_delivery_time=estimated_delivery_time,
            tracking_number=tracking_number
        )
        
        if order_id:
            return jsonify({
                'order_id': order_id,
                'tracking_number': tracking_number,
                'estimated_delivery_time': estimated_delivery_time
            })
        else:
            return jsonify({'error': 'Failed to create order'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/orders/<int:user_id>')
def api_get_user_orders(user_id):
    """Get orders for a specific user"""
    try:
        orders = db_utils.get_user_orders(user_id)
        return jsonify(orders)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai-search', methods=['POST'])
def api_ai_search():
    """Handle AI product search"""
    try:
        data = request.get_json()
        product_query = data.get('product_query')
        target_planet = data.get('target_planet')
        user_session = data.get('user_session', str(uuid.uuid4()))
        
        if not product_query or not target_planet:
            return jsonify({'error': 'Product query and target planet are required'}), 400
        
        # Get planet info
        planets = get_planets()
        planet_info = planets.get(target_planet)
        if not planet_info:
            return jsonify({'error': 'Invalid planet'}), 400
        
        # Get AI-generated product info and pricing
        try:
            product_description = generate_product_description(product_query, target_planet)
            ai_price = get_ai_pricing(product_query, planet_info)
            
            # Calculate total price
            delivery_cost = calculate_delivery_cost(ai_price['base_price'], planet_info)
            total_price = ai_price['base_price'] + delivery_cost
            
            # Add to search history
            db_utils.add_search_history(product_query, target_planet, total_price, user_session)
            
            return jsonify({
                'product_query': product_query,
                'target_planet': target_planet,
                'product_description': product_description,
                'base_price': ai_price['base_price'],
                'total_price': total_price,
                'multiplier': ai_price['multiplier'],
                'reasoning': ai_price['reasoning']
            })
            
        except Exception as ai_error:
            # Fallback to mock pricing if AI fails
            mock_price = random.uniform(50, 500)
            delivery_cost = calculate_delivery_cost(mock_price, planet_info)
            total_price = mock_price + delivery_cost
            
            return jsonify({
                'product_query': product_query,
                'target_planet': target_planet,
                'product_description': f"A {product_query} suitable for use on {target_planet}. Our AI is currently taking a coffee break, so here's our best guess!",
                'base_price': mock_price,
                'total_price': total_price,
                'multiplier': round(delivery_cost / mock_price, 1),
                'reasoning': f"Our AI is having space-sickness, so we used our backup pricing algorithm. Shipping to {target_planet} is still ridiculously expensive though!"
            })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics')
def api_analytics():
    """Get analytics data"""
    try:
        analytics = db_utils.get_analytics_data()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'SpaceBuy API'})

if __name__ == '__main__':
    # Ensure database is initialized
    try:
        db_utils.init_database()
        print("✅ Database initialized successfully")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
    
    # Run the server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Starting SpaceBuy server on port {port}")
    print(f"🌐 Access the application at: http://0.0.0.0:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)