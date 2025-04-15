import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

st.set_page_config(page_title="Image Extractor", layout="centered")

st.title("🖼️ Image Extractor App")

uploaded_file = st.file_uploader("Upload a PDF file to extract images", type=["pdf"])

if uploaded_file is not None:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    st.success(f"PDF uploaded successfully. Total pages: {len(doc)}")

    image_count = 0
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)
        
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            st.image(image, caption=f"Page {page_num + 1} - Image {img_index + 1}")
            image_count += 1

    if image_count == 0:
        st.warning("No images found in the PDF.")
    else:
        st.success(f"Extracted {image_count} image(s).")
