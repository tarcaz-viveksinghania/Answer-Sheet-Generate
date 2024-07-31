import streamlit as st
import fitz  # PyMuPDF
import page2  # Import the next_page module
import page3

st.set_page_config(page_title="Answer Sheet Evaluation", layout="wide")

# Function to render a specific page of the PDF
def render_pdf_page(pdf_document, page_number):
    page = pdf_document.load_page(page_number)
    pix = page.get_pixmap()
    img = pix.tobytes()
    return img

def pdf_viewer():
    st.title("Multiple PDF Viewer")

    # File uploader for multiple PDFs
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        # Store the uploaded files in session state
        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = []
        
        for uploaded_file in uploaded_files:
            if not any(file["name"] == uploaded_file.name for file in st.session_state.uploaded_files):
                st.session_state.uploaded_files.append({
                    "name": uploaded_file.name,
                    "content": uploaded_file.getvalue()
                })

        # Create a dictionary to store the PDF documents and their page counts
        pdf_documents = {}
        for file in st.session_state.uploaded_files:
            pdf_documents[file["name"]] = fitz.open(stream=file["content"], filetype="pdf")

        # Ensure the session state includes all uploaded PDFs
        if "page_numbers" not in st.session_state:
            st.session_state.page_numbers = {}
        for pdf_name in pdf_documents.keys():
            if pdf_name not in st.session_state.page_numbers:
                st.session_state.page_numbers[pdf_name] = 0

        # Selectbox to choose which PDF to view
        selected_pdf_name = st.selectbox("Select a PDF", list(pdf_documents.keys()))
        pdf_document = pdf_documents[selected_pdf_name]
        total_pages = pdf_document.page_count

        # Display the current page of the selected PDF
        img = render_pdf_page(pdf_document, st.session_state.page_numbers[selected_pdf_name])
        st.image(img)

        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Previous Page") and st.session_state.page_numbers[selected_pdf_name] > 0:
                st.session_state.page_numbers[selected_pdf_name] -= 1
                st.rerun()
        with col2:
            st.write(f"Page {st.session_state.page_numbers[selected_pdf_name] + 1} of {total_pages}")
        with col3:
            if st.button("Next Page") and st.session_state.page_numbers[selected_pdf_name] < total_pages - 1:
                st.session_state.page_numbers[selected_pdf_name] += 1
                st.rerun()

        
    st.divider()
    # Button to navigate to the next Streamlit page
    if st.button("Go to Next Page"):
        st.session_state.current_page = "next_page"
        st.rerun()

# Main function to manage page navigation
def main():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "pdf_viewer"

    if st.session_state.current_page == "pdf_viewer":
        pdf_viewer()
    elif st.session_state.current_page == "next_page":
        page2.display_next_page()
    elif st.session_state.current_page == "page3":
        page3.display_page3()

if __name__ == "__main__":
    main()
