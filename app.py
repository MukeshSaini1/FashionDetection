from flask import Flask, render_template, request
from fashion_model import FashionDetector
import os
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
detector = FashionDetector('best.pt')  # Update with your model path

# Function to fetch products from Meesho (web scraping)
def fetch_meesho_products(item):
    try:
        search_url = f"https://meesho.com/search?q={item}"
        response = requests.get(search_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []

            # Scrape product data (adjust selectors as needed)
            for product in soup.select('.product-card'):
                product_name = product.select_one('.product-name').text.strip()
                product_link = product.find('a')['href']  # Get the link to the product
                product_price = product.select_one('.product-price').text.strip()
                product_image = product.select_one('img')['src']  # Get the product image URL

                products.append({
                    'name': product_name,
                    'link': f"https://meesho.com{product_link}",  # Construct full URL
                    'price': product_price,
                    'image': product_image,  # Add image URL
                })
            return products
        else:
            print(f"Error fetching from Meesho: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred while fetching Meesho products: {e}")
        return []

# Placeholder functions for Amazon and Flipkart (to be implemented)
def fetch_amazon_products(item):
    # Implement web scraping logic for Amazon
    return []  # Return an empty list for now

def fetch_flipkart_products(item):
    # Implement web scraping logic for Flipkart
    return []  # Return an empty list for now

@app.route('/', methods=['GET', 'POST'])
def index():
    products = {
        'meesho': {},
        'amazon': {},
        'flipkart': {}
    }  # Initialize with Meesho, Amazon, and Flipkart keys

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            # Save uploaded file
            file_path = os.path.join('static/upload', file.filename)
            file.save(file_path)

            # Perform detection
            result_image_path, detected_items = detector.predict(file_path)

            # Fetch products for each detected item
            for item in detected_items:
                products['meesho'][item] = fetch_meesho_products(item)
                products['amazon'][item] = fetch_amazon_products(item)  # Fetch Amazon products
                products['flipkart'][item] = fetch_flipkart_products(item)  # Fetch Flipkart products

            return render_template('index.html', result_image=result_image_path, products=products)

    return render_template('index.html', result_image=None, products=None)

if __name__ == '__main__':
    app.run(debug=True)
