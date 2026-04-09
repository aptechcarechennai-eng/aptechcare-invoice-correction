import streamlit as st

# ── CASHFLOW ──────────────────────────────────────────────────────
def render():
    st.markdown('<p class="page-title">📊 Cash Flow</p>', unsafe_allow_html=True)

    invoices = st.session_state.invoices
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🏦 Accounts", "💸 Transactions", "📅 Calendar"])

    with tab1:
        total_in  = sum(i["amount"] for i in invoices if i["status"] == "paid")
        total_out = st.session_state.get("total_expenses", 45000)
        net = total_in - total_out

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div style="background:#D1FAE5;border-radius:14px;padding:20px;">
              <p style="margin:0;font-size:12px;font-weight:700;color:#065F46;">💰 Total Income</p>
              <p style="margin:8px 0 0;font-size:26px;font-weight:900;color:#065F46;">₹{total_in:,.0f}</p>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#FEE2E2;border-radius:14px;padding:20px;">
              <p style="margin:0;font-size:12px;font-weight:700;color:#991B1B;">💸 Total Expense</p>
              <p style="margin:8px 0 0;font-size:26px;font-weight:900;color:#991B1B;">₹{total_out:,.0f}</p>
            </div>""", unsafe_allow_html=True)
        with c3:
            color = "#065F46" if net >= 0 else "#991B1B"
            bg = "#D1FAE5" if net >= 0 else "#FEE2E2"
            st.markdown(f"""
            <div style="background:{bg};border-radius:14px;padding:20px;">
              <p style="margin:0;font-size:12px;font-weight:700;color:{color};">📈 Net Balance</p>
              <p style="margin:8px 0 0;font-size:26px;font-weight:900;color:{color};">₹{net:,.0f}</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Recent Paid Invoices**")
        paid = [i for i in invoices if i["status"] == "paid"]
        for inv in paid[:5]:
            st.markdown(f"""
            <div class="ap-card" style="display:flex;justify-content:space-between;margin-bottom:8px;">
              <div>
                <div style="font-weight:700;">{inv['customer']}</div>
                <div style="font-size:12px;color:#6b7280;">{inv['id']} • {inv['date']}</div>
              </div>
              <div style="font-weight:900;color:#10B981;font-size:16px;">+₹{inv['amount']:,.0f}</div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        accounts = st.session_state.settings.get("accounts", ["Cash", "G.M. Account", "Savings Account"])
        for acc in accounts:
            st.markdown(f"""
            <div class="ap-card" style="display:flex;justify-content:space-between;align-items:center;">
              <span style="font-weight:600;">💰 {acc}</span>
              <span style="font-weight:700;color:#00C896;">₹0</span>
            </div>""", unsafe_allow_html=True)

    with tab3:
        txns = st.session_state.get("transactions", [])
        if st.button("➕ Add Transaction", type="primary"):
            with st.form("add_txn"):
                c1, c2 = st.columns(2)
                with c1:
                    txn_type = st.selectbox("Type", ["Income", "Expense"])
                    amount = st.number_input("Amount ₹", min_value=0)
                with c2:
                    desc = st.text_input("Description")
                    acct = st.selectbox("Account", st.session_state.settings.get("accounts", ["Cash"]))
                if st.form_submit_button("Save Transaction"):
                    txns.append({"type": txn_type, "amount": amount, "desc": desc, "account": acct})
                    st.session_state.transactions = txns
                    st.rerun()
        if txns:
            for t in txns[-10:]:
                color = "#10B981" if t["type"] == "Income" else "#EF4444"
                sign = "+" if t["type"] == "Income" else "-"
                st.markdown(f"""
                <div class="ap-card" style="display:flex;justify-content:space-between;">
                  <div>
                    <div style="font-weight:600;">{t['desc']}</div>
                    <div style="font-size:12px;color:#6b7280;">{t['account']}</div>
                  </div>
                  <div style="font-weight:700;color:{color};">{sign}₹{t['amount']:,}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No transactions yet.")

    with tab4:
        st.info("📅 Calendar view coming soon!")
