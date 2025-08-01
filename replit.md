# SpaceBuy - Interplanetary E-Commerce Platform

## Overview

SpaceBuy is an AI-powered interplanetary e-commerce platform that enables customers to purchase Earth products and have them delivered to various planets across the solar system. The application uses Gemini AI to generate dynamic pricing based on planetary characteristics such as distance, gravity, atmosphere, and delivery difficulty. Built with Streamlit for the frontend, the platform provides an immersive space-themed shopping experience with realistic cost calculations for interplanetary logistics.

## User Preferences

Preferred communication style: Simple, everyday language.
Currency preference: Indian Rupees (₹) - All pricing converted from USD at rate of 1 USD = 83 INR.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit-based web application with custom CSS for space theming
- **UI Components**: Product catalog, planetary destination selector, cost breakdown displays, and interactive shopping interface
- **Styling**: Custom CSS with gradient backgrounds, planet cards, and space-themed visual elements
- **Layout**: Wide layout with expandable sidebar for enhanced user experience

### Backend Architecture
- **Core Logic**: Python-based modular architecture with separated concerns
- **Data Layer**: Mock data generation for products, planets, and space agencies stored in dedicated modules
- **Database Layer**: PostgreSQL database with user management, order tracking, analytics, and search history
- **Pricing Engine**: AI-powered dynamic pricing system using Google's Gemini AI
- **Utility Functions**: Mathematical calculations for delivery costs based on planetary physics

### AI Integration
- **Model**: Google Gemini 2.5 Flash for content generation
- **Pricing Logic**: Considers distance (AU), gravity (relative to Earth), atmospheric conditions, and delivery difficulty ratings
- **Output Format**: Structured JSON responses with base prices, multipliers, and humorous but scientifically plausible reasoning
- **Fallback**: Built-in mock pricing system for scenarios when AI service is unavailable

### Data Management
- **Product Catalog**: Static product definitions with categories, base prices, and descriptions
- **Planetary Database**: Comprehensive planet characteristics including distance, gravity, atmosphere, and delivery difficulty scores
- **Cost Calculation**: Mathematical models incorporating exponential distance factors, gravity deviations, atmospheric hazards, and market volatility
- **User Management**: PostgreSQL-based user accounts with loyalty levels and spending tracking
- **Order Processing**: Complete order lifecycle from creation to tracking with delivery status
- **Analytics System**: Real-time dashboard with sales metrics, planet performance, and customer insights

### Pricing Strategy
- **Base Pricing**: Earth retail prices as foundation
- **Dynamic Multipliers**: AI-generated multipliers (2x to 50x) based on delivery complexity
- **Cost Components**: Product price, shipping complexity, special handling, insurance, and fuel costs
- **Market Simulation**: Random volatility factors to simulate realistic market conditions

## External Dependencies

### AI Services
- **Google Gemini AI**: Core pricing intelligence and product description generation
- **API Key Management**: Environment variable-based configuration for secure API access

### Python Libraries
- **Streamlit**: Web application framework for interactive frontend
- **Pandas**: Data manipulation and analysis for product/planetary data
- **Google GenAI**: Official Google Generative AI client library

### Development Tools
- **Environment Variables**: Secure API key storage and configuration management
- **JSON Processing**: Structured data exchange between AI service and application logic

### Mock Data Sources
- **Product Database**: Electronics, vehicles, food & beverages, fashion items with realistic Earth pricing
- **Planetary Information**: Solar system bodies with scientifically-based characteristics
- **Space Agencies**: Fictional delivery partners for immersive experience