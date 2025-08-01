"""
Simple database utilities for SpaceBuy using direct SQL execution
"""

import streamlit as st
import uuid
from datetime import datetime

def create_user(name, email, planet_preference=None):
    """Create a new user and return user data"""
    try:
        # Check if user exists
        existing_user = st.connection("postgresql", type="sql").query(
            "SELECT * FROM users WHERE email = :email", 
            params={"email": email}
        )
        
        if not existing_user.empty:
            return existing_user.iloc[0].to_dict()
        
        # Create new user
        conn = st.connection("postgresql", type="sql")
        conn.session.execute(
            "INSERT INTO users (name, email, planet_preference) VALUES (:name, :email, :planet_pref)",
            {"name": name, "email": email, "planet_pref": planet_preference}
        )
        conn.session.commit()
        
        # Return the created user
        new_user = conn.query(
            "SELECT * FROM users WHERE email = :email", 
            params={"email": email}
        )
        return new_user.iloc[0].to_dict()
        
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

def create_order(user_id, product_name, product_category, destination_planet, 
                base_price_usd, delivery_cost_usd, total_price_inr, space_agency, 
                estimated_delivery_time, tracking_number, special_instructions=None):
    """Create a new order"""
    try:
        order_id = f"SB-{uuid.uuid4().hex[:8].upper()}"
        
        conn = st.connection("postgresql", type="sql")
        conn.session.execute("""
            INSERT INTO orders (
                order_id, user_id, product_name, product_category,
                destination_planet, base_price_usd, delivery_cost_usd,
                total_price_inr, space_agency, estimated_delivery_time,
                tracking_number, special_instructions
            ) VALUES (
                :order_id, :user_id, :product_name, :product_category,
                :destination_planet, :base_price_usd, :delivery_cost_usd,
                :total_price_inr, :space_agency, :estimated_delivery_time,
                :tracking_number, :special_instructions
            )
        """, {
            "order_id": order_id, "user_id": user_id, "product_name": product_name,
            "product_category": product_category, "destination_planet": destination_planet,
            "base_price_usd": base_price_usd, "delivery_cost_usd": delivery_cost_usd,
            "total_price_inr": total_price_inr, "space_agency": space_agency,
            "estimated_delivery_time": estimated_delivery_time, "tracking_number": tracking_number,
            "special_instructions": special_instructions
        })
        
        # Update user spending
        conn.session.execute("""
            UPDATE users 
            SET total_spent_inr = total_spent_inr + :total_inr,
                loyalty_level = CASE 
                    WHEN total_spent_inr + :total_inr > 10000000 THEN 'Galactic Emperor'
                    WHEN total_spent_inr + :total_inr > 1000000 THEN 'Cosmic Commander'
                    WHEN total_spent_inr + :total_inr > 100000 THEN 'Space Captain'
                    WHEN total_spent_inr + :total_inr > 10000 THEN 'Orbital Officer'
                    ELSE 'Space Cadet'
                END
            WHERE id = :user_id
        """, {"total_inr": total_price_inr, "user_id": user_id})
        
        conn.session.commit()
        return order_id
        
    except Exception as e:
        st.error(f"Order creation failed: {str(e)}")
        return None

def get_user_orders(user_id):
    """Get all orders for a user"""
    try:
        conn = st.connection("postgresql", type="sql")
        orders = conn.query(
            "SELECT * FROM orders WHERE user_id = :user_id ORDER BY created_at DESC",
            params={"user_id": user_id}
        )
        return orders
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None

def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        conn = st.connection("postgresql", type="sql")
        
        # Get basic stats
        stats = conn.query("""
            SELECT 
                COUNT(*) as total_orders,
                COALESCE(SUM(total_price_inr), 0) as total_revenue,
                COUNT(DISTINCT user_id) as total_users,
                COALESCE(AVG(total_price_inr), 0) as avg_order_value
            FROM orders
        """)
        
        # Get most popular planet
        popular_planet = conn.query("""
            SELECT destination_planet, COUNT(*) as order_count
            FROM orders 
            GROUP BY destination_planet 
            ORDER BY order_count DESC 
            LIMIT 1
        """)
        
        result = stats.iloc[0].to_dict() if not stats.empty else {
            'total_orders': 0, 'total_revenue': 0, 'total_users': 0, 'avg_order_value': 0
        }
        
        if not popular_planet.empty:
            result['most_popular_planet'] = popular_planet.iloc[0]['destination_planet']
        else:
            result['most_popular_planet'] = 'Mars'
            
        return result
        
    except Exception as e:
        st.error(f"Dashboard error: {str(e)}")
        return {'total_orders': 0, 'total_revenue': 0, 'total_users': 0, 'avg_order_value': 0, 'most_popular_planet': 'Mars'}

def add_search_history(search_query, target_planet, ai_price, user_session):
    """Add search to history"""
    try:
        conn = st.connection("postgresql", type="sql")
        conn.session.execute("""
            INSERT INTO search_history (search_query, target_planet, ai_generated_price, user_session)
            VALUES (:query, :planet, :price, :session)
        """, {
            "query": search_query, "planet": target_planet, 
            "price": ai_price, "session": user_session
        })
        conn.session.commit()
    except Exception as e:
        # Silently fail for search history
        pass

def get_planet_stats():
    """Get planet statistics"""
    try:
        conn = st.connection("postgresql", type="sql")
        return conn.query("""
            SELECT 
                destination_planet as planet_name,
                COUNT(*) as total_orders,
                SUM(total_price_inr) as total_revenue_inr,
                AVG(total_price_inr) as avg_order_value
            FROM orders
            GROUP BY destination_planet
            ORDER BY total_revenue_inr DESC
        """)
    except Exception as e:
        st.error(f"Planet stats error: {str(e)}")
        return None