"""
Utility functions for SpaceBuy interplanetary e-commerce platform
"""

import random
import math

def calculate_delivery_cost(base_price, planet_info):
    """
    Calculate delivery cost based on planet characteristics
    """
    # Base factors
    distance_factor = planet_info['distance'] ** 1.5  # Distance has exponential impact
    gravity_factor = abs(planet_info['gravity'] - 1.0) + 1.0  # Deviation from Earth gravity
    difficulty_factor = planet_info['delivery_difficulty'] / 10.0
    
    # Special atmosphere considerations
    atmosphere_multipliers = {
        'None': 2.5,  # Need life support
        'Toxic': 4.0,  # Hazmat protocols
        'Thin': 1.8,  # Partial life support
        'Dense': 3.0,  # Pressure suits
        'Icy': 2.2,   # Heating systems
        'Plasma': 10.0  # Impossible but we'll try
    }
    
    atmosphere_key = 'None'  # Default
    for key in atmosphere_multipliers:
        if key.lower() in planet_info['atmosphere'].lower():
            atmosphere_key = key
            break
    
    atmosphere_factor = atmosphere_multipliers[atmosphere_key]
    
    # Calculate base delivery cost
    base_delivery = base_price * 0.5  # Start with 50% of product price
    
    # Apply all factors
    delivery_cost = (base_delivery * 
                    distance_factor * 
                    gravity_factor * 
                    difficulty_factor * 
                    atmosphere_factor)
    
    # Add some randomness for "market conditions"
    market_volatility = random.uniform(0.8, 1.3)
    delivery_cost *= market_volatility
    
    # Minimum delivery cost (even to the Moon costs something)
    minimum_delivery = base_price * 0.1
    delivery_cost = max(delivery_cost, minimum_delivery)
    
    # Special case for Sun - astronomical costs
    if 'sun' in planet_info.get('fun_fact', '').lower() or planet_info.get('delivery_difficulty', 0) >= 10:
        delivery_cost *= 50  # Because it's literally the Sun
    
    return round(delivery_cost, 2)

def format_price(price):
    """
    Format price as currency in Indian Rupees with appropriate formatting for large numbers
    """
    # Convert USD to INR (approximate rate: 1 USD = 83 INR)
    inr_price = price * 83
    
    if inr_price >= 100_000_000_000:  # 100+ Billion INR
        return f"₹{inr_price:,.0f} (💸 BANKRUPTCY LEVEL)"
    elif inr_price >= 10_000_000_000:  # 10+ Billion INR
        return f"₹{inr_price/10_000_000:.1f} Cr (🏠 MORTGAGE YOUR HOUSE)"
    elif inr_price >= 100_000_000:  # 10+ Crore INR
        return f"₹{inr_price/10_000_000:.1f} Cr (🚗 SELL YOUR CAR)"
    elif inr_price >= 10_000_000:  # 1+ Crore INR
        return f"₹{inr_price/10_000_000:.2f} Cr (💳 MAX OUT CREDIT CARDS)"
    elif inr_price >= 100_000:  # 1+ Lakh INR
        return f"₹{inr_price/100_000:.1f} L (💰 EXPENSIVE)"
    elif inr_price >= 1_000:  # Thousands INR
        return f"₹{inr_price:,.0f}"
    else:
        return f"₹{inr_price:,.2f}"

def get_shipping_humor(planet_name, delivery_cost):
    """
    Generate humorous shipping messages based on cost and destination
    """
    # Convert to INR for comparison
    inr_cost = delivery_cost * 83
    
    if inr_cost > 83_000_000:  # 83M INR (1M USD)
        messages = [
            f"🚀 Shipping to {planet_name}: More expensive than a small nation's GDP!",
            f"💸 Fun fact: You could buy a private island instead of shipping to {planet_name}!",
            f"🏦 Your bank called - they want to discuss your {planet_name} shopping addiction.",
            f"⭐ Congratulations! You've unlocked the 'Cosmic Spender' achievement!"
        ]
    elif inr_cost > 8_300_000:  # 83L INR (100K USD)
        messages = [
            f"🎯 Shipping to {planet_name}: Costs more than most luxury cars in India!",
            f"📈 Investment tip: SpaceBuy stock goes up every time someone ships to {planet_name}!",
            f"🎓 You could fund multiple engineering degrees for this shipping cost!",
            f"🏠 Alternatively, you could buy a nice flat in Mumbai for this price!"
        ]
    elif inr_cost > 830_000:  # 8.3L INR (10K USD)
        messages = [
            f"💰 Shipping to {planet_name}: Expensive enough to make you question your priorities!",
            f"🎪 For this price, we could hire a Bollywood dance troupe to deliver your package!",
            f"📱 You could buy 10 iPhones instead of paying this shipping cost!",
            f"🛺 We could probably auto-rickshaw your package around India 1000 times for this price!"
        ]
    else:
        messages = [
            f"✨ Shipping to {planet_name}: Surprisingly reasonable for interplanetary delivery!",
            f"🎉 Great news! This shipping cost won't completely bankrupt you!",
            f"💡 Pro tip: {planet_name} is practically next door in cosmic terms!",
            f"🌟 Budget-friendly space delivery - your wallet will thank you!"
        ]
    
    return random.choice(messages)

