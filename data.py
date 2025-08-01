"""
Mock data for SpaceBuy interplanetary e-commerce platform
"""

def get_products():
    """Returns a list of Earth products available for interplanetary delivery"""
    return [
        {
            'name': 'iPhone 15 Pro Max',
            'emoji': '📱',
            'description': 'Latest smartphone with space-grade aluminum. Warning: May not work in vacuum of space.',
            'category': 'Electronics',
            'base_price': 1199.99
        },
        {
            'name': 'Tesla Model S Plaid',
            'emoji': '🚗',
            'description': 'Electric vehicle adapted for planetary surfaces. Includes magnetic wheels for low-gravity environments.',
            'category': 'Vehicles',
            'base_price': 89990.00
        },
        {
            'name': 'Starbucks Venti Latte',
            'emoji': '☕',
            'description': 'Premium coffee beverage. May freeze instantly in space. Warming systems sold separately.',
            'category': 'Food & Beverages',
            'base_price': 5.95
        },
        {
            'name': 'Nintendo Switch OLED',
            'emoji': '🎮',
            'description': 'Portable gaming console. Perfect for long space journeys. Battery life: 3 hours or 3 light-years.',
            'category': 'Electronics',
            'base_price': 349.99
        },
        {
            'name': 'MacBook Pro M3',
            'emoji': '💻',
            'description': 'High-performance laptop with space-resistant screen. Cosmic ray damage not covered by warranty.',
            'category': 'Electronics',
            'base_price': 2399.99
        },
        {
            'name': 'Air Jordan 4 Retro',
            'emoji': '👟',
            'description': 'Classic basketball shoes. Anti-gravity soles available for Jupiter deliveries at extra cost.',
            'category': 'Fashion',
            'base_price': 200.00
        },
        {
            'name': 'Dominos Large Pizza',
            'emoji': '🍕',
            'description': 'Hot and fresh pizza. Delivered hot or your money back! (Heat retention in space not guaranteed)',
            'category': 'Food & Beverages',
            'base_price': 15.99
        },
        {
            'name': 'IKEA Billy Bookshelf',
            'emoji': '📚',
            'description': 'Self-assembly furniture. Assembly instructions translated into 47 alien languages. Allen key included.',
            'category': 'Home & Garden',
            'base_price': 49.99
        },
        {
            'name': 'Rolex Submariner',
            'emoji': '⌚',
            'description': 'Luxury timepiece. Synchronized with galactic standard time. Works underwater and in vacuum.',
            'category': 'Fashion',
            'base_price': 8550.00
        },
        {
            'name': 'Amazon Echo Dot',
            'emoji': '🔊',
            'description': 'Smart speaker with Alexa. Now understands 12 alien languages. "Alexa, what\'s the weather on Mars?"',
            'category': 'Electronics',
            'base_price': 49.99
        },
        {
            'name': 'Instant Ramen',
            'emoji': '🍜',
            'description': 'Quick and easy meal. Just add hot water (bring your own heat source to space).',
            'category': 'Food & Beverages',
            'base_price': 0.99
        },
        {
            'name': 'Dyson V15 Vacuum',
            'emoji': '🌪️',
            'description': 'Powerful vacuum cleaner. Ironically useless in the vacuum of space. Great for spaceship interiors.',
            'category': 'Home & Garden',
            'base_price': 749.99
        }
    ]

