import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI

# Configure Streamlit page layout
st.set_page_config(layout="wide")

# Set up Google Generative AI model
llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", google_api_key='AIzaSyDlBFVsmV8pao6Ax-bcR0dc5h4CusiNCsc')

def generate_recommendation(image):
    # Display uploaded image
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Generate recommendation based on image content
    hmessage = {
        "content": [
            {
                "type": "text",
                "text": "Generate a book recommendation that matches the content of the uploaded image. Explain why that book was chosen and how it relates to the given image in 5 words."
            },
            {
                "type": "image",
                "image": image
            }
        ]
    }
    msg = llm.invoke(hmessage)
    recommendation = msg.content

    # Display recommendation
    st.write("**Book Recommendation:**")
    st.write(recommendation)

def main():
    st.title('Image-Based Book Recommendation')
    st.sidebar.title('Upload Image or Provide Image URL')

    # User input option: Upload image or provide image URL
    option = st.sidebar.radio('Choose Input Option:', ('Upload Image', 'Provide Image URL'))

    if option == 'Upload Image':
        # Allow user to upload image
        uploaded_image = st.sidebar.file_uploader(label='Upload Image', type=['jpg', 'jpeg', 'png'])

        if uploaded_image is not None:
            # Generate recommendation based on uploaded image
            generate_recommendation(uploaded_image)

    elif option == 'Provide Image URL':
        # Allow user to provide image URL
        image_url = st.sidebar.text_input(label='Enter Image URL:', value='')

        if image_url:
            # Fetch image from URL
            response = requests.get(image_url)
            if response.status_code == 200:
                # Read image data
                image_data = response.content
                # Create PIL Image object
                image = Image.open(BytesIO(image_data))
                # Generate recommendation based on image URL
                generate_recommendation(image)
            else:
                st.error('Failed to fetch the image from the provided URL. Please check the URL and try again.')

if __name__ == '__main__':
    main()
