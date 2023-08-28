import streamlit as st
import os
# File Processing Pkgs
from PIL import Image
import pandas as pd
import docx2txt
from PyPDF2 import PdfReader


PAGE_CONFIG = {"page_title":"FileUploader","page_icon":":smiley","layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

# Load Images
@st.cache_resource
def load_image(image_file):
    img = Image.open(image_file)
    return img

# Function to Save Uploaded File to Directory
def save_uploaded_file(uploadedfile):
    with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Arquivo salvo : {} em tempDir".format(uploadedfile.name))

    
def read_pdf(file):
    pdfReader = PdfReader(file)
    count = len(pdfReader.pages)
    all_page_text = ""
    for i in range(count):
        page = pdfReader.pages[i]
        all_page_text += page.extract_text()
    return all_page_text 

def main():
    st.title("File Upload Tutorial 😁")
    
    menu = ["Home","Dataset","DocumentFiles","About"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Home":
        st.subheader("Home")
        image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
        if image_file is not None:
            file_details = {"FileName":image_file.name,"Filetype":image_file.type}
            st.write(file_details)
            # st.write(type(image_file))
            img = load_image(image_file)
            st.image(img, width=250)     
            # Saving File
            # tempDir/imagename.png
            with open(os.path.join("tempDir",image_file.name),"wb") as f:
                f.write(image_file.getbuffer())
            st.success("Arquivo salvo")
                        
    elif choice == "Dataset":
        st.subheader("Dataset")
        data_file = st.file_uploader("Upload CSV", type=["csv"])
        if data_file is not None:
            file_details = {"FileName":data_file.name,"FileType":data_file.type}
            st.write(type(data_file))
            df = pd.read_csv(data_file)
            st.dataframe(df)
            save_uploaded_file(data_file)
        
    elif choice == "DocumentFiles":
        st.subheader("DocumentFiles")
        docx_file = st.file_uploader("Upload Document", type=["pdf","docx","txt"])
        if st.button("Process"):
            if docx_file is not None:
                file_details = {"filename":docx_file.name,"filetype":docx_file.type,"filesize":docx_file.size}
                st.write(file_details)
                if docx_file.type == "text/plain":
                    # raw_text = docx_file.read()
                    # st.write(raw_text)  # works but in bytes
                    # st.text(raw_text)   # does work as expected
                    raw_text = str(docx_file.read(),"utf-8") # Read as string (decode bytes to string)
                    st.write(raw_text)
                    st.text(raw_text)
                elif docx_file.type == 'application/pdf':
                    #try:
                    #    with pdfplumber.open(docx_file) as pdf:
                    #        pages = pdf.pages[0]
                    #        st.write(pages.extract_text())
                    #except:
                    #    st.write("None")
                    
                    # using PyPDF
                    raw_text = read_pdf(docx_file)
                    st.write(raw_text)
                else:
                    raw_text = docx2txt.process(docx_file)
                    st.write(raw_text)# works
                    # st.text(raw_text)# works
    else:
        st.subheader("About")

if __name__ == '__main__':
    main()