def get_planets():
    """Returns information about delivery destinations"""
    return {
        'Mercury': {
            'distance': 0.39,
            'gravity': 0.38,
            'atmosphere': 'None (Extreme temperatures)',
            'delivery_difficulty': 9.5,
            'population': 0,
            'fun_fact': 'Hot enough to melt lead!'
        },
        'Venus': {
            'distance': 0.72,
            'gravity': 0.90,
            'atmosphere': 'Toxic (Sulfuric acid clouds)',
            'delivery_difficulty': 9.8,
            'population': 0,
            'fun_fact': 'Surface pressure could crush a submarine!'
        },
        'Mars': {
            'distance': 1.52,
            'gravity': 0.38,
            'atmosphere': 'Thin (Mostly CO2)',
            'delivery_difficulty': 7.2,
            'population': 7,  # SpaceX colonists
            'fun_fact': 'Home to the first interplanetary Starbucks!'
        },
        'Jupiter': {
            'distance': 5.20,
            'gravity': 2.36,
            'atmosphere': 'Dense (Crushing gas giant)',
            'delivery_difficulty': 9.9,
            'population': 0,
            'fun_fact': 'Packages delivered to floating platforms only!'
        },
        'Saturn': {
            'distance': 9.58,
            'gravity': 0.92,
            'atmosphere': 'Dense (Beautiful but deadly)',
            'delivery_difficulty': 9.7,
            'population': 0,
            'fun_fact': 'Ring delivery available for small packages!'
        },
        'Uranus': {
            'distance': 19.22,
            'gravity': 0.89,
            'atmosphere': 'Icy (Sideways rotation)',
            'delivery_difficulty': 8.8,
            'population': 0,
            'fun_fact': 'The planet that makes everyone giggle!'
        },
        'Neptune': {
            'distance': 30.05,
            'gravity': 1.13,
            'atmosphere': 'Icy (Supersonic winds)',
            'delivery_difficulty': 9.1,
            'population': 0,
            'fun_fact': 'Winds faster than the speed of sound!'
        },
        'Pluto': {
            'distance': 39.48,
            'gravity': 0.07,
            'atmosphere': 'Thin (Very cold)',
            'delivery_difficulty': 6.5,
            'population': 1,  # The lonely astronomer who still believes it's a planet
            'fun_fact': 'Still a planet in our hearts!'
        },
        'Sun': {
            'distance': 0.00,  # We're orbiting it!
            'gravity': 27.01,
            'atmosphere': 'Plasma (Nuclear fusion)',
            'delivery_difficulty': 10.0,
            'population': 0,
            'fun_fact': 'Our delivery record: 0% success rate, 100% vaporization rate!'
        },
        'Moon': {
            'distance': 0.0026,  # 384,400 km converted to AU
            'gravity': 0.17,
            'atmosphere': 'None (But great views)',
            'delivery_difficulty': 4.5,
            'population': 2,  # Secret lunar base
            'fun_fact': 'Cheese reserves confirmed to be fake!'
        }
    }

def get_space_agencies():
    """Returns information about delivery service providers"""
    return {
        'SpaceX Mars Division': {
            'motto': 'Making Mars Great Again, One Package at a Time',
            'reliability': '73% (When Elon tweets positively)',
            'delivery_time': '6-9 months (Earth-Mars only)',
            'specialty': 'Reusable rockets, unreusable packages'
        },
        'NASA Planetary Logistics': {
            'motto': 'We Put the Science in Delivery Science',
            'reliability': '94% (But very expensive)',
            'delivery_time': '2-5 years (Includes scientific study)',
            'specialty': 'Peer-reviewed delivery receipts'
        },
        'Blue Origin Express': {
            'motto': 'Gradatim Ferociter (Step by Step, Package by Package)',
            'reliability': '45% (Still figuring it out)',
            'delivery_time': '8-12 years (Under development)',
            'specialty': 'Space tourism for your packages'
        },
        'Virgin Galactic Courier': {
            'motto': 'Your Package\'s Space Adventure Awaits',
            'reliability': '67% (Weather dependent)',
            'delivery_time': '3-6 months (Suborbital only)',
            'specialty': 'Luxury space experience for premium items'
        },
        'Roscosmos Reliable': {
            'motto': 'In Soviet Space, Package Delivers You',
            'reliability': '89% (Built like a tank)',
            'delivery_time': '4-8 months (Via Soyuz truck)',
            'specialty': 'Vodka-resistant packaging'
        },
        'JAXA Precision Delivery': {
            'motto': 'Precision, Politeness, and Planetary Packages',
            'reliability': '97% (Extremely methodical)',
            'delivery_time': '1-3 years (Worth the wait)',
            'specialty': 'Origami-folded packages'
        },
        'ESA European Express': {
            'motto': 'United in Delivery, Diverse in Delays',
            'reliability': '82% (Bureaucracy slows us down)',
            'delivery_time': '6 months - 2 years (Committee dependent)',
            'specialty': 'Multi-language delivery confirmations'
        },
        'CNSA Cosmic Courier': {
            'motto': 'The Great Wall of Space Delivery',
            'reliability': '76% (Rapidly improving)',
            'delivery_time': '3-7 months (Moon deliveries preferred)',
            'specialty': 'Bulk orders and space station construction'
        }
    }
