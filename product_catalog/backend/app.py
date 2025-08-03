from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Get all products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "quantity": p.quantity
        }
        for p in products
    ])
@app.route('/')
def home():
    return "Welcome to the Product Catalog API!"
# Add new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        quantity=int(data['quantity'])
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product added successfully"}), 201

# Delete product by ID
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
# Update product by ID
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    try:
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = float(data.get('price', product.price))
        product.quantity = int(data.get('quantity', product.quantity))

        db.session.commit()

        return jsonify({"message": "Product updated successfully"})
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid data types"}), 400


if __name__ == '__main__':

    app.run(debug=True)
