import streamlit as st

def render():
    st.markdown('<p class="page-title">📦 Items</p>', unsafe_allow_html=True)
    items = st.session_state.items_db

    col1, col2 = st.columns([3,1])
    with col2:
        if st.button("➕ Add Item", type="primary", use_container_width=True):
            st.session_state.show_add_item = True
            st.session_state.edit_item_idx = None

    search   = st.text_input("🔍 Search", placeholder="Item name or code...", label_visibility="collapsed")
    filtered = [i for i in items if not search or search.lower() in i["name"].lower() or search.lower() in i.get("code","").lower()]

    for item in filtered:
        real_idx = items.index(item)
        c1, c2, c3, c4 = st.columns([3,1,1,1])
        with c1:
            st.markdown(f"""<div style="padding:6px 0;">
              <div style="font-weight:600;font-size:14px;color:#111827;">{item['name']}</div>
              <div style="font-size:12px;color:#9CA3AF;">Code: {item.get('code','—')} &nbsp;•&nbsp; {item.get('unit','')}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div style='padding-top:8px;font-weight:700;color:#166534;'>₹{item['price']:,}</div>", unsafe_allow_html=True)
        with c3:
            if st.button("✏️", key=f"edit_item_{real_idx}"):
                st.session_state.edit_item_idx = real_idx
                st.session_state.show_add_item = False
        with c4:
            if st.button("🗑️", key=f"del_item_{real_idx}"):
                items.pop(real_idx)
                st.rerun()
        st.markdown("<hr style='margin:4px 0;border-color:#F3F4F6;'>", unsafe_allow_html=True)

    # ── Edit Form ─────────────────────────────────────────────────
    edit_idx = st.session_state.get("edit_item_idx")
    if edit_idx is not None and edit_idx < len(items):
        item = items[edit_idx]
        st.markdown("---")
        st.markdown(f"### ✏️ Edit — {item['name']}")
        with st.form("edit_item_form"):
            c1, c2 = st.columns(2)
            with c1:
                name  = st.text_input("Item Name *", value=item.get("name",""))
                price = st.number_input("Price ₹", min_value=0, value=int(item.get("price",0)))
            with c2:
                code = st.text_input("Product Code", value=item.get("code",""))
                unit = st.text_input("Unit Type",    value=item.get("unit","per unit"))
            desc = st.text_area("Description", value=item.get("desc",""), max_chars=10000)
            cs, cc = st.columns(2)
            with cs: save  = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
            with cc: close = st.form_submit_button("✕ Close", use_container_width=True)
            if save and name:
                items[edit_idx] = {"name":name,"code":code,"price":price,"unit":unit,"desc":desc}
                st.session_state.edit_item_idx = None
                st.success(f"✅ '{name}' updated!")
                st.rerun()
            if close:
                st.session_state.edit_item_idx = None
                st.rerun()

    # ── Add Form ──────────────────────────────────────────────────
    if st.session_state.get("show_add_item"):
        st.markdown("---")
        st.markdown("### ➕ New Item")
        with st.form("add_item_form"):
            c1, c2 = st.columns(2)
            with c1:
                name  = st.text_input("Item Name *")
                price = st.number_input("Price ₹", min_value=0)
            with c2:
                code = st.text_input("Product Code")
                unit = st.text_input("Unit Type", value="per unit")
            desc = st.text_area("Description", max_chars=10000)
            cs, cc = st.columns(2)
            with cs: save  = st.form_submit_button("💾 Save", type="primary", use_container_width=True)
            with cc: close = st.form_submit_button("✕ Close", use_container_width=True)
            if save and name:
                items.append({"name":name,"code":code,"price":price,"unit":unit,"desc":desc})
                st.session_state.show_add_item = False
                st.success(f"✅ '{name}' added!")
                st.rerun()
            if close:
                st.session_state.show_add_item = False
                st.rerun()
