from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Amit@1215'
app.config['MYSQL_DB'] = 'your_database_name'

mysql = MySQL(app)
@app.route('/')
def home():
    return "Welcome to the E-Commerce Inventory Management System!"


# Endpoint to create a new product
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data['name']
    description = data.get('description', '')
    price = data['price']
    quantity = data['quantity']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO products (name, description, price, quantity) VALUES (%s, %s, %s, %s)",
                (name, description, price, quantity))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Product created successfully'}), 201

# Endpoint to get all products
@app.route('/products', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    cur.close()

    product_list = []
    for product in products:
        product_list.append({
            'id': product[0],
            'name': product[1],
            'description': product[2],
            'price': float(product[3]),
            'quantity': product[4]
        })
    
    return jsonify(product_list)

# Endpoint to get a product by ID
@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cur.fetchone()
    cur.close()

    if not product:
        return jsonify({'message': 'Product not found'}), 404

    return jsonify({
        'id': product[0],
        'name': product[1],
        'description': product[2],
        'price': float(product[3]),
        'quantity': product[4]
    })

# Endpoint to update a product by ID
@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    name = data['name']
    description = data.get('description', '')
    price = data['price']
    quantity = data['quantity']

    cur = mysql.connection.cursor()
    cur.execute("UPDATE products SET name = %s, description = %s, price = %s, quantity = %s WHERE id = %s",
                (name, description, price, quantity, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Product updated successfully'})

# Endpoint to delete a product by ID
@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM products WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

