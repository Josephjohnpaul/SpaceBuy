"""
AI-powered pricing system using Gemini AI for dynamic interplanetary pricing
"""

import os
import json
import random
from google import genai
from google.genai import types

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "default_gemini_key"))

def get_ai_pricing(product_name, planet_info):
    """
    Use Gemini AI to generate realistic pricing for products on different planets
    """
    try:
        prompt = f"""
        You are a cosmic pricing expert for SpaceBuy, an interplanetary e-commerce platform.
        
        Calculate a realistic price for "{product_name}" to be delivered to a planet with these characteristics:
        - Distance from Earth: {planet_info['distance']} AU
        - Gravity: {planet_info['gravity']}g (compared to Earth)
        - Atmosphere: {planet_info['atmosphere']}
        - Delivery Difficulty: {planet_info['delivery_difficulty']}/10
        
        Consider factors like:
        1. Base Earth retail price for this product
        2. Shipping complexity based on distance and conditions
        3. Special handling requirements for the atmosphere/gravity
        4. Insurance costs for high-risk deliveries
        5. Fuel costs proportional to distance and gravity
        
        Respond with JSON in this exact format:
        {{
            "base_price": [estimated Earth price in USD],
            "multiplier": [price multiplier for this planet, between 2x and 50x],
            "reasoning": "[funny but logical explanation for the pricing]"
        }}
        
        Make the reasoning humorous but scientifically plausible. Be creative!
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        if response.text:
            pricing_data = json.loads(response.text)
            # Validate response structure
            if all(key in pricing_data for key in ['base_price', 'multiplier', 'reasoning']):
                return pricing_data
        
        # Fallback if AI response is invalid
        return get_fallback_pricing(product_name, planet_info)
        
    except Exception as e:
        print(f"AI Pricing Error: {e}")
        return get_fallback_pricing(product_name, planet_info)

def generate_product_description(product_name, planet_name):
    """
    Generate AI-powered product descriptions adapted for interplanetary delivery
    """
    try:
        prompt = f"""
        You are a creative copywriter for SpaceBuy, an interplanetary e-commerce platform.
        
        Write a humorous but detailed product description for "{product_name}" that will be delivered to {planet_name}.
        
        Include:
        1. What the product is and its main features
        2. How it's been adapted or modified for use on {planet_name}
        3. Any special considerations or warnings for interplanetary use
        4. A funny disclaimer or warning
        
        Keep it engaging, funny, and about 3-4 sentences long.
        Write in a marketing style but with space-themed humor.
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        if response.text:
            return response.text.strip()
        else:
            return get_fallback_description(product_name, planet_name)
            
    except Exception as e:
        print(f"AI Description Error: {e}")
        return get_fallback_description(product_name, planet_name)

def get_fallback_pricing(product_name, planet_info):
    """
    Fallback pricing when AI is unavailable
    """
    # Estimate base price based on product type keywords
    base_price = 50.0  # Default
    product_lower = product_name.lower()
    
    if any(word in product_lower for word in ['iphone', 'phone', 'smartphone']):
        base_price = 999.0
    elif any(word in product_lower for word in ['tesla', 'car', 'vehicle']):
        base_price = 50000.0
    elif any(word in product_lower for word in ['coffee', 'latte', 'drink']):
        base_price = 5.0
    elif any(word in product_lower for word in ['laptop', 'computer', 'macbook']):
        base_price = 1500.0
    elif any(word in product_lower for word in ['pizza', 'food']):
        base_price = 15.0
    elif any(word in product_lower for word in ['watch', 'rolex']):
        base_price = 5000.0
    
    # Calculate multiplier based on planet difficulty
    difficulty = planet_info.get('delivery_difficulty', 5.0)
    distance = planet_info.get('distance', 1.0)
    
    multiplier = max(2.0, difficulty * distance * random.uniform(0.8, 1.2))
    
    reasons = [
        f"Extreme shipping costs due to {planet_info['distance']} AU distance and {planet_info['atmosphere']} atmosphere",
        f"Special packaging required for {planet_info['gravity']}g gravity conditions",
        f"Insurance premiums skyrocketed due to {difficulty}/10 delivery difficulty rating",
        f"Fuel costs alone could buy a small country due to the journey to this hostile environment"
    ]
    
    return {
        'base_price': base_price,
        'multiplier': round(multiplier, 1),
        'reasoning': random.choice(reasons)
    }

def get_fallback_description(product_name, planet_name):
    """
    Fallback product description when AI is unavailable
    """
    descriptions = [
        f"The {product_name} has been specially modified for {planet_name} conditions. Features include radiation shielding, temperature regulation, and a built-in prayer function. Warning: May cause existential crisis when you realize how much you paid for shipping.",
        f"Experience {product_name} like never before - on {planet_name}! This interplanetary edition includes cosmic dust protection and gravity-adjustment features. Side effects may include questioning your life choices and bankruptcy.",
        f"Bringing you {product_name} across the vast emptiness of space to {planet_name}. Enhanced with space-grade materials and hope. Disclaimer: Product may arrive as cosmic dust, but at least you'll have a great story to tell."
    ]
    
    return random.choice(descriptions)
