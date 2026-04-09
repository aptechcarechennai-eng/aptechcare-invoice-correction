import streamlit as st
from datetime import datetime, timedelta, date
import io

DOC_LABELS = {
    "invoice":  {"title": "Invoices",        "icon": "📄", "header": "INVOICE",        "color": "#0F1923"},
    "estimate": {"title": "Estimates",        "icon": "📋", "header": "ESTIMATE",       "color": "#1E40AF"},
    "credit":   {"title": "Credit Notes",     "icon": "💳", "header": "CREDIT NOTE",    "color": "#7C3AED"},
    "delivery": {"title": "Delivery Notes",   "icon": "🚚", "header": "DELIVERY NOTE",  "color": "#065F46"},
    "purchase": {"title": "Purchase Orders",  "icon": "🛒", "header": "PURCHASE ORDER", "color": "#92400E"},
}

def get_docs(doc_type):
    return [i for i in st.session_state.invoices if i.get("type", "invoice") == doc_type]

def next_id(doc_type):
    prefixes = {"invoice": "AP", "estimate": "EST", "credit": "CN", "delivery": "DN", "purchase": "PO"}
    prefix = prefixes.get(doc_type, "AP")
    n = st.session_state.settings.get("next_invoice_no", 1001)
    return f"{prefix}-{n}"

def render(doc_type="invoice"):
    cfg = DOC_LABELS[doc_type]
    docs = get_docs(doc_type)

    # ── Header ────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f'<p class="page-title">{cfg["icon"]} {cfg["title"]}</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="page-sub">{len(docs)} total {cfg["title"].lower()}</p>', unsafe_allow_html=True)
    with col2:
        if st.button(f'➕ Create {cfg["title"][:-1]}', type="primary", use_container_width=True):
            st.session_state.show_new_invoice = True
            st.session_state.doc_type = doc_type

    # ── Filter Tabs ───────────────────────────────────────────────
    tabs = st.tabs(["All", "Draft", "Sent", "Read", "Paid", "Overdue"])
    filters = ["all", "draft", "sent", "read", "paid", "overdue"]

    for tab, flt in zip(tabs, filters):
        with tab:
            filtered = docs if flt == "all" else [d for d in docs if d["status"] == flt]

            # Search
            search = st.text_input("🔍 Search", placeholder=f"Search {cfg['title'].lower()}...", key=f"search_{doc_type}_{flt}", label_visibility="collapsed")
            if search:
                filtered = [d for d in filtered if search.lower() in d["customer"].lower() or search.lower() in d["id"].lower()]

            if not filtered:
                st.markdown(f'<div class="ap-card" style="text-align:center;padding:40px;color:#6b7280;">No {cfg["title"].lower()} found</div>', unsafe_allow_html=True)
            else:
                for doc in filtered:
                    _render_doc_row(doc, cfg, flt)

    # ── New Doc Modal ─────────────────────────────────────────────
    if st.session_state.get("show_new_invoice") and st.session_state.get("doc_type") == doc_type:
        _render_new_form(doc_type, cfg)

    # ── View/Print Modal ──────────────────────────────────────────
    if st.session_state.get("selected_invoice"):
        _render_print_view(st.session_state.selected_invoice, cfg)


