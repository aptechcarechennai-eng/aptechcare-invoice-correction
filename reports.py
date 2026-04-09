import streamlit as st
from datetime import datetime

def render():
    st.markdown('<p class="page-title">📈 Reports</p>', unsafe_allow_html=True)

    invoices = st.session_state.invoices
    tab1, tab2 = st.tabs(["📅 Monthly Report", "📊 Summary"])

    with tab1:
        months = {}
        for inv in invoices:
            try:
                m = datetime.strptime(inv["date"], "%Y-%m-%d").strftime("%b %Y")
                months.setdefault(m, {"total": 0, "paid": 0, "count": 0})
                months[m]["total"] += inv["amount"]
                months[m]["count"] += 1
                if inv["status"] == "paid":
                    months[m]["paid"] += inv["amount"]
            except:
                pass

        for month, data in months.items():
            st.markdown(f"""
            <div class="ap-card">
              <div style="font-weight:800;font-size:16px;margin-bottom:8px;">📅 {month}</div>
              <div style="display:flex;gap:24px;">
                <div><span style="font-size:12px;color:#6b7280;">Invoices</span><br><span style="font-weight:700;">{data['count']}</span></div>
                <div><span style="font-size:12px;color:#6b7280;">Total</span><br><span style="font-weight:700;">₹{data['total']:,}</span></div>
                <div><span style="font-size:12px;color:#6b7280;">Collected</span><br><span style="font-weight:700;color:#10B981;">₹{data['paid']:,}</span></div>
                <div><span style="font-size:12px;color:#6b7280;">Pending</span><br><span style="font-weight:700;color:#EF4444;">₹{data['total']-data['paid']:,}</span></div>
              </div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        total = sum(i["amount"] for i in invoices)
        collected = sum(i["amount"] for i in invoices if i["status"] == "paid")
        st.metric("Total Billed", f"₹{total:,}")
        st.metric("Collected", f"₹{collected:,}")
        st.metric("Outstanding", f"₹{total-collected:,}")
        top_customer = max(invoices, key=lambda x: x["amount"], default=None)
        if top_customer:
            st.metric("Top Customer", top_customer["customer"])
