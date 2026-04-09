import streamlit as st

def render():
    invoices = st.session_state.invoices
    settings = st.session_state.settings

    # ── Header ────────────────────────────────────────────────────
    st.markdown("""
    <p class="page-title">Dashboard</p>
    <p class="page-sub">AP Tech Care — Smart Tech Solutions</p>
    """, unsafe_allow_html=True)

    # ── Stats ─────────────────────────────────────────────────────
    total       = len(invoices)
    paid_amt    = sum(i["amount"] for i in invoices if i["status"] == "paid")
    pending_amt = sum(i["amount"] for i in invoices if i["status"] != "paid")
    overdue_n   = len([i for i in invoices if i["status"] == "overdue"])

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Invoices", total)
    with c2: st.metric("Collected",  f"₹{paid_amt/1000:.1f}K")
    with c3: st.metric("Outstanding", f"₹{pending_amt/1000:.1f}K")
    with c4: st.metric("Overdue",    overdue_n)

    st.markdown("<div class='ap-divider'></div>", unsafe_allow_html=True)

    # ── Quick Actions ─────────────────────────────────────────────
    st.markdown("<p style='font-size:13px;font-weight:600;color:#6B7280;margin-bottom:10px;'>QUICK ACTIONS</p>", unsafe_allow_html=True)

    q1, q2, q3, q4, q5, q6 = st.columns(6)
    actions = [
        (q1, "invoice",  "📄", "Invoice"),
        (q2, "estimate", "📋", "Estimate"),
        (q3, "credit",   "💳", "Credit Note"),
        (q4, "delivery", "🚚", "Delivery"),
        (q5, "purchase", "🛒", "Purchase"),
        (q6, "cashflow", "📊", "Cash Flow"),
    ]
    for col, pid, icon, label in actions:
        with col:
            if st.button(f"{icon}\n\n{label}", key=f"qa_{pid}", use_container_width=True):
                st.session_state.page = pid
                st.rerun()

    st.markdown("<div class='ap-divider'></div>", unsafe_allow_html=True)

    # ── Main content: Pending + Summary ──────────────────────────
    left, right = st.columns([2, 1])

    with left:
        st.markdown("<p style='font-size:14px;font-weight:600;color:#111827;margin-bottom:12px;'>Unpaid Invoices</p>", unsafe_allow_html=True)

        pending = [i for i in invoices if i["status"] != "paid"]
        if not pending:
            st.markdown("""
            <div class="ap-card" style="text-align:center;padding:32px;color:#9CA3AF;">
              ✅ All invoices are paid!
            </div>""", unsafe_allow_html=True)
        else:
            for inv in pending[:5]:
                is_overdue = inv["status"] == "overdue"
                badge_colors = {
                    "overdue": ("#FEE2E2","#991B1B"),
                    "sent":    ("#DBEAFE","#1E40AF"),
                    "draft":   ("#F3F4F6","#6B7280"),
                    "read":    ("#FEF9C3","#854D0E"),
                }
                bg, fg = badge_colors.get(inv["status"], ("#F3F4F6","#6B7280"))

                cl, cr = st.columns([3, 1])
                with cl:
                    overdue_label = '<span style="font-size:11px;color:#EF4444;font-weight:600;">● Overdue</span>' if is_overdue else ""
                    st.markdown(f"""
                    <div class="ap-card" style="margin-bottom:6px;">
                      <div style="font-weight:600;font-size:14px;color:#111827;">{inv['customer']}</div>
                      <div style="font-size:12px;color:#9CA3AF;margin-top:2px;">{inv['id']} &nbsp;•&nbsp; Due: {inv['due']}</div>
                      {overdue_label}
                    </div>""", unsafe_allow_html=True)
                with cr:
                    st.markdown(f"""
                    <div class="ap-card" style="margin-bottom:6px;text-align:right;">
                      <div style="font-weight:700;font-size:14px;color:#111827;">₹{inv['amount']:,.0f}</div>
                      <span style="background:{bg};color:{fg};padding:2px 8px;border-radius:20px;font-size:11px;font-weight:600;">{inv['status'].title()}</span>
                    </div>""", unsafe_allow_html=True)

        if st.button("View All Invoices →", key="home_view_all"):
            st.session_state.page = "invoice"
            st.rerun()

    with right:
        st.markdown("<p style='font-size:14px;font-weight:600;color:#111827;margin-bottom:12px;'>Summary</p>", unsafe_allow_html=True)

        # Status counts
        statuses = {}
        for inv in invoices:
            statuses[inv["status"]] = statuses.get(inv["status"], 0) + 1

        status_colors = {"paid":"#166534","sent":"#1E40AF","overdue":"#991B1B","draft":"#6B7280","read":"#854D0E"}
        for status, count in statuses.items():
            color = status_colors.get(status, "#6B7280")
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:10px 14px;background:#fff;border:1px solid #E8EAED;
                        border-radius:10px;margin-bottom:6px;">
              <span style="font-size:13px;color:#374151;">{status.title()}</span>
              <span style="font-weight:700;font-size:13px;color:{color};">{count}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div class='ap-divider'></div>", unsafe_allow_html=True)

        # Customers & Items count
        cust_count  = len(st.session_state.customers)
        items_count = len(st.session_state.items_db)

        st.markdown(f"""
        <div style="display:flex;flex-direction:column;gap:6px;">
          <div style="display:flex;justify-content:space-between;padding:10px 14px;background:#EEF2FF;border-radius:10px;">
            <span style="font-size:13px;color:#374151;">👥 Customers</span>
            <span style="font-weight:700;font-size:13px;color:#4F46E5;">{cust_count}</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding:10px 14px;background:#F0FDF4;border-radius:10px;">
            <span style="font-size:13px;color:#374151;">📦 Items</span>
            <span style="font-weight:700;font-size:13px;color:#166534;">{items_count}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div class='ap-divider'></div>", unsafe_allow_html=True)
        if st.button("➕ New Customer", use_container_width=True, key="home_add_cust"):
            st.session_state.page = "customers"
            st.rerun()
        if st.button("➕ New Item", use_container_width=True, key="home_add_item"):
            st.session_state.page = "items"
            st.rerun()
