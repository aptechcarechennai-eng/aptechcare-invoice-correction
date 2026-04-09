import streamlit as st

def render():
    st.markdown('<p class="page-title">👥 Customers</p>', unsafe_allow_html=True)

    # Safe migration
    st.session_state.customers = [
        {"name":c,"email":"","phone":"","address":""} if isinstance(c,str) else c
        for c in st.session_state.customers
    ]
    customers = st.session_state.customers

    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("➕ Add Customer", type="primary", use_container_width=True):
            st.session_state.show_add_customer = True
            st.session_state.edit_customer_idx = None

    search   = st.text_input("🔍 Search", placeholder="Name or email...", label_visibility="collapsed")
    filtered = [c for c in customers if not search or search.lower() in c["name"].lower() or search.lower() in c.get("email","").lower()]

    for cust in filtered:
        real_idx = customers.index(cust)
        c1, c2, c3 = st.columns([4,1,1])
        with c1:
            invoices = [i for i in st.session_state.invoices if i["customer"] == cust["name"]]
            total    = sum(i["amount"] for i in invoices)
            st.markdown(f"""<div style="padding:6px 0;">
              <div style="font-weight:600;font-size:14px;color:#111827;">{cust['name']}</div>
              <div style="font-size:12px;color:#9CA3AF;">{cust.get('email','—')} &nbsp;•&nbsp; {cust.get('phone','—')} &nbsp;•&nbsp; {len(invoices)} invoices &nbsp;•&nbsp; ₹{total:,}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            if st.button("✏️ Edit", key=f"edit_cust_{real_idx}"):
                st.session_state.edit_customer_idx = real_idx
                st.session_state.show_add_customer = False
        with c3:
            if st.button("🗑️", key=f"del_cust_{real_idx}"):
                customers.pop(real_idx)
                st.rerun()
        st.markdown("<hr style='margin:4px 0;border-color:#F3F4F6;'>", unsafe_allow_html=True)

    # ── Edit Form ─────────────────────────────────────────────────
    edit_idx = st.session_state.get("edit_customer_idx")
    if edit_idx is not None and edit_idx < len(customers):
        cust = customers[edit_idx]
        st.markdown("---")
        st.markdown(f"### ✏️ Edit — {cust['name']}")
        with st.form("edit_customer_form"):
            c1, c2 = st.columns(2)
            with c1:
                name  = st.text_input("Name *",   value=cust.get("name",""))
                phone = st.text_input("Phone",     value=cust.get("phone",""))
            with c2:
                email   = st.text_input("Email",   value=cust.get("email",""))
                address = st.text_input("Address", value=cust.get("address",""))
            cs, cc = st.columns(2)
            with cs: save  = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
            with cc: close = st.form_submit_button("✕ Close", use_container_width=True)
            if save and name:
                customers[edit_idx] = {"name":name,"email":email,"phone":phone,"address":address}
                st.session_state.edit_customer_idx = None
                st.success(f"✅ '{name}' updated!")
                st.rerun()
            if close:
                st.session_state.edit_customer_idx = None
                st.rerun()

    # ── Add Form ──────────────────────────────────────────────────
    if st.session_state.get("show_add_customer"):
        st.markdown("---")
        st.markdown("### ➕ New Customer")
        with st.form("add_customer_form"):
            c1, c2 = st.columns(2)
            with c1:
                name  = st.text_input("Name *")
                phone = st.text_input("Phone")
            with c2:
                email   = st.text_input("Email")
                address = st.text_input("Address")
            cs, cc = st.columns(2)
            with cs: save  = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
            with cc: close = st.form_submit_button("✕ Close", use_container_width=True)
            if save and name:
                customers.append({"name":name,"email":email,"phone":phone,"address":address})
                st.session_state.show_add_customer = False
                st.success(f"✅ '{name}' added!")
                st.rerun()
            if close:
                st.session_state.show_add_customer = False
                st.rerun()
