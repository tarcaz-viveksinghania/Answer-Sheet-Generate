import streamlit as st
import pandas as pd
import os
from st_aggrid import AgGrid, GridOptionsBuilder

def display_next_page():
    st.title("Next Page")
    st.write("This is the next page of the Streamlit app.")

    # Dropdown menu
    options = ["Option 1", "Option 2", "Option 3"]
    selected_option = st.selectbox("Choose an option", options)

    st.write(f"You selected: {selected_option}")

    # Show content from the specified CSV if "Option 2" is selected
    if selected_option == "Option 2":
        try:
            # Load CSV file
            df_question_paper = pd.read_csv("Database/Exam Evaluation_ CSVs.csv")

            # Configure the grid options to enable text wrapping
            gb = GridOptionsBuilder.from_dataframe(df_question_paper)
            gb.configure_default_column(
                wrapText=True,  # Enables text wrapping
                autoHeight=True,  # Adjusts row height based on content
            )
            grid_options = gb.build()

            # Display the dataframe with AgGrid
            AgGrid(df_question_paper, gridOptions=grid_options, fit_columns_on_grid_load=True)

        except FileNotFoundError:
            st.error("The file 'Database/Exam Evaluation_ CSVs.csv' was not found.")
        except pd.errors.EmptyDataError:
            st.error("The file is empty.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

    st.divider()

    # File uploader for CSV files
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        # Display the uploaded CSV data in grid format
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_default_column(
            wrapText=True,  # Enables text wrapping
            autoHeight=True,  # Adjusts row height based on content
        )
        grid_options = gb.build()

        AgGrid(df, gridOptions=grid_options, fit_columns_on_grid_load=True)

        # Save the uploaded file to the 'Database' folder
        try:
            os.makedirs("Database", exist_ok=True)  # Create the folder if it doesn't exist
            file_path = os.path.join("Database", uploaded_file.name)
            df.to_csv(file_path, index=False)
            st.success(f"File saved to {file_path}")
        except Exception as e:
            st.error(f"Failed to save file: {e}")


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
