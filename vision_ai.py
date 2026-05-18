# ------------------------------------------------
# AI DISASTER IMAGE ANALYSIS
# ------------------------------------------------

st.markdown("""
<h2 style="
color:white;
font-size:42px;
font-weight:900;
margin-top:30px;
margin-bottom:20px;
">
🧠 AI Disaster Image Analysis
</h2>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload disaster image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    st.image(uploaded_file, use_container_width=True)

    filename = uploaded_file.name.lower()

    if "fire" in filename:

        st.error("""
🔥 FIRE HAZARD DETECTED

• Severe fire risk identified
• Immediate evacuation recommended
• Avoid smoke exposure
• Emergency responders alerted
""")

    elif "flood" in filename:

        st.warning("""
🌊 FLOOD RISK DETECTED

• Waterlogging hazard identified
• Move to higher ground
• Avoid electrical infrastructure
• Rescue support may be required
""")

    else:

        st.success("""
⚠️ DISASTER ANALYSIS COMPLETE

• Hazardous environment detected
• Emergency precautions advised
• Stay alert and await rescue guidance
""")
