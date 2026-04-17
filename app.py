from flask import Flask, render_template, request, jsonify, session
import json
from datetime import datetime, timedelta
import random

app = Flask(__name__)
app.secret_key = 'travel_planner_secret_2024'

# Destination data
DESTINATIONS = {
    "paris": {
        "name": "Paris, France",
        "country": "France",
        "image": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=800&q=80",
        "hero": "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=1400&q=80",
        "description": "The City of Light awaits with iconic landmarks, world-class cuisine, and timeless romance.",
        "weather": "18°C / Partly Cloudy",
        "language": "French",
        "currency": "Euro (€)",
        "timezone": "CET (UTC+1)",
        "rating": 4.9,
        "reviews": 12847,
        "price_per_day": 180,
        "best_time": "April–June, Sep–Oct",
        "tags": ["Romance", "Culture", "Food", "Art"],
        "attractions": [
            {"name": "Eiffel Tower", "type": "Landmark", "duration": "2-3 hrs", "price": "€26", "img": "https://images.unsplash.com/photo-1543349689-9a4d426bee8e?w=400&q=80"},
            {"name": "Louvre Museum", "type": "Museum", "duration": "4-5 hrs", "price": "€17", "img": "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=400&q=80"},
            {"name": "Montmartre", "type": "Neighborhood", "duration": "3 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1550340499-a6c60fc8287c?w=400&q=80"},
            {"name": "Seine River Cruise", "type": "Activity", "duration": "1.5 hrs", "price": "€15", "img": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&q=80"},
        ],
        "hotels": [
            {"name": "Le Grand Hôtel", "stars": 5, "price": 380, "img": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80"},
            {"name": "Hôtel Riviera", "stars": 4, "price": 210, "img": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400&q=80"},
            {"name": "Maison Chic", "stars": 3, "price": 120, "img": "https://images.unsplash.com/photo-1445019980597-93fa8acb246c?w=400&q=80"},
        ]
    },
    "tokyo": {
        "name": "Tokyo, Japan",
        "country": "Japan",
        "image": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=800&q=80",
        "hero": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=1400&q=80",
        "description": "Where ancient tradition meets electric modernity — Tokyo is unlike anywhere else on Earth.",
        "weather": "22°C / Sunny",
        "language": "Japanese",
        "currency": "Yen (¥)",
        "timezone": "JST (UTC+9)",
        "rating": 4.8,
        "reviews": 9341,
        "price_per_day": 150,
        "best_time": "March–May, Oct–Nov",
        "tags": ["Culture", "Food", "Technology", "Shopping"],
        "attractions": [
            {"name": "Shibuya Crossing", "type": "Landmark", "duration": "1 hr", "price": "Free", "img": "https://images.unsplash.com/photo-1542051841857-5f90071e7989?w=400&q=80"},
            {"name": "Senso-ji Temple", "type": "Temple", "duration": "2 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&q=80"},
            {"name": "Tsukiji Market", "type": "Market", "duration": "3 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=400&q=80"},
            {"name": "teamLab Planets", "type": "Art", "duration": "2 hrs", "price": "¥3200", "img": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=400&q=80"},
        ],
        "hotels": [
            {"name": "Park Hyatt Tokyo", "stars": 5, "price": 450, "img": "https://images.unsplash.com/photo-1568084680786-a84f91d1153c?w=400&q=80"},
            {"name": "Shinjuku Grand", "stars": 4, "price": 190, "img": "https://images.unsplash.com/photo-1560347876-aeef00ee58a1?w=400&q=80"},
            {"name": "Tokyo Capsule Inn", "stars": 3, "price": 70, "img": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=400&q=80"},
        ]
    },
    "bali": {
        "name": "Bali, Indonesia",
        "country": "Indonesia",
        "image": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=800&q=80",
        "hero": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=1400&q=80",
        "description": "Lush rice terraces, sacred temples, and sun-soaked beaches make Bali pure paradise.",
        "weather": "30°C / Tropical",
        "language": "Balinese / Indonesian",
        "currency": "Rupiah (Rp)",
        "timezone": "WITA (UTC+8)",
        "rating": 4.7,
        "reviews": 15230,
        "price_per_day": 80,
        "best_time": "April–Oct (Dry Season)",
        "tags": ["Beach", "Spiritual", "Nature", "Wellness"],
        "attractions": [
            {"name": "Tanah Lot Temple", "type": "Temple", "duration": "2 hrs", "price": "Rp60k", "img": "https://images.unsplash.com/photo-1555400038-63f5ba517a47?w=400&q=80"},
            {"name": "Tegallalang Rice Terraces", "type": "Nature", "duration": "2 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400&q=80"},
            {"name": "Ubud Monkey Forest", "type": "Wildlife", "duration": "2 hrs", "price": "Rp80k", "img": "https://images.unsplash.com/photo-1518548419970-58e3b4079ab2?w=400&q=80"},
            {"name": "Seminyak Beach", "type": "Beach", "duration": "Half Day", "price": "Free", "img": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=400&q=80"},
        ],
        "hotels": [
            {"name": "Four Seasons Jimbaran", "stars": 5, "price": 520, "img": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400&q=80"},
            {"name": "Ubud Jungle Resort", "stars": 4, "price": 160, "img": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80"},
            {"name": "Kuta Beach Hostel", "stars": 3, "price": 45, "img": "https://images.unsplash.com/photo-1490122417551-6ee9691429d0?w=400&q=80"},
        ]
    },
    "newyork": {
        "name": "New York, USA",
        "country": "United States",
        "image": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=800&q=80",
        "hero": "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=1400&q=80",
        "description": "The city that never sleeps — skyscrapers, culture, food and energy like nowhere else.",
        "weather": "15°C / Clear",
        "language": "English",
        "currency": "US Dollar ($)",
        "timezone": "EST (UTC-5)",
        "rating": 4.8,
        "reviews": 21500,
        "price_per_day": 220,
        "best_time": "April–June, Sep–Nov",
        "tags": ["Urban", "Culture", "Food", "Shopping"],
        "attractions": [
            {"name": "Central Park", "type": "Park", "duration": "3 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=400&q=80"},
            {"name": "Metropolitan Museum", "type": "Museum", "duration": "4 hrs", "price": "$25", "img": "https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=400&q=80"},
            {"name": "Times Square", "type": "Landmark", "duration": "1 hr", "price": "Free", "img": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400&q=80"},
            {"name": "Statue of Liberty", "type": "Landmark", "duration": "3 hrs", "price": "$24", "img": "https://images.unsplash.com/photo-1503095396549-807759245b35?w=400&q=80"},
        ],
        "hotels": [
            {"name": "The Plaza Hotel", "stars": 5, "price": 650, "img": "https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400&q=80"},
            {"name": "Midtown Marriott", "stars": 4, "price": 280, "img": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=400&q=80"},
            {"name": "Brooklyn Budget Inn", "stars": 3, "price": 130, "img": "https://images.unsplash.com/photo-1462826303086-329426d1aef5?w=400&q=80"},
        ]
    },
    "santorini": {
        "name": "Santorini, Greece",
        "country": "Greece",
        "image": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=800&q=80",
        "hero": "https://images.unsplash.com/photo-1469796466635-455ede028aca?w=1400&q=80",
        "description": "Whitewashed villas, blue-domed churches and breathtaking caldera views define this Aegean gem.",
        "weather": "25°C / Sunny",
        "language": "Greek",
        "currency": "Euro (€)",
        "timezone": "EET (UTC+2)",
        "rating": 4.9,
        "reviews": 8760,
        "price_per_day": 200,
        "best_time": "May–Sep",
        "tags": ["Romance", "Beach", "Views", "Luxury"],
        "attractions": [
            {"name": "Oia Sunset", "type": "Experience", "duration": "2 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=400&q=80"},
            {"name": "Red Beach", "type": "Beach", "duration": "3 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1601581875039-e899893d520c?w=400&q=80"},
            {"name": "Akrotiri Ruins", "type": "History", "duration": "2 hrs", "price": "€12", "img": "https://images.unsplash.com/photo-1533105079780-92b9be482077?w=400&q=80"},
            {"name": "Caldera Boat Tour", "type": "Activity", "duration": "4 hrs", "price": "€35", "img": "https://images.unsplash.com/photo-1469796466635-455ede028aca?w=400&q=80"},
        ],
        "hotels": [
            {"name": "Katikies Santorini", "stars": 5, "price": 700, "img": "https://images.unsplash.com/photo-1602343168117-bb8ffe3e2e9f?w=400&q=80"},
            {"name": "Oia Cliffside Villa", "stars": 4, "price": 320, "img": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=400&q=80"},
            {"name": "Fira Guesthouse", "stars": 3, "price": 150, "img": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&q=80"},
        ]
    },
    "dubai": {
        "name": "Dubai, UAE",
        "country": "United Arab Emirates",
        "image": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800&q=80",
        "hero": "https://images.unsplash.com/photo-1518684079-3c830dcef090?w=1400&q=80",
        "description": "Futuristic skyline, desert adventures and luxury shopping — Dubai does everything in excess.",
        "weather": "35°C / Sunny",
        "language": "Arabic / English",
        "currency": "Dirham (AED)",
        "timezone": "GST (UTC+4)",
        "rating": 4.7,
        "reviews": 11200,
        "price_per_day": 250,
        "best_time": "Nov–March",
        "tags": ["Luxury", "Shopping", "Adventure", "Modern"],
        "attractions": [
            {"name": "Burj Khalifa", "type": "Landmark", "duration": "2 hrs", "price": "AED149", "img": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&q=80"},
            {"name": "Dubai Desert Safari", "type": "Adventure", "duration": "6 hrs", "price": "AED200", "img": "https://images.unsplash.com/photo-1509023464722-18d996393ca8?w=400&q=80"},
            {"name": "Dubai Mall", "type": "Shopping", "duration": "4 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1518684079-3c830dcef090?w=400&q=80"},
            {"name": "Palm Jumeirah", "type": "Landmark", "duration": "3 hrs", "price": "Free", "img": "https://images.unsplash.com/photo-1548438294-1ad5d5f4f063?w=400&q=80"},
        ],
        "hotels": [
            {"name": "Burj Al Arab", "stars": 5, "price": 1200, "img": "https://images.unsplash.com/photo-1526495124232-a04e1849168c?w=400&q=80"},
            {"name": "Atlantis The Palm", "stars": 5, "price": 480, "img": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=400&q=80"},
            {"name": "TRYP Dubai", "stars": 4, "price": 180, "img": "https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=400&q=80"},
        ]
    }
}

@app.route('/')
def index():
    featured = list(DESTINATIONS.values())[:6]
    return render_template('index.html', destinations=featured)

@app.route('/explore')
def explore():
    tag_filter = request.args.get('tag', '')
    search_q = request.args.get('q', '')
    dests = list(DESTINATIONS.values())
    if tag_filter:
        dests = [d for d in dests if tag_filter in d['tags']]
    if search_q:
        sq = search_q.lower()
        dests = [d for d in dests if sq in d['name'].lower() or sq in d['country'].lower()]
    all_tags = sorted(set(tag for d in DESTINATIONS.values() for tag in d['tags']))
    return render_template('explore.html', destinations=dests, tags=all_tags, active_tag=tag_filter, search=search_q)

@app.route('/destination/<dest_id>')
def destination(dest_id):
    dest = DESTINATIONS.get(dest_id)
    if not dest:
        return "Destination not found", 404
    return render_template('destination.html', dest=dest, dest_id=dest_id)

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    dest_id = request.args.get('dest', 'paris')
    dest = DESTINATIONS.get(dest_id, DESTINATIONS['paris'])
    if request.method == 'POST':
        data = request.form
        days = int(data.get('days', 5))
        budget = data.get('budget', 'mid')
        
        # Build itinerary
        hotel_idx = {'budget': 2, 'mid': 1, 'luxury': 0}.get(budget, 1)
        hotel = dest['hotels'][min(hotel_idx, len(dest['hotels'])-1)]
        
        # Generate day-by-day plan
        itinerary = []
        attractions = dest['attractions']
        for i in range(days):
            day_attractions = []
            for j in range(2):
                idx = (i * 2 + j) % len(attractions)
                day_attractions.append(attractions[idx])
            itinerary.append({
                'day': i + 1,
                'activities': day_attractions
            })
        
        hotel_cost = hotel['price'] * days
        flight_cost = random.randint(400, 1200)
        misc_cost = dest['price_per_day'] * days * 0.3
        total = hotel_cost + flight_cost + misc_cost
        
        result = {
            'destination': dest,
            'dest_id': dest_id,
            'days': days,
            'budget': budget,
            'hotel': hotel,
            'itinerary': itinerary,
            'costs': {
                'hotel': round(hotel_cost),
                'flight': flight_cost,
                'misc': round(misc_cost),
                'total': round(total)
            },
            'travelers': int(data.get('travelers', 2)),
        }
        return render_template('plan.html', result=result, destinations=DESTINATIONS, dest=dest, dest_id=dest_id)
    
    return render_template('plan.html', result=None, destinations=DESTINATIONS, dest=dest, dest_id=dest_id)

@app.route('/api/destinations')
def api_destinations():
    return jsonify(list(DESTINATIONS.keys()))

@app.route('/api/destination/<dest_id>')
def api_destination(dest_id):
    dest = DESTINATIONS.get(dest_id)
    if dest:
        return jsonify(dest)
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
