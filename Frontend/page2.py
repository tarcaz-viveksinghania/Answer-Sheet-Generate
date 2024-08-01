import streamlit as st
import pandas as pd
import json

def display_next_page():
    st.title("Next Page")
    st.write("This is the next page of the Streamlit app.")

    # Dropdown menu
    options = ["Option 1", "Option 2", "Option 3"]
    selected_option = st.selectbox("Choose an option", options)

    st.write(f"You selected: {selected_option}")

    # Check if Option 2 is selected
    if selected_option == "Option 2":
        # Load and display JSON data
        try:
            with open("MOCK_DATA.json", "r") as json_file:
                json_data = json.load(json_file)
                
                # Convert JSON data to DataFrame
                df = pd.DataFrame(json_data)
                
                # Display the DataFrame as a grid
                # print(df)
                st.dataframe(df)  # Use st.dataframe for interactive grid
        except FileNotFoundError:
            st.error("MOCK_DATA.json file not found.")
        except ValueError as e:
            st.error(f"Error reading JSON: {e}")

    st.divider()

    # File uploader for CSV files
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)

    # Create a three-column layout
    col1, col2, col3 = st.columns(3)

    # Place the "Go to Page 3" button in the rightmost column
    with col3:
        if st.button("Go to Page 3"):
            st.session_state.current_page = "page3"
            st.rerun()

    # Place the "Go Back" button in the leftmost column
    with col1:
        if st.button("Go Back"):
            st.session_state.current_page = "pdf_viewer"
            st.rerun()