def _render_doc_row(doc, cfg, flt="all"):
    col1, col2, col3 = st.columns([4, 2, 1])
    with col1:
        st.markdown(f"""
        <div style="padding:4px 0;">
          <div style="font-weight:700;font-size:14px;">{doc['customer']}</div>
          <div style="font-size:12px;color:#6b7280;">{doc['id']} • {doc['date']} • Due: {doc['due']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style="padding:4px 0;text-align:right;">
          <div style="font-weight:800;font-size:15px;">₹{doc['amount']:,.0f}</div>
          <span class="badge-{doc['status']}">{doc['status'].title()}</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if st.button("👁 View", key=f"view_{flt}_{doc['id']}", use_container_width=True):
            st.session_state.selected_invoice = doc
            st.rerun()
    st.markdown("<hr style='margin:4px 0;border-color:#f3f4f6;'>", unsafe_allow_html=True)


def _render_new_form(doc_type, cfg):
    st.markdown("---")
    st.markdown(f"### ➕ New {cfg['title'][:-1]}")

    with st.form(key=f"new_{doc_type}_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            cust_names = [c["name"] if isinstance(c, dict) else c for c in st.session_state.customers]
            customer = st.selectbox("Customer *", cust_names + ["+ Add New Customer"])
        with col2:
            inv_no = st.text_input("Document #", value=next_id(doc_type))
        with col3:
            inv_date = st.date_input("Date", value=date.today())

        col4, col5 = st.columns(2)
        with col4:
            due_date = st.date_input("Due Date", value=date.today() + timedelta(days=15))
        with col5:
            status = st.selectbox("Status", ["draft", "sent", "read", "paid"])

        st.markdown("**Items**")

        # Item rows - up to 10
        item_rows = st.session_state.get(f"item_rows_{doc_type}", 1)
        items = []
        item_names = [i["name"] for i in st.session_state.items_db]

        for i in range(item_rows):
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1:
                name = st.selectbox(f"Item {i+1}", [""] + item_names, key=f"item_name_{doc_type}_{i}")
            with c2:
                qty = st.number_input("Qty", min_value=1, value=1, key=f"item_qty_{doc_type}_{i}")
            with c3:
                # Auto-fill price
                default_price = 0
                if name:
                    found = next((x for x in st.session_state.items_db if x["name"] == name), None)
                    if found: default_price = found["price"]
                price = st.number_input("Price ₹", min_value=0, value=default_price, key=f"item_price_{doc_type}_{i}")
            with c4:
                amt = qty * price
                st.markdown(f"<div style='padding-top:28px;font-weight:700;color:#00C896;'>₹{amt:,}</div>", unsafe_allow_html=True)
            if name:
                items.append({"name": name, "qty": qty, "price": price, "amount": amt})

        subtotal = sum(x["amount"] for x in items)
        tax_rate = st.session_state.settings.get("tax_rate", 18)
        tax = int(subtotal * tax_rate / 100)
        total = subtotal + tax

        # Totals display
        st.markdown(f"""
        <div style="background:#f8f9fa;border-radius:10px;padding:14px 18px;margin:10px 0;">
          <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
            <span style="color:#6b7280;font-size:13px;">Subtotal</span>
            <span style="font-weight:600;">₹{subtotal:,}</span>
          </div>
          <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
            <span style="color:#6b7280;font-size:13px;">GST ({tax_rate}%)</span>
            <span style="font-weight:600;">₹{tax:,}</span>
          </div>
          <div style="display:flex;justify-content:space-between;padding-top:8px;border-top:2px solid #e5e7eb;">
            <span style="font-weight:800;font-size:16px;">Total</span>
            <span style="font-weight:900;font-size:18px;color:#00C896;">₹{total:,}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

        c_save, c_add, c_cancel = st.columns([2, 1, 1])
        with c_save:
            save = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
        with c_add:
            add_row = st.form_submit_button("➕ Row", use_container_width=True)
        with c_cancel:
            cancel = st.form_submit_button("✕ Cancel", use_container_width=True)

        if save and customer and customer != "+ Add New Customer":
            new_doc = {
                "id": inv_no,
                "type": doc_type,
                "customer": customer,
                "date": str(inv_date),
                "due": str(due_date),
                "amount": total,
                "status": status,
                "items": items,
                "subtotal": subtotal,
                "tax": tax,
            }
            st.session_state.invoices.insert(0, new_doc)
            st.session_state.settings["next_invoice_no"] = st.session_state.settings.get("next_invoice_no", 1001) + 1
            st.session_state.show_new_invoice = False
            st.session_state[f"item_rows_{doc_type}"] = 1
            st.success(f"✅ {cfg['title'][:-1]} {inv_no} saved!")
            st.rerun()

        if add_row:
            st.session_state[f"item_rows_{doc_type}"] = item_rows + 1
            st.rerun()

        if cancel:
            st.session_state.show_new_invoice = False
            st.session_state[f"item_rows_{doc_type}"] = 1
            st.rerun()


def _render_print_view(doc, cfg):
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back to List", key="print_back"):
            st.session_state.selected_invoice = None
            st.rerun()
    with col3:
        # PDF download button placeholder
        st.button("🖨️ Print / PDF", key="print_btn")

    s = st.session_state.settings
    items = doc.get("items", [])
    subtotal = doc.get("subtotal", sum(i.get("amount", 0) for i in items))
    tax_rate = s.get("tax_rate", 18)
    tax = doc.get("tax", int(subtotal * tax_rate / 100))
    total = doc.get("amount", subtotal + tax)

    # ── Invoice HTML Preview ──────────────────────────────────────
    items_html = ""
    for idx, item in enumerate(items, 1):
        items_html += f"""
        <tr style="background:{'#ffffff' if idx%2==0 else '#f8f9fa'}">
          <td style="padding:10px 14px;color:#6b7280;font-size:13px;">{idx}</td>
          <td style="padding:10px 14px;font-weight:600;font-size:14px;">{item.get('name','')}</td>
          <td style="padding:10px 14px;text-align:center;font-size:13px;">{item.get('qty',1)}</td>
          <td style="padding:10px 14px;text-align:right;font-size:13px;">₹{item.get('price',0):,}</td>
          <td style="padding:10px 14px;text-align:right;font-size:14px;font-weight:700;">₹{item.get('amount',0):,}</td>
        </tr>
        """

    if not items_html:
        items_html = '<tr><td colspan="5" style="padding:20px;text-align:center;color:#9ca3af;">No items</td></tr>'

    invoice_html = f"""
    <div style="max-width:680px;margin:0 auto;background:#fff;border-radius:16px;box-shadow:0 4px 24px rgba(0,0,0,0.08);overflow:hidden;">
      <!-- Header -->
      <div style="padding:36px 40px 28px;border-bottom:2px solid #f3f4f6;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;">
          <div>
            <div style="width:56px;height:56px;border-radius:12px;background:#0F1923;display:flex;align-items:center;justify-content:center;margin-bottom:12px;">
              <span style="color:#00C896;font-weight:900;font-size:14px;letter-spacing:0.5px;">AP</span>
            </div>
            <div style="font-weight:800;font-size:20px;color:#0F1923;">{s.get('company_name','AP Tech Care')}</div>
            <div style="font-size:12px;color:#6b7280;margin-top:2px;">Smart Tech Solutions</div>
            <div style="font-size:12px;color:#6b7280;">{s.get('company_address1','Chennai, Tamil Nadu')}</div>
            <div style="font-size:12px;color:#6b7280;">GST: {s.get('gst_no','33XXXXX1234Z1')}</div>
          </div>
          <div style="text-align:right;">
            <div style="font-size:34px;font-weight:900;color:#00C896;letter-spacing:-1px;">{cfg['header']}</div>
            <div style="font-size:18px;font-weight:700;color:#0F1923;margin-top:4px;">{doc['id']}</div>
            <div style="font-size:13px;color:#6b7280;margin-top:10px;">Date: {doc['date']}</div>
            <div style="font-size:13px;color:#6b7280;">Due: {doc['due']}</div>
          </div>
        </div>
      </div>

      <!-- Bill To -->
      <div style="padding:20px 40px;">
        <div style="background:#f8f9fa;border-radius:10px;padding:14px 18px;margin-bottom:24px;">
          <div style="font-size:10px;font-weight:700;color:#9ca3af;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">Bill To</div>
          <div style="font-weight:700;font-size:16px;color:#1a1a2e;">{doc['customer']}</div>
          <div style="font-size:13px;color:#6b7280;">Chennai, Tamil Nadu, India</div>
        </div>

        <!-- Items Table -->
        <table style="width:100%;border-collapse:collapse;margin-bottom:24px;">
          <thead>
            <tr style="background:#0F1923;color:#fff;">
              <th style="padding:10px 14px;text-align:left;font-size:12px;font-weight:700;border-radius:8px 0 0 0;">#</th>
              <th style="padding:10px 14px;text-align:left;font-size:12px;font-weight:700;">Item</th>
              <th style="padding:10px 14px;text-align:center;font-size:12px;font-weight:700;">Qty</th>
              <th style="padding:10px 14px;text-align:right;font-size:12px;font-weight:700;">Rate</th>
              <th style="padding:10px 14px;text-align:right;font-size:12px;font-weight:700;border-radius:0 8px 0 0;">Amount</th>
            </tr>
          </thead>
          <tbody>{items_html}</tbody>
        </table>

        <!-- Totals -->
        <div style="display:flex;justify-content:flex-end;">
          <div style="width:260px;">
            <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #e5e7eb;">
              <span style="font-size:13px;color:#6b7280;">Subtotal</span>
              <span style="font-size:13px;font-weight:600;">₹{subtotal:,}</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid #e5e7eb;">
              <span style="font-size:13px;color:#6b7280;">GST ({tax_rate}%)</span>
              <span style="font-size:13px;font-weight:600;">₹{tax:,}</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:12px;background:#0F1923;border-radius:8px;margin-top:6px;">
              <span style="font-size:15px;font-weight:700;color:#fff;">Total</span>
              <span style="font-size:17px;font-weight:900;color:#00C896;">₹{total:,}</span>
            </div>
          </div>
        </div>

        <!-- Payment Instructions -->
        <div style="margin-top:28px;padding-top:20px;border-top:2px solid #e5e7eb;">
          <div style="font-size:11px;font-weight:700;color:#9ca3af;letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Payment Instructions</div>
          <div style="font-size:13px;color:#374151;line-height:1.7;">{s.get('payment_instructions','').replace(chr(10),'<br>')}</div>
        </div>

        <!-- Footer -->
        <div style="margin-top:24px;text-align:center;font-size:11px;color:#9ca3af;padding-bottom:8px;">
          Thank you for your business! — {s.get('company_name','AP Tech Care')} • Smart Tech Solutions
        </div>
      </div>
    </div>
    """

    st.markdown(invoice_html, unsafe_allow_html=True)
