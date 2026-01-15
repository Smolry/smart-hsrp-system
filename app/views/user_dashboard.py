import streamlit as st
from datetime import datetime

def render_user_dashboard():
    """Render the complete user dashboard"""
    st.title("👤 User Dashboard")
    
    # Top metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Role", "User")
    with col2:
        st.metric("User ID", st.session_state.user_id)
    with col3:
        st.metric("Status", "Active")
    
    st.divider()
    
    # Tabs for user sections
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "👤 Profile", "📚 Resources"])
    
    with tab1:
        render_overview_tab()
    
    with tab2:
        render_profile_tab()
    
    with tab3:
        render_resources_tab()

def render_overview_tab():
    """Render the overview tab"""
    st.subheader("Welcome to Smart HSRP System")
    st.info(f"Hello **{st.session_state.user_email}**! You're logged in as a regular user.")
    
    st.markdown("### Your Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Available Features")
        st.write("✅ View your account information")
        st.write("✅ Access user-specific features")
        st.write("✅ Manage your profile settings")
        st.write("✅ View system resources")
        st.write("✅ Update preferences")
    
    with col2:
        st.markdown("#### Quick Actions")
        if st.button("📝 Edit Profile", use_container_width=True):
            st.info("Profile editing feature - Coming soon!")
        
        if st.button("🔔 View Notifications", use_container_width=True):
            st.info("Notifications feature - Coming soon!")
        
        if st.button("📊 View Activity", use_container_width=True):
            st.info("Activity log feature - Coming soon!")
    
    st.divider()
    st.success("All systems operational!")

def render_profile_tab():
    """Render the profile tab"""
    st.subheader("Profile Information")
    
    with st.container():
        st.markdown("### Account Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Personal Information**")
            st.write(f"📧 Email: {st.session_state.user_email}")
            st.write(f"🆔 User ID: {st.session_state.user_id}")
            st.write(f"🎭 Role: {st.session_state.user_role.capitalize()}")
        
        with col2:
            st.markdown("**Session Information**")
            st.write(f"🕒 Session Active: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"🔐 Authentication: JWT Token")
            st.write(f"✅ Status: Active")
    
    st.divider()
    
    st.markdown("### Security")
    st.info("Your account is secured with encrypted authentication tokens and bcrypt password hashing.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Security Features**")
        st.write("🔒 Password hashing: bcrypt")
        st.write("🔑 Token-based authentication")
        st.write("⏱️ Session timeout: 30 minutes")
    
    with col2:
        st.markdown("**Account Actions**")
        if st.button("🔄 Change Password", use_container_width=True):
            st.info("Password change feature - Coming soon!")
        
        if st.button("🔐 Security Settings", use_container_width=True):
            st.info("Security settings - Coming soon!")

def render_resources_tab():
    """Render the resources tab"""
    st.subheader("Resources & Help")
    
    st.markdown("### Getting Started")
    
    with st.expander("📖 How to use the system", expanded=True):
        st.write("""
        Welcome to the Smart HSRP System! Here's how to get started:
        
        1. **Dashboard**: View your account overview and quick stats
        2. **Profile**: Manage your account information and settings
        3. **Resources**: Access help documentation and guides
        4. **Logout**: Use the sidebar to safely log out of your account
        """)
    
    with st.expander("❓ Frequently Asked Questions"):
        st.write("""
        **Q: How do I change my password?**
        A: Go to the Profile tab and click on "Change Password" button.
        
        **Q: How long does my session last?**
        A: Sessions are valid for 30 minutes of inactivity.
        
        **Q: Can I upgrade to an admin account?**
        A: Please contact your system administrator for role changes.
        
        **Q: How do I report an issue?**
        A: Contact your system administrator or IT support team.
        """)
    
    with st.expander("🔧 System Information"):
        st.write("""
        **System Version**: 1.0.0
        **Last Updated**: January 2026
        **API Status**: Online ✅
        **Database**: PostgreSQL
        """)
    
    st.divider()
    
    st.markdown("### Need Help?")
    st.info("If you need assistance, please contact your system administrator.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Support Options**")
        st.write("📧 Email: support@example.com")
        st.write("📞 Phone: +1 (555) 123-4567")
    
    with col2:
        st.markdown("**Quick Links**")
        st.write("📚 [Documentation](#)")
        st.write("💬 [Community Forum](#)")
        st.write("🐛 [Report Bug](#)")