import streamlit as st
from utils.auth import init_session_state, login_user, signup_user
from utils.sidebar import render_sidebar
from views.admin_dashboard import render_admin_dashboard
from views.user_dashboard import render_user_dashboard

# Page configuration
st.set_page_config(
    page_title="Smart HSRP System",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

def render_login_page():
    """Render the login/signup page"""
    st.title("🔐 Welcome to Smart HSRP System")
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Signup"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_signup_form()

def render_login_form():
    """Render the login form"""
    st.subheader("Login to your account")
    
    with st.form("login_form", clear_on_submit=False):
        email = st.text_input(
            "Email", 
            placeholder="user@example.com", 
            key="login_email"
        )
        password = st.text_input(
            "Password", 
            type="password", 
            placeholder="Enter your password", 
            key="login_password"
        )
        submit = st.form_submit_button("🔑 Login", use_container_width=True)
    
    if submit:
        if email and password:
            with st.spinner("Logging in..."):
                success, message = login_user(email, password)
                if success:
                    st.success(message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.warning("Please fill in all fields")

def render_signup_form():
    """Render the signup form"""
    st.subheader("Create a new account")
    
    with st.form("signup_form", clear_on_submit=False):
        email = st.text_input(
            "Email", 
            placeholder="user@example.com", 
            key="signup_email"
        )
        password = st.text_input(
            "Password", 
            type="password", 
            placeholder="Create a password", 
            key="signup_password"
        )
        role = st.selectbox(
            "Role", 
            ["user", "admin"], 
            key="signup_role",
            help="Select 'admin' for full system access"
        )
        submit = st.form_submit_button("📝 Sign Up", use_container_width=True)
    
    if submit:
        if email and password:
            with st.spinner("Creating account..."):
                success, message = signup_user(email, password, role)
                if success:
                    st.success(message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)
        else:
            st.warning("Please fill in all fields")

def main():
    """Main application entry point"""
    # Initialize session state
    init_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Route to appropriate page based on login status and role
    if not st.session_state.logged_in:
        render_login_page()
    else:
        if st.session_state.user_role == 'admin':
            render_admin_dashboard()
        else:
            render_user_dashboard()

if __name__ == "__main__":
    main()