import streamlit as st 
from rembg import remove
from PIL import Image 
import os 
import io 

st.write("# Remove background from Image. ")

uploaded_image = st.file_uploader("Choose an Image", type=["jpg", "png", "jpeg", "webp", "ico"])

st.write("### Input Images")

if uploaded_image is not None:
   # Open and display the original image
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded', use_column_width=True)

    #Get image name and extension
    image_name = uploaded_image.name
    name, extension = os.path.splitext(image_name)

    #Remove the background
    nobg_image = remove(image)

    
    # Check if the image has an alpha channel and convert if necessary
    #Apha channel prevent an image from being transparent so we cant remove the background
    if nobg_image.mode == 'RGBA':
        # Convert to RGB without alpha channel for JPEG or save as PNG to keep alpha channel
        nobg_image = nobg_image.convert('RGB')
        extension = ".png"  # Make it a PNG to support alpha channel
    
    # Save the processed image to an in-memory file
    img_bytes = io.BytesIO()
    nobg_image.save(img_bytes, format='PNG' if extension == '.png' else image.format)
    img_bytes.seek(0)

    st.image(nobg_image, caption=f"{name}-no-bg{extension}")

    
    download_btn = st.download_button(
        label="Download Image",
        data = img_bytes,
        file_name=f"{name}-nobackground{extension}",
        mime=f"image/{extension.strip('.')}"
    )
   
else:
    st.write("Please upload an Image")


