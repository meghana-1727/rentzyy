# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 00:56:14 2026

@author: Meghana
"""

import streamlit as st
from modifydb import add_user, get_user_by_mobile, add_item, get_items, add_request, get_requests_for_user, update_request_status, update_trust

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Rentzy", page_icon="🏠", layout="wide")

# ---------------- GLOBAL STYLES ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.main {
    background-color: #0e1117;
}
.big-title {
    font-size: 42px;
    font-weight: 800;
}
.sub-text {
    color: #9ca3af;
}
.card {
    background-color: #161b22;
    padding: 1.2rem;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.4);
    margin-bottom: 1rem;
    color: white;
}
.metric-card {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    padding: 1.4rem;
    border-radius: 18px;
    text-align: center;
    font-weight: 700;
}
.badge {
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    display: inline-block;
}
.badge-green {
    background-color: #065f46;
    color: #d1fae5;
}
.badge-yellow {
    background-color: #92400e;
    color: #fef3c7;
}
.badge-red {
    background-color: #991b1b;
    color: #fee2e2;
}
.action-btn > button {
    width: 100%;
    border-radius: 10px;
    font-weight: 600;
}
.filter-label {
    font-weight: 600;
    color: #e5e7eb;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

# ---------------- HOME PAGE ----------------
def home_page():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="big-title">🏠 Rentzy</div>', unsafe_allow_html=True)
        st.markdown("#### Rent Smarter. Earn Faster. Trust Better.")
        st.markdown('<p class="sub-text">A trust-powered peer-to-peer rental platform.</p>', unsafe_allow_html=True)

        st.markdown("### 🚀 Why Rentzy?")
        st.success("✔ Trust scores\n✔ Secure requests\n✔ Fast approvals\n✔ No middlemen")

        if st.button("🚀 Get Started"):
            st.session_state.page = "auth"
            st.rerun()

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3105/3105810.png", width=300)

# ---------------- AUTH PAGE ----------------
def auth_page():
    st.title("🔐 Login / Signup")

    role = st.radio("Choose role", ["Owner", "Consumer"], horizontal=True)
    name = st.text_input("Full Name")
    mobile = st.text_input("Mobile Number")
    email = st.text_input("Email")
    aadhar = st.text_input("Aadhar Number", type="password")

    if st.button("Continue"):
        if not all([name, mobile, email, aadhar]):
            st.error("Fill all fields")
            return
        if len(aadhar) != 12 or not aadhar.isdigit():
            st.error("Invalid Aadhar")
            return
        if len(mobile) != 10 or not mobile.isdigit():
            st.error("Invalid Mobile")
            return

        user = get_user_by_mobile(mobile)
        if not user:
            add_user(name, mobile, email, aadhar, role)
            user = get_user_by_mobile(mobile)

        st.session_state.user = user
        st.session_state.role = role
        st.session_state.page = "dashboard"
        st.success("Login successful!")
        st.rerun()

# ---------------- DASHBOARD ----------------
def dashboard_page():
    # -------- SIDEBAR --------
    with st.sidebar:
        st.markdown("## 🏠 Rentzy")
        st.markdown("---")
        st.markdown(f"### 👤 {st.session_state.user['name']}")
        st.metric("⭐ Trust Score", st.session_state.user['trust'])

        if st.session_state.user["trust"] >= 90:
            st.markdown('<span class="badge badge-green">Elite Trusted</span>', unsafe_allow_html=True)
        elif st.session_state.user["trust"] >= 70:
            st.markdown('<span class="badge badge-yellow">Verified</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge badge-red">Low Trust</span>', unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.page = "home"
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()

    # -------- MAIN HEADER --------
    st.markdown(f"## 👋 Welcome, {st.session_state.user['name']}")

    tabs = st.tabs(["🏠 Browse", "➕ Add Item", "📩 Requests", "👤 Profile"])

    # ---------------- BROWSE ----------------
    with tabs[0]:
        st.markdown("### 🔍 Available Items")

        locations = ["Hyderabad", "Bangalore", "Chennai", "Mumbai", "Delhi"]
        categories = ["Electronics", "Vehicles", "Furniture", "Tools", "Others"]

        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<span class="filter-label">📍 Location</span>', unsafe_allow_html=True)
            loc_filter = st.selectbox("", ["All"] + locations)
        with c2:
            st.markdown('<span class="filter-label">📦 Category</span>', unsafe_allow_html=True)
            cat_filter = st.selectbox("", ["All"] + categories)

        items = get_items()
        if loc_filter != "All":
            items = [i for i in items if i["location"] == loc_filter]
        if cat_filter != "All":
            items = [i for i in items if i["category"] == cat_filter]

        if not items:
            st.info("No items found")
        else:
            for item in items:
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <h4>{item['name']}</h4>
                        <p>📦 {item['category']} &nbsp;&nbsp; 📍 {item['location']}</p>
                        <p><b>₹{item['rent']}</b> / day</p>
                        <p>👤 Owner: {item['owner']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    if st.session_state.role == "Consumer":
                        if st.button("📩 Request Item", key=f"req_{item['id']}"):
                            success = add_request(item["id"], st.session_state.user["name"], item["owner"])
                            if success:
                                st.success("Request sent!")
                            else:
                                st.warning("Already requested!")

    # ---------------- ADD ITEM ----------------
    with tabs[1]:
        if st.session_state.role != "Owner":
            st.warning("Only owners can add items")
        else:
            st.markdown("### ➕ Add New Item")

            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                name = st.text_input("Item Name")
                category = st.selectbox("Category", ["Electronics", "Vehicles", "Furniture", "Tools", "Others"])
                location = st.selectbox("Location", ["Hyderabad", "Bangalore", "Chennai", "Mumbai", "Delhi"])
                rent = st.number_input("Rent per day", min_value=0, step=50)

                if st.button("✅ Add Item"):
                    if not all([name, category, location]):
                        st.error("Fill all fields")
                    else:
                        add_item(name, category, location, rent, st.session_state.user["name"])
                        st.success("Item added successfully!")
                st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- REQUESTS ----------------
    with tabs[2]:
        st.markdown("### 📩 Rental Requests")

        requests = get_requests_for_user(st.session_state.user["name"])
        if not requests:
            st.info("No requests yet")
        else:
            for r in requests:
                with st.container():
                    st.markdown(f"""
                    <div class="card">
                        <b>{r['name']}</b><br>
                        Consumer: {r['consumer']}<br>
                        Status: <b>{r['status']}</b>
                    </div>
                    """, unsafe_allow_html=True)

                    if r["owner"] == st.session_state.user["name"] and r["status"] == "Pending":
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Approve", key=f"app_{r['id']}"):
                                update_request_status(r["id"], "Approved")
                                update_trust(r["consumer"], +5)
                                update_trust(r["owner"], +3)
                                st.success("Approved!")
                                st.rerun()

                        with col2:
                            if st.button("❌ Reject", key=f"rej_{r['id']}"):
                                update_request_status(r["id"], "Rejected")
                                update_trust(r["consumer"], -5)
                                st.warning("Rejected")
                                st.rerun()

    # ---------------- PROFILE ----------------
    with tabs[3]:
        st.markdown("### 👤 Profile Overview")

        trust = st.session_state.user["trust"]

        st.markdown(f"""
        <div class="metric-card">
            ⭐ Trust Score<br>
            <span style="font-size:36px;">{trust}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if trust >= 90:
            st.success("🏆 Elite Trusted User")
        elif trust >= 70:
            st.info("✅ Verified User")
        else:
            st.warning("⚠️ Low Trust – Complete more rentals")

# ---------------- ROUTER ----------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "auth":
    auth_page()
else:
    dashboard_page()
