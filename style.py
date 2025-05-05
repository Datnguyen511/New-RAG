def inject_custom_css():
    import streamlit as st
    st.markdown("""
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            color: #E6E6FA;
        }
        .stApp {
            background: linear-gradient(135deg, #0A0B1A, #1E1E3A);
        }
        h1 {
            color: #00D4FF;
            text-align: center;
        }
        .stChatMessage {
            background: #2A2A4A;
            border-radius: 12px;
            padding: 12px;
        }
        .stChatMessage:nth-child(odd) {
            background: #3A3A5A;
        }
    </style>
    """, unsafe_allow_html=True)
