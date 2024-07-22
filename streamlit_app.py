import streamlit as st
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, Inches
from docx.enum.table import WD_TABLE_ALIGNMENT
import csv
import pandas as pd
import io

def set_font(para, font_name='Arial', size=Pt(9)):
    for run in para.runs:
        run.font.name = font_name
        run.font.size = size

def add_page_number(paragraph):
    run = paragraph.add_run("Page ")
    run.font.size = Pt(7)
    run.font.name = 'Arial'

    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

    run = paragraph.add_run()
    run.font.size = Pt(7)
    run.font.name = 'Arial'

def set_table_borders(table):
    tbl = table._element
    tbl_pr = tbl.xpath('./w:tblPr')[0]
    tbl_borders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '4')
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), 'CCCCCC')
        tbl_borders.append(border)
    tbl_pr.append(tbl_borders)

def add_header(doc):
    section = doc.sections[0]
    header = section.header
    header_paragraph = header.paragraphs[0]
    header_paragraph.alignment = 1
    add_page_number(header_paragraph)
    header_paragraph.add_run("\n\n")

    p1 = header.add_paragraph("Student Name ________________________________________________________________________________________")
    p1.paragraph_format.left_indent = Inches(-0.5)
    p1.paragraph_format.right_indent = Inches(-0.5)
    set_font(p1)

    p2 = header.add_paragraph("Class _____________________________    Section _____________________  Roll Number _________________________")
    p2.paragraph_format.left_indent = Inches(-0.5)
    p2.paragraph_format.right_indent = Inches(-0.5)
    set_font(p2)

    p3 = header.add_paragraph("_______________________________________________________________________________________________________")
    p3.paragraph_format.left_indent = Inches(-1)
    p3.paragraph_format.right_indent = Inches(-1)
    set_font(p3, size=Pt(10))
    run = p3.runs[0]
    run.bold = True
    p3.add_run("\n")

def add_question_section(doc, question_num, rows):
    p = doc.add_paragraph(f"Q{question_num}")
    set_font(p, size=Pt(10))
    run = p.runs[0]
    run.bold = True
    
    table = doc.add_table(rows=rows, cols=1)
    set_table_borders(table)
    
    doc.add_paragraph()
    doc.add_paragraph()

def add_single_word_question(doc, question_number):
    p = doc.add_paragraph(f"Q{question_number} _____")        
    set_font(p, size=Pt(10))
    run = p.runs[0]
    run.bold = True
    p.add_run("\n\n")

def create_answer_sheet(csv_file):
    doc = Document()
    add_header(doc)

    p = doc.add_paragraph("SECTION 1")
    p.paragraph_format.alignment = 1
    set_font(p, size=Pt(17))
    run = p.runs[0]
    run.bold = True
    p.add_run("\n\n")

    reader = csv.reader(csv_file)
    next(reader)  # Skip the header row
    for row in reader:
        question_num, question_type, rows = row            
        if question_type == "single_word":                
            add_single_word_question(doc, question_num)
        elif question_type == "table":
            add_question_section(doc, question_num, int(rows))

    return doc

st.title("Answer Sheet Generator")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    csv_file = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
    
    # Create the answer sheet
    doc = create_answer_sheet(csv_file)
    
    # Save the document to a BytesIO object
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    
    # Provide download link
    st.download_button(
        label="Download Generated Answer Sheet",
        data=doc_io,
        file_name="Generated_Answer_Sheet.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
