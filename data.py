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
            'base_price': 4999.99
        },
        {
            'name': 'Tesla Model S Plaid',
            'emoji': '🚗',
            'description': 'Electric vehicle adapted for planetary surfaces. Includes magnetic wheels for low-gravity environments.',
            'category': 'Vehicles',
            'base_price': 299990.00
        },
        {
            'name': 'Starbucks Venti Latte',
            'emoji': '☕',
            'description': 'Premium coffee beverage. May freeze instantly in space. Warming systems sold separately.',
            'category': 'Food & Beverages',
            'base_price': 49.95
        },
        {
            'name': 'Nintendo Switch OLED',
            'emoji': '🎮',
            'description': 'Portable gaming console. Perfect for long space journeys. Battery life: 3 hours or 3 light-years.',
            'category': 'Electronics',
            'base_price': 1299.99
        },
        {
            'name': 'MacBook Pro M3',
            'emoji': '💻',
            'description': 'High-performance laptop with space-resistant screen. Cosmic ray damage not covered by warranty.',
            'category': 'Electronics',
            'base_price': 8999.99
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
            'base_price': 89.99
        },
        {
            'name': 'IKEA Billy Bookshelf',
            'emoji': '📚',
            'description': 'Self-assembly furniture. Assembly instructions translated into 47 alien languages. Allen key included.',
            'category': 'Home & Garden',
            'base_price': 299.99
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
        },
        # Additional Earth Products
        {
            'name': 'PlayStation 5 Pro',
            'emoji': '🎮',
            'description': 'Next-gen gaming console. Ray tracing works even better with cosmic rays!',
            'category': 'Electronics',
            'base_price': 699.99
        },
        {
            'name': 'Samsung Galaxy S24 Ultra',
            'emoji': '📱',
            'description': 'Android flagship with S Pen. Perfect for signing interplanetary contracts.',
            'category': 'Electronics',
            'base_price': 1299.99
        },
        {
            'name': 'KitchenAid Stand Mixer',
            'emoji': '🥧',
            'description': 'Professional mixer. Gravity-adjustable settings for different planets.',
            'category': 'Home & Garden',
            'base_price': 449.99
        },
        {
            'name': 'Tata Nano (Classic)',
            'emoji': '🚙',
            'description': 'World\'s cheapest car! Still costs more to deliver than to buy.',
            'category': 'Vehicles',
            'base_price': 2500.00
        },
        {
            'name': 'Royal Enfield Bullet',
            'emoji': '🏍️',
            'description': 'Classic Indian motorcycle. Thump works even in vacuum (sound not included).',
            'category': 'Vehicles',
            'base_price': 1800.00
        },
        {
            'name': 'Masala Chai Kit',
            'emoji': '🫖',
            'description': 'Authentic Indian tea experience. Includes cardamom, ginger, and homesickness.',
            'category': 'Food & Beverages',
            'base_price': 12.99
        },
        {
            'name': 'Biryani (Family Pack)',
            'emoji': '🍛',
            'description': 'Hyderabadi biryani for 4 people. Warning: May cause food coma across galaxies.',
            'category': 'Food & Beverages',
            'base_price': 25.99
        },
        {
            'name': 'Bollywood Movie Collection',
            'emoji': '🎬',
            'description': '100 classic films. Subtitles available in Martian and Venusian.',
            'category': 'Entertainment',
            'base_price': 99.99
        },
        {
            'name': 'Yoga Mat (Premium)',
            'emoji': '🧘',
            'description': 'Eco-friendly yoga mat. Meditation works better with zero gravity.',
            'category': 'Health & Fitness',
            'base_price': 89.99
        },
        {
            'name': 'Saree (Silk)',
            'emoji': '👗',
            'description': 'Traditional Indian attire. Flows beautifully in low gravity environments.',
            'category': 'Fashion',
            'base_price': 299.99
        },
        {
            'name': 'Cricket Bat (Signed)',
            'emoji': '🏏',
            'description': 'Autographed by Virat Kohli. Perfect for space cricket leagues.',
            'category': 'Sports',
            'base_price': 499.99
        },
        {
            'name': 'Tabla Set',
            'emoji': '🥁',
            'description': 'Classical Indian drums. Sound travels differently in space atmosphere.',
            'category': 'Music',
            'base_price': 349.99
        },
        {
            'name': 'Instant Maggi Noodles',
            'emoji': '🍜',
            'description': '2-minute noodles (may take longer in different time zones). Taste of home.',
            'category': 'Food & Beverages',
            'base_price': 1.99
        },
        {
            'name': 'Gaming Chair (RGB)',
            'emoji': '🪑',
            'description': 'Pro gamer chair with LED lights. RGB makes everything faster, even in space.',
            'category': 'Electronics',
            'base_price': 299.99
        },
        {
            'name': 'Instant Coffee (3-in-1)',
            'emoji': '☕',
            'description': 'Quick caffeine fix. Essential for surviving interplanetary jet lag.',
            'category': 'Food & Beverages',
            'base_price': 8.99
        },
        {
            'name': 'Power Bank (50,000mAh)',
            'emoji': '🔋',
            'description': 'Massive battery pack. Charges everything except your motivation.',
            'category': 'Electronics',
            'base_price': 79.99
        }
    ]