def calculate_estimated_delivery_time(planet_info):
    """
    Calculate realistic delivery time based on distance and current technology
    """
    distance_au = planet_info['distance']
    
    # Assume average spacecraft speed of 20 km/s (realistic for cargo missions)
    # 1 AU = 149,597,870.7 km
    km_distance = distance_au * 149_597_870.7
    speed_km_per_second = 20
    
    # Calculate travel time in seconds
    travel_time_seconds = km_distance / speed_km_per_second
    
    # Convert to days
    travel_time_days = travel_time_seconds / (24 * 3600)
    
    # Double it for round trip planning and add processing time
    total_days = (travel_time_days * 2) + random.randint(30, 90)  # Processing time
    
    # Format as human-readable time
    if total_days < 365:
        return f"{int(total_days)} days"
    else:
        years = total_days / 365
        if years < 2:
            return f"{years:.1f} year"
        else:
            return f"{years:.1f} years"

def get_planet_emoji(planet_name):
    """
    Get appropriate emoji for each planet
    """
    planet_emojis = {
        'mercury': '☿️',
        'venus': '♀️',
        'earth': '🌍',
        'mars': '🔴',
        'jupiter': '🪐',
        'saturn': '🪐',
        'uranus': '🟦',
        'neptune': '🔵',
        'pluto': '⚫',
        'sun': '☀️',
        'moon': '🌙'
    }
    
    return planet_emojis.get(planet_name.lower(), '🪐')

def generate_tracking_number():
    """
    Generate a space-themed tracking number
    """
    prefixes = ['SPACE', 'COSMIC', 'STELLAR', 'GALAX', 'ORBIT', 'NEBULA']
    numbers = ''.join([str(random.randint(0, 9)) for _ in range(8)])
    return f"{random.choice(prefixes)}-{numbers}"

def calculate_carbon_footprint(planet_info, delivery_cost):
    """
    Calculate the absurdly high carbon footprint of interplanetary delivery
    """
    # Base rocket fuel consumption
    distance_au = planet_info['distance']
    fuel_consumption = distance_au * 1000000  # Arbitrary large number
    
    # Convert to CO2 emissions (rocket fuel is very dirty)
    co2_tons = fuel_consumption * 3.14  # Pi makes everything more scientific
    
    # Add atmosphere entry/exit costs
    if 'None' not in planet_info['atmosphere']:
        co2_tons *= 2  # Double for atmospheric entry
    
    return {
        'co2_tons': round(co2_tons, 2),
        'trees_needed': round(co2_tons * 16),  # Trees needed to offset
        'comparison': f"Equivalent to driving around Earth {round(co2_tons / 4.6)} times"
    }

def get_insurance_disclaimer(planet_name, planet_info):
    """
    Generate appropriate insurance disclaimers for each planet
    """
    disclaimers = {
        'sun': "⚠️ EXTREME RISK: 100% chance of package vaporization. Insurance void due to laws of physics.",
        'venus': "☠️ HIGH RISK: Sulfuric acid damage not covered. Package may arrive as toxic sludge.",
        'jupiter': "🌪️ MODERATE RISK: Crushing atmospheric pressure may compress package to atomic level.",
        'mercury': "🔥❄️ EXTREME RISK: Thermal shock may cause package to simultaneously melt and freeze.",
        'mars': "🟤 LOW RISK: Dust storms may delay delivery by several decades.",
        'saturn': "💍 MODERATE RISK: Package may get stuck in rings. Retrieval missions extra.",
        'uranus': "💨 MODERATE RISK: Methane atmosphere may cause unpleasant odors upon opening.",
        'neptune': "🌊 HIGH RISK: Supersonic winds may scatter package across multiple dimensions.",
        'pluto': "🥶 LOW RISK: Package may be perfectly preserved in ice for millions of years.",
        'moon': "🌙 VERY LOW RISK: Lowest insurance rates in the solar system!"
    }
    
    planet_key = planet_name.lower()
    return disclaimers.get(planet_key, 
        f"⚠️ UNKNOWN RISK: {planet_name} delivery insurance calculated by space lawyers.")
