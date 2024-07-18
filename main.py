import os

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with LHS!",
    layout="centered",  # Page layout option
)

left_column, center_column, right_column = st.columns([6, 7, 1])
with center_column:
    st.image("logo.png", width=150)


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Predefined questions and answers
predefined_data = {
    "who are you": "I am Lighthouse Info Systems Pvt. Ltd., a leading provider of ERP solutions for various industries. A multimodal AI model developed by LHS.",
    "who made you": "I was created by the team at LHS.",
    "when was Lighthouse Info Systems founded": "Lighthouse Info Systems was founded in 1987.",
    "where is Lighthouse Info Systems headquartered": "Lighthouse Info Systems is headquartered in Nagpur, India.",
    "what industries does Lighthouse serve": "Lighthouse serves industries such as manufacturing, distribution, retail, and services.",
    "what is the flagship product of Lighthouse Info Systems": "The flagship product of Lighthouse Info Systems is its comprehensive ERP solution.",
    "what ERP solutions does Lighthouse offer": "Lighthouse offers ERP solutions that include modules for finance, inventory, production, sales, human resources, and more.",
    "can Lighthouse ERP be customized": "Yes, Lighthouse ERP solutions can be customized to meet the specific needs of different businesses.",
    "does Lighthouse offer cloud-based ERP solutions": "Yes, Lighthouse offers both on-premises and cloud-based ERP solutions.",
    "what is the mission of Lighthouse Info Systems": "The mission of Lighthouse Info Systems is to provide innovative and reliable ERP solutions that help businesses streamline their operations and improve efficiency.",
    "how can I contact Lighthouse Info Systems": "You can contact Lighthouse Info Systems through their website or by calling their customer service number.",
    "what are the key features of Lighthouse ERP": "Key features of Lighthouse ERP include real-time data access, scalability, flexibility, and integration with other systems.",
    "does Lighthouse provide training for its ERP solutions": "Yes, Lighthouse provides comprehensive training and support for its ERP solutions.",
    "how can I request a demo of Lighthouse ERP": "You can request a demo of Lighthouse ERP by visiting their website and filling out the demo request form.",
    "what is the pricing model for Lighthouse ERP": "The pricing for Lighthouse ERP varies based on the specific needs and scale of the business. It is best to contact Lighthouse directly for a customized quote.",
    "does Lighthouse offer support services": "Yes, Lighthouse offers extensive support services, including technical support, training, and consultation.",
    "what is the Lighthouse Info Systems customer portal": "The customer portal is an online platform where Lighthouse clients can access support, resources, and updates about their ERP solutions.",
    "are there any case studies or success stories from Lighthouse clients": "Yes, Lighthouse Info Systems has several case studies and success stories that showcase how their ERP solutions have helped businesses succeed.",
    "what is the implementation process for Lighthouse ERP": "The implementation process for Lighthouse ERP involves assessment, planning, customization, training, and go-live support.",
    "can Lighthouse ERP integrate with other software": "Yes, Lighthouse ERP can integrate with various other software systems to provide a seamless workflow.",
    "what are the system requirements for Lighthouse ERP": "The system requirements for Lighthouse ERP depend on the deployment option (cloud or on-premises). Detailed requirements can be obtained from Lighthouse Info Systems.",
    "does Lighthouse provide mobile access to its ERP solutions": "Yes, Lighthouse ERP solutions are accessible via mobile devices, allowing users to manage their business on the go.",
    "what is the Lighthouse partner program": "The Lighthouse partner program is designed to collaborate with technology and business partners to extend the reach and capabilities of Lighthouse ERP solutions.",
    "how does Lighthouse ensure data security in its ERP solutions": "Lighthouse implements robust security measures, including encryption, access controls, and regular audits, to ensure the security of data in its ERP solutions.",
    "can Lighthouse ERP handle multi-location operations": "Yes, Lighthouse ERP is designed to handle multi-location operations efficiently.",
    "does Lighthouse offer industry-specific ERP solutions": "Yes, Lighthouse offers industry-specific ERP solutions tailored to the unique requirements of different sectors.",
    "what is the process for upgrading Lighthouse ERP": "Upgrading Lighthouse ERP involves a planned process that includes data backup, testing, and deployment of the latest version.",
    "can Lighthouse ERP handle multi-currency transactions": "Yes, Lighthouse ERP supports multi-currency transactions, making it suitable for global businesses.",
    "what makes Lighthouse ERP unique": "Lighthouse ERP is unique due to its comprehensive functionality, customization options, and dedicated customer support.",
    "does Lighthouse offer consulting services": "Yes, Lighthouse offers consulting services to help businesses optimize their processes and implement ERP solutions effectively.",
    "how can I stay updated with the latest news from Lighthouse": "You can stay updated with the latest news from Lighthouse by subscribing to their newsletter or following them on social media.",
    "what awards has Lighthouse Info Systems won": "Lighthouse Info Systems has won several awards for its innovative ERP solutions and excellent customer service.",
    "what are the benefits of using Lighthouse ERP": "Benefits of using Lighthouse ERP include improved efficiency, real-time insights, better decision-making, and streamlined operations.",
    "does Lighthouse ERP support business intelligence and analytics": "Yes, Lighthouse ERP includes business intelligence and analytics features to help businesses make data-driven decisions.",
    "can Lighthouse ERP be scaled for growing businesses": "Yes, Lighthouse ERP is scalable and can grow with your business needs.",
    "what is the backup and disaster recovery plan for Lighthouse ERP": "Lighthouse ERP includes comprehensive backup and disaster recovery plans to ensure business continuity.",
    "how does Lighthouse handle software updates and maintenance": "Lighthouse handles software updates and maintenance through regular patches, updates, and technical support.",
    "is there a community or forum for Lighthouse ERP users": "Yes, there is a community forum where Lighthouse ERP users can share experiences, ask questions, and get support.",
    "what languages does Lighthouse ERP support": "Lighthouse ERP supports multiple languages to cater to a diverse user base.",
    "can Lighthouse ERP be used by small businesses": "Yes, Lighthouse ERP is suitable for businesses of all sizes, including small and medium-sized enterprises.",
    "how does Lighthouse ensure customer satisfaction": "Lighthouse ensures customer satisfaction through dedicated support, continuous improvement, and by listening to customer feedback."
}

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"  # Emoji for user role
    else:
        return "user"  # Emoji for assistant role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Function to replace "Gemini" or "Google" with "Lighthouse" and "LHS" in responses
def replace_lighthouse_terms(response):
    response = response.replace("Gemini", "LHS-BOT")
    response = response.replace("Google", "Lighthouse Info Systems Pvt. Ltd.")
    return response

# Display the chatbot's title on the page
#st.title("LightHouse - ChatBot")
left_column, center_column, right_column = st.columns([3, 7, 1])
with center_column:
    st.header("LightHouse - ChatBot")
# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        response_text = replace_lighthouse_terms(message.parts[0].text)
        st.markdown(response_text)

# Input field for user's message
user_prompt = st.chat_input("Ask LightHouse...")

if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Check if the user's message is a predefined question
    if user_prompt.lower() in predefined_data:
        # Display predefined answer
        with st.chat_message("assistant"):
            predefined_answer = replace_lighthouse_terms(predefined_data[user_prompt.lower()])
            st.markdown(predefined_answer)
    else:
        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        
        # Display Gemini-Pro's response
        with st.chat_message("assistant"):
            gemini_answer = replace_lighthouse_terms(gemini_response.text)
            st.markdown(gemini_answer)