def get_planet_exclusive_products():
    """Returns planet-exclusive products that are 'locally sourced' and cheaper"""
    return {
        'Mercury': [
            {
                'name': 'Mercury Solar Crystals',
                'emoji': '💎',
                'description': 'Pure energy crystals formed by Mercury\'s extreme solar exposure. Powers small cities!',
                'category': 'Energy & Resources',
                'base_price': 50.00,  # Cheaper because it's local
                'exclusive_to': 'Mercury'
            },
            {
                'name': 'Heat-Resistant Alloy Tools',
                'emoji': '🔧',
                'description': 'Tools forged in Mercury\'s volcanic core. Can withstand temperatures of 1000°C.',
                'category': 'Tools & Equipment',
                'base_price': 120.00,
                'exclusive_to': 'Mercury'
            }
        ],
        'Venus': [
            {
                'name': 'Venusian Acid-Proof Gear',
                'emoji': '🥽',
                'description': 'Local specialty! Protective equipment that laughs at sulfuric acid.',
                'category': 'Safety Equipment',
                'base_price': 80.00,
                'exclusive_to': 'Venus'
            },
            {
                'name': 'Pressure-Forged Diamonds',
                'emoji': '💍',
                'description': 'Diamonds created by Venus\'s crushing atmosphere. Harder than Earth diamonds!',
                'category': 'Luxury Items',
                'base_price': 200.00,
                'exclusive_to': 'Venus'
            },
            {
                'name': 'Venus Cloud Perfume',
                'emoji': '🌸',
                'description': 'Eau de sulfur dioxide. Surprisingly popular among space hipsters.',
                'category': 'Beauty & Personal Care',
                'base_price': 45.00,
                'exclusive_to': 'Venus'
            }
        ],
        'Mars': [
            {
                'name': 'Martian Rust Paint',
                'emoji': '🎨',
                'description': 'Authentic red paint made from Mars\' iron oxide. Perfect for that retro Mars look.',
                'category': 'Art & Crafts',
                'base_price': 25.00,
                'exclusive_to': 'Mars'
            },
            {
                'name': 'Low-Gravity Sports Equipment',
                'emoji': '⚽',
                'description': 'Sports gear designed for 0.38g. Jump higher, run faster, fall slower!',
                'category': 'Sports',
                'base_price': 150.00,
                'exclusive_to': 'Mars'
            },
            {
                'name': 'Martian Potato Chips',
                'emoji': '🥔',
                'description': 'Grown in Martian soil by Matt Damon himself! Now with 30% more radiation.',
                'category': 'Food & Beverages',
                'base_price': 8.99,
                'exclusive_to': 'Mars'
            },
            {
                'name': 'SpaceX Branded Merchandise',
                'emoji': '🚀',
                'description': 'Official Martian colony swag. T-shirts, mugs, and "I survived Mars" bumper stickers.',
                'category': 'Souvenirs',
                'base_price': 35.00,
                'exclusive_to': 'Mars'
            },
            {
                'name': 'Martian Sand Hourglass',
                'emoji': '⏳',
                'description': 'Genuine red sand from the Martian desert. Tells time in Martian days (24h 37min).',
                'category': 'Home Decor',
                'base_price': 65.00,
                'exclusive_to': 'Mars'
            },
            {
                'name': 'Rover Tire Treads Shoes',
                'emoji': '👟',
                'description': 'Footwear with actual rover tire patterns. Leave tracks like Curiosity!',
                'category': 'Fashion',
                'base_price': 120.00,
                'exclusive_to': 'Mars'
            },
            {
                'name': 'Dehydrated Martian Water',
                'emoji': '💧',
                'description': 'Just add... water? The most expensive nothing you\'ll ever buy!',
                'category': 'Food & Beverages',
                'base_price': 199.99,
                'exclusive_to': 'Mars'
            }
        ],
        'Jupiter': [
            {
                'name': 'Jupiter Storm Energy Collector',
                'emoji': '⚡',
                'description': 'Harnesses the power of Jupiter\'s Great Red Spot. Unlimited energy for millennia!',
                'category': 'Energy & Resources',
                'base_price': 500.00,
                'exclusive_to': 'Jupiter'
            },
            {
                'name': 'Anti-Gravity Training Gear',
                'emoji': '🏋️',
                'description': 'Exercise equipment designed for 2.36g gravity. Get buff or get crushed!',
                'category': 'Health & Fitness',
                'base_price': 300.00,
                'exclusive_to': 'Jupiter'
            },
            {
                'name': 'Jovian Gas Cologne',
                'emoji': '💨',
                'description': 'Eau de hydrogen and helium. Lighter than air, heavier than your wallet.',
                'category': 'Beauty & Personal Care',
                'base_price': 75.00,
                'exclusive_to': 'Jupiter'
            },
            {
                'name': 'Great Red Spot Mood Ring',
                'emoji': '💍',
                'description': 'Changes color based on Jupiter\'s storm intensity. Currently stuck on "apocalyptic red".',
                'category': 'Fashion Accessories',
                'base_price': 450.00,
                'exclusive_to': 'Jupiter'
            },
            {
                'name': 'Moon-Jumping Boots (Set of 4)',
                'emoji': '🥾',
                'description': 'Hop between Jupiter\'s 95 moons! Io to Europa in one giant leap!',
                'category': 'Transportation',
                'base_price': 850.00,
                'exclusive_to': 'Jupiter'
            },
            {
                'name': 'Radiation-Proof Sunglasses',
                'emoji': '🕶️',
                'description': 'Essential eyewear for Jupiter\'s intense radiation belts. Style meets survival!',
                'category': 'Safety Equipment',
                'base_price': 220.00,
                'exclusive_to': 'Jupiter'
            }
        ],
        'Saturn': [
            {
                'name': 'Saturn Ring Jewelry Collection',
                'emoji': '💫',
                'description': 'Actual pieces of Saturn\'s rings! Each piece is billions of years old.',
                'category': 'Luxury Items',
                'base_price': 400.00,
                'exclusive_to': 'Saturn'
            },
            {
                'name': 'Ice Crystal Decorations',
                'emoji': '❄️',
                'description': 'Beautiful ice sculptures from Saturn\'s moons. Guaranteed to not melt in space.',
                'category': 'Home & Garden',
                'base_price': 180.00,
                'exclusive_to': 'Saturn'
            },
            {
                'name': 'Hexagonal Storm Pattern Art',
                'emoji': '🎭',
                'description': 'Unique hexagonal art inspired by Saturn\'s polar storm. Geometry has never been cooler.',
                'category': 'Art & Crafts',
                'base_price': 95.00,
                'exclusive_to': 'Saturn'
            }
        ],
        'Uranus': [
            {
                'name': 'Sideways Compass',
                'emoji': '🧭',
                'description': 'The only compass that works on a sideways planet. Points in directions you never knew existed.',
                'category': 'Navigation Tools',
                'base_price': 60.00,
                'exclusive_to': 'Uranus'
            },
            {
                'name': 'Methane Ice Cubes',
                'emoji': '🧊',
                'description': 'Keep your drinks cold for 84 Earth years! Warning: May smell like rotten eggs.',
                'category': 'Food & Beverages',
                'base_price': 15.00,
                'exclusive_to': 'Uranus'
            },
            {
                'name': 'Tilted Architecture Plans',
                'emoji': '📐',
                'description': 'Building blueprints designed for a planet that spins on its side. Confusing but functional.',
                'category': 'Construction & Design',
                'base_price': 220.00,
                'exclusive_to': 'Uranus'
            }
        ],
        'Neptune': [
            {
                'name': 'Supersonic Wind Instruments',
                'emoji': '🎺',
                'description': 'Musical instruments powered by Neptune\'s 2,100 km/h winds. Ear protection included.',
                'category': 'Music',
                'base_price': 350.00,
                'exclusive_to': 'Neptune'
            },
            {
                'name': 'Diamond Rain Umbrella',
                'emoji': '☂️',
                'description': 'Protection from Neptune\'s literal diamond rain. Luxury and practicality combined!',
                'category': 'Weather Protection',
                'base_price': 800.00,
                'exclusive_to': 'Neptune'
            },
            {
                'name': 'Deep Blue Meditation Stones',
                'emoji': '🔵',
                'description': 'Calming stones infused with Neptune\'s serene blue energy. Inner peace guaranteed.',
                'category': 'Wellness & Spirituality',
                'base_price': 125.00,
                'exclusive_to': 'Neptune'
            }
        ],
        'Pluto': [
            {
                'name': 'Former Planet Support Group Kit',
                'emoji': '😢',
                'description': 'Emotional support items for dealing with planetary status changes. Includes tissues and therapy.',
                'category': 'Mental Health',
                'base_price': 40.00,
                'exclusive_to': 'Pluto'
            },
            {
                'name': 'Vintage Planetary Classification Certificate',
                'emoji': '📜',
                'description': 'Original 1930-2006 planet certificate. A piece of astronomical history!',
                'category': 'Collectibles',
                'base_price': 150.00,
                'exclusive_to': 'Pluto'
            },
            {
                'name': 'Ultra-Cold Storage System',
                'emoji': '🥶',
                'description': 'Storage system that keeps things colder than Pluto\'s heart. Perfect for preserving memories.',
                'category': 'Storage Solutions',
                'base_price': 275.00,
                'exclusive_to': 'Pluto'
            }
        ]
    }

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
