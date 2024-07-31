import streamlit as st
import fitz  # PyMuPDF

def display_page3():
    st.title("Page 3")
    st.write("This is the third page of the Streamlit app.")

    # Check if there are uploaded files in session state
    if "uploaded_files" in st.session_state and st.session_state.uploaded_files:
        # Create a selectbox to choose one PDF from the uploaded files
        pdf_files = st.session_state.uploaded_files
        selected_pdf_name = st.selectbox("Select a PDF to view", [file["name"] for file in pdf_files])

        # Find the selected PDF file
        selected_file = next(file for file in pdf_files if file["name"] == selected_pdf_name)
        pdf_document = fitz.open(stream=selected_file["content"], filetype="pdf")

        # Display the first page of the selected PDF
        img = pdf_document.load_page(0).get_pixmap().tobytes()
        st.image(img)
    else:
        st.write("No PDFs uploaded. Please go back to the first page to upload PDFs.")

    # Button to navigate back to the previous page
    if st.button("Go Back to Next Page"):
        st.session_state.current_page = "next_page"
        st.rerun()
