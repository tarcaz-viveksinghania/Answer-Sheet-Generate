import streamlit as st
import pandas as pd
import os

# Function to save data to CSV
def save_to_csv(data, filename):
    new_data = pd.DataFrame(data, index=[0])
    if not os.path.isfile(filename):
        new_data.to_csv(filename, index=False)
    else:
        df = pd.read_csv(filename)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(filename, index=False)

# Function to clear form inputs for the first form
def clear_form1():
    st.session_state["paper_name"] = ""
    st.session_state["examiner_name"] = ""
    st.session_state["class_name"] = ""

# Function to clear form inputs for the second form
def clear_form2():
    st.session_state["section"] = ""
    st.session_state["question_number"] = ""
    st.session_state["part"] = ""
    st.session_state["subpart"] = ""
    st.session_state["question_type"] = ""
    st.session_state["question"] = ""
    st.session_state["marks"] = ""
    st.session_state["examiner_answer"] = ""
    st.session_state["expectation"] = ""
    st.session_state["outside_scope"] = ""

# Initialize session state for inputs of the first form
if 'paper_name' not in st.session_state:
    st.session_state.paper_name = ''
if 'examiner_name' not in st.session_state:
    st.session_state.examiner_name = ''
if 'class_name' not in st.session_state:
    st.session_state.class_name = ''

# Initialize session state for inputs of the second form
if 'section' not in st.session_state:
    st.session_state.section = ''
if 'question_number' not in st.session_state:
    st.session_state.question_number = ''
if 'part' not in st.session_state:
    st.session_state.part = ''
if 'subpart' not in st.session_state:
    st.session_state.subpart = ''
if 'question_type' not in st.session_state:
    st.session_state.question_type = ''
if 'question' not in st.session_state:
    st.session_state.question = ''
if 'marks' not in st.session_state:
    st.session_state.marks = ''
if 'examiner_answer' not in st.session_state:
    st.session_state.examiner_answer = ''
if 'expectation' not in st.session_state:
    st.session_state.expectation = ''
if 'outside_scope' not in st.session_state:
    st.session_state.outside_scope = ''




# Streamlit App
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

# Display the saved data of the first form (optional)
if os.path.isfile('exam_details.csv'):
    st.subheader("Saved Exam Details")
    df1 = pd.read_csv('exam_details.csv')
    st.dataframe(df1)












# Second Form
st.header("Form 2: Question Details Submission")

with st.form("question_form"):
    g1, g2, g3, g4, g5 = st.columns(5)
    with g1:
        st.text_input("Section", key="section")
    with g2:
        st.text_input("Question Number", key="question_number")
    with g3:
        st.text_input("Part", key="part")
    with g4:
        st.text_input("Subpart", key="subpart")
    with g5:
        st.text_input("Question Type", key="question_type")
    
    st.text_area("Question", key="question")
    st.text_input("Marks", key="marks")
    st.text_area("Examiner's Answer", key="examiner_answer")
    st.text_area("Expectation from the right answer, for full credit", key="expectation")
    st.text_input("Will outside scope be acceptable in the answer", key="outside_scope")
    
    g6, g7 = st.columns(2)
    with g6:
        submit2 = st.form_submit_button(label="Submit")
    with g7:
        clear2 = st.form_submit_button(label="Clear", on_click=clear_form2)

if submit2:
    if st.session_state.section and st.session_state.question_number and st.session_state.part and st.session_state.subpart and st.session_state.question_type and st.session_state.question and st.session_state.marks and st.session_state.examiner_answer and st.session_state.expectation and st.session_state.outside_scope:
        data2 = {
            'Paper ID': st.session_state.paper_id,
            'Section': st.session_state.section,
            'Question Number': st.session_state.question_number,
            'Part': st.session_state.part,
            'Subpart': st.session_state.subpart,
            'Question Type': st.session_state.question_type,
            'Question': st.session_state.question,
            'Marks': st.session_state.marks,
            "Examiner's Answer": st.session_state.examiner_answer,
            'Expectation from the right answer, for full credit': st.session_state.expectation,
            'Will outside scope be acceptable in the answer': st.session_state.outside_scope
        }
        save_to_csv(data2, 'question_details.csv')
        st.success("Data saved successfully!")
    else:
        st.error("Please fill out all fields.")

# Display the saved data of the second form (optional)
if os.path.isfile('question_details.csv'):
    st.subheader("Saved Question Details")
    df2 = pd.read_csv('question_details.csv')
    st.dataframe(df2)



