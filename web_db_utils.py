"""
Database utilities for SpaceBuy web server (Flask version)
"""

import os
import uuid
import psycopg2
from datetime import datetime
from typing import Optional, Dict, List, Any

class DatabaseManager:
    def __init__(self):
        self.connection_string = os.environ.get(
            'DATABASE_URL',
            'postgresql://localhost:5432/spacebuy'
        )
    
    def get_connection(self):
        """Get database connection"""
        try:
            return psycopg2.connect(self.connection_string)
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            return None
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = self.get_connection()
            if not conn:
                return False
                
            cursor = conn.cursor()
            
            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    planet_preference VARCHAR(100),
                    total_spent_inr DECIMAL(12,2) DEFAULT 0,
                    loyalty_level VARCHAR(50) DEFAULT 'Space Cadet',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create orders table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    order_id VARCHAR(50) UNIQUE NOT NULL,
                    user_id INTEGER REFERENCES users(id),
                    product_name VARCHAR(255) NOT NULL,
                    product_category VARCHAR(100),
                    destination_planet VARCHAR(100) NOT NULL,
                    base_price_usd DECIMAL(10,2) NOT NULL,
                    delivery_cost_usd DECIMAL(10,2) NOT NULL,
                    total_price_inr DECIMAL(12,2) NOT NULL,
                    space_agency VARCHAR(255),
                    tracking_number VARCHAR(100),
                    estimated_delivery_time VARCHAR(100),
                    special_instructions TEXT,
                    status VARCHAR(50) DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create search_history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS search_history (
                    id SERIAL PRIMARY KEY,
                    product_query VARCHAR(500) NOT NULL,
                    target_planet VARCHAR(100) NOT NULL,
                    calculated_price DECIMAL(12,2),
                    user_session VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Database initialization error: {e}")
            return False

# Global database manager instance
db_manager = DatabaseManager()

def init_database():
    """Initialize database tables"""
    return db_manager.init_database()

def create_user(name: str, email: str, planet_preference: Optional[str] = None) -> Optional[Dict]:
    """Create a new user and return user data"""
    try:
        conn = db_manager.get_connection()
        if not conn:
            return None
            
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            # Return existing user data
            columns = [desc[0] for desc in cursor.description]
            user_dict = dict(zip(columns, existing_user))
            cursor.close()
            conn.close()
            return user_dict
        
        # Create new user
        cursor.execute("""
            INSERT INTO users (name, email, planet_preference)
            VALUES (%s, %s, %s)
            RETURNING *
        """, (name, email, planet_preference))
        
        new_user = cursor.fetchone()
        conn.commit()
        
        if new_user:
            columns = [desc[0] for desc in cursor.description]
            user_dict = dict(zip(columns, new_user))
            cursor.close()
            conn.close()
            return user_dict
        
        cursor.close()
        conn.close()
        return None
        
    except Exception as e:
        print(f"Create user error: {e}")
        return None

def create_order(user_id: int, product_name: str, product_category: str, 
                destination_planet: str, base_price_usd: float, delivery_cost_usd: float,
                total_price_inr: float, space_agency: str, estimated_delivery_time: str,
                tracking_number: str, special_instructions: Optional[str] = None) -> Optional[int]:
    """Create a new order and return order ID"""
    try:
        conn = db_manager.get_connection()
        if not conn:
            return None
            
        cursor = conn.cursor()
        
        order_id = f"SB-{uuid.uuid4().hex[:8].upper()}"
        
        cursor.execute("""
            INSERT INTO orders (
                order_id, user_id, product_name, product_category,
                destination_planet, base_price_usd, delivery_cost_usd,
                total_price_inr, space_agency, estimated_delivery_time,
                tracking_number, special_instructions
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            order_id, user_id, product_name, product_category,
            destination_planet, base_price_usd, delivery_cost_usd,
            total_price_inr, space_agency, estimated_delivery_time,
            tracking_number, special_instructions
        ))
        
        created_order_id = cursor.fetchone()[0]
        
        # Update user spending and loyalty
        cursor.execute("""
            UPDATE users 
            SET total_spent_inr = total_spent_inr + %s,
                loyalty_level = CASE 
                    WHEN total_spent_inr + %s > 10000000 THEN 'Galactic Emperor'
                    WHEN total_spent_inr + %s > 1000000 THEN 'Cosmic Commander'
                    WHEN total_spent_inr + %s > 100000 THEN 'Star Captain'
                    WHEN total_spent_inr + %s > 10000 THEN 'Space Pilot'
                    ELSE 'Space Cadet'
                END
            WHERE id = %s
        """, (total_price_inr, total_price_inr, total_price_inr, total_price_inr, total_price_inr, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        return created_order_id
        
    except Exception as e:
        print(f"Create order error: {e}")
        return None

def get_user_orders(user_id: int) -> List[Dict]:
    """Get all orders for a user"""
    try:
        conn = db_manager.get_connection()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM orders 
            WHERE user_id = %s 
            ORDER BY created_at DESC
        """, (user_id,))
        
        orders = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        order_list = []
        for order in orders:
            order_dict = dict(zip(columns, order))
            # Convert datetime to string for JSON serialization
            if 'created_at' in order_dict and order_dict['created_at']:
                order_dict['created_at'] = order_dict['created_at'].isoformat()
            order_list.append(order_dict)
        
        cursor.close()
        conn.close()
        return order_list
        
    except Exception as e:
        print(f"Get user orders error: {e}")
        return []

def add_search_history(product_query: str, target_planet: str, calculated_price: float, user_session: str):
    """Add search query to history"""
    try:
        conn = db_manager.get_connection()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO search_history (product_query, target_planet, calculated_price, user_session)
            VALUES (%s, %s, %s, %s)
        """, (product_query, target_planet, calculated_price, user_session))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Add search history error: {e}")
        return False

def get_analytics_data() -> Dict[str, Any]:
    """Get analytics data for dashboard"""
    try:
        conn = db_manager.get_connection()
        if not conn:
            return {}
            
        cursor = conn.cursor()
        
        # Total orders
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]
        
        # Total revenue
        cursor.execute("SELECT SUM(total_price_inr) FROM orders")
        total_revenue = cursor.fetchone()[0] or 0
        
        # Most popular planets
        cursor.execute("""
            SELECT destination_planet, COUNT(*) as order_count
            FROM orders 
            GROUP BY destination_planet 
            ORDER BY order_count DESC 
            LIMIT 5
        """)
        popular_planets = cursor.fetchall()
        
        # Recent orders
        cursor.execute("""
            SELECT order_id, product_name, destination_planet, total_price_inr, created_at
            FROM orders 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        recent_orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return {
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'popular_planets': [{'planet': p[0], 'orders': p[1]} for p in popular_planets],
            'recent_orders': [
                {
                    'order_id': r[0],
                    'product_name': r[1],
                    'destination_planet': r[2],
                    'total_price_inr': float(r[3]),
                    'created_at': r[4].isoformat() if r[4] else None
                } for r in recent_orders
            ]
        }
        
    except Exception as e:
        print(f"Get analytics error: {e}")
        return {}