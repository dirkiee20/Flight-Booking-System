import streamlit as st
import pandas as pd
import json
import os

# File to store flight data
DATA_FILE = "flights.json"
BOOKINGS_FILE = "bookings.json"

# Initialize JSON data files if they don't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as file:
        initial_data = [
            {"Flight Number": "AI101", "From": "New York", "To": "London", "Price": 450, "Duration": 7},
            {"Flight Number": "BA202", "From": "London", "To": "Dubai", "Price": 350, "Duration": 6},
            {"Flight Number": "EK303", "From": "Dubai", "To": "Sydney", "Price": 950, "Duration": 14},
            {"Flight Number": "QA404", "From": "Sydney", "To": "Tokyo", "Price": 700, "Duration": 10},
            {"Flight Number": "DL505", "From": "Tokyo", "To": "New York", "Price": 1200, "Duration": 12},
        ]
        json.dump(initial_data, file, indent=4)

if not os.path.exists(BOOKINGS_FILE):
    with open(BOOKINGS_FILE, "w") as file:
        json.dump([], file, indent=4)

# Functions to load and save data
def load_data(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_data(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Load initial data
flights_data = load_data(DATA_FILE)
bookings_data = load_data(BOOKINGS_FILE)

# Function for quicksort
def quicksort(arr, key):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x[key] < pivot[key]]
    middle = [x for x in arr if x[key] == pivot[key]]
    right = [x for x in arr if x[key] > pivot[key]]
    return quicksort(left, key) + middle + quicksort(right, key)

# Streamlit UI
st.title("Flight Booking System")

# Sidebar for sorting flights
st.sidebar.header("Sort Available Flights")
sort_key = st.sidebar.selectbox("Sort By", ["Price", "Duration"])

# Map sort key to JSON keys
key_mapping = {"Price": "Price", "Duration": "Duration"}
selected_key = key_mapping[sort_key]

# Apply quicksort
sorted_flights = quicksort(flights_data, selected_key)
sorted_df = pd.DataFrame(sorted_flights)

# Display sorted available flights
st.subheader("Available Flights (Sorted)")
st.dataframe(sorted_df)

# Sidebar for search
st.sidebar.header("Search Available Flights")
search_key = st.sidebar.selectbox("Search By", ["Flight Number", "From", "To"])
search_value = st.sidebar.text_input("Enter Search Value", key="search_value")  # Added key

if st.sidebar.button("Search"):
    results = [flight for flight in flights_data if flight[search_key] == search_value]
    if results:
        st.subheader("Search Results")
        st.dataframe(pd.DataFrame(results))
    else:
        st.error("No matching flights found.")

# Booking feature
st.subheader("Book a Flight")
book_flight_number = st.selectbox("Select Flight to Book", [flight["Flight Number"] for flight in flights_data], key="book_flight_number")  # Added key
passenger_name = st.text_input("Passenger Name", key="passenger_name")  # Added key

if st.button("Book Flight"):
    booking = next((flight for flight in flights_data if flight["Flight Number"] == book_flight_number), None)
    if booking:
        booking_details = {**booking, "Passenger Name": passenger_name}
        bookings_data.append(booking_details)
        save_data(BOOKINGS_FILE, bookings_data)
        st.success(f"Flight {book_flight_number} successfully booked for {passenger_name}!")

        # Display the booking details with enhanced design
        st.subheader("Your Booking Details")

        # Enhanced design using HTML and CSS
        st.markdown(
            f"""
            <div style="border: 2px solid #4CAF50; border-radius: 8px; padding: 20px; background-color: #f0f8ff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);">
                <h3 style="text-align: center; color: #4CAF50;">Booking Confirmation</h3>
                <hr style="border: 1px solid #4CAF50;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #333;">Flight Number:</span>
                    <span style="color: #555;">{booking_details['Flight Number']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #333;">From:</span>
                    <span style="color: #555;">{booking_details['From']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #333;">To:</span>
                    <span style="color: #555;">{booking_details['To']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #333;">Price:</span>
                    <span style="color: #555;">${booking_details['Price']}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #333;">Duration:</span>
                    <span style="color: #555;">{booking_details['Duration']} hours</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold; color: #333;">Passenger Name:</span>
                    <span style="color: #555;">{booking_details['Passenger Name']}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("Flight not found.")

# **Update Available Flight**
st.sidebar.header("Update Available Flight")

# Allow the user to select a flight to update
flight_to_update = st.sidebar.selectbox("Select Flight to Update", [flight["Flight Number"] for flight in flights_data], key="flight_to_update")  # Added key

# Get selected flight details
selected_flight = next((flight for flight in flights_data if flight["Flight Number"] == flight_to_update), None)

if selected_flight:
    st.sidebar.write(f"Updating flight: {selected_flight['Flight Number']}")

    # Input fields for updating the flight details
    new_price = st.sidebar.number_input("New Price", min_value=1, value=selected_flight["Price"], step=50, key="new_price")
    new_duration = st.sidebar.number_input("New Duration (hours)", min_value=1, value=selected_flight["Duration"], step=1, key="new_duration")
    new_from = st.sidebar.text_input("New From", value=selected_flight["From"], key="new_from")
    new_to = st.sidebar.text_input("New To", value=selected_flight["To"], key="new_to")

    # Update flight data when the user clicks the 'Update Flight' button
    if st.sidebar.button("Update Flight"):
        # Update the selected flight
        selected_flight["Price"] = new_price
        selected_flight["Duration"] = new_duration
        selected_flight["From"] = new_from
        selected_flight["To"] = new_to

        # Save updated flight data
        save_data(DATA_FILE, flights_data)
        st.sidebar.success(f"Flight {flight_to_update} updated successfully!")

        # Refresh the displayed data
        st.experimental_rerun()

# **Display All Booked Flights**
st.subheader("All Booked Flights")

# Sorting booked flights
if bookings_data:
    sort_booked_key = st.selectbox("Sort Booked Flights By", ["Flight Number", "From", "To", "Passenger Name", "Price", "Duration"], key="sort_booked_key")  # Added key
    sorted_booked_flights = quicksort(bookings_data, sort_booked_key)
    booked_flights_df = pd.DataFrame(sorted_booked_flights)
    st.dataframe(booked_flights_df)
else:
    st.write("No bookings yet.")

# **Search Booked Flights**
st.sidebar.header("Search Booked Flights")

search_booked_key = st.sidebar.selectbox("Search Booked Flights By", ["Flight Number", "Passenger Name", "From"], key="search_booked_key")  # Added key
search_booked_value = st.sidebar.text_input("Enter Search Value", key="search_booked_value")  # Added key

if st.sidebar.button("Search Booked Flights"):
    search_results = [booking for booking in bookings_data if booking[search_booked_key] == search_booked_value]
    if search_results:
        st.subheader("Search Results for Booked Flights")
        st.dataframe(pd.DataFrame(search_results))
    else:
        st.sidebar.error("No matching booked flights found.")

# **Delete Booked Flight Feature**
st.sidebar.header("Delete Booked Flight")
# Display list of booked flights for deletion
if bookings_data:
    booked_flights = [f"{booking['Flight Number']} - {booking['Passenger Name']}" for booking in bookings_data]
    flight_to_delete = st.sidebar.selectbox("Select Flight to Delete", booked_flights, key="flight_to_delete")  # Added key

    if st.sidebar.button("Delete Flight"):
        # Find the selected flight in the bookings data
        flight_info = flight_to_delete.split(" - ")
        flight_number = flight_info[0]
        passenger_name = flight_info[1]

        # Find and delete the selected booking
        booking_to_delete = next((booking for booking in bookings_data if booking['Flight Number'] == flight_number and booking['Passenger Name'] == passenger_name), None)

        if booking_to_delete:
            bookings_data.remove(booking_to_delete)
            save_data(BOOKINGS_FILE, bookings_data)
            st.sidebar.success(f"Booking for flight {flight_number} by {passenger_name} has been deleted.")
            st.experimental_rerun()
        else:
            st.sidebar.error("Booking not found.")
else:
    st.sidebar.write("No bookings available to delete.")
