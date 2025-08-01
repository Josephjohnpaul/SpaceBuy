// SpaceBuy Frontend JavaScript
class SpaceBuy {
    constructor() {
        this.currentUser = null;
        this.products = [];
        this.planets = {};
        this.spaceAgencies = {};
        this.planetExclusiveProducts = {};
        this.currentPlanet = 'Mars';
        
        this.init();
    }
    
    async init() {
        await this.loadData();
        this.setupEventListeners();
        this.populateSelectors();
        this.showPage('browse');
        this.updateProductDisplay();
    }
    
    async loadData() {
        try {
            this.showLoading(true);
            
            // Load all data from the backend
            const [productsRes, planetsRes, agenciesRes, exclusiveRes] = await Promise.all([
                fetch('/api/products'),
                fetch('/api/planets'),
                fetch('/api/agencies'),
                fetch('/api/exclusive-products')
            ]);
            
            this.products = await productsRes.json();
            this.planets = await planetsRes.json();
            this.spaceAgencies = await agenciesRes.json();
            this.planetExclusiveProducts = await exclusiveRes.json();
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.showNotification('Failed to load data', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const page = e.target.dataset.page;
                this.showPage(page);
            });
        });
        
        // Login form
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });
        
        // Logout
        document.getElementById('logout-btn').addEventListener('click', () => {
            this.handleLogout();
        });
        
        // Planet selection
        document.getElementById('destination-planet').addEventListener('change', (e) => {
            this.currentPlanet = e.target.value;
            this.updateProductDisplay();
            this.checkSunWarning();
        });
        
        // Filters
        document.getElementById('category-filter').addEventListener('change', () => {
            this.updateProductDisplay();
        });
        
        // Sun job application
        document.getElementById('sun-job-btn').addEventListener('click', () => {
            this.showNotification('🎉 Congratulations! Please proceed to our Careers section to apply!');
            this.showPage('contact');
        });
        
        // AI Search
        document.getElementById('search-btn').addEventListener('click', () => {
            this.handleAISearch();
        });
    }
    
    populateSelectors() {
        // Populate planet selectors
        const planetSelectors = [
            document.getElementById('destination-planet'),
            document.getElementById('target-planet'),
            document.getElementById('planet-pref')
        ];
        
        planetSelectors.forEach(selector => {
            if (selector) {
                selector.innerHTML = '';
                if (selector.id === 'planet-pref') {
                    selector.innerHTML = '<option value="">Select Favorite Planet</option>';
                }
                
                Object.keys(this.planets).forEach(planet => {
                    const option = document.createElement('option');
                    option.value = planet;
                    option.textContent = planet;
                    if (planet === 'Mars' && selector.id === 'destination-planet') {
                        option.selected = true;
                    }
                    selector.appendChild(option);
                });
            }
        });
        
        // Populate category filter
        const categoryFilter = document.getElementById('category-filter');
        const categories = [...new Set(this.products.map(p => p.category))];
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category;
            option.textContent = category;
            categoryFilter.appendChild(option);
        });
        
        // Populate agency filter  
        const agencyFilter = document.getElementById('agency-filter');
        Object.keys(this.spaceAgencies).forEach(agency => {
            const option = document.createElement('option');
            option.value = agency;
            option.textContent = agency;
            agencyFilter.appendChild(option);
        });
    }
    
    showPage(pageName) {
        // Hide all pages
        document.querySelectorAll('.page').forEach(page => {
            page.classList.remove('active');
        });
        
        // Show selected page
        document.getElementById(`${pageName}-page`).classList.add('active');
        
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-page="${pageName}"]`).classList.add('active');
        
        // Load page-specific content
        if (pageName === 'orders') {
            this.loadUserOrders();
        }
    }
    
    async handleLogin() {
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const planetPref = document.getElementById('planet-pref').value;
        
        if (!name || !email) {
            this.showNotification('Please fill in all required fields', 'error');
            return;
        }
        
        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, planet_pref: planetPref || null })
            });
            
            if (response.ok) {
                this.currentUser = await response.json();
                this.updateUserDisplay();
                this.showNotification(`Welcome to SpaceBuy, ${this.currentUser.name}!`);
            } else {
                this.showNotification('Login failed: Please try again', 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showNotification('Login failed: Please try again', 'error');
        }
    }
    
    handleLogout() {
        this.currentUser = null;
        this.updateUserDisplay();
        this.showNotification('Logged out successfully');
    }
    
    updateUserDisplay() {
        const loginForm = document.getElementById('login-form');
        const userInfo = document.getElementById('user-info');
        
        if (this.currentUser) {
            loginForm.style.display = 'none';
            userInfo.style.display = 'block';
            document.getElementById('user-greeting').textContent = `👋 ${this.currentUser.name}`;
            document.getElementById('user-loyalty').textContent = `🏅 ${this.currentUser.loyalty_level}`;
        } else {
            loginForm.style.display = 'block';
            userInfo.style.display = 'none';
            // Clear form
            document.getElementById('loginForm').reset();
        }
    }
    
    checkSunWarning() {
        const sunWarning = document.getElementById('sun-warning');
        const productsContainer = document.getElementById('products-container');
        
        if (this.currentPlanet && this.currentPlanet.toLowerCase() === 'sun') {
            sunWarning.style.display = 'block';
            productsContainer.style.display = 'none';
        } else {
            sunWarning.style.display = 'none';
            productsContainer.style.display = 'block';
        }
    }
    
    updateProductDisplay() {
        if (!this.currentPlanet) return;
        
        this.checkSunWarning();
        if (this.currentPlanet.toLowerCase() === 'sun') return;
        
        // Update planet info
        const planetInfo = this.planets[this.currentPlanet];
        if (planetInfo) {
            document.getElementById('planet-distance').textContent = 
                `Distance from Earth: ${planetInfo.distance} AU`;
        }
        
        // Update titles
        document.getElementById('earth-products-title').textContent = 
            `🌍 Earth Products for ${this.currentPlanet}`;
        
        // Filter products
        const categoryFilter = document.getElementById('category-filter').value;
        let filteredProducts = this.products;
        if (categoryFilter !== 'All') {
            filteredProducts = this.products.filter(p => p.category === categoryFilter);
        }
        
        // Display Earth products
        this.displayEarthProducts(filteredProducts);
        
        // Display exclusive products
        this.displayExclusiveProducts();
    }
    
    displayEarthProducts(products) {
        const container = document.getElementById('earth-products-list');
        container.innerHTML = '';
        
        products.forEach(product => {
            const productCard = this.createProductCard(product, false);
            container.appendChild(productCard);
        });
    }
    
    displayExclusiveProducts() {
        const container = document.getElementById('exclusive-products-list');
        const exclusiveSection = document.getElementById('exclusive-products');
        
        if (this.planetExclusiveProducts[this.currentPlanet]) {
            exclusiveSection.style.display = 'block';
            container.innerHTML = '';
            
            document.getElementById('exclusive-products-title').textContent = 
                `⭐ ${this.currentPlanet} Exclusive Products`;
            
            this.planetExclusiveProducts[this.currentPlanet].forEach(product => {
                const productCard = this.createProductCard(product, true);
                container.appendChild(productCard);
            });
        } else {
            exclusiveSection.style.display = 'none';
        }
    }
    
    createProductCard(product, isExclusive) {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        const planetInfo = this.planets[this.currentPlanet];
        let deliveryCost = 0;
        let totalPrice = product.base_price;
        
        if (!isExclusive) {
            // Calculate delivery cost for Earth products
            deliveryCost = this.calculateDeliveryCost(product.base_price, planetInfo);
            totalPrice = product.base_price + deliveryCost;
        }
        
        const agency = this.getRandomAgency();
        const agencyInfo = this.spaceAgencies[agency];
        
        card.innerHTML = `
            <div class="product-header">
                <div class="product-title">${product.emoji} ${product.name}</div>
                <div class="product-price">${this.formatPrice(totalPrice)}</div>
            </div>
            <div class="product-details">
                <div class="product-info">
                    <p><strong>Description:</strong> ${product.description}</p>
                    <p><strong>Category:</strong> ${product.category}</p>
                    ${isExclusive ? 
                        `<p><strong>Exclusive to:</strong> ${product.exclusive_to}</p>
                         <p style="color: #28a745;"><strong>✨ FREE LOCAL DELIVERY! No interplanetary shipping costs!</strong></p>
                         <p><strong>Local Delivery by:</strong> ${this.currentPlanet} Express Delivery</p>
                         <p><strong>Estimated Delivery:</strong> Same day delivery!</p>` :
                        `<p><strong>Earth Price:</strong> ${this.formatPrice(product.base_price)}</p>
                         <p><strong>${this.currentPlanet} Price:</strong> ${this.formatPrice(totalPrice)}</p>
                         <p><strong>Delivery by:</strong> ${agency} - ${agencyInfo.motto}</p>
                         <p><strong>Reliability:</strong> ${agencyInfo.reliability}</p>
                         <p><strong>Estimated Delivery:</strong> ${agencyInfo.delivery_time}</p>`
                    }
                </div>
                <div class="product-actions">
                    <button class="buy-btn" onclick="spaceBuy.handlePurchase('${product.name}', ${totalPrice}, '${agency}', ${isExclusive})">
                        ${isExclusive ? `💳 Buy Local for ${this.formatPrice(totalPrice)}` : `💸 Buy for ${this.formatPrice(totalPrice)}`}
                    </button>
                    ${!isExclusive ? 
                        `<button class="breakdown-btn" onclick="spaceBuy.showCostBreakdown('${product.name}', ${product.base_price}, ${deliveryCost})">
                            📊 Cost Breakdown
                        </button>` : 
                        `<div style="background: rgba(40, 167, 69, 0.2); padding: 10px; border-radius: 5px; margin-top: 10px; font-size: 12px;">
                            🏪 <strong>Local Product Benefits:</strong><br>
                            • No shipping costs<br>
                            • Same day delivery<br>
                            • Authentic local quality<br>
                            • Support local economy
                        </div>`
                    }
                </div>
            </div>
        `;
        
        return card;
    }
    
    calculateDeliveryCost(basePrice, planetInfo) {
        // Simplified cost calculation based on distance and gravity
        const distanceFactor = Math.pow(planetInfo.distance, 2);
        const gravityFactor = Math.abs(planetInfo.gravity - 1) + 1;
        const baseCost = basePrice * 5; // 500% base delivery cost
        
        return baseCost * distanceFactor * gravityFactor;
    }
    
    getRandomAgency() {
        const agencies = Object.keys(this.spaceAgencies);
        return agencies[Math.floor(Math.random() * agencies.length)];
    }
    
    formatPrice(price) {
        // Convert USD to INR (1 USD = 83 INR)
        const inrPrice = price * 83;
        return `₹${inrPrice.toLocaleString('en-IN', { maximumFractionDigits: 0 })}`;
    }
    
    async handlePurchase(productName, totalPrice, agency, isExclusive) {
        if (!this.currentUser) {
            this.showNotification('🚀 Please login first to place orders!', 'warning');
            return;
        }
        
        try {
            const response = await fetch('/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: this.currentUser.id,
                    product_name: isExclusive ? `${productName} (${this.currentPlanet} Exclusive)` : productName,
                    destination_planet: this.currentPlanet,
                    total_price_inr: totalPrice * 83,
                    space_agency: isExclusive ? `${this.currentPlanet} Express` : agency,
                    is_exclusive: isExclusive
                })
            });
            
            if (response.ok) {
                const order = await response.json();
                this.showNotification(`🎉 Order placed! Order ID: ${order.order_id}`);
                this.showNotification(`📦 Tracking: ${order.tracking_number}`, 'info');
            } else {
                this.showNotification('💸 Order failed: Please try again!', 'error');
            }
        } catch (error) {
            console.error('Purchase error:', error);
            this.showNotification('💸 Order failed: Please try again!', 'error');
        }
    }
    
    showCostBreakdown(productName, basePrice, deliveryCost) {
        const breakdown = `
            <div class="cost-breakdown">
                <h4>💰 Cost Breakdown for ${productName}</h4>
                <p><strong>Base Product Price:</strong> ${this.formatPrice(basePrice)}</p>
                <p><strong>Interplanetary Shipping:</strong> ${this.formatPrice(deliveryCost)}</p>
                <p><strong>Total Price:</strong> ${this.formatPrice(basePrice + deliveryCost)}</p>
                <p><em>Warning: Prices may cause financial ruin! 🚨</em></p>
            </div>
        `;
        
        // Show breakdown in a modal or alert
        this.showNotification(breakdown, 'info', 5000);
    }
    
    async handleAISearch() {
        const query = document.getElementById('product-query').value;
        const targetPlanet = document.getElementById('target-planet').value;
        
        if (!query) {
            this.showNotification('Please enter a product to search for', 'warning');
            return;
        }
        
        if (targetPlanet.toLowerCase() === 'sun') {
            document.getElementById('search-results').innerHTML = `
                <div class="hiring-notice">
                    <h2>🔥 SUN DELIVERY REQUEST DETECTED! 🔥</h2>
                    <p><strong>How are you alive there?!</strong></p>
                    <p>None of our employees came back alive attempting to deliver packages to the Sun...</p>
                    <p><strong>Are you interested in joining our delivery team?</strong></p>
                    <p>We need someone with your... unique heat resistance!</p>
                </div>
            `;
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/api/ai-search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    product_query: query,
                    target_planet: targetPlanet,
                    user_session: this.getUserSession()
                })
            });
            
            if (response.ok) {
                const result = await response.json();
                this.displaySearchResults(result);
            } else {
                this.showNotification('AI search failed. Please try again.', 'error');
            }
        } catch (error) {
            console.error('AI search error:', error);
            this.showNotification('AI search failed. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }
    
    displaySearchResults(result) {
        const container = document.getElementById('search-results');
        container.innerHTML = `
            <div class="product-card">
                <div class="product-header">
                    <div class="product-title">🛍️ ${result.product_query} on ${result.target_planet}</div>
                    <div class="product-price">${this.formatPrice(result.total_price)}</div>
                </div>
                <div class="product-details">
                    <div class="product-info">
                        <p>${result.product_description}</p>
                        <p><strong>Earth Price:</strong> ${this.formatPrice(result.base_price)}</p>
                        <p><strong>${result.target_planet} Price:</strong> ${this.formatPrice(result.total_price)}</p>
                        <p><strong>Price Multiplier:</strong> ${result.multiplier}x</p>
                        <p><strong>Reasoning:</strong> ${result.reasoning}</p>
                    </div>
                    <div class="product-actions">
                        <button class="buy-btn" onclick="spaceBuy.handleAISearchPurchase('${result.product_query}', ${result.total_price}, '${result.target_planet}')">
                            💸 Buy for ${this.formatPrice(result.total_price)}
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    async handleAISearchPurchase(productName, totalPrice, targetPlanet) {
        if (!this.currentUser) {
            this.showNotification('🚀 Please login first to place orders!', 'warning');
            return;
        }
        
        // Similar to regular purchase but for AI search results
        this.handlePurchase(productName, totalPrice, this.getRandomAgency(), false);
    }
    
    async loadUserOrders() {
        if (!this.currentUser) {
            document.getElementById('orders-list').innerHTML = '<p>Please login to view your orders.</p>';
            return;
        }
        
        try {
            const response = await fetch(`/api/orders/${this.currentUser.id}`);
            if (response.ok) {
                const orders = await response.json();
                this.displayUserOrders(orders);
            } else {
                document.getElementById('orders-list').innerHTML = '<p>Failed to load orders.</p>';
            }
        } catch (error) {
            console.error('Error loading orders:', error);
            document.getElementById('orders-list').innerHTML = '<p>Failed to load orders.</p>';
        }
    }
    
    displayUserOrders(orders) {
        const container = document.getElementById('orders-list');
        
        if (orders.length === 0) {
            container.innerHTML = '<p>No orders found. Start shopping to see your orders here!</p>';
            return;
        }
        
        container.innerHTML = orders.map(order => `
            <div class="order-item">
                <div class="order-header">
                    <div>
                        <strong>Order #${order.id}</strong> - ${order.product_name}
                    </div>
                    <div class="order-status ${order.status}">
                        ${order.status.toUpperCase()}
                    </div>
                </div>
                <p><strong>Destination:</strong> ${order.destination_planet}</p>
                <p><strong>Total Price:</strong> ₹${order.total_price_inr.toLocaleString('en-IN')}</p>
                <p><strong>Space Agency:</strong> ${order.space_agency}</p>
                <p><strong>Tracking:</strong> ${order.tracking_number}</p>
                <p><strong>Estimated Delivery:</strong> ${order.estimated_delivery_time}</p>
                <p><strong>Order Date:</strong> ${new Date(order.created_at).toLocaleDateString()}</p>
            </div>
        `).join('');
    }
    
    getUserSession() {
        if (!this.userSession) {
            this.userSession = 'user_' + Math.random().toString(36).substr(2, 9);
        }
        return this.userSession;
    }
    
    showLoading(show) {
        document.getElementById('loading').style.display = show ? 'flex' : 'none';
    }
    
    showNotification(message, type = 'success', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = message;
        
        // Add click to dismiss
        notification.addEventListener('click', () => {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        });
        
        document.getElementById('notifications').appendChild(notification);
        
        // Auto dismiss
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.transform = 'translateX(100%)';
                notification.style.opacity = '0';
                setTimeout(() => notification.remove(), 300);
            }
        }, duration);
        
        // Success notification effects
        if (type === 'success') {
            // Add some celebration particles
            this.createParticles(5);
        }
    }
    
    createParticles(count) {
        for (let i = 0; i < count; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.cssText = `
                position: fixed;
                width: 6px;
                height: 6px;
                background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
                border-radius: 50%;
                pointer-events: none;
                z-index: 1002;
                top: 50%;
                left: 50%;
                animation: particle-float 2s ease-out forwards;
            `;
            
            document.body.appendChild(particle);
            
            // Random direction and remove after animation
            const angle = (Math.PI * 2 * i) / count;
            const velocity = 100 + Math.random() * 50;
            particle.style.setProperty('--dx', `${Math.cos(angle) * velocity}px`);
            particle.style.setProperty('--dy', `${Math.sin(angle) * velocity}px`);
            
            setTimeout(() => particle.remove(), 2000);
        }
    }
}

// Initialize the application
let spaceBuy;
document.addEventListener('DOMContentLoaded', () => {
    spaceBuy = new SpaceBuy();
});