"""
Database operations for SpaceBuy interplanetary e-commerce platform
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime
import uuid

class SpaceBuyDB:
    def __init__(self):
        self.database_url = os.environ.get('DATABASE_URL')
        self.connected = False
        try:
            self.init_tables()
            self.connected = True
        except Exception as e:
            print(f"Database initialization failed: {e}")
            self.connected = False
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
    
    def init_tables(self):
        """Initialize database tables"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Users table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        planet_preference VARCHAR(100),
                        total_spent_inr DECIMAL(15,2) DEFAULT 0,
                        loyalty_level VARCHAR(50) DEFAULT 'Space Cadet',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Orders table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,
                        order_id VARCHAR(100) UNIQUE NOT NULL,
                        user_id INTEGER REFERENCES users(id),
                        product_name VARCHAR(255) NOT NULL,
                        product_category VARCHAR(100),
                        destination_planet VARCHAR(100) NOT NULL,
                        base_price_usd DECIMAL(10,2) NOT NULL,
                        delivery_cost_usd DECIMAL(15,2) NOT NULL,
                        total_price_inr DECIMAL(15,2) NOT NULL,
                        space_agency VARCHAR(255),
                        order_status VARCHAR(50) DEFAULT 'Pending Launch',
                        estimated_delivery_time VARCHAR(100),
                        tracking_number VARCHAR(100),
                        special_instructions TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Planet delivery stats table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS planet_stats (
                        id SERIAL PRIMARY KEY,
                        planet_name VARCHAR(100) UNIQUE NOT NULL,
                        total_orders INTEGER DEFAULT 0,
                        total_revenue_inr DECIMAL(15,2) DEFAULT 0,
                        success_rate DECIMAL(5,2) DEFAULT 0,
                        average_delivery_days INTEGER DEFAULT 0,
                        last_delivery TIMESTAMP,
                        most_popular_product VARCHAR(255)
                    )
                ''')
                
                # Product search history table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS search_history (
                        id SERIAL PRIMARY KEY,
                        search_query VARCHAR(500) NOT NULL,
                        target_planet VARCHAR(100) NOT NULL,
                        ai_generated_price DECIMAL(15,2),
                        search_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_session VARCHAR(100)
                    )
                ''')
                
                # Customer feedback table
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS feedback (
                        id SERIAL PRIMARY KEY,
                        order_id VARCHAR(100) REFERENCES orders(order_id),
                        rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                        comment TEXT,
                        feedback_type VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
    
    def create_user(self, name, email, planet_preference=None):
        """Create a new user"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO users (name, email, planet_preference)
                    VALUES (%s, %s, %s)
                    RETURNING id
                ''', (name, email, planet_preference))
                return cur.fetchone()['id']
    
    def get_user(self, email):
        """Get user by email"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM users WHERE email = %s', (email,))
                return cur.fetchone()
    
    def create_order(self, user_id, product_name, product_category, 
                    destination_planet, base_price_usd, delivery_cost_usd, 
                    total_price_inr, space_agency, estimated_delivery_time, 
                    tracking_number, special_instructions=None):
        """Create a new order"""
        order_id = f"SB-{uuid.uuid4().hex[:8].upper()}"
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO orders (
                        order_id, user_id, product_name, product_category,
                        destination_planet, base_price_usd, delivery_cost_usd,
                        total_price_inr, space_agency, estimated_delivery_time,
                        tracking_number, special_instructions
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                ''', (order_id, user_id, product_name, product_category,
                     destination_planet, base_price_usd, delivery_cost_usd,
                     total_price_inr, space_agency, estimated_delivery_time,
                     tracking_number, special_instructions))
                
                # Update user's total spent
                total_inr = float(total_price_inr)
                cur.execute('''
                    UPDATE users 
                    SET total_spent_inr = total_spent_inr + %s,
                        loyalty_level = CASE 
                            WHEN total_spent_inr + %s > 10000000 THEN 'Galactic Emperor'
                            WHEN total_spent_inr + %s > 1000000 THEN 'Cosmic Commander'
                            WHEN total_spent_inr + %s > 100000 THEN 'Space Captain'
                            WHEN total_spent_inr + %s > 10000 THEN 'Orbital Officer'
                            ELSE 'Space Cadet'
                        END
                    WHERE id = %s
                ''', (total_inr, total_inr, total_inr, total_inr, total_inr, user_id))
                
                # Update planet stats
                self.update_planet_stats(destination_planet, total_inr, product_name)
                
                conn.commit()
                return order_id
    
    def update_planet_stats(self, planet_name, revenue_inr, product_name):
        """Update planet delivery statistics"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Insert or update planet stats
                cur.execute('''
                    INSERT INTO planet_stats (planet_name, total_orders, total_revenue_inr, most_popular_product)
                    VALUES (%s, 1, %s, %s)
                    ON CONFLICT (planet_name) DO UPDATE SET
                        total_orders = planet_stats.total_orders + 1,
                        total_revenue_inr = planet_stats.total_revenue_inr + %s,
                        most_popular_product = %s,
                        last_delivery = CURRENT_TIMESTAMP
                ''', (planet_name, revenue_inr, product_name, revenue_inr, product_name))
    
    def get_user_orders(self, user_id):
        """Get all orders for a user"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT * FROM orders 
                    WHERE user_id = %s 
                    ORDER BY created_at DESC
                ''', (user_id,))
                return cur.fetchall()
    
    def get_planet_stats(self):
        """Get statistics for all planets"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT * FROM planet_stats 
                    ORDER BY total_revenue_inr DESC
                ''')
                return cur.fetchall()
    
    def add_search_history(self, search_query, target_planet, ai_price, user_session):
        """Add search to history"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO search_history (search_query, target_planet, ai_generated_price, user_session)
                    VALUES (%s, %s, %s, %s)
                ''', (search_query, target_planet, ai_price, user_session))
    
    def get_popular_searches(self, limit=10):
        """Get most popular search queries"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    SELECT search_query, target_planet, COUNT(*) as search_count,
                           AVG(ai_generated_price) as avg_price
                    FROM search_history 
                    GROUP BY search_query, target_planet
                    ORDER BY search_count DESC
                    LIMIT %s
                ''', (limit,))
                return cur.fetchall()
    
    def add_feedback(self, order_id, rating, comment, feedback_type='general'):
        """Add customer feedback"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    INSERT INTO feedback (order_id, rating, comment, feedback_type)
                    VALUES (%s, %s, %s, %s)
                ''', (order_id, rating, comment, feedback_type))
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                # Total orders
                cur.execute('SELECT COUNT(*) as total_orders FROM orders')
                total_orders = cur.fetchone()['total_orders']
                
                # Total revenue
                cur.execute('SELECT SUM(total_price_inr) as total_revenue FROM orders')
                total_revenue = cur.fetchone()['total_revenue'] or 0
                
                # Total users
                cur.execute('SELECT COUNT(*) as total_users FROM users')
                total_users = cur.fetchone()['total_users']
                
                # Most popular planet
                cur.execute('''
                    SELECT destination_planet, COUNT(*) as order_count
                    FROM orders 
                    GROUP BY destination_planet 
                    ORDER BY order_count DESC 
                    LIMIT 1
                ''')
                popular_planet = cur.fetchone()
                
                # Average order value
                cur.execute('SELECT AVG(total_price_inr) as avg_order_value FROM orders')
                avg_order_value = cur.fetchone()['avg_order_value'] or 0
                
                return {
                    'total_orders': total_orders,
                    'total_revenue': float(total_revenue),
                    'total_users': total_users,
                    'most_popular_planet': popular_planet['destination_planet'] if popular_planet else 'Mars',
                    'avg_order_value': float(avg_order_value)
                }

# Global database instance
db = SpaceBuyDB()