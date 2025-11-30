import streamlit as st
import pandas as pd
import joblib
import json
from PIL import Image
import base64
import io


# Make text color black
# Force light theme and set text color to black
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    /* Main app text */
    .stApp, .stApp div, .stApp span, .stApp p, .stApp li, .stApp label {
        color: black !important;
    }
    /* Titles and headers */
    h1, h2, h3, h4, h5, h6 {
        color: black !important;
    }
    /* Sidebar text */
    section[data-testid="stSidebar"] div, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] label {
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ---- Function to add a PIL background image via base64 ----
def add_bg_with_pil(image_path):
    image = Image.open(image_path)
    # Ensure RGB and resize or convert if needed
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{img_b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ---------- Load saved objects ----------
@st.cache_resource
def load_artifacts():
    model = joblib.load("intrusion_model.pkl")
    label_encoders = joblib.load("label_encoder.pkl")
    feature_cols = joblib.load("feature_cols.pkl")
    with open("category_mappings.json", "r") as f:
        category_mappings = json.load(f)
    return model,label_encoders,feature_cols, category_mappings

model, label_encoders, feature_cols, category_mappings = load_artifacts()


# Add background image with PIL
add_bg_with_pil('cyber.png')  # Change to your image file name

st.title("Cybersecurity Intrusion Detection (No Scaling)")
st.write("Enter session details to predict whether it's an attack.")


#st.title("Cybersecurity Intrusion Detection")
#st.write("Predict whether a session is an attack using your trained ML model.")

# ---------- Build UI inputs ----------
col1, col2 = st.columns(2)

with col1:
    network_packet_size = st.number_input("Network packet size", min_value=0, max_value=2000, value=500)
    login_attempts = st.number_input("Login attempts", min_value=0, max_value=20, value=3)
    session_duration = st.number_input("Session duration (seconds)", min_value=0.0, max_value=10000.0, value=500.0, step=10.0)
    ip_reputation_score = st.slider("IP reputation score", 0.0, 1.0, 0.5, step=0.01)

with col2:
    failed_logins = st.number_input("Failed logins", min_value=0, max_value=20, value=1)
    unusual_time_access = st.selectbox("Unusual time access", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

    protocol_type = st.selectbox("Protocol type", category_mappings["protocol_type"])
    encryption_used = st.selectbox("Encryption used", category_mappings["encryption_used"])
    browser_type = st.selectbox("Browser type", category_mappings["browser_type"])

# ---------- Encode categoricals with saved LabelEncoders ----------
proto_enc = label_encoders["protocol_type"].transform([protocol_type])[0]
enc_enc = label_encoders["encryption_used"].transform([encryption_used])[0]
browser_enc = label_encoders["browser_type"].transform([browser_type])[0]

# ---------- Build single-row DataFrame ----------
row = {
    "network_packet_size": network_packet_size,
    "protocol_type": proto_enc,
    "login_attempts": login_attempts,
    "session_duration": session_duration,
    "encryption_used": enc_enc,
    "ip_reputation_score": ip_reputation_score,
    "failed_logins": failed_logins,
    "browser_type": browser_enc,
    "unusual_time_access": unusual_time_access,
}

X_input = pd.DataFrame([row])

# Ensure column order matches training
X_input = X_input[feature_cols]

st.subheader("Encoded input vector")
st.dataframe(X_input)

# ---------- Scale and predict (manually, no pipeline) ----------
if st.button("Predict attack"):
    # Scale with same scaler used in training
    
    prob = model.predict_proba(X_input)[0][1]
    pred = model.predict(X_input)[0]

    st.write(f"Attack probability: *{prob:.3f}*")
    if pred == 1:
        st.error("🚨 Model prediction: ATTACK DETECTED")
    else:
        st.success("✅ Model prediction: NO ATTACK")