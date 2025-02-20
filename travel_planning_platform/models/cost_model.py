import geocoder
from math import radians, sin, cos, sqrt, atan2

# Hardcoded locations dictionary
locations = {
    "ooty": (11.4064, 76.6962),
    "goa": (15.2993, 74.1240),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "hyderabad": (17.3850, 78.4867),
    "kolkata": (22.5726, 88.3639),
    "jaipur": (26.9124, 75.7873),
    "agra": (27.1767, 78.0081),
    "vishakhapatnam": (17.6868, 83.2185),
    "pune": (18.5204, 73.8567),
    "kochi": (9.9312, 76.2673),
    # Add more cities and their coordinates as needed
}

# Function to get the latitude and longitude of a location using OpenCage Geocoder
def get_coordinates(location):
    # Check if location is in the hardcoded list
    location = location.lower()
    if location in locations:
        return locations[location]
    
    # If not found in hardcoded list, use the geocoding API
    g = geocoder.opencage(location, key='YOUR_API_KEY')  # Replace with your API key
    if g.ok:
        return g.latlng
    else:
        return None

# Function to calculate the distance in kilometers between two locations
def calculate_kilometers(origin, destination):
    origin_coords = get_coordinates(origin)
    destination_coords = get_coordinates(destination)

    if origin_coords is None or destination_coords is None:
        return "Unknown location"
    
    lat1, lon1 = origin_coords
    lat2, lon2 = destination_coords

    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)

    # Haversine formula to calculate the distance
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in kilometers
    radius = 6371.0

    # Calculate the distance in kilometers
    distance = radius * c
    return round(distance, 2)

# Function to estimate the travel cost
def estimate_travel_cost(destination, origin, date, duration, people, budget_type, travel_mode):
    # Get coordinates and calculate the kilometers
    kilometers = calculate_kilometers(origin, destination)

    if kilometers == "Unknown location":
        return "Unknown location"

    # Logic to calculate travel cost based on budget type, travel mode, etc.
    # Example:
    if budget_type == "luxury":
        cost_per_km = 10  # Luxury cost per km
    else:
        cost_per_km = 5  # Budget cost per km

    # Travel mode logic (can be expanded with specific multipliers for each mode)
    if travel_mode == "flight":
        cost_multiplier = 2  # Flight multiplier
    elif travel_mode == "train":
        cost_multiplier = 1.5  # Train multiplier
    else:
        cost_multiplier = 1  # Default multiplier for other modes

    estimated_cost = kilometers * cost_per_km * cost_multiplier
    return round(estimated_cost, 2)
