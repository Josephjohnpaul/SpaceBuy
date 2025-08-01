import streamlit as st
import pandas as pd
from data import get_products, get_planets, get_space_agencies, get_planet_exclusive_products
from ai_pricing import get_ai_pricing, generate_product_description
from utils import calculate_delivery_cost, format_price, generate_tracking_number, calculate_estimated_delivery_time
import db_utils
import random
import uuid

# Configure page
st.set_page_config(
    page_title="🚀 SpaceBuy - Interplanetary E-Commerce",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for space theme
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .planet-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(157, 78, 221, 0.3);
        margin: 0.5rem 0;
    }
    .cost-breakdown {
        background: rgba(255, 0, 0, 0.1);
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff4444;
    }
    .hiring-notice {
        background: rgba(255, 165, 0, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        border: 2px solid orange;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'products' not in st.session_state:
    st.session_state.products = get_products()
if 'planets' not in st.session_state:
    st.session_state.planets = get_planets()
if 'space_agencies' not in st.session_state:
    st.session_state.space_agencies = get_space_agencies()
if 'planet_exclusive_products' not in st.session_state:
    st.session_state.planet_exclusive_products = get_planet_exclusive_products()
if 'user_session' not in st.session_state:
    st.session_state.user_session = str(uuid.uuid4())
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 SpaceBuy India</h1>', unsafe_allow_html=True)
    st.markdown("### *The Galaxy's Most Expensive Delivery Service* ⭐")
    st.markdown("*All prices in Indian Rupees (₹)*")
    
    # Sidebar
    st.sidebar.title("🌌 Navigation")
    
    # User login section
    if not st.session_state.current_user:
        with st.sidebar.expander("👨‍🚀 Customer Login"):
            with st.form("login_form"):
                name = st.text_input("Name:")
                email = st.text_input("Email:")
                planet_pref = st.selectbox("Favorite Planet:", ["None"] + list(st.session_state.planets.keys()))
                
                if st.form_submit_button("🚀 Join SpaceBuy"):
                    if name and email:
                        user_data = db_utils.create_user(name, email, planet_pref if planet_pref != "None" else None)
                        if user_data:
                            st.session_state.current_user = user_data
                            st.success(f"Welcome to SpaceBuy, {user_data['name']}!")
                            st.rerun()
                        else:
                            st.error("Login failed: Please try again")
    else:
        st.sidebar.success(f"👋 {st.session_state.current_user['name']}")
        st.sidebar.write(f"🏅 {st.session_state.current_user['loyalty_level']}")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.current_user = None
            st.rerun()
    
    page = st.sidebar.selectbox(
        "Choose your adventure:",
        ["🛒 Browse Products", "🔍 AI Product Search", "⚖️ Price Comparison", 
         "📊 Analytics Dashboard", "📦 My Orders", "📞 Contact & Careers"]
    )
    
    if page == "🛒 Browse Products":
        browse_products()
    elif page == "🔍 AI Product Search":
        ai_product_search()
    elif page == "⚖️ Price Comparison":
        price_comparison()
    elif page == "📊 Analytics Dashboard":
        analytics_dashboard()
    elif page == "📦 My Orders":
        my_orders()
    elif page == "📞 Contact & Careers":
        contact_and_careers()

def browse_products():
    st.header("🛒 Interplanetary Product Catalog")
    
    # Planet selection
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_planet = st.selectbox(
            "🪐 Select destination planet:",
            options=list(st.session_state.planets.keys()),
            help="Choose where you want your overpriced items delivered!"
        )
    
    with col2:
        st.metric(
            "Distance from Earth",
            f"{st.session_state.planets[selected_planet]['distance']} AU",
            help="Astronomical Units - the further, the more expensive!"
        )
    
    # Check for Sun delivery Easter egg
    if selected_planet and selected_planet.lower() == "sun":
        st.markdown("""
        <div class="hiring-notice">
            <h2>⚠️ HOLD UP THERE, HOTSHOT! ⚠️</h2>
            <p><strong>How are you still alive there?!</strong> 🔥</p>
            <p>None of our delivery employees have ever returned from Sun deliveries...</p>
            <p><strong>🚨 URGENT: Are you interested in joining our team? 🚨</strong></p>
            <p>We desperately need heat-resistant delivery personnel!</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔥 YES! I WANT TO WORK ON THE SUN! 🔥"):
            st.balloons()
            st.success("🎉 Congratulations! Please proceed to our Careers section to apply!")
            return
    
    # Product filters
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox(
            "📱 Category:",
            ["All"] + list(set([p['category'] for p in st.session_state.products]))
        )
    
    with col2:
        price_range = st.select_slider(
            "💰 Price Range:",
            options=["Cheap", "Expensive", "Bankruptcy", "Sell Your Soul"],
            value="Expensive"
        )
    
    with col3:
        agency_filter = st.selectbox(
            "🚀 Space Agency:",
            ["All"] + list(st.session_state.space_agencies.keys())
        )
    
    # Filter products
    filtered_products = st.session_state.products
    if category_filter != "All":
        filtered_products = [p for p in filtered_products if p['category'] == category_filter]
    
    # Display Earth products
    st.subheader(f"🌍 Earth Products for {selected_planet}")
    st.write("*Shipped from Earth (expensive due to interplanetary logistics)*")
    
    for product in filtered_products:
        with st.expander(f"{product['emoji']} {product['name']} - {format_price(product['base_price'])}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Description:** {product['description']}")
                st.write(f"**Category:** {product['category']}")
                
                # Calculate interplanetary price
                planet_info = st.session_state.planets[selected_planet]
                delivery_cost = calculate_delivery_cost(product['base_price'], planet_info)
                total_price = product['base_price'] + delivery_cost
                
                st.write(f"**Earth Price:** {format_price(product['base_price'])}")
                st.write(f"**{selected_planet} Price:** {format_price(total_price)}")
                
                # Delivery agency
                agency = random.choice(list(st.session_state.space_agencies.keys()))
                agency_info = st.session_state.space_agencies[agency]
                st.write(f"**Delivery by:** {agency} - {agency_info['motto']}")
                st.write(f"**Reliability:** {agency_info['reliability']}")
                st.write(f"**Estimated Delivery:** {agency_info['delivery_time']}")
            
            with col2:
                if st.button(f"💸 Buy for {format_price(total_price)}", key=f"buy_{product['name']}_{selected_planet}"):
                    if st.session_state.current_user:
                        # Create order in database
                        tracking_num = generate_tracking_number()
                        delivery_time = calculate_estimated_delivery_time(planet_info)
                        
                        order_id = db_utils.create_order(
                            user_id=st.session_state.current_user['id'],
                            product_name=product['name'],
                            product_category=product['category'],
                            destination_planet=selected_planet,
                            base_price_usd=product['base_price'],
                            delivery_cost_usd=delivery_cost,
                            total_price_inr=total_price * 83,  # Convert to INR
                            space_agency=agency,
                            estimated_delivery_time=delivery_time,
                            tracking_number=tracking_num
                        )
                        
                        if order_id:
                            st.success(f"🎉 Order placed! Order ID: {order_id}")
                            st.info(f"📦 Tracking: {tracking_num}")
                            st.balloons()
                        else:
                            st.error("💸 Order failed: Please try again!")
                    else:
                        st.warning("🚀 Please login first to place orders!")
                
                if st.button(f"📊 Cost Breakdown", key=f"breakdown_{product['name']}_{selected_planet}"):
                    show_cost_breakdown(product, planet_info, delivery_cost)
    
    # Display planet-exclusive products
    if selected_planet in st.session_state.planet_exclusive_products:
        st.markdown("---")
        st.subheader(f"⭐ {selected_planet} Exclusive Products")
        st.write("*Locally sourced items available only on this planet (cheaper due to no interplanetary shipping!)*")
        
        exclusive_products = st.session_state.planet_exclusive_products[selected_planet]
        for product in exclusive_products:
            with st.expander(f"{product['emoji']} {product['name']} - {format_price(product['base_price'])} ⭐ LOCAL"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Description:** {product['description']}")
                    st.write(f"**Category:** {product['category']}")
                    st.write(f"**Exclusive to:** {product['exclusive_to']}")
                    
                    # For exclusive products, no delivery cost since they're local
                    local_price = product['base_price']
                    st.write(f"**Local {selected_planet} Price:** {format_price(local_price)}")
                    st.success("✨ FREE LOCAL DELIVERY! No interplanetary shipping costs!")
                    
                    # Local delivery agency
                    st.write(f"**Local Delivery by:** {selected_planet} Express Delivery")
                    st.write(f"**Estimated Delivery:** Same day delivery!")
                
                with col2:
                    if st.button(f"💳 Buy Local for {format_price(local_price)}", key=f"buy_local_{product['name']}_{selected_planet}"):
                        if st.session_state.current_user:
                            # Create order in database for exclusive product
                            tracking_num = generate_tracking_number()
                            
                            order_id = db_utils.create_order(
                                user_id=st.session_state.current_user['id'],
                                product_name=f"{product['name']} ({selected_planet} Exclusive)",
                                product_category=product['category'],
                                destination_planet=selected_planet,
                                base_price_usd=product['base_price'],
                                delivery_cost_usd=0.0,  # No delivery cost for local products
                                total_price_inr=local_price * 83,  # Convert to INR
                                space_agency=f"{selected_planet} Express",
                                estimated_delivery_time="Same day",
                                tracking_number=tracking_num
                            )
                            
                            if order_id:
                                st.success(f"🎉 Local order placed! Order ID: {order_id}")
                                st.info(f"📦 Tracking: {tracking_num}")
                                st.balloons()
                            else:
                                st.error("💸 Order failed: Please try again!")
                        else:
                            st.warning("🚀 Please login first to place orders!")
                    
                    st.info("🏪 **Local Product Benefits:**\n• No shipping costs\n• Same day delivery\n• Authentic local quality\n• Support local economy")

def ai_product_search():
    st.header("🔍 AI-Powered Interplanetary Product Search")
    st.write("Ask our AI about any Earth product and get pricing for any planet!")
    
    col1, col2 = st.columns(2)
    with col1:
        product_query = st.text_input(
            "🛍️ What product are you looking for?",
            placeholder="e.g., iPhone 15, Tesla Model S, Pizza..."
        )
    
    with col2:
        target_planet = st.selectbox(
            "🪐 Target planet:",
            options=list(st.session_state.planets.keys())
        )
    
    if st.button("🚀 Get Interplanetary Pricing!") and product_query:
        with st.spinner("🤖 Our AI is calculating astronomical prices..."):
            # Check for Sun delivery Easter egg
            if target_planet and target_planet.lower() == "sun":
                st.markdown("""
                <div class="hiring-notice">
                    <h2>🔥 SUN DELIVERY REQUEST DETECTED! 🔥</h2>
                    <p><strong>How are you alive there?!</strong></p>
                    <p>None of our employees came back alive attempting to deliver packages to the Sun...</p>
                    <p><strong>Are you interested in joining our delivery team?</strong></p>
                    <p>We need someone with your... unique heat resistance!</p>
                </div>
                """, unsafe_allow_html=True)
                return
            
            try:
                # Get AI-generated product info and pricing
                product_info = generate_product_description(product_query, target_planet)
                planet_info = st.session_state.planets[target_planet]
                ai_price = get_ai_pricing(product_query, planet_info)
                
                # Add to search history
                total_ai_price = ai_price['base_price'] * ai_price['multiplier']
                db_utils.add_search_history(product_query, target_planet, total_ai_price, st.session_state.user_session)
                
                # Display results
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader(f"🛍️ {product_query} on {target_planet}")
                    st.write(product_info)
                    
                    # Price breakdown
                    delivery_cost = calculate_delivery_cost(ai_price['base_price'], planet_info)
                    total_price = ai_price['base_price'] + delivery_cost
                    
                    st.write(f"**Earth Price:** {format_price(ai_price['base_price'])}")
                    st.write(f"**{target_planet} Price:** {format_price(total_price)}")
                    st.write(f"**Price Multiplier:** {ai_price['multiplier']}x")
                    st.write(f"**Reasoning:** {ai_price['reasoning']}")
                
                with col2:
                    agency = random.choice(list(st.session_state.space_agencies.keys()))
                    agency_info = st.session_state.space_agencies[agency]
                    
                    st.info(f"**Delivery by:** {agency}")
                    st.write(f"*{agency_info['motto']}*")
                    st.write(f"**Reliability:** {agency_info['reliability']}")
                    st.write(f"**ETA:** {agency_info['delivery_time']}")
                    
                    if st.button("💸 Order Now!"):
                        if st.session_state.current_user:
                            # Create order in database for AI product
                            tracking_num = generate_tracking_number()
                            delivery_time = calculate_estimated_delivery_time(planet_info)
                            
                            order_id = db_utils.create_order(
                                user_id=st.session_state.current_user['id'],
                                product_name=product_query,
                                product_category='AI Generated',
                                destination_planet=target_planet,
                                base_price_usd=ai_price['base_price'],
                                delivery_cost_usd=delivery_cost,
                                total_price_inr=total_price * 83,  # Convert to INR
                                space_agency=agency,
                                estimated_delivery_time=delivery_time,
                                tracking_number=tracking_num
                            )
                            
                            if order_id:
                                st.success(f"🎉 Order placed! Order ID: {order_id}")
                                st.info(f"📦 Tracking: {tracking_num}")
                                st.balloons()
                            else:
                                st.error("💸 Order failed: Please try again!")
                        else:
                            st.warning("🚀 Please login first to place orders!")
                
                # Cost breakdown
                if st.button("📊 Show Detailed Cost Breakdown"):
                    show_ai_cost_breakdown(ai_price, planet_info, delivery_cost, product_query, target_planet)
                        
            except Exception as e:
                st.error(f"🚨 AI System Error: {str(e)}")
                st.info("💡 Our AI is probably calculating prices for a black hole. Try again!")

def price_comparison():
    st.header("⚖️ Interplanetary Price Comparison")
    st.write("Compare prices across the galaxy and cry about delivery costs!")
    
    # Product selection
    product_names = [p['name'] for p in st.session_state.products]
    selected_product = st.selectbox("🛍️ Select product:", product_names)
    
    # Planet selection for comparison
    st.write("🪐 Select planets to compare:")
    planet_options = list(st.session_state.planets.keys())
    
    col1, col2, col3, col4 = st.columns(4)
    selected_planets = []
    
    for i, planet in enumerate(planet_options[:8]):  # Limit to 8 planets for display
        col = [col1, col2, col3, col4][i % 4]
        if col.checkbox(planet, key=f"compare_{planet}"):
            selected_planets.append(planet)
    
    if len(selected_planets) < 2:
        st.warning("⚠️ Please select at least 2 planets for comparison!")
        return
    
    if st.button("🚀 Compare Prices Across the Galaxy!"):
        # Find the selected product
        product = next(p for p in st.session_state.products if p['name'] == selected_product)
        
        # Calculate prices for each planet
        comparison_data = []
        for planet in selected_planets:
            planet_info = st.session_state.planets[planet]
            delivery_cost = calculate_delivery_cost(product['base_price'], planet_info)
            total_price = product['base_price'] + delivery_cost
            
            comparison_data.append({
                'Planet': planet,
                'Base Price': format_price(product['base_price']),
                'Delivery Cost': format_price(delivery_cost),
                'Total Price': format_price(total_price),
                'Distance (AU)': planet_info['distance'],
                'Gravity': f"{planet_info['gravity']}g",
                'Atmosphere': planet_info['atmosphere']
            })
        
        # Display comparison table
        df = pd.DataFrame(comparison_data)
        st.subheader(f"💰 Price Comparison for {selected_product}")
        st.dataframe(df, use_container_width=True)
        
        # Find cheapest and most expensive (extract numeric values from INR format)
        prices = []
        for row in comparison_data:
            price_str = row['Total Price']
            # Extract numeric value from various INR formats
            if 'Cr' in price_str:
                numeric_part = float(price_str.split('₹')[1].split(' Cr')[0])
                prices.append(numeric_part * 10_000_000)  # Convert crores to actual INR
            elif 'L' in price_str:
                numeric_part = float(price_str.split('₹')[1].split(' L')[0])
                prices.append(numeric_part * 100_000)  # Convert lakhs to actual INR
            else:
                # Regular INR amount
                numeric_part = float(price_str.replace('₹', '').replace(',', ''))
                prices.append(numeric_part)
        cheapest_idx = prices.index(min(prices))
        expensive_idx = prices.index(max(prices))
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"🏆 Cheapest: {comparison_data[cheapest_idx]['Planet']} - {comparison_data[cheapest_idx]['Total Price']}")
        with col2:
            st.error(f"💸 Most Expensive: {comparison_data[expensive_idx]['Planet']} - {comparison_data[expensive_idx]['Total Price']}")
        
        # Show savings
        savings = prices[expensive_idx] - prices[cheapest_idx]
        if savings > 0:
            # Convert INR savings back to USD equivalent for format_price function
            savings_usd = savings / 83
            st.info(f"💡 You could save {format_price(savings_usd)} by choosing {comparison_data[cheapest_idx]['Planet']} over {comparison_data[expensive_idx]['Planet']}!")
            st.write("*Note: Savings calculated before accounting for the emotional cost of living on an alien planet.*")

def contact_and_careers():
    st.header("📞 Contact & Careers")
    
    tab1, tab2 = st.tabs(["🚀 Join Our Team", "📧 Contact Us"])
    
    with tab1:
        st.subheader("🔥 Extreme Delivery Jobs Available!")
        
        st.markdown("""
        <div class="hiring-notice">
            <h3>🌟 NOW HIRING: Interplanetary Delivery Specialists! 🌟</h3>
            <p><strong>Positions Available:</strong></p>
            <ul>
                <li>🔥 <strong>Sun Delivery Specialist</strong> - High mortality rate, excellent hazard pay!</li>
                <li>🪐 <strong>Gas Giant Navigator</strong> - Must be comfortable with crushing pressure</li>
                <li>❄️ <strong>Ice Planet Courier</strong> - Bring your own heating system</li>
                <li>🌋 <strong>Volcanic Moon Mailman</strong> - Heat-resistant suits provided (maybe)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Job application form
        st.subheader("🚀 Apply Now!")
        
        with st.form("job_application"):
            name = st.text_input("👨‍🚀 Full Name:")
            email = st.text_input("📧 Email:")
            position = st.selectbox(
                "🎯 Desired Position:",
                ["Sun Delivery Specialist", "Gas Giant Navigator", "Ice Planet Courier", "Volcanic Moon Mailman", "Black Hole Logistics Coordinator"]
            )
            
            experience = st.text_area("🏆 Relevant Experience:", 
                                    placeholder="e.g., Survived a volcano, can hold breath for 3 hours, immune to radiation...")
            
            why_hire = st.text_area("💪 Why should we hire you?",
                                  placeholder="e.g., I have nothing left to lose, I can survive in space, I'm already dead inside...")
            
            heat_resistant = st.checkbox("🔥 I am heat resistant (required for Sun deliveries)")
            can_breathe_methane = st.checkbox("💨 I can breathe methane (useful for Titan deliveries)")
            own_spaceship = st.checkbox("🚀 I own my own spaceship (major plus!)")
            
            submitted = st.form_submit_button("🚀 Submit Application")
            
            if submitted:
                if not name or not email:
                    st.error("⚠️ Please fill in all required fields!")
                else:
                    st.success("🎉 Application submitted successfully!")
                    st.balloons()
                    st.info("📧 You will receive a response within 5-7 galactic standard days (if you survive that long).")
                    
                    if position == "Sun Delivery Specialist":
                        st.warning("🔥 SPECIAL NOTICE: Please update your will before starting work.")
    
    with tab2:
        st.subheader("📧 Contact Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🏢 SpaceBuy Headquarters**
            
            📍 **Address:**
            Galaxy Trade Center, Level 42
            Milky Way, Local Group
            Universe Sector 7-G
            
            📞 **Phone:** +1-800-SPACE-99
            📧 **Email:** help@spacebuy.galaxy
            🌐 **Website:** www.spacebuy.galaxy
            """)
        
        with col2:
            st.markdown("""
            **🚀 Delivery Complaints:**
            
            📞 **Hotline:** +1-800-WHERE-IS-MY-STUFF
            📧 **Email:** complaints@spacebuy.galaxy
            
            **⏰ Business Hours:**
            - Earth Time: 24/7
            - Mars Time: 24 hours 37 minutes/7
            - Jupiter Time: We gave up calculating
            
            **💬 Average Response Time:**
            - Earth: 1-2 business days
            - Mars: 6-8 months
            - Jupiter: When the stars align
            """)
        
        # Customer service form
        st.subheader("💬 Send us a Message")
        
        with st.form("contact_form"):
            customer_name = st.text_input("👤 Your Name:")
            customer_email = st.text_input("📧 Your Email:")
            issue_type = st.selectbox(
                "🎯 Issue Type:",
                ["Product Inquiry", "Delivery Complaint", "Refund Request", "My Package is in a Black Hole", "Alien Interference", "Other"]
            )
            
            message = st.text_area("💬 Message:", 
                                 placeholder="Describe your issue... (Please be specific about which dimension your package is lost in)")
            
            submitted_contact = st.form_submit_button("🚀 Send Message")
            
            if submitted_contact:
                if not customer_name or not customer_email or not message:
                    st.error("⚠️ Please fill in all required fields!")
                else:
                    st.success("📧 Message sent successfully!")
                    st.info("🤖 Our customer service AI will respond within 1-2 galactic business cycles.")
                    
                    if issue_type == "My Package is in a Black Hole":
                        st.error("🕳️ Unfortunately, black hole retrievals are not covered under our standard warranty.")
                        st.info("💡 Consider this a unique storage solution!")

def show_cost_breakdown(product, planet_info, delivery_cost):
    st.markdown(f"""
    <div class="cost-breakdown">
        <h4>💸 Detailed Cost Breakdown for {product['name']}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate individual cost components
    base_shipping = delivery_cost * 0.15
    fuel_cost = delivery_cost * 0.35
    insurance = delivery_cost * 0.20
    hazard_pay = delivery_cost * 0.15
    spaceship_maintenance = delivery_cost * 0.10
    bureaucracy_fee = delivery_cost * 0.05
    
    breakdown_data = {
        'Cost Component': [
            'Base Product Price',
            'Basic Interplanetary Shipping',
            'Rocket Fuel (Premium Grade)',
            'Insurance (Things Go Wrong)',
            'Hazard Pay for Crew',
            'Spaceship Maintenance',
            'Galactic Bureaucracy Fee',
            '**TOTAL PRICE**'
        ],
        'Amount': [
            format_price(product['base_price']),
            format_price(base_shipping),
            format_price(fuel_cost),
            format_price(insurance),
            format_price(hazard_pay),
            format_price(spaceship_maintenance),
            format_price(bureaucracy_fee),
            f"**{format_price(product['base_price'] + delivery_cost)}**"
        ],
        'Notes': [
            'Same price as on Earth!',
            f"Distance: {planet_info['distance']} AU",
            f"Gravity factor: {planet_info['gravity']}g",
            '73% chance of mission failure',
            'Emotional trauma included',
            'Cosmic debris is expensive',
            'Someone has to pay the space bureaucrats',
            '🚀 Ready to bankrupt yourself?'
        ]
    }
    
    df_breakdown = pd.DataFrame(breakdown_data)
    st.dataframe(df_breakdown, use_container_width=True)

def show_ai_cost_breakdown(ai_price, planet_info, delivery_cost, product_name, planet_name):
    st.markdown(f"""
    <div class="cost-breakdown">
        <h4>💸 AI-Generated Cost Breakdown for {product_name} → {planet_name}</h4>
        <p><strong>AI Reasoning:</strong> {ai_price['reasoning']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate individual cost components
    base_shipping = delivery_cost * 0.15
    fuel_cost = delivery_cost * 0.35
    insurance = delivery_cost * 0.20
    hazard_pay = delivery_cost * 0.15
    spaceship_maintenance = delivery_cost * 0.10
    ai_processing_fee = delivery_cost * 0.05
    
    breakdown_data = {
        'Cost Component': [
            f'{product_name} (Earth Price)',
            'AI Price Adjustment',
            'Interplanetary Shipping',
            'Rocket Fuel',
            'Mission Insurance',
            'Crew Hazard Pay',
            'Spaceship Maintenance',
            'AI Processing Fee',
            '**TOTAL PRICE**'
        ],
        'Amount': [
            format_price(ai_price['base_price']),
            f"+{ai_price['multiplier']}x multiplier",
            format_price(base_shipping),
            format_price(fuel_cost),
            format_price(insurance),
            format_price(hazard_pay),
            format_price(spaceship_maintenance),
            format_price(ai_processing_fee),
            f"**{format_price(ai_price['base_price'] + delivery_cost)}**"
        ],
        'Justification': [
            'AI-estimated Earth retail price',
            f'Planet-specific adjustments for {planet_name}',
            f"Base shipping to {planet_info['distance']} AU",
            f"Extra fuel for {planet_info['gravity']}g gravity",
            f"High risk due to {planet_info['atmosphere']}",
            'Crew therapy included',
            'Space is hard on machinery',
            'Our AI needs to eat too (electricity)',
            '🤖 AI-optimized bankruptcy!'
        ]
    }
    
    df_breakdown = pd.DataFrame(breakdown_data)
    st.dataframe(df_breakdown, use_container_width=True)

def analytics_dashboard():
    st.header("📊 SpaceBuy Analytics Dashboard")
    
    # Get dashboard stats
    stats = db_utils.get_dashboard_stats()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", stats['total_orders'])
    with col2:
        st.metric("Total Revenue", format_price(stats['total_revenue'] / 83))  # Convert back to USD for formatting
    with col3:
        st.metric("Total Customers", stats['total_users'])
    with col4:
        st.metric("Most Popular Planet", stats['most_popular_planet'])
    
    st.markdown("---")
    
    # Planet statistics
    st.subheader("🪐 Planet Performance")
    planet_stats = db_utils.get_planet_stats()
    
    if planet_stats is not None and not planet_stats.empty:
        # Create charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Orders by Planet**")
            chart_data = planet_stats.set_index('planet_name')['total_orders']
            st.bar_chart(chart_data)
        
        with col2:
            st.write("**Revenue by Planet (₹)**")
            chart_data = planet_stats.set_index('planet_name')['total_revenue_inr']
            st.bar_chart(chart_data)
        
        # Show detailed table
        st.subheader("📈 Detailed Planet Statistics")
        display_stats = planet_stats.copy()
        display_stats['total_revenue_inr'] = display_stats['total_revenue_inr'].apply(lambda x: format_price(x / 83))
        display_stats['avg_order_value'] = display_stats['avg_order_value'].apply(lambda x: format_price(x / 83))
        st.dataframe(display_stats, use_container_width=True)
    else:
        st.info("📊 No order data available yet. Start placing some orders to see analytics!")

def my_orders():
    st.header("📦 My Orders")
    
    if not st.session_state.current_user:
        st.warning("🚀 Please login to view your orders!")
        return
    
    orders = db_utils.get_user_orders(st.session_state.current_user['id'])
    
    if orders is not None and not orders.empty:
        st.write(f"**Total Orders:** {len(orders)}")
        
        for _, order in orders.iterrows():
            with st.expander(f"🚀 Order {order['order_id']} - {order['product_name']} → {order['destination_planet']}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Product:** {order['product_name']}")
                    st.write(f"**Category:** {order['product_category']}")
                    st.write(f"**Destination:** {order['destination_planet']}")
                    st.write(f"**Total Price:** {format_price(order['total_price_inr'] / 83)}")
                    st.write(f"**Space Agency:** {order['space_agency']}")
                    st.write(f"**Status:** {order['order_status']}")
                    st.write(f"**Estimated Delivery:** {order['estimated_delivery_time']}")
                    
                with col2:
                    st.write(f"**Tracking:** {order['tracking_number']}")
                    st.write(f"**Order Date:** {order['created_at'].strftime('%Y-%m-%d')}")
                    
                    # Mock status updates
                    if st.button(f"📍 Track Order", key=f"track_{order['order_id']}"):
                        st.info("🚀 Package launched from Earth!")
                        st.info("🛸 Currently somewhere in the asteroid belt...")
                        st.warning("⚠️ Minor delay due to space pirates")
                        st.success("📡 ETA updated: Still very, very long!")
    else:
        st.info("📦 No orders found. Start shopping across the galaxy!")
        
        # Show some product recommendations
        st.subheader("🛍️ Recommended Products")
        recommended_products = random.sample(st.session_state.products, 3)
        
        cols = st.columns(3)
        for i, product in enumerate(recommended_products):
            with cols[i]:
                st.write(f"**{product['emoji']} {product['name']}**")
                st.write(f"{format_price(product['base_price'])}")
                st.write(f"*{product['category']}*")

if __name__ == "__main__":
    main()
