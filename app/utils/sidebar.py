import streamlit as st
from utils.auth import logout_user

def render_sidebar():
    """Render the sidebar with navigation and user info"""
    with st.sidebar:
        st.title("🔐 Smart HSRP System")
        
        if st.session_state.logged_in:
            render_logged_in_sidebar()
        else:
            render_logged_out_sidebar()

def render_logged_in_sidebar():
    """Render sidebar for logged-in users"""
    st.success(f"Logged in as: **{st.session_state.user_email}**")
    st.info(f"Role: **{st.session_state.user_role.upper()}**")
    
    st.divider()
    
    if st.session_state.user_role == 'admin':
        render_admin_menu()
    else:
        render_user_menu()
    
    st.divider()
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True, type="primary"):
        logout_user()
        st.rerun()

def render_admin_menu():
    """Render admin-specific menu"""
    st.markdown("### 🛡️ Admin Menu")
    st.markdown("""
    **Navigation**
    - 📊 Dashboard Overview
    - 👥 User Management
    - ⚙️ System Settings
    
    **Quick Actions**
    - View all users
    - Monitor system health
    - Configure settings
    """)

def render_user_menu():
    """Render user-specific menu"""
    st.markdown("### 👤 User Menu")
    st.markdown("""
    **Navigation**
    - 📊 Dashboard Overview
    - 👤 My Profile
    - 📚 Resources & Help
    
    **Quick Actions**
    - View profile
    - Update settings
    - Access resources
    """)

def render_logged_out_sidebar():
    """Render sidebar for logged-out users"""
    st.info("Please login or signup to continue")
    
    st.divider()
    
    st.markdown("### 📋 Features")
    st.markdown("""
    - 🔐 Secure authentication
    - 🛡️ Role-based access control
    - 👥 User management (Admin)
    - 📊 Personal dashboard
    - ⚙️ Profile settings
    """)
    
    st.divider()
    
    st.markdown("### ℹ️ About")
    st.write("Smart HSRP System v1.0")
    st.write("Secure RBAC Authentication")