from flask import Flask, request, jsonify, render_template_string, abort, redirect, url_for

app = Flask(__name__)

# Fake database to simulate finding/missing items
fake_db = {
    1: {"id": 1, "name": "Laptop", "price": 1000},
    2: {"id": 2, "name": "Phone", "price": 500}
}

# ==========================================
# 200 OK: Standard Success
# ==========================================
@app.route('/')
def home():
    # Scenario: User just visits the homepage. Everything is fine.
    # Flask defaults to 200, so we don't need to type it explicitly.
    return "<h1>Welcome to the Shop!</h1> <p>Visit /product/1 to see an item.</p>"

# ==========================================
# 201 Created: Successful Creation (API)
# ==========================================
@app.route('/api/product', methods=['POST'])
def create_product():
    # Scenario: An external app sends JSON to create a new product.
    data = request.get_json()
    
    # Simulate saving to DB...
    new_id = 3
    fake_db[new_id] = data
    
    # We return 201 to tell the client: "Resource created successfully."
    return jsonify({"message": "Product created", "id": new_id}), 201

# ==========================================
# 302 Found: Redirection
# ==========================================
@app.route('/old-shop')
def old_shop():
    # Scenario: User visits an old URL that we moved.
    # We redirect them to the new home. This sends a 302 automatically.
    return redirect(url_for('home'))

# ==========================================
# 400 Bad Request: Invalid Input
# ==========================================
@app.route('/search')
def search():
    # Scenario: User tries to search but forgets the query parameter.
    # Example URL: /search (Missing ?q=...)
    query = request.args.get('q')
    
    if not query:
        # We stop here because the client made a mistake.
        return "Error: You must provide a search term (e.g., /search?q=laptop)", 400
        
    return f"Searching for: {query}", 200

# ==========================================
# 401 Unauthorized: Not Logged In
# ==========================================
@app.route('/dashboard')
def dashboard():
    # Scenario: A guest tries to access a protected area.
    is_logged_in = False # Simulating a guest user
    
    if not is_logged_in:
        # We deny access because they aren't authenticated.
        return "Error: You must login to view this page.", 401
    
    return "Welcome to your dashboard!", 200

# ==========================================
# 403 Forbidden: Logged In, But No Permission
# ==========================================
@app.route('/admin')
def admin_panel():
    # Scenario: A regular user tries to access the Super Admin panel.
    user_role = "regular_user"
    
    if user_role != "admin":
        # They are logged in (401 is wrong), but they lack permission (403 is right).
        abort(403) 
        
    return "Welcome, Admin.", 200

# ==========================================
# 404 Not Found: Item Missing
# ==========================================
@app.route('/product/<int:product_id>')
def get_product(product_id):
    # Scenario: User asks for Product #99, but we only have #1 and #2.
    product = fake_db.get(product_id)
    
    if product is None:
        # The resource doesn't exist.
        abort(404)
        
    return jsonify(product) # Defaults to 200

# ==========================================
# 500 Internal Server Error: The Crash
# ==========================================
@app.route('/crash')
def crash_me():
    # Scenario: Bad code. We try to divide by zero.
    # You don't usually return 500 manually; Flask does it when your code breaks.
    x = 10 / 0 
    return "This line will never be reached"

# ==========================================
# CUSTOM ERROR HANDLERS (Making errors pretty)
# ==========================================
@app.errorhandler(404)
def page_not_found(e):
    # Instead of a plain text error, we show a nice page.
    return "<h1>404 Error</h1><p>Sorry, that product doesn't exist!</p>", 404

@app.errorhandler(500)
def server_error(e):
    return "<h1>500 Error</h1><p>Ouch! Something went wrong on our end.</p>", 500

if __name__ == '__main__':
    app.run(debug=True)