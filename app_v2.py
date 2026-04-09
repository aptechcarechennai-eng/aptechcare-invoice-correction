import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date
import base64, json
from supabase import create_client

st.set_page_config(page_title="AP Tech Care v2", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SUPABASE DATABASE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@st.cache_resource
def get_supabase():
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except:
        st.error("⚠️ Supabase not configured")
        return None

def db_load(key, default=None):
    try:
        supabase = get_supabase()
        if not supabase: return default
        result = supabase.table("ap_settings").select("value").eq("key", key).execute()
        if result.data: return json.loads(result.data[0]["value"])
        return default
    except:
        return default

def db_save(key, value):
    try:
        supabase = get_supabase()
        if not supabase: return False
        data = {"key": key, "value": json.dumps(value, default=str)}
        existing = supabase.table("ap_settings").select("key").eq("key", key).execute()
        if existing.data:
            supabase.table("ap_settings").update(data).eq("key", key).execute()
        else:
            supabase.table("ap_settings").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Save error: {e}")
        return False

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STYLING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*{font-family:'Inter',sans-serif!important;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stSidebarCollapseButton"]{display:none!important;}
section[data-testid="stSidebar"]{min-width:220px!important;width:220px!important;background:#fff!important;border-right:1px solid #E5E7EB!important;}
.block-container{padding:1.5rem 2rem!important;max-width:100%!important;}
.stApp{background:#F7F8FA!important;}
.stButton>button{background:transparent!important;border:none!important;color:#6B7280!important;text-align:left!important;width:100%!important;padding:8px 12px!important;border-radius:6px!important;font-size:13px!important;font-weight:500!important;}
.stButton>button:hover{background:#F3F4F6!important;color:#111!important;}
.stButton>button[kind="primary"]{background:#4F46E5!important;color:#fff!important;font-weight:600!important;}
.stTextInput input,.stTextArea textarea,.stNumberInput input,.stDateInput input{border:1px solid #E5E7EB!important;border-radius:7px!important;background:#fff!important;font-size:13px!important;}
.stSelectbox>div>div{border:1px solid #E5E7EB!important;border-radius:7px!important;font-size:13px!important;}
</style>""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# INITIALIZE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if "loaded" not in st.session_state:
    st.session_state.page = "home"
    st.session_state.invoices = db_load("invoices", [])
    st.session_state.customers = db_load("customers", [])
    st.session_state.items = db_load("items", [])
    st.session_state.settings = db_load("settings", {
        "company_name": "AP Tech Care",
        "company_tagline": "Smart Tech Solutions",
        "owner_name": "T.Arunprasad, BE., MBA.,",
        "logo_b64": None,
        "company_phone": "",
        "company_email": "",
        "company_address1": "",
        "company_address2": "",
        "payment_instructions": "Bank transfer or UPI accepted."
    })
    st.session_state.loaded = True

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def nav(p):
    st.session_state.page = p
    st.rerun()

def fd(d):
    try: return datetime.strptime(str(d), "%Y-%m-%d").strftime("%d/%m/%Y")
    except: return str(d) if d else ""

def invoice_html(doc, settings):
    items = doc.get("items", [])
    sub = doc.get("subtotal", 0)
    tax = doc.get("tax", 0)
    total = doc.get("amount", 0)
    
    logo = ""
    if settings.get("logo_b64"):
        logo = f'<img src="data:image/png;base64,{settings["logo_b64"]}" style="max-height:80px;max-width:140px;">'
    
    rows = ""
    for it in items:
        rows += f"""<tr>
            <td style="padding:10px 12px;font-weight:600;border-bottom:1px solid #eee;">{it.get("name","")}</td>
            <td style="padding:10px 12px;text-align:center;border-bottom:1px solid #eee;">{it.get("qty",1)}</td>
            <td style="padding:10px 12px;text-align:right;border-bottom:1px solid #eee;">Rs.{it.get("price",0):,.2f}</td>
            <td style="padding:10px 12px;text-align:right;border-bottom:1px solid #eee;">Rs.{it.get("amount",0):,.2f}</td>
        </tr>"""
    
    tax_row = ""
    if tax > 0:
        tax_row = f'<tr><td colspan="3" style="padding:8px 12px;text-align:right;color:#555;">Tax:</td><td style="padding:8px 12px;text-align:right;font-weight:600;">Rs.{tax:,.2f}</td></tr>'
    
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>{doc["id"]}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:Arial,sans-serif;padding:40px;background:#fff;}}
.wrap{{max-width:720px;margin:0 auto;}}
.hdr{{display:flex;justify-content:space-between;margin-bottom:28px;padding-bottom:20px;border-bottom:2px solid #e5e7eb;}}
.inv-title{{font-size:34px;font-weight:900;}}
.co-name{{font-size:16px;font-weight:800;margin-bottom:2px;}}
.co-tagline{{font-size:12px;font-weight:600;color:#4F46E5;margin-bottom:3px;}}
.co-owner{{font-size:12px;font-weight:600;color:#374151;margin-bottom:3px;}}
.co-info{{font-size:12px;color:#555;line-height:1.7;}}
.mid{{display:flex;justify-content:space-between;margin-bottom:22px;padding:14px 16px;border:1px solid #e5e7eb;border-radius:4px;}}
.bill-to h4{{font-size:11px;font-weight:700;color:#555;text-transform:uppercase;margin-bottom:5px;}}
.bill-to .cn{{font-size:15px;font-weight:700;}}
.bill-to .ci{{font-size:12px;color:#666;line-height:1.6;}}
table.items{{width:100%;border-collapse:collapse;margin-bottom:20px;}}
table.items thead tr{{background:#1a1a1a;color:#fff;}}
table.items thead th{{padding:10px 12px;text-align:left;font-size:12px;font-weight:600;}}
table.items thead th:nth-child(2){{text-align:center;}}
table.items thead th:nth-child(3),table.items thead th:nth-child(4){{text-align:right;}}
.bot{{display:flex;justify-content:space-between;gap:24px;}}
.tots table{{width:100%;border-collapse:collapse;border:1px solid #e5e7eb;}}
.amt-box{{border:1px solid #e5e7eb;border-top:none;padding:14px;text-align:center;}}
.amt-label{{font-size:12px;color:#777;margin-bottom:4px;}}
.amt-val{{font-size:24px;font-weight:900;}}
@media print{{body{{padding:20px;}}}}
</style></head><body><div class="wrap">
<div class="hdr">
  <div>{logo}</div>
  <div style="text-align:right;">
    <div class="inv-title">Invoice</div>
    <div class="co-name">{settings.get("company_name","AP Tech Care")}</div>
    <div class="co-owner">{settings.get("owner_name","")}</div>
    <div class="co-tagline">{settings.get("company_tagline","")}</div>
    <div class="co-info">{settings.get("company_address1","")}<br>{settings.get("company_address2","")}<br>📞 {settings.get("company_phone","")}<br>✉ {settings.get("company_email","")}</div>
  </div>
</div>
<div class="mid">
  <div class="bill-to">
    <h4>Bill To</h4>
    <div class="cn">{doc.get("customer","")}</div>
    <div class="ci">{doc.get("customer_address","")}</div>
  </div>
  <div style="text-align:right;">
    <table>
      <tr><td style="padding:3px 8px;color:#555;">Invoice #</td><td style="padding:3px 8px;font-weight:700;">{doc["id"]}</td></tr>
      <tr><td style="padding:3px 8px;color:#555;">Date</td><td style="padding:3px 8px;font-weight:700;">{fd(doc["date"])}</td></tr>
    </table>
  </div>
</div>
<table class="items">
  <thead><tr><th>Item</th><th>Qty</th><th>Price</th><th>Amount</th></tr></thead>
  <tbody>{rows}</tbody>
</table>
<div class="bot">
  <div style="flex:1;">
    <h4 style="font-size:11px;font-weight:700;text-transform:uppercase;margin-bottom:6px;">Payment Instructions</h4>
    <p style="font-size:12px;color:#444;line-height:1.8;">{settings.get("payment_instructions","")}</p>
  </div>
  <div style="min-width:230px;">
    <table style="width:100%;border:1px solid #e5e7eb;border-collapse:collapse;">
      <tr><td colspan="3" style="padding:8px 12px;text-align:right;color:#555;">Subtotal:</td><td style="padding:8px 12px;text-align:right;font-weight:600;">Rs.{sub:,.2f}</td></tr>
      {tax_row}
      <tr><td colspan="3" style="padding:8px 12px;text-align:right;color:#555;">Total:</td><td style="padding:8px 12px;text-align:right;font-weight:700;">Rs.{total:,.2f}</td></tr>
    </table>
    <div class="amt-box">
      <div class="amt-label">Amount Due</div>
      <div class="amt-val">Rs.{total:,.2f}</div>
    </div>
  </div>
</div>
<div style="margin-top:32px;padding-top:12px;border-top:1px solid #e5e7eb;text-align:center;font-size:11px;color:#aaa;">
  Thank you for your business!
</div>
</div></body></html>"""

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.sidebar:
    s = st.session_state.settings
    if s.get("logo_b64"):
        st.markdown(f'<div style="text-align:center;margin-bottom:10px"><img src="data:image/png;base64,{s["logo_b64"]}" style="max-height:70px;"></div>', unsafe_allow_html=True)
    
    st.markdown(f'''<div style="text-align:center;margin-bottom:16px;">
        <div style="font-size:17px;font-weight:800;">{s.get("company_name","AP Tech Care")}</div>
        <div style="font-size:11px;font-weight:600;color:#4F46E5;">{s.get("company_tagline","")}</div>
        <div style="font-size:11px;font-weight:600;color:#6B7280;">{s.get("owner_name","")}</div>
    </div><hr style="border-top:1px solid #E5E7EB;margin:12px 0;">''', unsafe_allow_html=True)
    
    if st.button("🏠 Home"): nav("home")
    if st.button("📄 Invoices"): nav("invoices")
    if st.button("👥 Customers"): nav("customers")
    if st.button("📦 Items"): nav("items")
    st.markdown('<hr style="border-top:1px solid #E5E7EB;margin:12px 0;">', unsafe_allow_html=True)
    if st.button("⚙️ Settings"): nav("settings")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: HOME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def page_home():
    st.markdown('<p style="font-size:20px;font-weight:700;margin-bottom:20px;">🏠 Dashboard</p>', unsafe_allow_html=True)
    
    invs = st.session_state.invoices
    total = sum(inv.get("amount", 0) for inv in invs)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Invoices", len(invs))
    c2.metric("Total Amount", f"₹{total:,.0f}")
    c3.metric("Customers", len(st.session_state.customers))
    
    st.markdown("---")
    st.markdown("**📄 Recent Invoices**")
    
    if invs:
        for inv in reversed(invs[-5:]):
            st.markdown(f'''<div style="padding:12px;background:#fff;border:1px solid #E5E7EB;border-radius:8px;margin-bottom:8px;">
                <div style="font-weight:700;font-size:14px;">{inv["id"]}</div>
                <div style="font-size:12px;color:#9CA3AF;">{inv.get("customer","")} • ₹{inv.get("amount",0):,} • {fd(inv["date"])}</div>
            </div>''', unsafe_allow_html=True)
    else:
        st.info("No invoices yet. Create your first one!")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: INVOICES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def page_invoices():
    st.markdown('<p style="font-size:20px;font-weight:700;">📄 Invoices</p>', unsafe_allow_html=True)
    
    _, c2 = st.columns([3, 1])
    with c2:
        if st.button("➕ New Invoice", type="primary", use_container_width=True):
            st.session_state.show_form = True
            st.session_state.edit_idx = None
    
    if st.session_state.get("show_form"):
        invs = st.session_state.invoices
        edit_idx = st.session_state.get("edit_idx")
        doc = invs[edit_idx] if edit_idx is not None else {}
        
        st.markdown("---")
        st.markdown(f"**{'✏️ Edit' if edit_idx is not None else '➕ New'} Invoice**")
        
        with st.form("inv_form"):
            c1, c2 = st.columns(2)
            with c1:
                inv_id = st.text_input("Invoice # *", value=doc.get("id", f"AP-{len(invs)+1001}"))
                
                # Customer search
                custs = st.session_state.customers
                search = st.text_input("🔍 Search Customer", value=doc.get("customer", ""))
                matches = [c["name"] for c in custs if search.lower() in c["name"].lower()] if search else [c["name"] for c in custs]
                
                if matches:
                    cust = st.selectbox("Select Customer *", [""] + matches, 
                        index=0 if not doc.get("customer") else (matches.index(doc["customer"]) + 1 if doc.get("customer") in matches else 0))
                else:
                    cust = ""
                    if search:
                        st.info(f"No match for '{search}'")
                        if st.form_submit_button(f"➕ Quick Add '{search}'"):
                            custs.append({"name": search, "phone": "", "email": "", "address": ""})
                            db_save("customers", custs)
                            st.success(f"✅ Added '{search}'!")
                            st.rerun()
                
                inv_date = st.date_input("Date *", value=datetime.strptime(doc.get("date", str(date.today())), "%Y-%m-%d") if doc.get("date") else date.today())
            
            with c2:
                st.text_input("Customer Address", value=doc.get("customer_address", ""), key="cust_addr")
            
            st.markdown("**Items**")
            
            if "temp_items" not in st.session_state:
                st.session_state.temp_items = doc.get("items", [{"name": "", "qty": 1, "price": 0, "amount": 0}])
            
            for i, it in enumerate(st.session_state.temp_items):
                ic1, ic2, ic3, ic4, ic5 = st.columns([3, 1, 1, 1, 0.5])
                
                with ic1:
                    items_db = st.session_state.items
                    item_names = [itm["name"] for itm in items_db]
                    sel = st.selectbox(f"Item {i+1}", [""] + item_names, key=f"it_{i}")
                    
                    if sel:
                        for itm in items_db:
                            if itm["name"] == sel:
                                st.session_state.temp_items[i]["name"] = sel
                                st.session_state.temp_items[i]["price"] = itm.get("price", 0)
                    else:
                        st.session_state.temp_items[i]["name"] = st.text_input("Custom", value=it.get("name", ""), key=f"name_{i}", label_visibility="collapsed")
                
                with ic2:
                    st.session_state.temp_items[i]["qty"] = st.number_input("Qty", min_value=0, value=int(it.get("qty", 1)), key=f"qty_{i}", label_visibility="collapsed")
                with ic3:
                    st.session_state.temp_items[i]["price"] = st.number_input("Price", min_value=0, value=int(it.get("price", 0)), key=f"price_{i}", label_visibility="collapsed")
                with ic4:
                    amt = st.session_state.temp_items[i]["qty"] * st.session_state.temp_items[i]["price"]
                    st.session_state.temp_items[i]["amount"] = amt
                    st.markdown(f"<div style='padding-top:6px;font-weight:700;'>₹{amt:,}</div>", unsafe_allow_html=True)
                with ic5:
                    if len(st.session_state.temp_items) > 1 and st.form_submit_button("🗑️", key=f"del_{i}"):
                        st.session_state.temp_items.pop(i)
                        st.rerun()
            
            if st.form_submit_button("➕ Add Row"):
                st.session_state.temp_items.append({"name": "", "qty": 1, "price": 0, "amount": 0})
                st.rerun()
            
            sub = sum(it["amount"] for it in st.session_state.temp_items)
            total = sub
            
            st.markdown(f"<div style='text-align:right;padding:10px 0;'><div style='font-size:16px;font-weight:700;'>Total: ₹{total:,.2f}</div></div>", unsafe_allow_html=True)
            
            s1, s2, s3 = st.columns(3)
            with s1:
                save = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
            with s2:
                preview = st.form_submit_button("👁️ Preview", use_container_width=True)
            with s3:
                close = st.form_submit_button("✕ Close", use_container_width=True)
            
            if save and inv_id and cust:
                cust_addr = st.session_state.get("cust_addr", "")
                new_doc = {
                    "id": inv_id,
                    "customer": cust,
                    "customer_address": cust_addr,
                    "date": str(inv_date),
                    "items": [it for it in st.session_state.temp_items if it["name"]],
                    "subtotal": sub,
                    "tax": 0,
                    "amount": total
                }
                
                if edit_idx is not None:
                    invs[edit_idx] = new_doc
                else:
                    invs.append(new_doc)
                
                db_save("invoices", invs)
                st.session_state.show_form = False
                st.session_state.temp_items = []
                st.success("✅ Invoice saved to database!")
                st.rerun()
            
            if preview and inv_id and cust:
                cust_addr = st.session_state.get("cust_addr", "")
                preview_doc = {
                    "id": inv_id,
                    "customer": cust,
                    "customer_address": cust_addr,
                    "date": str(inv_date),
                    "items": [it for it in st.session_state.temp_items if it["name"]],
                    "subtotal": sub,
                    "tax": 0,
                    "amount": total
                }
                html = invoice_html(preview_doc, st.session_state.settings)
                components.html(html, height=800, scrolling=True)
            
            if close:
                st.session_state.show_form = False
                st.session_state.temp_items = []
                st.rerun()
    
    else:
        # List view
        invs = st.session_state.invoices
        search = st.text_input("🔍 Search", placeholder="Search invoices...")
        filtered = [inv for inv in invs if not search or search.lower() in inv.get("id", "").lower() or search.lower() in inv.get("customer", "").lower()]
        
        for inv in reversed(filtered):
            idx = invs.index(inv)
            c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
            
            with c1:
                st.markdown(f'''<div style="padding:5px 0;">
                    <div style="font-weight:700;font-size:14px;">{inv["id"]}</div>
                    <div style="font-size:11px;color:#9CA3AF;">{inv.get("customer","")} • {fd(inv["date"])}</div>
                </div>''', unsafe_allow_html=True)
            
            with c2:
                st.markdown(f"<div style='padding-top:6px;font-weight:700;font-size:14px;color:#059669;'>₹{inv.get('amount',0):,}</div>", unsafe_allow_html=True)
            
            with c3:
                if st.button("✏️", key=f"edit_{idx}"):
                    st.session_state.edit_idx = idx
                    st.session_state.show_form = True
                    st.session_state.temp_items = inv.get("items", [])
                    st.rerun()
            
            with c4:
                if st.button("🗑️", key=f"del_{idx}"):
                    if st.session_state.get(f"confirm_{idx}"):
                        invs.pop(idx)
                        db_save("invoices", invs)
                        st.session_state[f"confirm_{idx}"] = False
                        st.success("✅ Deleted!")
                        st.rerun()
                    else:
                        st.session_state[f"confirm_{idx}"] = True
                        st.warning("Click again to confirm")
            
            st.markdown("<hr style='margin:4px 0;border-color:#F3F4F6;'>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: CUSTOMERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def page_customers():
    st.markdown('<p style="font-size:20px;font-weight:700;">👥 Customers</p>', unsafe_allow_html=True)
    
    _, c2 = st.columns([3, 1])
    with c2:
        if st.button("➕ Add", type="primary", use_container_width=True):
            st.session_state.show_cust_form = True
    
    if st.session_state.get("show_cust_form"):
        st.markdown("---")
        with st.form("cust_form"):
            st.markdown("**➕ New Customer**")
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Name *")
                phone = st.text_input("Phone")
            with c2:
                email = st.text_input("Email")
                addr = st.text_area("Address", height=60)
            
            s1, s2 = st.columns(2)
            with s1:
                save = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
            with s2:
                close = st.form_submit_button("✕ Close", use_container_width=True)
            
            if save and name:
                st.session_state.customers.append({"name": name, "phone": phone, "email": email, "address": addr})
                db_save("customers", st.session_state.customers)
                st.session_state.show_cust_form = False
                st.success(f"✅ '{name}' added!")
                st.rerun()
            
            if close:
                st.session_state.show_cust_form = False
                st.rerun()
    
    custs = st.session_state.customers
    search = st.text_input("🔍 Search", placeholder="Search customers...")
    filtered = [c for c in custs if not search or search.lower() in c["name"].lower()]
    
    for c in filtered:
        idx = custs.index(c)
        c1, c2 = st.columns([4, 1])
        
        with c1:
            st.markdown(f'''<div style="padding:8px 0;">
                <div style="font-weight:600;font-size:14px;">{c["name"]}</div>
                <div style="font-size:11px;color:#9CA3AF;">📞 {c.get("phone","")} • ✉ {c.get("email","")}</div>
            </div>''', unsafe_allow_html=True)
        
        with c2:
            if st.button("🗑️", key=f"delc_{idx}"):
                custs.pop(idx)
                db_save("customers", custs)
                st.rerun()
        
        st.markdown("<hr style='margin:4px 0;border-color:#F3F4F6;'>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: ITEMS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def page_items():
    st.markdown('<p style="font-size:20px;font-weight:700;">📦 Items</p>', unsafe_allow_html=True)
    
    _, c2 = st.columns([3, 1])
    with c2:
        if st.button("➕ Add", type="primary", use_container_width=True):
            st.session_state.show_item_form = True
    
    if st.session_state.get("show_item_form"):
        st.markdown("---")
        with st.form("item_form"):
            st.markdown("**➕ New Item**")
            c1, c2 = st.columns(2)
            with c1:
                name = st.text_input("Item Name *")
                price = st.number_input("Price ₹", min_value=0)
            with c2:
                code = st.text_input("Code")
                unit = st.text_input("Unit", value="per visit")
            
            s1, s2 = st.columns(2)
            with s1:
                save = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
            with s2:
                close = st.form_submit_button("✕ Close", use_container_width=True)
            
            if save and name:
                st.session_state.items.append({"name": name, "code": code, "price": price, "unit": unit})
                db_save("items", st.session_state.items)
                st.session_state.show_item_form = False
                st.success(f"✅ '{name}' added!")
                st.rerun()
            
            if close:
                st.session_state.show_item_form = False
                st.rerun()
    
    items = st.session_state.items
    search = st.text_input("🔍 Search", placeholder="Search items...")
    filtered = [it for it in items if not search or search.lower() in it["name"].lower()]
    
    for it in filtered:
        idx = items.index(it)
        c1, c2, c3 = st.columns([3, 1, 1])
        
        with c1:
            st.markdown(f'''<div style="padding:8px 0;">
                <div style="font-weight:600;font-size:14px;">{it["name"]}</div>
                <div style="font-size:11px;color:#9CA3AF;">Code: {it.get("code","—")} • {it.get("unit","")}</div>
            </div>''', unsafe_allow_html=True)
        
        with c2:
            st.markdown(f"<div style='padding-top:8px;font-weight:700;color:#059669;'>₹{it['price']:,}</div>", unsafe_allow_html=True)
        
        with c3:
            if st.button("🗑️", key=f"deli_{idx}"):
                items.pop(idx)
                db_save("items", items)
                st.rerun()
        
        st.markdown("<hr style='margin:4px 0;border-color:#F3F4F6;'>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: SETTINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def page_settings():
    st.markdown('<p style="font-size:20px;font-weight:700;">⚙️ Settings</p>', unsafe_allow_html=True)
    
    s = st.session_state.settings
    
    # Logo upload
    logo_file = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg"])
    if logo_file:
        s["logo_b64"] = base64.b64encode(logo_file.read()).decode()
        db_save("settings", s)
        st.success("✅ Logo saved!")
        st.rerun()
    
    if s.get("logo_b64"):
        st.markdown(f'<img src="data:image/png;base64,{s["logo_b64"]}" style="height:60px;border-radius:8px;margin-bottom:10px;">', unsafe_allow_html=True)
        if st.button("🗑️ Remove Logo"):
            s["logo_b64"] = None
            db_save("settings", s)
            st.rerun()
    
    c1, c2 = st.columns(2)
    with c1:
        comp_name = st.text_input("Company Name", value=s.get("company_name", ""))
        tagline = st.text_input("Tagline", value=s.get("company_tagline", ""))
        owner = st.text_input("Owner Name", value=s.get("owner_name", ""))
        phone = st.text_input("Phone", value=s.get("company_phone", ""))
    
    with c2:
        email = st.text_input("Email", value=s.get("company_email", ""))
        addr1 = st.text_input("Address Line 1", value=s.get("company_address1", ""))
        addr2 = st.text_input("Address Line 2", value=s.get("company_address2", ""))
    
    pay_inst = st.text_area("Payment Instructions", value=s.get("payment_instructions", ""), height=80)
    
    if st.button("💾 Save Settings", type="primary"):
        s.update({
            "company_name": comp_name,
            "company_tagline": tagline,
            "owner_name": owner,
            "company_phone": phone,
            "company_email": email,
            "company_address1": addr1,
            "company_address2": addr2,
            "payment_instructions": pay_inst
        })
        db_save("settings", s)
        st.success("✅ Settings saved to database!")
        st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ROUTING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

pg = st.session_state.page
if pg == "home": page_home()
elif pg == "invoices": page_invoices()
elif pg == "customers": page_customers()
elif pg == "items": page_items()
elif pg == "settings": page_settings()
