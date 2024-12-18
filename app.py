import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import datetime
import base64
from PIL import Image
import io
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
    /* Set the uploaded image as the background */
    .stApp {{
        background-image: url('data:image/png;base64,{img_base64}');
        background-size: cover;
        color: black; /* Set default text color to black */
    }}
    
    /* Center the bold text in the header */
    .header-text {{
        text-align: center;
        font-weight: bold;
        font-size: 50px;
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
        height:50px !important;
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
        height:50px !important;
    }}

    div[data-baseweb="select"] > div {{
        color: #000000 !important; /* White text for dropdown and select options */
    }}
    .stTextInput>div>div>input {{
        width: 300px;  /* Set width */
        height: 50px;  /* Set height */
    }}
    .stTextInput label {{
        font-size: 50px;  /* Adjust font size */
        font-weight: bold;  /* Make text bold */
    }}
    /* Style for the dropdown label */
    .custom-label {{
        font-weight: bold !important;
        color: black !important;
        font-size: 18px !important; /* Increase label size */
        display: block;
        margin-bottom: 8px;
    }}
    .stSelectbox {{
        margin-top: -30px; /* Reduce spacing above the dropdown */
    }}

    /* Button styling */
    .stButton button {{
        background-color: yellow !important; /* Yellow background */
        color: black !important; /* Black text */
        border: 2px solid #f9a825; /* Border to match select box */
        padding: 10px 20px;
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
</style>
""", unsafe_allow_html=True)

# Display logo
st.markdown('<img src="https://mir-s3-cdn-cf.behance.net/project_modules/disp/302bf6105854045.5f82a86549930.png" class="logo">', unsafe_allow_html=True)

# Display bold header text
st.markdown('<div class="header-text">Onboarding Audit Portal</div>', unsafe_allow_html=True)

# Session State Initialization
if "login_email" not in st.session_state:
    st.session_state["login_email"] = None
if "selected_page" not in st.session_state:
    st.session_state["selected_page"] = "How to Use"

# Page Navigation
selected_page = st.session_state["selected_page"]

# How to Use Page and Login Section
if selected_page == "How to Use":
    st.title("How to Use the App")
    st.markdown(
        """
        1. Review the **How to Use** section below.
        2. Enter your email ID in the **Login** section and click Login.
        3. Once logged in, you will be redirected to the **Input Form** page.
        """
    )

    st.header("Login Section")
    if "button_text" not in st.session_state:
        st.session_state.button_text = "Login"
    if "login_message" not in st.session_state:
        st.session_state.login_message = ""
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Login Section"

# Define allowed emails
    allowed_emails = ["mis.operations@mpokket.com"]

# Page navigation logic
    if st.session_state.selected_page == "Login Section":
        st.header("Login Section")

    email = st.text_input("Enter your email ID", key="email_input")

    if st.button(st.session_state.button_text):
        if st.session_state.button_text == "Login":
            if email in allowed_emails:
            # Update session state upon successful login
                st.session_state.login_message = "You are successfully logged in.Click another time to get in"
                st.session_state["selected_page"] = "Input Form"
                st.success("Welcome! You can now proceed.")
            else:
                st.error("Invalid email ID. Please try again.")
        elif st.session_state.button_text == "Get In":
            st.session_state["selected_page"] = "Input Form"
            st.success("Welcome! You can now proceed.")

# Display the login message
    if st.session_state.login_message:
        st.write(st.session_state.login_message)
# Input Form Page
elif selected_page == "Input Form":

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
        st.markdown('<div class="custom-label">Enter Date of Audit:</div>', unsafe_allow_html=True)
        date_of_audit = st.date_input("",key="date_of_audit")

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
        

        

        # Team Leader (No validation)
        st.markdown('<div class="custom-label">Enter Team Leader Name:</div>', unsafe_allow_html=True)
        team_leader = st.text_input("")

        # Audit Name (No validation)
        st.markdown('<div class="custom-label">Enter Audit Name:</div>', unsafe_allow_html=True)
        audit_name = st.text_input("",key="audit_name")

        # Auditor Center (List validation)
        st.markdown('<div class="custom-label">Select Auditor Center:</div>', unsafe_allow_html=True)
        auditor_center = st.selectbox("",
                                      ["Indore", "Vijaywada", "Mysore", "Bhopal", "Noida", "Kolkata", "Coimbatore",
                                       "HYD", "Ranchi"])

        # Auditor Designation (List validation)
        st.markdown('<div class="custom-label">Select Auditor Designation:</div>', unsafe_allow_html=True)
        auditor_designation = st.selectbox("", ["TL", "Trainer"])

    with col2:
        
        # User Register Number (Numeric validation)
        st.markdown('<div class="custom-label">Enter User Register Number:</div>', unsafe_allow_html=True)
        user_register_number = st.text_input("",key="user_register_number")

        # Calling Number (Numeric validation)
        st.markdown('<div class="custom-label">Enter Calling Number:</div>', unsafe_allow_html=True)
        calling_number = st.text_input("",key="calling_number")

        # Date of Call (Date format validation)
        st.markdown('<div class="custom-label">Enter Date of Call:</div>', unsafe_allow_html=True)
        date_of_call = st.date_input("",key="date_of_call")
        
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
        motive_of_call = st.selectbox("", ["Yes", "No"])

        # Probe / Confirm User's Profession (Yes/No validation)
        st.markdown("""<div class="custom-label">Probe / Confirm User's Profession:</div>""", unsafe_allow_html=True)
        probe_confirm_user_profession = st.selectbox("", ["Yes", "No", "NA"])

        # Current Profile Stage / Previous Interaction
        st.markdown('<div class="custom-label">Current Profile Stage / Previous Interaction:</div>', unsafe_allow_html=True)
        Current_Profile_Stage_Previous_Interaction = st.selectbox("",
                                                                  ["Yes", "No", "FATAL"])

        st.markdown('<div class="custom-label">Probe If User have any doc releated Profession Study Business:</div>', unsafe_allow_html=True)
        Probe_If_User_have_any_doc_releated_Profession_Study_Business = st.selectbox(
            "", ["Yes", "No", "NA"])

        st.markdown('<div class="custom-label">Current Profile Stage / Previous Interaction:</div>', unsafe_allow_html=True)
        Guide_User_with_required_documents_One_by_one = st.selectbox("",
                                                                     ["Yes", "Fatal", "NA"])

        st.markdown('<div class="custom-label">Urgency:</div>', unsafe_allow_html=True)
        Urgency = st.selectbox("", ["Yes", "Fatal", "NA"])

        st.markdown('<div class="custom-label">Objection Handling:</div>', unsafe_allow_html=True)
        Objection_Handling = st.selectbox("", ["Yes", "Fatal", "NA"])



    # Section 2 (Right Column)
    with col3:
        st.markdown('<div class="custom-label">Explained user how to take first loan:</div>', unsafe_allow_html=True)
        Explained_user_how_to_take_first_loan = st.selectbox("",
                                                             ["Yes", "Fatal", "NA"])

        st.markdown('<div class="custom-label">Reconfirmation / Call back script:</div>', unsafe_allow_html=True)
        Reconfirmation_Call_back_script = st.selectbox("", ["Yes", "Fatal", "NA"])
        
        st.markdown('<div class="custom-label">Energetic Tone and Clear articulation:</div>', unsafe_allow_html=True)
        Energetic_Tone_and_Clear_articulation=st.selectbox("", ["Yes","No"])

        st.markdown('<div class="custom-label">Two way communication:</div>', unsafe_allow_html=True)
        Two_way_communication = st.selectbox("", ["Yes", "NO"])
        
        st.markdown('<div class="custom-label">Active listening and Dead Air:</div>', unsafe_allow_html=True)
        Active_listening_and_Dead_Air = st.selectbox("", ["Yes", "NO"])
        
        st.markdown('<div class="custom-label">Professional Communication:</div>', unsafe_allow_html=True)
        Professional_Communication = st.selectbox("", ["Yes", "NO"])

        st.markdown('<div class="custom-label">Informationr:</div>', unsafe_allow_html=True)
        Information = st.selectbox("", ["Yes", "NO"])

        st.markdown('<div class="custom-label">Follow Up:</div>', unsafe_allow_html=True)
        Follow_Up = st.selectbox("", ["Yes", "NO"])

        st.markdown('<div class="custom-label">Tagging:</div>', unsafe_allow_html=True)
        Tagging = st.selectbox("", ["Yes", "NA", "NO"])

        st.markdown('<div class="custom-label">Enter User Register Number:</div>', unsafe_allow_html=True)
        Benefits= st.selectbox("Tagging", ["Informed","Not Informed"])

        st.markdown('<div class="custom-label">Benefits:</div>', unsafe_allow_html=True)
        Fatal = st.selectbox("", ["Yes", "NO"])

        st.markdown('<div class="custom-label">Remarks:</div>', unsafe_allow_html=True)
        Remarks = st.text_input("",key="Remarks")

        st.markdown('<div class="custom-label">Agent Feedback Status:</div>', unsafe_allow_html=True)
        Agent_Feedback_Status = st.selectbox("", ["Closed", "Open"])


    with col4:
        st.markdown('<div class="custom-label">Profile completion status prior to call:</div>', unsafe_allow_html=True)
        Profile_completion_status_prior_to_call = st.selectbox("",
                                                               ["Blank profile", "Partially complete",
                                                                "Almost complete"])

        st.markdown('<div class="custom-label">PIP/SFA Status:</div>', unsafe_allow_html=True)
        PIP_SFA_Status = st.selectbox("", ["Correct", "Incorrect", "NA"])
        

        st.markdown('<div class="custom-label">VOC:</div>', unsafe_allow_html=True)
        VOC = st.selectbox("",list(VOC))
        
        
        st.markdown('<div class="custom-label">AOI:</div>', unsafe_allow_html=True)
        AOI = st.selectbox("",list(AOI))

        st.markdown('<div class="custom-label">Enter Call Duration (HH:mm:ss):</div>', unsafe_allow_html=True)
        call_duration = st.text_input("",key="call_duration")

        st.markdown('<div class="custom-label">KYC Type:</div>', unsafe_allow_html=True)
        KYC_type = st.selectbox("", ["Not Updated", "OKYC", "VKYC", "CKYC"])

        st.markdown('<div class="custom-label">Disposition Accuracy:</div>', unsafe_allow_html=True)
        Disposition_Accuracy = st.selectbox("", ["Correct", "Incorrect", "Not Done"])

        st.markdown('<div class="custom-label">Enter DCS Tagging L1:</div>', unsafe_allow_html=True)
        DCS_Tagging_L1 = st.text_input("",key="DCS_Tagging_L1")

        st.markdown('<div class="custom-label">Enter DCS Tagging L2:</div>', unsafe_allow_html=True)
        DCS_Tagging_L2 = st.text_input("",key="DCS_Tagging_L2")

        st.markdown('<div class="custom-label">Enter DCS Tagging L3:</div>', unsafe_allow_html=True)
        DCS_Tagging_L3 = st.text_input("",key="DCS_Tagging_L3")

        st.markdown('<div class="custom-label">Actual Tagging L1:</div>', unsafe_allow_html=True)
        Actual_Tagging_L1 = st.text_input("",key="Actual_Tagging_L1")

        st.markdown('<div class="custom-label">Actual Tagging L2:</div>', unsafe_allow_html=True)
        Actual_Tagging_L2 = st.text_input("",key="Actual_Tagging_L2")

        st.markdown('<div class="custom-label">Actual Tagging L3:</div>', unsafe_allow_html=True)
        Actual_Tagging_L3 = st.text_input("",key="Actual_Tagging_L3")

    # Add Row Button
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
        if missing_fields:
            error_placeholder.error(f"Missing required fields: {', '.join(missing_fields)}")
        else:
            st.session_state["input_table"].append(data)

    # Display Table
    if st.session_state["input_table"]:
        st.write("Your Input Table:")
        df = pd.DataFrame(st.session_state["input_table"])
        st.dataframe(df)

        # Delete Row
        row_to_delete = st.number_input(
            "Enter Row Number to Delete (1-based index):",
            min_value=1,
            max_value=len(df),
            step=1
        )
        if st.button("Delete Row"):
            # Adjust for 1-based index
            st.session_state["input_table"].pop(row_to_delete - 1)

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
st.markdown("""
    <div class="footer">
        Developed by MIS Team<br>
        For any query, email at <a href="mailto:mis.operations@mpokket.com" style="color:white;">mis.operations@mpokket.com</a>
    </div>
""", unsafe_allow_html=True)
