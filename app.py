!pip install python-dotenv
!pip install streamlit
!pip install pdf2image
!apt-get install poppler-utils
!pip install pymupdf


from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import io
import pdf2image
import base64
import fitz

import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, pdf_content[0], prompt])
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        # Take the first page for simplicity, or loop through images for all pages
        first_page = images[0]
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
        # Read the PDF file
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        # Initialize a list to hold the text of each page
        text_parts = []
        # Iterate over the pages of the PDF to extract the text
        for page in document:
            text_parts.append(page.get_text())
        # Concatenate the list into a single string with a space in between each part
        pdf_text_content = " ".join(text_parts)
        return pdf_text_content
    else:
        raise FileNotFoundError("No file uploaded")

@@ -62,6 +58,10 @@

submit4 = st.button("Percentage match")

input_promp = st.text_input("Queries: Feel Free to Ask here")
submit5 = st.button("Answer My Query")
input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
@@ -123,6 +123,20 @@
    else:
        st.write("Please upload a PDF file to proceed.")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_promp, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file to proceed.")
footer = """
---
#### Made By [Koushik](https://www.linkedin.com/in/gandikota-sai-koushik/)
For Queries, Reach out on [LinkedIn](https://www.linkedin.com/in/gandikota-sai-koushik/)  
*Resume Expert - Making Job Applications Easier*
"""

st.markdown("---")
st.caption("Resume Expert - Making Job Applications Easier")
st.markdown(footer, unsafe_allow_html=True)
‎frquent_conda_comands.md
+132


Original file line number	Diff line number	Diff line change
@@ -0,0 +1,132 @@
conda env list -- Allows you to check for existing list of Virtual Environments 
cls to clear the termnial
# Conda Commands Tutorial
Conda is an open-source package management and environment management system that is widely used in the data science and machine learning communities. It allows users to easily install, run, and update packages and their dependencies. This tutorial will guide you through the basics of using Conda, including installation, creating environments, managing packages, and more.
## Installing Conda
To use Conda, you first need to install it. Conda is included in Anaconda and Miniconda distributions. Anaconda includes Conda and a large number of scientific packages by default, while Miniconda includes Conda and a minimal set of packages.
- **Anaconda:** Download the Anaconda installer from the [official website](https://www.anaconda.com/products/distribution) and follow the installation instructions.
- **Miniconda:** Download the Miniconda installer from the [Miniconda website](https://docs.conda.io/en/latest/miniconda.html) and follow the installation instructions.
## Checking Conda Installation
After installing, you can check the installation by opening a terminal or command prompt and typing:
```bash
conda --version
```
This command should display the version of Conda installed.
## Managing Environments
### Creating a New Environment
To create a new environment with a specific Python version, use:
```bash
conda create --name myenv python=3.8
```
Replace `myenv` with your desired environment name and `3.8` with your desired Python version.
### Activating an Environment
To activate the environment, use:
- **On Windows:**
  ```bash
  activate myenv
  ```
- **On macOS and Linux:**
  ```bash
  source activate myenv
  ```
### Deactivating an Environment
To deactivate the current environment and return to the base environment, use:
- **On Windows:**
  ```bash
  deactivate
  ```
- **On macOS and Linux:**
  ```bash
  source deactivate
  ```
### Listing Environments
To list all environments you have created, use:
```bash
conda env list
```
or
```bash
conda info --envs
```
## Managing Packages
### Installing Packages
To install a package in the active environment, use:
```bash
conda install numpy
```
Replace `numpy` with the name of the package you wish to install.
### Updating Packages
To update a specific package, use:
```bash
conda update numpy
```
To update all packages in the current environment, use:
```bash
conda update --all
```
### Listing Installed Packages
To list all packages installed in the current environment, use:
```bash
conda list
```
## Removing Packages or Environments
### Removing a Package
To remove a package from the current environment, use:
```bash
conda remove numpy
```
### Removing an Environment
To remove an entire environment, use:
```bash
conda env remove --name myenv
```
