
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import datetime
import os
import base64
from PIL import Image
import io
import time
import re
from google.oauth2.service_account import Credentials
# Google Sheets Authentication

def authenticate_google_sheets():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )
    client = gspread.authorize(credentials)
    return client
def image_to_base64(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode()

image_base64 = image_to_base64("logo.png")

@st.cache_data(ttl=1200)
def fetch_data_from_gsheet(sheet_name):
    client = authenticate_google_sheets()
    sheet = client.open(sheet_name).get_worksheet(1)  # Access Sheet 2 (index starts at 0)
    data = sheet.col_values(1)  # Get all values from the first column
    return data[1:]  # Skip header row if there's one

# Fetch cached data


# Write data to Google Sheets
def write_to_sheet(sheet_name, data, email):
    client = authenticate_google_sheets()
    sheet = client.open(sheet_name).sheet1

    # Get the number of rows already in the sheet
    current_data = sheet.get_all_values()

    # Determine the row index to append data
    row_index = len(current_data) + 1  # Append below the last existing row

    # Convert date and time objects to string
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    data_with_meta = []
    for item in data:
        if isinstance(item, (datetime.date, datetime.datetime)):
            item = item.strftime("%Y-%m-%d")  # Convert to date string format
        elif isinstance(item, datetime.time):
            item = item.strftime("%H:%M:%S")  # Convert to time string format
        data_with_meta.append(item)

    # Add email and date columns to the data
    data_with_meta += [email, current_date]

    # Append the data to the sheet
    sheet.append_row(data_with_meta)

# Add custom CSS for styling
st.set_page_config(page_title="Multi-Page App", layout="wide")

# CSS styling
uploaded_file = "Picture2.png"
df=pd.read_csv('drop_down_list.csv')
call_time_slot=df['Call Time Slot'].dropna()
Bucket_name=df['Bucket Name'].dropna()
VOC=df['VOC'].dropna()
AOI=df['AOI'].dropna()





if uploaded_file is not None:
    # Convert uploaded image to Image object
    image = Image.open(uploaded_file)
    
    
    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Encode image to base64
    import base64
    img_base64 = base64.b64encode(img_bytes.read()).decode()

    # Add custom CSS with local image as background
    
    st.markdown(f"""
    <style>
        .main {{
        overflow: auto; /* Enable scrolling */
        width: 100vw; /* Set viewport width */
        height: 100vh; /* Set viewport height */
        white-space: nowrap; /* Prevent wrapping */
    }}
    /* Ensure columns and content don't wrap */
    .block-container {{
        display: flex; 
        flex-wrap: nowrap; /* Disable wrapping */
    }}
    .stApp {{
            background-image: url('data:image/png;base64,{img_base64}');
            background-size: cover;
            color: black; /* Set default text color to black */
            max-width: 100%;
            padding: 0;
            margin: 0;
            overflow-x: hidden; /* Prevent horizontal scrolling */
        }}

    /* Make tables responsive */
        
    /* Center the bold text in the header */
    .header-text {{
        text-align: center;
        font-weight: bold;
        font-size: 80px;
        color: black;
        padding-top: 20px;
    }}

    /* Dropdown container and options styling */
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important; /* Black dropdown background */
        color: #000000 !important; /* White text */
        border: 2px solid #000000 !important; /* Orange border */
        font-size: 16px !important; /* Larger text */
        border-radius: 5px !important; /* Rounded corners */
        padding: 5px !important;
        width: 300px !important;
        height:60px !important;
    }}

    div[data-baseweb="select"] > div {{
        color: #000000 !important; /* White text for dropdown and select options */
    }}

    /* Style for the dropdown label */
    label {{
        font-weight: bold !important;
        color: black !important;
        font-size: 18px !important; /* Increase label size */
        display: block;
        margin-bottom: 8px;
    }}
    div[data-baseweb="input"] > div {{
        background-color: #FFFFFF !important; /* Black dropdown background */
        color: #000000 !important; /* White text */
        border: 2px solid #000000 !important; /* Orange border */
        font-size: 16px !important; /* Larger text */
        border-radius: 5px !important; /* Rounded corners */
        width: 300px !important;
        height:60px !important;
        padding: 5px !important;
        margin: 5px 0;
    }}
    div[data-baseweb="select"] > div {{
        color: #000000 !important; /* White text for dropdown and select options */
    }}
    /* Style for the dropdown label */
    label {{
        font-weight: bold !important;
        color: black !important;
        font-size: 18px !important; /* Increase label size */
        display: block;
        margin-bottom: 8px;
    }}

    /* Button styling */
    .stButton button {{
        background-color: yellow !important; /* Yellow background */
        color: black !important; /* Black text */
        border: 2px solid #000000; /* Border to match select box */
        padding: 20px 30px;
        font-weight: bold;
        font-size: 14px;
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-top: 20px; /* Centering the button */
    }}
    
    /* Button hover effect */
    .stButton button:hover {{
        background-color: #f9a825 !important;
        color: black !important;
    }}

    /* Increase logo size */
    .logo {{
        width: 250px;
        position: absolute;
        top: 20px;
        left: 20px;
    }}

    /* Footer text styling */
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1E90FF;
        color: black;
        text-align: center;
        padding: 10px 0;
        font-weight: bold;
    }}
    .custom-label {{
        font-size: 18px; /* Adjust font size */
        font-weight: bold; /* Optional: Make it bold */
        color: #333; /* Optional: Change text color */
        margin-bottom: 0px; /* Reduce spacing below the label */
    }}
    .stSelectbox {{
        margin-top: -20px; /* Reduce spacing above the dropdown */
    }}
    .stTextInput div[role="textbox"]::after {{
            content: none;
        }}
    .stTextInput input {{
            background-color: #ffffff !important; /* Light grey background */
            color: #000000 !important; /* Dark text */
            font-size: 16px !important; /* Larger text */
            width: 300px !important; /* Set a fixed width */
            height: 40px !important; /* Adjust input height */
        }}

    .stTextInput input:focus {{
            border-color: #ff6347 !important; /* Focus border color */
            background-color: #fff !important; /* White background on focus */
        }}
    .stTextArea textarea {{
            background-color: #FFFFFF !important;
            border: 2px solid #000000 !important;
            color: #000000 !important;
            padding: 10px !important;
            font-size: 16px !important;
            width: 300px ;
            border-radius: 5px ;
            height: 35px;
        }}
    </style>
""", unsafe_allow_html=True)

# Display logo
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Path to your image file
image_path = "logo.png"

try:
    # Encode the image as Base64
    encoded_image = encode_image_to_base64(image_path)
    
    # Inject the header with the image
    st.markdown(f"""
        <style>
        header {{
            display: flex;
            padding: 0px;
          
        }}
        header img {{
                height: 110px; 
                width:300px;
                margin-right: 300px;
               
        }}
        .H {{
            padding: 15px;
            font-size: 50px;
            color: #333;
            text-align: center;
        }}
        </style>
        <header>
            <img src="data:image/png;base64,{encoded_image}" alt="Logo">
        </header>
        <div class="H" ><h1>Onboarding Audit Portal</h1></div>

        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.error("Image file not found. Please check the file path.")

#st.markdown('<img src="https://mir-s3-cdn-cf.behance.net/project_modules/disp/302bf6105854045.5f82a86549930.png" class="logo">', unsafe_allow_html=True)

# Display bold header text
#st.markdown('<div class="header-text">Onboarding Audit Portal</div>', unsafe_allow_html=True)
#st.image("logo.png")

# Session State Initialization
if "login_email" not in st.session_state:
    st.session_state["login_email"] = None
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "Login"

# Page Navigation
selected_page = st.session_state["selected_page"]

# Define allowed emails and passwords (this is for demonstration; never hardcode credentials in production!)
allowed_credentials = {"mis.operations@mpokket.com": "password123"}

# Login Page
if selected_page == "Login":
    col1,col2,col3,col4,col5=st.columns(5)
    
    st.markdown(
        """
        <style>
            /* Center-aligned container for the Login Page */
        .login-container {
             display: flex;
             justify-content: center;
             align-items: center;
             flex-direction: column;
        }
        .login-input-box {
            width: 300px; /* Adjust width as needed */
            text-align: center;
            align-items: center;
            margin-bottom: 15px; /* Add spacing between inputs */
        }
        .stTextInput {
        width: 300px;
        height: 70px;
        
        }
        
        .login-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        .stButton button {
            width: 200px;
            margin-top: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with col3:
    # Center-aligned container
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Login Page</div>', unsafe_allow_html=True)
    
        # Input fields for email and password (scoped CSS class applied)
        email = st.text_input(
            "Email ID",
            key="email_input",
            placeholder="Enter your email ID",
            label_visibility="collapsed",
        )
        password = st.text_input(
            "Password",
            type="password",
            key="password_input",
            placeholder="Enter your password",
            label_visibility="collapsed",
        )

    # Login button
    if st.button("Login"):
        if email in allowed_credentials and allowed_credentials[email] == password:
            st.session_state["login_email"] = email
            st.session_state["selected_page"] = "How to Use"
            st.success("Login successful! Redirecting to 'How to Use'...")
            st.rerun()
        else:
            st.error("Invalid email or password. Please try again.")
    st.markdown('</div>', unsafe_allow_html=True)  # Close the login-container div

# How to Use Page
elif selected_page == "How to Use":
    st.title("How to Use the App")
    st.markdown(
        """
        1. Review the **How to Use** section below.
        2. Once ready, click **Next** to proceed to the **Input Form**.
        """
    )

    if st.button("Next"):
        st.session_state["selected_page"] = "Input Form"
        st.rerun()

# Input Form Page
elif selected_page == "Input Form":
    st.markdown(f"""
    <style>
    .main {{
        overflow: auto; /* Enable scrolling */
        width: 100vw; /* Set viewport width */
        height: 100vh; /* Set viewport height */
        white-space: nowrap; /* Prevent wrapping */
    }}
    /* Ensure columns and content don't wrap */
    .block-container {{
        display: flex; 
        flex-wrap: nowrap; /* Disable wrapping */
    }}
    .stApp {{
            background-image: url('data:image/png;base64,{img_base64}');
            background-size: cover;
            color: black; /* Set default text color to black */
            max-width: 100%;
            padding: 0;
            margin: 0;
            overflow-x: hidden; /* Prevent horizontal scrolling */
        }}

    /* Make tables responsive */
        
    /* Center the bold text in the header */
    .header-text {{
        text-align: center;
        font-weight: bold;
        font-size: 80px;
        color: black;
        padding-top: 20px;
    }}

    /* Dropdown container and options styling */
    div[data-baseweb="select"] > div {{
        background-color: #ffffff !important; /* Black dropdown background */
        color: #000000 !important; /* White text */
        border: 2px solid #000000 !important; /* Orange border */
        font-size: 16px !important; /* Larger text */
        border-radius: 5px !important; /* Rounded corners */
        padding: 5px !important;
        width: 300px !important;
        height:60px !important;
    }}

    div[data-baseweb="select"] > div {{
        color: #000000 !important; /* White text for dropdown and select options */
    }}

    /* Style for the dropdown label */
    label {{
        font-weight: bold !important;
        color: black !important;
        font-size: 18px !important; /* Increase label size */
        display: block;
        margin-bottom: 8px;
    }}
    div[data-baseweb="input"] > div {{
        background-color: #FFFFFF !important; /* Black dropdown background */
        color: #000000 !important; /* White text */
        border: 2px solid #000000 !important; /* Orange border */
        font-size: 16px !important; /* Larger text */
        border-radius: 5px !important; /* Rounded corners */
        width: 300px !important;
        height:60px !important;
        padding: 5px !important;
        margin: 5px 0;
    }}
    div[data-baseweb="select"] > div {{
        color: #000000 !important; /* White text for dropdown and select options */
    }}
    /* Style for the dropdown label */
    label {{
        font-weight: bold !important;
        color: black !important;
        font-size: 18px !important; /* Increase label size */
        display: block;
        margin-bottom: 8px;
    }}

    /* Button styling */
    .stButton button {{
        background-color: yellow !important; /* Yellow background */
        color: black !important; /* Black text */
        border: 2px solid #000000; /* Border to match select box */
        padding: 20px 30px;
        font-weight: bold;
        font-size: 14px;
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-top: 20px; /* Centering the button */
    }}
    
    /* Button hover effect */
    .stButton button:hover {{
        background-color: #f9a825 !important;
        color: black !important;
    }}

    /* Increase logo size */
    .logo {{
        width: 250px;
        position: absolute;
        top: 20px;
        left: 20px;
    }}

    /* Footer text styling */
    .footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #1E90FF;
        color: black;
        text-align: center;
        padding: 10px 0;
        font-weight: bold;
    }}
    .custom-label {{
        font-size: 18px; /* Adjust font size */
        font-weight: bold; /* Optional: Make it bold */
        color: #333; /* Optional: Change text color */
        margin-bottom: 0px; /* Reduce spacing below the label */
    }}
    .stSelectbox {{
        margin-top: -20px; /* Reduce spacing above the dropdown */
    }}
    .stTextInput div[role="textbox"]::after {{
            content: none;
        }}
    .stTextInput input {{
            background-color: #ffffff !important; /* Light grey background */
            color: #000000 !important; /* Dark text */
            font-size: 16px !important; /* Larger text */
            width: 300px !important; /* Set a fixed width */
            height: 40px !important; /* Adjust input height */
        }}

    .stTextInput input:focus {{
            border-color: #ff6347 !important; /* Focus border color */
            background-color: #fff !important; /* White background on focus */
        }}
    .stTextArea textarea {{
            background-color: #FFFFFF !important;
            border: 2px solid #000000 !important;
            color: #000000 !important;
            padding: 10px !important;
            font-size: 16px !important;
            width: 300px ;
            border-radius: 5px ;
            height: 35px;
        }}
    </style>
""", unsafe_allow_html=True)

    # Data storage
    if "input_table" not in st.session_state:
        st.session_state["input_table"] = []

    # Split the form into two columns using st.columns
    col1, col2,col3,col4 = st.columns(4)

    # Section 1 (Left Column)
    with col1:

        # Date of Birth input (DOB)
        st.markdown('<div class="custom-label">LOB:</div>', unsafe_allow_html=True)
        LOB = st.selectbox("", ["SE", "SIB", "SIC", "Student"])
        # Center selection
        st.markdown('<div class="custom-label">Select your Center:</div>', unsafe_allow_html=True)
        center = st.selectbox("",
                              ["Bhopal", "Indore", "Vijaywada", "MYS", "Noida", "Kolkata", "Coimbatore", "Ranchi"])

        # Partner Name (List format)
        st.markdown('<div class="custom-label">Select Partner Name:</div>', unsafe_allow_html=True)
        partner_name = st.selectbox("",
                                    ["Tarus", "TTBS", "MAGNUM", "ICCS", "INHOUSE", "HRH NEXT", "AYUDA"])

        # Date of Audit (Date format)
        

        # Week (List format)
        st.markdown('<div class="custom-label">Select Week:</div>', unsafe_allow_html=True)
        week = st.selectbox("", ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"])

        # Audit Category (List format)
        st.markdown('<div class="custom-label">Select Audit Category:</div>', unsafe_allow_html=True)
        audit_category = st.selectbox("", ["Floor", "RCA"])
        client = authenticate_google_sheets()

# Open the Google Sheet by its URL or name
        spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Qi_wJmG-Y1rQaeF1bI51zuAPEP3f-iNdUwVk1RHpM0s/edit?gid=1871398781#gid=1871398781")
# Specify the sheet name you want to read
        sheet = spreadsheet.worksheet("Agent_Data")
          # Replace with your sheet name
        dropdown_values = sheet.get_all_records(expected_headers=None)

    # Show the dropdown menu with the data fetched from Google Sheets
        st.markdown('<div class="custom-label">Agent EMP ID:</div>', unsafe_allow_html=True)
        EMP_ID = st.selectbox("", list(set(row['EMP_ID'] for row in dropdown_values )))
        selected_login_id = next(item["Ameyo_Id"] for item in dropdown_values if item["EMP_ID"] == EMP_ID)
        selected_Name = next(item["Name"] for item in dropdown_values if item["EMP_ID"] == EMP_ID)

        # Login ID (Numeric validation)
        sheet = spreadsheet.worksheet("Agent_Data")
        dropdown=[]
        for i in dropdown_values:
            dropdown.append(i['Ameyo_Id'])
    # Show the dropdown menu with the data fetched from Google Sheets
        st.markdown('<div class="custom-label">Enter Login ID:</div>', unsafe_allow_html=True)
        Login_ID = st.selectbox("", dropdown,index=dropdown.index(selected_login_id))

        # Agent Name (No validation)
        dropdown=[]
        for i in dropdown_values:
            dropdown.append(i['Name'])
    # Show the dropdown menu with the data fetched from Google Sheets
        st.markdown('<div class="custom-label">Enter Agent Name:</div>', unsafe_allow_html=True)
        Agent_Name = st.selectbox("", dropdown,index=dropdown.index(selected_Name))

        # Auditor Center (List validation)
        st.markdown('<div class="custom-label">Select Auditor Center:</div>', unsafe_allow_html=True)
        auditor_center = st.selectbox("",
                                      ["Indore", "Vijaywada", "Mysore", "Bhopal", "Noida", "Kolkata", "Coimbatore",
                                       "HYD", "Ranchi"])

        # Auditor Designation (List validation)
        st.markdown('<div class="custom-label">Select Auditor Designation:</div>', unsafe_allow_html=True)
        auditor_designation = st.selectbox("", ["TL", "Trainer"])
        
        st.markdown('<div class="custom-label">Enter Call Duration (HH:mm:ss):</div>', unsafe_allow_html=True)
        call_duration = st.text_area("",key="call_duration",label_visibility="collapsed")

        st.markdown('<div class="custom-label">Actual Tagging L1:</div>', unsafe_allow_html=True)
        Actual_Tagging_L1 = st.text_area("",key="Actual_Tagging_L1",label_visibility="collapsed")

        # Date of Call (Date format validation)
        st.markdown('<div class="custom-label">Enter Date of Call:</div>', unsafe_allow_html=True)
        date_of_call = st.date_input("",key="date_of_call",label_visibility="collapsed")
        
        

    with col2:

        # Call Time Slot (Time format validation)
        st.markdown('<div class="custom-label">Call_Time_Slot:</div>', unsafe_allow_html=True)
        call_time_slot = st.selectbox("",list(call_time_slot))
        
        # Bucket (List format)
        st.markdown('<div class="custom-label">Bucket:</div>', unsafe_allow_html=True)
    # Show the dropdown menu with the data fetched from Google Sheets
        bucket = st.selectbox("",list(Bucket_name))

        # Energetic Opening and Closing (Yes/No validation)
        st.markdown('<div class="custom-label">Energetic Opening and Closing:</div>', unsafe_allow_html=True)
        energetic_opening_closing = st.selectbox("", ["Yes", "No"])

        # Motive of the Call (Yes/No validation)
        st.markdown('<div class="custom-label">Motive of the Call:</div>', unsafe_allow_html=True)
        motive_of_call = st.selectbox("", ["Yes", "No"],key="motive_of_call")

        # Probe / Confirm User's Profession (Yes/No validation)
        st.markdown("""<div class="custom-label">Probe / Confirm User's Profession:</div>""", unsafe_allow_html=True)
        probe_confirm_user_profession = st.selectbox("", ["Yes", "No", "NA"],key="probe_confirm_user_profession")

        # Current Profile Stage / Previous Interaction
        st.markdown('<div class="custom-label">Current Profile Stage / Previous Interaction:</div>', unsafe_allow_html=True)
        Current_Profile_Stage_Previous_Interaction = st.selectbox("",
                                                                  ["Yes", "No", "FATAL"],key="Current_Profile_Stage_Previous_Interaction")

        st.markdown('<div class="custom-label"> Doc Releated Profession Study Business:</div>', unsafe_allow_html=True)
        Probe_If_User_have_any_doc_releated_Profession_Study_Business = st.selectbox(
            "", ["Yes", "No", "NA"],key="Probe_If_User_have_any_doc_releated_Profession_Study_Business")

        st.markdown('<div class="custom-label">Current Profile Stage / Previous Interaction:</div>', unsafe_allow_html=True)
        Guide_User_with_required_documents_One_by_one = st.selectbox("",
                                                                     ["Yes", "Fatal", "NA"],key="Guide_User_with_required_documents_One_by_one")

        st.markdown('<div class="custom-label">Urgency:</div>', unsafe_allow_html=True)
        Urgency = st.selectbox("", ["Yes", "Fatal", "NA"],key="Urgency")

        st.markdown('<div class="custom-label">Objection Handling:</div>', unsafe_allow_html=True)
        Objection_Handling = st.selectbox("", ["Yes", "Fatal", "NA"],key="Objection_Handling")

        # User Register Number (Numeric validation)
        st.markdown('<div class="custom-label">Enter User Register Number:</div>', unsafe_allow_html=True)
        user_register_number = st.text_area("",key="user_register_number",label_visibility="collapsed")

        st.markdown('<div class="custom-label">Enter Calling Number:</div>', unsafe_allow_html=True)
        calling_number = st.text_area("",key="calling_number",label_visibility="collapsed")
        #remarks
        st.markdown('<div class="custom-label">Remarks:</div>', unsafe_allow_html=True)
        Remarks = st.text_area("",key="remarks",label_visibility="collapsed")

        

    # Section 2 (Right Column)
    with col3:
        st.markdown('<div class="custom-label">Explained user how to take first loan:</div>', unsafe_allow_html=True)
        Explained_user_how_to_take_first_loan = st.selectbox("",
                                                             ["Yes", "Fatal", "NA"],key="Explained_user_how_to_take_first_loan")

        st.markdown('<div class="custom-label">Reconfirmation / Call back script:</div>', unsafe_allow_html=True)
        Reconfirmation_Call_back_script = st.selectbox("", ["Yes", "Fatal", "NA"],key="Reconfirmation_Call_back_script")
        
        st.markdown('<div class="custom-label">Energetic Tone and Clear articulation:</div>', unsafe_allow_html=True)
        Energetic_Tone_and_Clear_articulation=st.selectbox("", ["Yes","No"],key="Energetic_Tone_and_Clear_articulation")

        st.markdown('<div class="custom-label">Two way communication:</div>', unsafe_allow_html=True)
        Two_way_communication = st.selectbox("", ["Yes", "NO"],key="Two_way_communication")
        
        st.markdown('<div class="custom-label">Active listening and Dead Air:</div>', unsafe_allow_html=True)
        Active_listening_and_Dead_Air = st.selectbox("", ["Yes", "NO"],key="Active_listening_and_Dead_Air")
        
        st.markdown('<div class="custom-label">Professional Communication:</div>', unsafe_allow_html=True)
        Professional_Communication = st.selectbox("", ["Yes", "NO"],key="Professional_Communication")

        st.markdown('<div class="custom-label">Informationr:</div>', unsafe_allow_html=True)
        Information = st.selectbox("", ["Yes", "NO"],key="Information")

        st.markdown('<div class="custom-label">Follow Up:</div>', unsafe_allow_html=True)
        Follow_Up = st.selectbox("", ["Yes", "NO"],key="Follow_Up")

        st.markdown('<div class="custom-label">Tagging:</div>', unsafe_allow_html=True)
        Tagging = st.selectbox("", ["Yes", "NA", "NO"],key="Tagging")

        st.markdown('<div class="custom-label">Benefits:</div>', unsafe_allow_html=True)
        Benefits= st.selectbox("", ["Informed","Not Informed"],key="Benefits")

        

        

        st.markdown('<div class="custom-label">Enter DCS Tagging L1:</div>', unsafe_allow_html=True)
        DCS_Tagging_L1 = st.text_area("",key="DCS_Tagging_L1",label_visibility="collapsed")

        st.markdown('<div class="custom-label">Enter DCS Tagging L2:</div>', unsafe_allow_html=True)
        DCS_Tagging_L2 = st.text_area("",key="DCS_Tagging_L2",label_visibility="collapsed")
        
        st.markdown('<div class="custom-label">Enter DCS Tagging L3:</div>', unsafe_allow_html=True)
        DCS_Tagging_L3 = st.text_area("",key="DCS_Tagging_L3",label_visibility="collapsed")

    with col4:
        st.markdown('<div class="custom-label">Fatal:</div>', unsafe_allow_html=True)
        Fatal = st.selectbox("", ["Yes", "NO"],key="Fatal")

        st.markdown('<div class="custom-label">Agent Feedback Status:</div>', unsafe_allow_html=True)
        Agent_Feedback_Status = st.selectbox("", ["Closed", "Open"],key="Agent_Feedback_Status")
        
        st.markdown('<div class="custom-label">Profile completion status prior to call:</div>', unsafe_allow_html=True)
        Profile_completion_status_prior_to_call = st.selectbox("",
                                                               ["Blank profile", "Partially complete",
                                                                "Almost complete"],key="Profile_completion_status_prior_to_call")

        st.markdown('<div class="custom-label">PIP/SFA Status:</div>', unsafe_allow_html=True)
        PIP_SFA_Status = st.selectbox("", ["Correct", "Incorrect", "NA"],key="PIP_SFA_Status")
        

        st.markdown('<div class="custom-label">VOC:</div>', unsafe_allow_html=True)
        VOC = st.selectbox("",list(VOC),key="VOC")
        
        
        st.markdown('<div class="custom-label">AOI:</div>', unsafe_allow_html=True)
        AOI = st.selectbox("",list(AOI),key="AOI")

        

        st.markdown('<div class="custom-label">KYC Type:</div>', unsafe_allow_html=True)
        KYC_type = st.selectbox("", ["Not Updated", "OKYC", "VKYC", "CKYC"])

        st.markdown('<div class="custom-label">Disposition Accuracy:</div>', unsafe_allow_html=True)
        Disposition_Accuracy = st.selectbox("", ["Correct", "Incorrect", "Not Done"])

        st.markdown('<div class="custom-label">Enter Team Leader Name:</div>', unsafe_allow_html=True)
        team_leader = st.selectbox("", ["1", "2"],key="team_leader")
        
        st.markdown('<div class="custom-label">Enter Audit Name:</div>', unsafe_allow_html=True)
        audit_name = st.selectbox("", ["1", "2"],key="audit_name")

        st.markdown('<div class="custom-label">Actual Tagging L2:</div>', unsafe_allow_html=True)
        Actual_Tagging_L2 = st.text_area("",key="Actual_Tagging_L2",label_visibility="collapsed")

        st.markdown('<div class="custom-label">Actual Tagging L3:</div>', unsafe_allow_html=True)
        Actual_Tagging_L3 = st.text_area("",key="Actual_Tagging_L3",label_visibility="collapsed")
        
        st.markdown('<div class="custom-label">Enter Date of Audit:</div>', unsafe_allow_html=True)
        date_of_audit = st.date_input("",key="date_of_audit",label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)  # Close the login-container div
    # Add Row Button
    if "input_table" not in st.session_state:
        st.session_state["input_table"] = []
    
    # Initialize session state for the update form values
    if "update_form_values" not in st.session_state:
        st.session_state["update_form_values"] = {}
    error_placeholder = st.empty()
    if st.button("Add Row"):
        data = {
            "LOB": LOB,
            "Center": center,
            "Partner Name": partner_name,
            "Date of Audit": date_of_audit,
            "Week": week,
            "Audit Category": audit_category,
            "EMP ID": EMP_ID,
            "Login ID": Login_ID,
            "Agent Name": Agent_Name,
            "Team Leader": team_leader,
            "Audit Name": audit_name,
            "Auditor Center": auditor_center,
            "Auditor Designation": auditor_designation,
            "User Register Number": user_register_number,
            "Calling Number": calling_number,
            "Date of Call": date_of_call,
            "Call Time Slot": call_time_slot,
            "Bucket": bucket,
            "Energetic Opening and Closing": energetic_opening_closing,
            "Motive of the Call": motive_of_call,
            "Probe / Confirm User's Profession": probe_confirm_user_profession,
            "Current Profile Stage / Previous Interaction": Current_Profile_Stage_Previous_Interaction,
            "Probe If User has Doc Related to Profession/Study/Business": Probe_If_User_have_any_doc_releated_Profession_Study_Business,
            "Guide User with Required Documents": Guide_User_with_required_documents_One_by_one,
            "Urgency": Urgency,
            "Objection Handling": Objection_Handling,
            "Explained User How to Take First Loan": Explained_user_how_to_take_first_loan,
            "Reconfirmation Call Back Script": Reconfirmation_Call_back_script,
            "Energetic Tone and Clear articulation":Energetic_Tone_and_Clear_articulation,
            "Two-way Communication": Two_way_communication,
            "Active Listening and Dead Air": Active_listening_and_Dead_Air,
            "Professional Communication": Professional_Communication,
            "Information": Information,
            "Follow Up": Follow_Up,
            "Tagging": Tagging,
            "Benefits":Benefits,
            "Fatal": Fatal,
            "Remarks": Remarks,
            "Agent Feedback Status": Agent_Feedback_Status,
            "Profile Completion Status Prior to Call": Profile_completion_status_prior_to_call,
            "PIP/SFA Status": PIP_SFA_Status,
            "VOC": VOC,
            "AOI": AOI,
            "Call Duration": call_duration,
            "KYC Type": KYC_type,
            "Disposition Accuracy": Disposition_Accuracy,
            "DCS Tagging L1": DCS_Tagging_L1,
            "DCS Tagging L2": DCS_Tagging_L2,
            "DCS Tagging L3": DCS_Tagging_L3,
            "Actual Tagging L1": Actual_Tagging_L1,
            "Actual Tagging L2": Actual_Tagging_L2,
            "Actual Tagging L3": Actual_Tagging_L3
        }
        missing_fields = [key for key, value in data.items() if not value or value == ""]
        new_row = data.copy()  # Create a copy of the data as new row
    
        # Handle missing fields
        time_pattern = r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$"
        if missing_fields:
            error_placeholder.error(f"Missing required fields: {', '.join(missing_fields)}")
        # Handle duplicate row check
        elif any(row["EMP ID"] == EMP_ID and row["User Register Number"] == user_register_number and row["Call Time Slot"] == call_time_slot for row in st.session_state.get("input_table", [])):
            st.warning("A row with the same EMP ID, User Register Number, or Call Time already exists. Please verify the input.")
        elif not user_register_number.isdigit() or len(user_register_number) != 10:
            st.error("User Register Number must be exactly 10 digits.")
        elif not calling_number.isdigit() or len(calling_number) != 10:
            st.error("Calling Number must be exactly 10 digits.")
        
        elif not re.match(time_pattern, call_duration):
            st.error("Invalid time format! Please enter the time in HH:mm:ss format (e.g., 02:30:45).")
        else:
            # If no missing fields and no duplicate, add the new row to the table
            if "input_table" not in st.session_state:
                st.session_state["input_table"] = []
            st.session_state["input_table"].append(new_row)
            st.success("Row added successfully!")

    # Display Table
    if st.session_state["input_table"]:
        st.markdown(
            """
            <style>
            /* Change background color */
            .stApp {
                background-color: #f5f5f5; /* Light gray */
            }
                    
            /* Table styling */
            .scrollable-table {
                max-height: 800px;
                overflow-y: auto;
                border: 1px solid #ddd;
                width: 100%;
            }
            .styled-table {
                border-collapse: collapse;
                width: 100%;
                font-size: 14px;
                text-align: left;
                background-color: #FFFFFF; /* Light gray background */
            }
            .styled-table th, .styled-table td {
                border: 1px solid #000000;
                padding: 8px;
                white-space: nowrap; /* Prevent text wrapping */
            }
            .styled-table th {
                background-color: #009879;
                color: white;
            }
            
                    
            /* Custom form styling */
            .stForm {
                background-color: #ADD8E6; /* Light blue */
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            .form-header {
                text-align: center;
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #333333; /* Dark gray */
            }
            .custom-label {
                font-size: 20px;
                margin-bottom: 0px;
                color: #333333; /* Dark gray */
            }
            /* Radio button styling */
            .stRadio > label {
                font-size: 25px; /* Larger text */
                font-weight: bold;
            }
            .stRadio div[role="radio"] {
                transform: scale(10); /* Increase button size */
                margin-right: 15px; /* Space between buttons */
            }
    
            .stButton > button {
                background-color: #1E90FF !important; /* Dodger blue */
                color: white !important;
                font-size: 24px !important;
                padding: 30px 40px !important;
                border-radius: 8px;
                border: none;
            }
            .stButton > button:hover {
                background-color: #0059b3 !important; /* Darker blue on hover */
            }
            .stForm button {
                background-color: #FFD700 !important; /* Dodger blue */
                color: black !important;
                font-size: 24px !important; /* Larger button text */
                padding: 20px 30px !important; /* Increased button size */
                border-radius: 8px;
                border: none;
                font-weight: bold;
            }
            .stForm button:hover {
                background-color: #DAA520 !important; /* Darker blue on hover */
            }
            </style>
            """,
        unsafe_allow_html=True,
            )
    
        # Generate the HTML table
        st.markdown('<div class="form-header">Data Table</div>', unsafe_allow_html=True)
        table_html = "<div class='scrollable-table'><table class='styled-table'>"
        headers = list(st.session_state["input_table"][0].keys())
    
        # Create the table header row
        table_html += "<thead><tr>"
        table_html += "".join(f"<th>{header}</th>" for header in headers)
        table_html += "</tr></thead>"
    
        # Create the table body rows
        table_html += "<tbody>"
        for row in st.session_state["input_table"]:
            table_html += "<tr>"
            for value in row.values():
                table_html += f"<td>{value}</td>"
            table_html += "</tr>"
        table_html += "</tbody></table></div>"

    # Display the table
        st.markdown(table_html, unsafe_allow_html=True)

            
            # Create a column layout for buttons
          # Adjust the width as needed
        
        # Place buttons beside the table
        with st.form("row_operations_form"):
            st.markdown('<div class="form-header">Update or Delete a Row</div>', unsafe_allow_html=True)

            # Using 4 columns for inputs
            col1, col2, col3, col4 = st.columns(4)
        
            with col1:
                st.markdown('<div class="custom-label">Enter User Register Number:</div>', unsafe_allow_html=True)
                user_register_number_input = st.text_area("", key="1",label_visibility="collapsed")
        
            with col2:
                st.markdown('<div class="custom-label">Enter EMP ID:</div>', unsafe_allow_html=True)
                emp_id_input = st.text_area("", key="emp_id_input",placeholder="Type here...",label_visibility="collapsed")
        
            with col3:
                st.markdown('<div class="custom-label">Select Operation:</div>', unsafe_allow_html=True)
                operation = st.radio("", ["***Update Row***", "***Delete Row***"], key="operation")
        
            with col4:  # Alignment adjustment
                submit_button = st.form_submit_button("Submit")

        
        if submit_button:
            matching_index = None
            for index, row in enumerate(st.session_state["input_table"]):
                if (row.get("User Register Number") == user_register_number_input
                        and row.get("EMP ID") == emp_id_input):
                    matching_index = index
                    break
                
            if matching_index is None:
                st.error("No matching row found. Please check the inputs.")
            else:
                if operation == "Delete Row":
                    st.session_state["input_table"].pop(matching_index)
                    st.success("Row deleted successfully!")
                    st.rerun()
                elif operation == "Update Row":
                    st.session_state["row_index_to_update"] = matching_index
                    st.session_state["selected_row"] = st.session_state["input_table"][matching_index]
                    st.session_state["show_update_form"] = True
                    st.rerun()
                
                # Show update form if selected
        if st.session_state.get("show_update_form", False):
            st.markdown("### Update Row:")
            updated_row = {}
            cols = st.columns(4)
                
                    # Populate the update form with existing values
            for i, (key, value) in enumerate(st.session_state["selected_row"].items()):
                with cols[i % 4]:
                    updated_row[key] = st.text_input(f"{key}:", value=value)
                
                    # Save updated row
            if st.button("Save Updated Row"):
                st.session_state["input_table"][st.session_state["row_index_to_update"]] = updated_row
                del st.session_state["selected_row"]
                del st.session_state["row_index_to_update"]
                st.session_state["show_update_form"] = False  # Hide update form after saving
                st.success("Row updated!")
                st.rerun()

    
        # Final Submit Button
        if st.session_state["input_table"] and st.button("Final Submit"):
            try:
                for row in st.session_state["input_table"]:
                    write_to_sheet(
                        "Quality_Requirment",
                        list(row.values()),
                        st.session_state["login_email"]
                    )
                st.success("Data successfully written to Google Sheets!")
                st.session_state["input_table"] = []  # Clear after submission
            except Exception as e:
                st.error(f"An error occurred: {e}")
            
            # Refresh Button
st.markdown("""
    <div class="footer">
        Developed by MIS Team<br>
        For any query, email at <a href="mailto:mis.operations@mpokket.com" style="color:white;">mis.operations@mpokket.com</a>
    </div>
""", unsafe_allow_html=True)
