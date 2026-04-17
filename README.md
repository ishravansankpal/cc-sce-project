# 🌍 Wanderlust — Travel Planner

A beautiful, professional Flask travel planner web application with 3 dynamic pages.

## Pages
1. **Home** (`/`) — Hero landing, search bar, featured destinations, features
2. **Explore** (`/explore`) — Browse & filter all destinations with search
3. **Destination Detail** (`/destination/<id>`) — Full page with attractions, hotels, info
4. **Plan Trip** (`/plan`) — Interactive trip planner with itinerary + cost breakdown

## Destinations
Paris, Tokyo, Bali, New York, Santorini, Dubai

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python app.py

# 3. Open browser
http://localhost:5000
```

## Project Structure
```
travel_planner/
├── app.py               # Flask app + all route logic + destination data
├── requirements.txt
├── templates/
│   ├── base.html        # Navigation + footer + shared styles
│   ├── index.html       # Homepage
│   ├── explore.html     # Explore/filter destinations
│   ├── destination.html # Destination detail
│   └── plan.html        # Trip planner + itinerary generator
└── static/              # (static assets folder, CSS/JS in templates)
```

## Features
- Responsive design with professional typography (Playfair Display + DM Sans)
- Dynamic destination filtering by tag/search
- Animated hero sections with high-quality Unsplash images
- Interactive trip planner: choose destination, days, budget, travelers
- Auto-generated day-by-day itinerary
- Cost breakdown (hotel + flight + misc)
- Hotel recommendations by budget level
- Sticky booking card on destination pages
- FontAwesome icons throughout
