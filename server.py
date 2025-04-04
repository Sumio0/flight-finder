from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import re
import os

app = Flask(__name__)

# Load flights data
flights = {
    # New York → China (First 5 flights)
    "1": {
        "id": "1",
        "title": "Delta DL289",
        "image": "https://images.unsplash.com/photo-1513622790541-eaa84d356909?q=80&w=2274&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
        "year": "2024",
        "summary": "A non-stop Delta flight from New York (JFK) to Hong Kong (HKG).",
        "airline": "Delta Airlines",
        "departure": "JFK - New York John F. Kennedy International Airport",
        "arrival": "HKG - Hong Kong International Airport",
        "flight_time": "16h 10m",
        "price": "1080",
        "baggage_policy": "1 free checked bag + 1 carry-on",
        "schedule": ["Monday", "Wednesday", "Friday"],
        "reviews": ["Smooth flight.", "Excellent food and service."]
    },
        "2": {
        "id": "2",
        "title": "United Airlines UA089",
        "image": "https://images.unsplash.com/photo-1548919973-5cef591cdbc9?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8N3x8c2hhbmdoYWl8ZW58MHx8MHx8fDA%3D",
        "year": "2024",
        "summary": "A direct flight from New York (EWR) to Shanghai (PVG) operated by United Airlines.",
        "airline": "United Airlines",
        "departure": "EWR - Newark Liberty International Airport",
        "arrival": "PVG - Shanghai Pudong International Airport",
        "flight_time": "16h 15m",
        "price": "890",
        "baggage_policy": "1 free checked bag + 1 carry-on",
        "schedule": ["Thursday", "Sunday"],
        "reviews": ["Great inflight experience.", "Comfortable seats."]
    },
    "3": {
        "id": "3",
        "title": "American Airlines AA182",
        "image": "https://images.unsplash.com/photo-1620964780032-81ef649db4d9?w=900&auto=format&fit=crop&q=60",
        "year": "2024",
        "summary": "A direct flight from New York (JFK) to Beijing (PEK) by American Airlines.",
        "airline": "American Airlines",
        "departure": "JFK - New York John F. Kennedy International Airport",
        "arrival": "PEK - Beijing Capital International Airport",
        "flight_time": "14h 50m",
        "price": "1050",
        "baggage_policy": "2 free checked bags",
        "schedule": ["Sunday", "Wednesday"],
        "reviews": ["Best value for money.", "Friendly staff."]
    },
    "4": {
        "id": "4",
        "title": "JetBlue B6790",
        "image": "https://media.istockphoto.com/id/2042619432/photo/scenery-of-high-rise-buildings-and-yangtze-river-cableways-in-chongqing-china.jpg?s=612x612&w=0&k=20&c=E4MnDmL4cOIm6ajuQ7n4O10aABV8c3-K-dofwad_wwg=",
        "year": "2024",
        "summary": "A direct flight from New York (LGA) to Chongqing (CKG) operated by JetBlue.",
        "airline": "JetBlue",
        "departure": "LGA - New York LaGuardia Airport",
        "arrival": "CKG - Chongqing Jiangbei International Airport",
        "flight_time": "15h 20m",
        "price": "990",
        "baggage_policy": "1 free checked bag",
        "schedule": ["Monday", "Friday"],
        "reviews": ["Great service.", "Comfortable seating."]
    },
    "5": {
        "id": "5",
        "title": "Delta DL829",
        "image": "https://images.unsplash.com/photo-1635086407834-3f09fc29717f?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8Z3Vhbmd6aG91fGVufDB8fDB8fHww",
        "year": "2024",
        "summary": "A budget-friendly non-stop flight from New York (EWR) to Guangzhou (CAN).",
        "airline": "Delta Airlines",
        "departure": "EWR - Newark Liberty International Airport",
        "arrival": "CAN - Guangzhou Baiyun International Airport",
        "flight_time": "16h 10m",
        "price": "920",
        "baggage_policy": "1 free checked bag",
        "schedule": ["Wednesday", "Sunday"],
        "reviews": ["Affordable price.", "Good in-flight meals."]
    },
    "6": {
        "id": "6",
        "title": "American Airlines AA846",
        "image": "https://images.unsplash.com/photo-1622471645219-eedda198d36f?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fGNoZW5nZHV8ZW58MHx8MHx8fDA%3D",
        "year": "2024",
        "summary": "A premium non-stop flight from New York (JFK) to Chengdu (CTU) by American Airlines.",
        "airline": "American Airlines",
        "departure": "JFK - New York John F. Kennedy International Airport",
        "arrival": "CTU - Chengdu Tianfu International Airport",
        "flight_time": "15h 40m",
        "price": "1180",
        "baggage_policy": "2 free checked bags",
        "schedule": ["Tuesday", "Saturday"],
        "reviews": ["Best service.", "Smooth flight experience."]
    },
    "7": {
        "id": "7",
        "title": "United Airlines UA857",
        "image": "https://images.unsplash.com/photo-1630511941331-78b86ddba27c?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHd1aGFufGVufDB8fDB8fHww",
        "year": "2024",
        "summary": "A direct United flight from New York (EWR) to Wuhan (WUH).",
        "airline": "United Airlines",
        "departure": "EWR - Newark Liberty International Airport",
        "arrival": "WUH - Wuhan Tianhe International Airport",
        "flight_time": "15h 45m",
        "price": "960",
        "baggage_policy": "2 free checked bags",
        "schedule": ["Tuesday", "Thursday", "Saturday"],
        "reviews": ["Best airline for long-haul flights.", "Plenty of legroom."]
    },
    "8": {
        "id": "8",
        "title": "Delta DL589",
        "image": "https://media.istockphoto.com/id/1250162628/photo/qingdao-fushan-bay-architectural-landscape-skyline.jpg?s=612x612&w=0&k=20&c=G-8gBlYgXS1uDjAYO3Tg5YR9n8vBmkfA-FK_lyMRmQk=",
        "year": "2024",
        "summary": "A direct flight from New York (LGA) to Qingdao (TAO) with Delta Airlines.",
        "airline": "Delta Airlines",
        "departure": "LGA - New York LaGuardia Airport",
        "arrival": "TAO - Qingdao Jiaodong International Airport",
        "flight_time": "14h 30m",
        "price": "1020",
        "baggage_policy": "2 free checked bags",
        "schedule": ["Wednesday", "Saturday"],
        "reviews": ["Best airline staff.", "Amazing food."]
    },
    "9": {
        "id": "9",
        "title": "JetBlue B6992",
        "image": "https://images.unsplash.com/photo-1608381742187-ea4b48c56630?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8c2hlbnpoZW58ZW58MHx8MHx8fDA%3D",
        "year": "2024",
        "summary": "A non-stop flight from New York (LGA) to Shenzhen (SZX) by JetBlue.",
        "airline": "JetBlue",
        "departure": "LGA - New York LaGuardia Airport",
        "arrival": "SZX - Shenzhen Bao'an International Airport",
        "flight_time": "15h 45m",
        "price": "950",
        "baggage_policy": "1 free checked bag",
        "schedule": ["Monday", "Thursday"],
        "reviews": ["Excellent long-haul flight.", "Spacious legroom."]
    },
    "10": {
        "id": "10",
        "title": "American Airlines AA024",
        "image": "https://images.unsplash.com/photo-1515975325863-a4ceb4b7d6c0?w=700&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHRhaXBlaXxlbnwwfHwwfHx8MA%3D%3D",
        "year": "2024",
        "summary": "A premium long-haul flight from New York (JFK) to Taipei (TPE) operated by American Airlines.",
        "airline": "American Airlines",
        "departure": "JFK - New York John F. Kennedy International Airport",
        "arrival": "TPE - Taiwan Taoyuan International Airport",
        "flight_time": "16h 10m",
        "price": "1150",
        "baggage_policy": "2 free checked bags + 1 carry-on",
        "schedule": ["Tuesday", "Saturday"],
        "reviews": ["Incredible in-flight experience!", "Loved the spacious seating.", "Smooth takeoff and landing."]
    }
}

