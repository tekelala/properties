import streamlit as st

# Define the path or URL to the image file
image_path = "livinghotels.png"

# Define the headline text
headline_text = "Welcome to Properties by Colombian Living Hotels"

# Define the flat types and their base prices
FLAT_TYPES = {
    'Type 1  42 m2 - 4 people': {'size': 42, 'base_price': 23750000},
    'Type 2  135 m2 - 8 people': {'size': 135, 'base_price': 76339286},
    'Type 3  67 m2 - 4 people': {'size': 67, 'base_price': 35625000},
    'Type 4  92 m2 - 6 people': {'size': 92, 'base_price': 52023810},
    'Type 5  110 m2 - 6 people': {'size': 110, 'base_price': 62202381},
}

# Define the pricing multipliers for different seasons
SEASONS = {
    'Mid Season': 1.0,  # Base price
    'High Season': 1.32,  # 32% premium on base price
    'Hyper Season': 1.64, # 64% premium on base price
    '2-51 Season': 1.7, # 70% premium on base price
    '1-52 Season': 2.21, # 121% premium on base price
}

# Define the floor premium multipliers
FLOOR_PREMIUMS = {
    6: 1.0,   # Base price
    7: 1.01,  # 1% premium
    8: 1.01,  # 2% premium  
    9: 1.01,
    10: 1.01,
    11: 1.01,
    12: 1.01,
    13: 1.02,
    14: 1.02,
    15: 1.02,
    16: 1.02,
    17: 1.02,
    18: 1.02,
    19: 1.02,
    20: 1.02,
    21: 1.02,
    22: 1.02,
    23: 1.02, # 17% premium
    # Review these premiums with Antonio
}

# Define the weeks for each season
MID_SEASON_WEEKS = list(range(3, 13)) + list(range(40, 51)) # Weeks 3-12 and 40-50
HIGH_SEASON_WEEKS = list(range(13, 21)) + list(range(34, 40)) # Weeks 13-20 and 34-39
HYPER_SEASON_WEEKS = list(range(21, 34)) # Weeks 21-33
TWO_FIFTYONE = [2, 51]  # Weeks 2 and 51
ONE_FIFTYTWO = [1, 52]  # Weeks 1 and 52

# Define the weeks of the year
WEEKS = list(range(1, 53))

# Define flat numbers for each type
FLAT_NUMBERS = {
    'Type 1  42 m2 - 4 people': ['02', '03', '04', '05', '06', '11', '12', '13', '14'],
    'Type 2  135 m2 - 8 people': ['07'],
    'Type 3  67 m2 - 4 people': ['08', '16'],
    'Type 4  92 m2 - 6 people': ['01', '09'],
    'Type 5  110 m2 - 6 people': ['15'],
}

# Initialize availability data structure (floor, flat type, flat number, week, status)
availability = {
    floor: {
        flat_type: {
            flat_number: {
                week: 'Free' for week in WEEKS
            } for flat_number in FLAT_NUMBERS[flat_type]
        } for flat_type in FLAT_TYPES
    } for floor in FLOOR_PREMIUMS
}

# Define Streamlit app
def app():
    # Display the image
    st.image(image_path, width=400)  # You can adjust the width as needed

    # Display the headline text
    st.header(headline_text)

    st.title("Let's find your dream property for vacations and investment")
    st.write("Welcome and let's find your property")

    # Let the user select a flat type
    flat_type = st.selectbox("Select a flat type:", list(FLAT_TYPES.keys()))

    # Let the user select a floor (convert floor numbers to strings)
    floor_number = st.selectbox("Select a floor number:", list(map(str, FLOOR_PREMIUMS.keys())))
    floor_number = int(floor_number)  # Convert back to integer for calculations

    # Filter flats with free weeks on the selected floor and flat type
    available_flats = [num for num, weeks in availability[floor_number][flat_type].items() if any(status == 'Free' for status in weeks.values())]

    # Let the user select a specific flat with free weeks
    flat_number = st.selectbox("Select a flat number:", available_flats, key='flat_number')

    # Filter free weeks for the selected flat
    free_weeks = [week for week, status in availability[floor_number][flat_type][flat_number].items() if status == 'Free']
    
    # Let the user select four weeks of the year
    selected_weeks = st.multiselect("Select 4 weeks of the year:", free_weeks, default=[], key='selected_weeks')

    # Initialize the variables before the if statement
    total_price = 0
    total_base_price = 0
    total_extras = 0

    # Check if exactly 4 weeks are selected
    if len(selected_weeks) != 4:
        st.warning("Please select exactly 4 weeks.")
    else:
        # Calculate the total price, base price, and extras
        base_price = FLAT_TYPES[flat_type]['base_price']
        floor_premium = FLOOR_PREMIUMS[floor_number]

        for week in selected_weeks:
            # Determine the season for the selected week
            if week in MID_SEASON_WEEKS:
                season = 'Mid Season'
            elif week in HIGH_SEASON_WEEKS:
                season = 'High Season'
            elif week in HYPER_SEASON_WEEKS:
                season = 'Hyper Season'
            elif week in TWO_FIFTYONE:
                season = '2-51 Season'
            else:
                season = '1-52 Season'

            # Calculate price for the selected week
            season_multiplier = SEASONS[season]
            week_price = base_price * season_multiplier * floor_premium
            total_price += week_price

            # Accumulate base price and extras
            total_base_price += base_price
            extras = week_price - base_price
            total_extras += extras

    # Display the base price, extras, and total price
    st.success(f"Base price for all selected weeks: ${total_base_price:,.2f}")
    st.success(f"Price of extras (weeks and floor): ${total_extras:,.2f}")
    st.success(f"Total price: ${total_price:,.2f}")

    # Let the user choose to Buy or Reserve using buttons
    buy_button = st.button("Buy")
    reserve_button = st.button("Reserve")

    if buy_button:
        new_status = 'Paid'
        # Update availability status for the selected weeks in the flat
        for week in selected_weeks:
            availability[floor_number][flat_type][flat_number][week] = new_status
        # Display success message
        st.success(f"You have successfully Bought the selected weeks in {flat_type} on floor {floor_number}, flat number {flat_number}.")
    elif reserve_button:
        new_status = 'Reserved'
        # Update availability status for the selected weeks in the flat
        for week in selected_weeks:
            availability[floor_number][flat_type][flat_number][week] = new_status
        # Display success message
        st.success(f"You have successfully Reserved the selected weeks in {flat_type} on floor {floor_number}, flat number {flat_number}.")



# Call the app function to run the Streamlit app
app()
