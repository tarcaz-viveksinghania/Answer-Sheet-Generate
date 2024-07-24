import streamlit as st
import pandas as pd
import os

# Set page configuration to wide layout
st.set_page_config(layout="wide")

def save_to_csv(data, filename):
    new_data = pd.DataFrame(data, index=[0])
    if not os.path.isfile(filename):
        new_data.to_csv(filename, index=False)
    else:
        df = pd.read_csv(filename)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(filename, index=False)

def clear_form1():
    st.session_state.paper_name = ""
    st.session_state.examiner_name = ""
    st.session_state.class_name = ""

def clear_form2(form_key):
    st.session_state[f'section_{form_key}'] = ""
    st.session_state[f'question_number_{form_key}'] = ""
    st.session_state[f'part_{form_key}'] = ""
    st.session_state[f'subpart_{form_key}'] = ""
    st.session_state[f'question_type_{form_key}'] = ""
    st.session_state[f'question_{form_key}'] = ""
    st.session_state[f'marks_{form_key}'] = ""
    st.session_state[f'examiner_answer_{form_key}'] = ""
    st.session_state[f'expectation_{form_key}'] = ""
    st.session_state[f'outside_scope_{form_key}'] = ""

# Initialize session state for dynamic question forms
if 'question_forms' not in st.session_state:
    st.session_state.question_forms = []

if 'question_data' not in st.session_state:
    st.session_state.question_data = []

# Function to add a new question form
def add_question_form():
    form_key = len(st.session_state.question_forms)
    st.session_state.question_forms.append(form_key)
    st.rerun()

# Function to save question form data to CSV
def save_question_data(form_key):
    if (st.session_state[f'section_{form_key}'] and st.session_state[f'question_number_{form_key}'] and 
        st.session_state[f'part_{form_key}'] and st.session_state[f'subpart_{form_key}'] and 
        st.session_state[f'question_type_{form_key}'] and st.session_state[f'question_{form_key}'] and 
        st.session_state[f'marks_{form_key}'] and st.session_state[f'examiner_answer_{form_key}'] and 
        st.session_state[f'expectation_{form_key}'] and st.session_state[f'outside_scope_{form_key}']):
        
        data = {
            'Paper ID': st.session_state.paper_id,
            'Section': st.session_state[f'section_{form_key}'],
            'Question Number': st.session_state[f'question_number_{form_key}'],
            'Part': st.session_state[f'part_{form_key}'],
            'Subpart': st.session_state[f'subpart_{form_key}'],
            'Question Type': st.session_state[f'question_type_{form_key}'],
            'Question': st.session_state[f'question_{form_key}'],
            'Marks': st.session_state[f'marks_{form_key}'],
            "Examiner's Answer": st.session_state[f'examiner_answer_{form_key}'],
            'Expectation from the right answer, for full credit': st.session_state[f'expectation_{form_key}'],
            'Will outside scope be acceptable in the answer': st.session_state[f'outside_scope_{form_key}']
        }
        st.session_state.question_data.append(data)
        save_to_csv(data, 'question_details.csv')
        st.success(f"Question {form_key+1} data saved successfully!")
    else:
        st.error(f"Please fill out all fields in Question {form_key+1}.")

st.title("Exam Details Submission")

# First Form
st.header("Form 1: Exam Details Submission")

with st.form("exam_form"):
    f1, f2, f3 = st.columns(3)
    with f1:
        st.text_input("Paper Name", key="paper_name")
    with f2:
        st.text_input("Examiner's Name", key="examiner_name")
    with f3:
        st.text_input("Class", key="class_name")
    
    f4, f5 = st.columns(2)
    with f4:
        submit1 = st.form_submit_button(label="Submit")
    with f5:
        clear1 = st.form_submit_button(label="Clear", on_click=clear_form1)

if submit1:
    if st.session_state.paper_name and st.session_state.examiner_name and st.session_state.class_name:
        paper_id = f"{st.session_state.paper_name[:3].upper()}_{st.session_state.examiner_name[:3].upper()}_{st.session_state.class_name[:3].upper()}"
        st.session_state.paper_id = paper_id
        data1 = {
            'Paper ID': paper_id,
            'Paper Name': st.session_state.paper_name, 
            "Examiner's Name": st.session_state.examiner_name, 
            'Class': st.session_state.class_name
        }
        save_to_csv(data1, 'exam_details.csv')
        st.success("Data saved successfully!")
    else:
        st.error("Please fill out all fields.")

# Second Form
st.header("Form 2: Question Details Submission")

if 'paper_id' in st.session_state:
    for form_key in st.session_state.question_forms:
        st.markdown(f"Question {form_key + 1}")
        with st.form(f"question_form_{form_key + 1}"):
            g1, g2, g3, g4, g5 = st.columns(5)
            with g1:
                st.text_input("Section", key=f"section_{form_key}")
            with g2:
                st.text_input("Question Number", key=f"question_number_{form_key}")
            with g3:
                st.text_input("Part", key=f"part_{form_key}")
            with g4:
                st.text_input("Subpart", key=f"subpart_{form_key}")
            with g5:
                st.text_input("Question Type", key=f"question_type_{form_key}")
            
            st.text_area("Question", key=f"question_{form_key}")
            st.text_input("Marks", key=f"marks_{form_key}")
            st.text_area("Examiner's Answer", key=f"examiner_answer_{form_key}")
            st.text_area("Expectation from the right answer, for full credit", key=f"expectation_{form_key}")
            st.text_input("Will outside scope be acceptable in the answer", key=f"outside_scope_{form_key}")
            
            g6, g7 = st.columns(2)
            with g6:
                submit2 = st.form_submit_button(label="Submit", on_click=save_question_data, args=(form_key,))
            with g7:
                clear2 = st.form_submit_button(label="Clear", on_click=clear_form2, args=(form_key,))
    
    st.button("Add Another Question", on_click=add_question_form)

else:
    st.warning("Please submit the Exam Details form first to generate a Paper ID.")


# Convert the question data to CSV and create a download button
if st.session_state.question_data:
    df = pd.DataFrame(st.session_state.question_data)
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='question_details.csv',
        mime='text/csv'
    )
else:
    st.warning("No question data available to download.")

