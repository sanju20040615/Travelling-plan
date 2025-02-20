from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/estimate', methods=['POST'])
def estimate():
    try:
        # Retrieve form data
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        duration = int(request.form.get('duration'))
        people = int(request.form.get('people'))
        travel_mode = request.form.get('travel_mode')  # e.g., bus, train, car, flight
        budget_type = request.form.get('budget_type')  # luxury or budget
        ac_preference = request.form.get('ac_preference')  # AC or Non-AC

        # Distance in kilometers between common destinations (as an example)
        distances = {
            ("CityA", "CityB"): 300,
            ("CityA", "CityC"): 500,
            ("CityB", "CityC"): 200,
        }
        distance = distances.get((origin, destination), 100)  # Default 100 km if not found

        # Transport rates for different modes and preferences
        transport_rates = {
            "luxury": {
                "bus": {"AC": 25, "Non-AC": 20},
                "car": {"AC": 20, "Non-AC": 15},
                "train": {"AC": 15, "Non-AC": 10},
                "flight": {"AC": 6000, "Non-AC": 5000},
            },
            "budget": {
                "bus": {"AC": 8, "Non-AC": 5},
                "car": {"AC": 5, "Non-AC": 3},
                "train": {"AC": 2, "Non-AC": 1.5},
                "flight": {"AC": 2500, "Non-AC": 2000},
            },
        }

        # Destination-specific hotel and meal rates
        hotel_meal_rates = {
            "CityA": {
                "luxury": {"hotel_per_day": 3000, "meal": 2000},
                "budget": {"hotel_per_day": 1000, "meal": 250},
            },
            "CityB": {
                "luxury": {"hotel_per_day": 2500, "meal": 3000},
                "budget": {"hotel_per_day": 1500, "meal": 200},
            },
            "CityC": {
                "luxury": {"hotel_per_day": 5000, "meal": 4000},
                "budget": {"hotel_per_day": 800, "meal": 300},
            },
        }

        # Fetch rates for the selected destination
        rates = hotel_meal_rates.get(destination, hotel_meal_rates["CityA"])  # Default to CityA rates
        selected_rates = rates[budget_type]

        # Fetch transport rate for the selected mode and preference
        selected_transport_rate = (
            transport_rates
            .get(budget_type, {})
            .get(travel_mode, {})
            .get(ac_preference, 10)  # Default rate
        )

        # Transport cost calculation
        transport_cost = distance * people * selected_transport_rate

        # Accommodation cost calculation
        accommodation_cost = duration * selected_rates["hotel_per_day"]

        # Meal cost calculation (3 meals per day: breakfast, lunch, dinner)
        meal_cost = duration * 3 * selected_rates["meal"]

        # Total cost
        total_cost = transport_cost + accommodation_cost + meal_cost

        # Debugging output to verify calculations
        print(f"Origin: {origin}")
        print(f"Destination: {destination}")
        print(f"Distance: {distance} km")
        print(f"Travel Mode: {travel_mode}")
        print(f"AC Preference: {ac_preference}")
        print(f"Duration: {duration} days")
        print(f"People: {people}")
        print(f"Transport Cost: {transport_cost}")
        print(f"Accommodation Cost: {accommodation_cost}")
        print(f"Meal Cost: {meal_cost}")
        print(f"Total Cost: {total_cost}")

        # Render result template with the calculated values
        return render_template(
            'result.html',
            origin=origin,
            destination=destination,
            kilometers=distance,
            transport_cost=round(transport_cost, 2),
            accommodation_cost=round(accommodation_cost, 2),
            meal_cost=round(meal_cost, 2),
            total_cost=round(total_cost, 2)
        )

    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template(
            'result.html',
            origin="Unknown",
            destination="Unknown",
            kilometers="N/A",
            transport_cost=0,
            accommodation_cost=0,
            meal_cost=0,
            total_cost=0,
            error="An error occurred while processing your request. Please try again."
        )

if __name__ == '__main__':
    # Ensure templates folder exists
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Ensure static folder exists
    if not os.path.exists('static'):
        os.makedirs('static')

    app.run(debug=True)
