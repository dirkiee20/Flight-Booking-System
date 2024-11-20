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

# Sidebar (only for adding new flights and search)
st.sidebar.header("Flight Management")
# Allow adding new available flights
with st.sidebar.form(key='add_flight_form'):
    st.subheader("Add New Flight")
    flight_number = st.text_input("Flight Number", key="add_flight_number")
    from_location = st.text_input("From", key="add_from_location")
    to_location = st.text_input("To", key="add_to_location")
    price = st.number_input("Price", min_value=0, step=10, key="add_price")
    duration = st.number_input("Duration (hours)", min_value=1, step=1, key="add_duration")
    add_flight_button = st.form_submit_button("Add Flight")

    if add_flight_button:
        new_flight = {
            "Flight Number": flight_number,
            "From": from_location,
            "To": to_location,
            "Price": price,
            "Duration": duration
        }
        flights_data.append(new_flight)
        save_data(DATA_FILE, flights_data)
        st.sidebar.success(f"Flight {flight_number} added successfully!")
        st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

# Sidebar Search Function
st.sidebar.header("Search Flights")
search_key = st.sidebar.selectbox("Search By", ["Flight Number", "From", "To"])
search_value = st.sidebar.text_input("Enter Search Value", key="search_value")

if st.sidebar.button("Search"):
    search_results = [flight for flight in flights_data if flight[search_key] == search_value]
    if search_results:
        st.subheader("Search Results")
        st.dataframe(pd.DataFrame(search_results))
    else:
        st.error("No matching flights found.")

# **Main Page: Display and Manage Flights**

# Columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    # Sorting flights by price or duration
    st.header("Available Flights")
    sort_key = st.selectbox("Sort By", ["Price", "Duration"], key="sort_key")
    key_mapping = {"Price": "Price", "Duration": "Duration"}
    selected_key = key_mapping[sort_key]

    # Apply quicksort
    sorted_flights = quicksort(flights_data, selected_key)
    sorted_flights_df = pd.DataFrame(sorted_flights)

    st.dataframe(sorted_flights_df)

    # **Book Flight Feature**
    st.subheader("Book a Flight")
    book_flight_number = st.selectbox("Select Flight to Book", [flight["Flight Number"] for flight in flights_data], key="book_flight_number")
    passenger_name = st.text_input("Passenger Name", key="passenger_name")

    if st.button("Book Flight"):
        booking = next((flight for flight in flights_data if flight["Flight Number"] == book_flight_number), None)
        if booking:
            booking_details = {**booking, "Passenger Name": passenger_name}
            bookings_data.append(booking_details)
            save_data(BOOKINGS_FILE, bookings_data)
            st.success(f"Flight {book_flight_number} successfully booked for {passenger_name}!")

            # Display booking details with design
            st.subheader("Your Booking Details")
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

# **Update and Delete Available Flight**
with col2:
    st.header("Update or Delete Available Flight")

    # Select a flight to update or delete
    flight_to_update = st.selectbox("Select Flight to Update or Delete", [flight["Flight Number"] for flight in flights_data], key="flight_to_update")
    selected_flight = next((flight for flight in flights_data if flight["Flight Number"] == flight_to_update), None)

    if selected_flight:
        st.write(f"Updating or Deleting flight: {selected_flight['Flight Number']}")

        # Inputs for updating the flight
        new_price = st.number_input("New Price", min_value=0, value=selected_flight["Price"], step=50, key="new_price")
        new_duration = st.number_input("New Duration (hours)", min_value=1, value=selected_flight["Duration"], step=1, key="new_duration")
        new_from = st.text_input("New From", value=selected_flight["From"], key="new_from")
        new_to = st.text_input("New To", value=selected_flight["To"], key="new_to")

        # Create columns for side-by-side buttons
        update_col, delete_col = st.columns(2)

        # Update button
        with update_col:
            if st.button("Update Flight"):
                selected_flight["Price"] = new_price
                selected_flight["Duration"] = new_duration
                selected_flight["From"] = new_from
                selected_flight["To"] = new_to
                save_data(DATA_FILE, flights_data)
                st.success(f"Flight {flight_to_update} updated successfully!")
                st.rerun()  # Reload to reflect changes

        # Delete button
        with delete_col:
            if st.button("Delete Flight"):
                flights_data = [flight for flight in flights_data if flight["Flight Number"] != flight_to_update]
                save_data(DATA_FILE, flights_data)
                st.success(f"Flight {flight_to_update} deleted successfully!")
                st.rerun()  # Reload to reflect changes
    else:
        st.error("Please select a flight to update or delete.")

# **Display and Delete Booked Flights**
st.header("Booked Flights")
if bookings_data:
    booked_flights_df = pd.DataFrame(bookings_data)
    st.dataframe(booked_flights_df)

    # Delete booked flight functionality
    flight_to_delete = st.selectbox("Select a Booking to Delete", [booking["Flight Number"] for booking in bookings_data], key="flight_to_delete")
    if flight_to_delete:
        if st.button(f"Delete Booking for {flight_to_delete}"):
            bookings_data = [booking for booking in bookings_data if booking["Flight Number"] != flight_to_delete]
            save_data(BOOKINGS_FILE, bookings_data)
            st.success(f"Booking for flight {flight_to_delete} deleted successfully!")
            st.rerun()  # Reload to reflect changes
else:
    st.write("No bookings yet.")