# Save data to a JSON file to persist changes
def save_flights_data():
    with open('flights_data.json', 'w') as f:
        json.dump(flights, f)

# Load data from JSON file if it exists
if os.path.exists('flights_data.json'):
    with open('flights_data.json', 'r') as f:
        flights = json.load(f)

# Extract city name from airport field
def extract_city(field):
    parts = field.split(" - ")
    return parts[-1] if len(parts) > 1 else field

# Precompute cities for autocomplete
precomputed_cities = sorted({
    extract_city(f["departure"]) for f in flights.values()
} | {
    extract_city(f["arrival"]) for f in flights.values()
})

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# API for popular flights (to be displayed on the home page)
@app.route('/api/popular_flights')
def api_popular_flights():
    return jsonify(list(flights.values())[:3])  # Return top 3 flights as popular

# Autocomplete API for search
@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify(precomputed_cities)

    matching_cities = [city for city in precomputed_cities if query in city.lower()]
    return jsonify(matching_cities[:10])

# View flight details
@app.route('/view/<id>')
def view_flight(id):
    flight = flights.get(id)
    if not flight:
        return "Flight Not Found", 404
    return render_template('view.html', flight=flight)

# Search flights
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip().lower()
    if not query:
        return render_template('search_results.html', query=query, results=[])

    results = []
    for flight in flights.values():
        search_fields = [
            flight['title'].lower(),
            flight['airline'].lower(),
            extract_city(flight['arrival']).lower(),
            extract_city(flight['departure']).lower(),
            flight['summary'].lower()
        ]
        if any(query in field for field in search_fields):
            results.append(flight)

    return render_template('search_results.html', query=query, results=results, count=len(results))

