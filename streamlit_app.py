import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", google_api_key='AIzaSyDlBFVsmV8pao6Ax-bcR0dc5h4CusiNCsc')
def generate_recommendation(image):
    image = image.resize((380,280))
    st.image(image, caption='Uploaded Image')
    hmessage = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Generate a book recommendation that match the content of the uploaded image.explain why that book was chosen and how it relates to the given image in 5 words"
        },  
        {"type": "image_url", 
         "image_url": image},
    ]
       )
    response = llm.invoke([hmessage])
    recommendation = response.content
    st.write("**Book Recommendation:**")
    st.write(recommendation)

def main():
    st.title('Image-Based Book Recommendation')
    st.sidebar.title('Upload Image or Provide Image URL')
    option = st.sidebar.radio('Choose Input Option:', ('Upload Image', 'Provide Image URL'))

    if option == 'Upload Image':
        uploaded_image = st.sidebar.file_uploader(label='Upload Image', type=['jpg', 'jpeg', 'png'])

        if uploaded_image is not None:
            generate_recommendation(uploaded_image)

    elif option == 'Provide Image URL':
        image_url = st.sidebar.text_input(label='Enter Image URL:', value='')

        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                image = Image.open(BytesIO(image_data))
                generate_recommendation(image)
            else:
                st.error('Failed to fetch the image from the provided URL. Please check the URL and try again.')

if __name__ == '__main__':
    main()
