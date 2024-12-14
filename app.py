import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import datetime
import base64
from PIL import Image
import io
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
def fetch_data_from_gsheet(sheet_name):
    client = authenticate_google_sheets()
    sheet = client.open(sheet_name).get_worksheet(1)  # Access Sheet 2 (index starts at 0)
    data = sheet.col_values(1)  # Get all values from the first column
    return data[1:]  # Skip header row if there's one

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

     /* Input, dropdown container, and options styling */
    input, select, div[data-baseweb="select"] > div {{
        background-color: black !important; /* Black dropdown background */
        color: white !important; /* White text */
        font-size: 16px !important; /* Larger text */
        border-radius: 5px !important; /* Rounded corners */
        padding: 5px !important;
        width: 300px !important; /* Increased width */
        height: 50px !important; /* Increased height */
    }}
    
    /* Style for the labels */
    label {{
        font-weight: bold !important;
        color: black !important;
        font-size: 20px !important; /* Increased label size */
        display: block;
        margin-bottom: 8px;
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
                st.session_state.login_message = "You are successfully logged in. Click on the 'Get In' button."
                st.session_state.button_text = "Get In"
                st.session_state.login_email = email
                st.success(st.session_state.login_message)
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
        LOB = st.selectbox("LOB:", ["SE", "SIB", "SIC", "Student"])

        # Center selection
        center = st.selectbox("Select your Center:",
                              ["Bhopal", "Indore", "Vijaywada", "MYS", "Noida", "Kolkata", "Coimbatore", "Ranchi"])

        # Partner Name (List format)
        partner_name = st.selectbox("Select Partner Name:",
                                    ["Tarus", "TTBS", "MAGNUM", "ICCS", "INHOUSE", "HRH NEXT", "AYUDA"])

        # Date of Audit (Date format)
        date_of_audit = st.date_input("Enter Date of Audit:")

        # Week (List format)
        week = st.selectbox("Select Week:", ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5"])

        # Audit Category (List format)
        audit_category = st.selectbox("Select Audit Category:", ["Floor", "RCA"])
        client = authenticate_google_sheets()

# Open the Google Sheet by its URL or name
        spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Qi_wJmG-Y1rQaeF1bI51zuAPEP3f-iNdUwVk1RHpM0s/edit?gid=1871398781#gid=1871398781")
# Specify the sheet name you want to read
        sheet = spreadsheet.worksheet("Agent_Data")
          # Replace with your sheet name
        dropdown_values = sheet.get_all_records(expected_headers=None)
        dropdown=[]
        for i in dropdown_values:
            dropdown.append(i['EMP_ID'])
    # Show the dropdown menu with the data fetched from Google Sheets
        EMP_ID = st.selectbox("Agent EMP ID", dropdown)
        selected_login_id = next(item["Ameyo_Id"] for item in dropdown_values if item["EMP_ID"] == EMP_ID)
        selected_Name = next(item["Name"] for item in dropdown_values if item["EMP_ID"] == EMP_ID)

        # Login ID (Numeric validation)
        sheet = spreadsheet.worksheet("Agent_Data")
        dropdown=[]
        for i in dropdown_values:
            dropdown.append(i['Ameyo_Id'])
    # Show the dropdown menu with the data fetched from Google Sheets
        Login_ID = st.selectbox("Enter Login ID:", dropdown,index=dropdown.index(selected_login_id))

        # Agent Name (No validation)
        dropdown=[]
        for i in dropdown_values:
            dropdown.append(i['Name'])
    # Show the dropdown menu with the data fetched from Google Sheets
        Agent_Name = st.selectbox("Enter Agent Name:", dropdown,index=dropdown.index(selected_Name))
        

        # Team Leader (No validation)
        team_leader = st.text_input("Enter Team Leader Name:")

        # Audit Name (No validation)
        audit_name = st.text_input("Enter Audit Name:")

        # Auditor Center (List validation)
        auditor_center = st.selectbox("Select Auditor Center:",
                                      ["Indore", "Vijaywada", "Mysore", "Bhopal", "Noida", "Kolkata", "Coimbatore",
                                       "HYD", "Ranchi"])

        # Auditor Designation (List validation)
        auditor_designation = st.selectbox("Select Auditor Designation:", ["TL", "Trainer"])

    with col2:
        
        # User Register Number (Numeric validation)
        user_register_number = st.text_input("Enter User Register Number:")

        # Calling Number (Numeric validation)
        calling_number = st.text_input("Enter Calling Number:")

        # Date of Call (Date format validation)
        date_of_call = st.date_input("Enter Date of Call:")
        
        # Call Time Slot (Time format validation)
        call_time_slot = st.time_input("Enter Call Time Slot:")

        # Bucket (List format)
        bucket = st.selectbox("Select Bucket:", ["Bucket 1", "Bucket 2", "Bucket 3", "Bucket 4"])

        # Energetic Opening and Closing (Yes/No validation)
        energetic_opening_closing = st.selectbox("Energetic Opening and Closing?", ["Yes", "No"])

        # Motive of the Call (Yes/No validation)
        motive_of_call = st.selectbox("Motive of the Call?", ["Yes", "No"])

        # Probe / Confirm User's Profession (Yes/No validation)
        probe_confirm_user_profession = st.selectbox("Probe / Confirm User's Profession?", ["Yes", "No", "NA"])

        # Current Profile Stage / Previous Interaction
        Current_Profile_Stage_Previous_Interaction = st.selectbox("Current Profile Stage / Previous Interaction",
                                                                  ["Yes", "No", "FATAL"])

        Probe_If_User_have_any_doc_releated_Profession_Study_Business = st.selectbox(
            "Current Profile Stage / Previous Interaction", ["Yes", "No", "NA"])

        Guide_User_with_required_documents_One_by_one = st.selectbox("Current Profile Stage / Previous Interaction",
                                                                     ["Yes", "Fatal", "NA"])

        Urgency = st.selectbox("Urgency", ["Yes", "Fatal", "NA"])

        Objection_Handling = st.selectbox("Objection Handling", ["Yes", "Fatal", "NA"])



    # Section 2 (Right Column)
    with col3:
        Explained_user_how_to_take_first_loan = st.selectbox("Explained user how to take first loan",
                                                             ["Yes", "Fatal", "NA"])

        Reconfirmation_Call_back_script = st.selectbox("Reconfirmation / Call back script", ["Yes", "Fatal", "NA"])
        Energetic_Tone_and_Clear_articulation=st.selectbox("Energetic Tone and Clear articulation", ["Yes","No"])

        Two_way_communication = st.selectbox("Two way communication", ["Yes", "NO"])

        Active_listening_and_Dead_Air = st.selectbox("Active listening and Dead Air", ["Yes", "NO"])

        Professional_Communication = st.selectbox("Professional Communication", ["Yes", "NO"])

        Information = st.selectbox("Information", ["Yes", "NO"])

        Follow_Up = st.selectbox("Follow Up", ["Yes", "NO"])

        Tagging = st.selectbox("Tagging", ["Yes", "NA", "NO"])
        Benefits= st.selectbox("Tagging", ["Informed","Not Informed"])

        Fatal = st.selectbox("Fatal", ["Yes", "NO"])

        Remarks = st.text_input("Remarks:")

        Agent_Feedback_Status = st.selectbox("Agent Feedback Status", ["Closed", "Open"])


    with col4:
        Profile_completion_status_prior_to_call = st.selectbox("Profile completion status prior to call",
                                                               ["Blank profile", "Partially complete",
                                                                "Almost complete"])

        PIP_SFA_Status = st.selectbox("PIP/SFA Status", ["Correct", "Incorrect", "NA"])
        
        VOC = st.text_input("VOC")

        AOI = st.text_input("AOI")

        call_duration = st.text_input("Enter Call Duration (HH:mm:ss):")

        KYC_type = st.selectbox("KYC Type", ["Not Updated", "OKYC", "VKYC", "CKYC"])

        Disposition_Accuracy = st.selectbox("Disposition Accuracy", ["Correct", "Incorrect", "Not Done"])

        DCS_Tagging_L1 = st.text_input("Enter DCS Tagging L1")

        DCS_Tagging_L2 = st.text_input("Enter DCS Tagging L2")

        DCS_Tagging_L3 = st.text_input("Enter DCS Tagging L3")

        Actual_Tagging_L1 = st.text_input("Actual Tagging L1")

        Actual_Tagging_L2 = st.text_input("Actual Tagging L2")

        Actual_Tagging_L3 = st.text_input("Actual Tagging L3")

    # Add Row Button
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