# Add new flight form
@app.route('/add')
def add_form():
    return render_template('add_flight.html', flight=None)

# Process new flight submission (AJAX)
@app.route('/api/add', methods=['POST'])
def add_flight():
    data = request.get_json()
    
    # Validation
    errors = {}
    required_fields = ['title', 'airline', 'departure', 'arrival', 'price', 'flight_time', 'year', 'image']
    
    for field in required_fields:
        if not data.get(field, '').strip():
            errors[field] = f"{field.capitalize()} is required"
    
    # Check if price is a number
    if 'price' not in errors and not data.get('price', '').strip().isdigit():
        errors['price'] = "Price must be a number"
    
    # If there are validation errors, return them
    if errors:
        return jsonify({"success": False, "errors": errors}), 400
    
    # Create new flight with a new ID
    new_id = str(max(int(id) for id in flights.keys()) + 1)
    
    # Format the data
    new_flight = {
        "id": new_id,
        "title": data.get('title', '').strip(),
        "image": data.get('image', '').strip(),
        "year": data.get('year', '').strip(),
        "summary": data.get('summary', '').strip(),
        "airline": data.get('airline', '').strip(),
        "departure": data.get('departure', '').strip(),
        "arrival": data.get('arrival', '').strip(),
        "flight_time": data.get('flight_time', '').strip(),
        "price": data.get('price', '').strip(),
        "baggage_policy": data.get('baggage_policy', '').strip(),
        "schedule": [day.strip() for day in data.get('schedule', '').split(',') if day.strip()],
        "reviews": [review.strip() for review in data.get('reviews', '').split(',') if review.strip()]
    }
    
    # Add to flights dictionary
    flights[new_id] = new_flight
    
    # Save to JSON file
    save_flights_data()
    
    return jsonify({"success": True, "id": new_id})

# Edit flight form
@app.route('/edit/<id>')
def edit_form(id):
    flight = flights.get(id)
    if not flight:
        return "Flight Not Found", 404
    return render_template('edit_flight.html', flight=flight)

# Process flight edit (AJAX)
@app.route('/api/edit/<id>', methods=['POST'])
def edit_flight(id):
    if id not in flights:
        return jsonify({"success": False, "error": "Flight not found"}), 404
    
    data = request.get_json()
    
    # Validation
    errors = {}
    required_fields = ['title', 'airline', 'departure', 'arrival', 'price', 'flight_time']
    
    for field in required_fields:
        if not data.get(field, '').strip():
            errors[field] = f"{field.capitalize()} is required"
    
    # Check if price is a number
    if 'price' not in errors and not data.get('price', '').strip().isdigit():
        errors['price'] = "Price must be a number"
    
    # If there are validation errors, return them
    if errors:
        return jsonify({"success": False, "errors": errors}), 400
    
    # Update flight data
    flight = flights[id]
    flight['title'] = data.get('title', flight['title']).strip()
    flight['image'] = data.get('image', flight['image']).strip()
    flight['year'] = data.get('year', flight['year']).strip()
    flight['summary'] = data.get('summary', flight['summary']).strip()
    flight['airline'] = data.get('airline', flight['airline']).strip()
    flight['departure'] = data.get('departure', flight['departure']).strip()
    flight['arrival'] = data.get('arrival', flight['arrival']).strip()
    flight['flight_time'] = data.get('flight_time', flight['flight_time']).strip()
    flight['price'] = data.get('price', flight['price']).strip()
    flight['baggage_policy'] = data.get('baggage_policy', flight['baggage_policy']).strip()
    
    # Handle lists
    if 'schedule' in data:
        flight['schedule'] = [day.strip() for day in data['schedule'].split(',') if day.strip()]
    
    if 'reviews' in data:
        flight['reviews'] = [review.strip() for review in data['reviews'].split(',') if review.strip()]
    
    # Save to JSON file
    save_flights_data()
    
    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(debug=True, port=5001)