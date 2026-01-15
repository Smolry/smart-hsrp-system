import requests
import streamlit as st

# Configuration
API_BASE_URL = "http://localhost:8000"

def login_user(email, password):
    """Authenticate user and store session data"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.logged_in = True
            st.session_state.user_email = data['email']
            st.session_state.user_role = data['role']
            st.session_state.token = data['access_token']
            st.session_state.user_id = data['user_id']
            return True, "Login successful!"
        else:
            return False, response.json().get('detail', 'Login failed')
    except Exception as e:
        return False, f"Error: {str(e)}"

def signup_user(email, password, role):
    """Register new user and store session data"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/signup",
            json={"email": email, "password": password, "role": role}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.logged_in = True
            st.session_state.user_email = data['email']
            st.session_state.user_role = data['role']
            st.session_state.token = data['access_token']
            st.session_state.user_id = data['user_id']
            return True, "Signup successful!"
        else:
            return False, response.json().get('detail', 'Signup failed')
    except Exception as e:
        return False, f"Error: {str(e)}"

def logout_user():
    """Clear session data"""
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_role = None
    st.session_state.token = None
    st.session_state.user_id = None

def get_all_users():
    """Fetch all users (admin only)"""
    try:
        response = requests.get(
            f"{API_BASE_URL}/users",
            params={"token": st.session_state.token}
        )
        if response.status_code == 200:
            return response.json().get('users', [])
        return []
    except Exception as e:
        st.error(f"Error fetching users: {str(e)}")
        return []

def init_session_state():
    """Initialize session state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'token' not in st.session_state:
        st.session_state.token = None
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None