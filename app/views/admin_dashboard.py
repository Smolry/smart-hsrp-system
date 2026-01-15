import streamlit as st
from datetime import datetime
from utils.auth import get_all_users

def render_admin_dashboard():
    """Render the complete admin dashboard"""
    st.title("🛡️ Admin Dashboard")
    
    # Top metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Role", "Administrator")
    with col2:
        st.metric("User ID", st.session_state.user_id)
    with col3:
        st.metric("Status", "Active")
    
    st.divider()
    
    # Tabs for different admin sections
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "👥 User Management", "⚙️ Settings"])
    
    with tab1:
        render_overview_tab()
    
    with tab2:
        render_user_management_tab()
    
    with tab3:
        render_settings_tab()

def render_overview_tab():
    """Render the overview tab with statistics"""
    st.subheader("System Overview")
    st.info("Welcome to the Smart HSRP Admin Dashboard. You have full access to all system features.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Quick Stats")
        users = get_all_users()
        total_users = len(users)
        admin_count = sum(1 for u in users if u.get('role') == 'admin')
        user_count = sum(1 for u in users if u.get('role') == 'user')
        
        st.metric("Total Users", total_users)
        st.metric("Admins", admin_count)
        st.metric("Regular Users", user_count)
    
    with col2:
        st.markdown("### Recent Activity")
        st.write("System running smoothly ✅")
        st.write(f"Last login: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"Active session for: {st.session_state.user_email}")

def render_user_management_tab():
    """Render the user management tab"""
    st.subheader("User Management")
    
    # Fetch and display all users
    users = get_all_users()
    
    if users:
        st.markdown(f"**Total Users: {len(users)}**")
        st.divider()
        
        # Display users in a structured format
        for user in users:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                
                with col1:
                    st.write(f"📧 **{user.get('email', 'N/A')}**")
                
                with col2:
                    role = user.get('role', 'unknown')
                    role_badge = "🛡️ Admin" if role == 'admin' else "👤 User"
                    st.write(role_badge)
                
                with col3:
                    st.write(f"ID: {user.get('id', 'N/A')}")
                
                with col4:
                    created = user.get('created_at', 'N/A')
                    if isinstance(created, str):
                        created = created.split('T')[0]
                    st.write(f"📅 {created}")
                
                st.divider()
    else:
        st.warning("No users found in the system.")
    
    # Add user statistics
    if users:
        st.markdown("### User Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            admin_percentage = (sum(1 for u in users if u.get('role') == 'admin') / len(users)) * 100
            st.metric("Admin %", f"{admin_percentage:.1f}%")
        
        with col2:
            user_percentage = (sum(1 for u in users if u.get('role') == 'user') / len(users)) * 100
            st.metric("User %", f"{user_percentage:.1f}%")
        
        with col3:
            st.metric("Total Accounts", len(users))

def render_settings_tab():
    """Render the settings tab"""
    st.subheader("System Settings")
    st.info("Configuration options for system administrators")
    
    with st.expander("🔐 Security Settings", expanded=True):
        st.write("**Authentication Configuration**")
        st.write("- Token expiration: 30 minutes")
        st.write("- Password hashing: bcrypt")
        st.write("- JWT Algorithm: HS256")
        st.write("- CORS: Enabled")
    
    with st.expander("📝 Database Settings"):
        st.write("**Database Information**")
        st.write("- Database: PostgreSQL")
        st.write("- Table: users")
        st.write("- Connection: Active ✅")
        st.write("- Host: localhost")
    
    with st.expander("🌐 API Settings"):
        st.write("**API Configuration**")
        st.write("- Base URL: http://localhost:8000")
        st.write("- Status: Online ✅")
        st.write("- Endpoints: /signup, /login, /users, /verify-token")
    
    with st.expander("👤 User Preferences"):
        st.write("**Admin Account Settings**")
        st.write(f"- Email: {st.session_state.user_email}")
        st.write(f"- User ID: {st.session_state.user_id}")
        st.write(f"- Role: {st.session_state.user_role}")
        st.write("- Status: Active")