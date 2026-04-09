import streamlit as st

def render():
    st.markdown('<p class="page-title">⚙️ Settings</p>', unsafe_allow_html=True)

    s = st.session_state.settings

    section = st.radio("", [
        "👤 User Account", "🏢 Logo & Company", "✍️ Signature",
        "💳 Payment Instructions", "🧾 Tax", "💹 Transactions",
        "💱 Currency & Date", "🎨 Theme"
    ], horizontal=True, label_visibility="collapsed")

    st.markdown("---")

    # ── 1. USER ACCOUNT ───────────────────────────────────────────
    if section == "👤 User Account":
        st.markdown("### 👤 User Account")
        col1, col2 = st.columns(2)
        with col1:
            first = st.text_input("First Name", value=s.get("first_name", ""))
            email = st.text_input("Email ID", value=s.get("email", ""))
        with col2:
            last = st.text_input("Last Name", value=s.get("last_name", ""))
            st.text_input("User Name", value=s.get("username", ""), disabled=True)

        if st.button("💾 Save Profile", type="primary"):
            s.update({"first_name": first, "last_name": last, "email": email})
            st.success("✅ Profile saved!")

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔑 Reset Password", use_container_width=True):
                st.info("Password reset link sent to your email.")
        with col2:
            if st.button("🗑️ Delete Account", use_container_width=True):
                st.warning("⚠️ This will permanently delete your account.")

    # ── 2. LOGO & COMPANY ─────────────────────────────────────────
    elif section == "🏢 Logo & Company":
        st.markdown("### 🏢 Logo & Company Information")

        logo_file = st.file_uploader("Upload Logo", type=["png", "jpg", "jpeg", "svg"])
        if logo_file:
            st.image(logo_file, width=120)
            st.slider("Zoom Size", 50, 200, 100)

        st.markdown("**Company Information**")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Company Name", value=s.get("company_name", "AP Tech Care"))
            phone = st.text_input("Phone", value=s.get("company_phone", ""))
        with col2:
            email = st.text_input("Email", value=s.get("company_email", ""))
            extra = st.text_input("Additional Information", value=s.get("company_extra", ""))

        st.markdown("**Business Details**")
        col1, col2 = st.columns(2)
        with col1:
            abbr = st.text_input("Abbreviation", value=s.get("abbreviation", "AP"))
            biz_no = st.text_input("Business Number", value=s.get("biz_no", ""))
        with col2:
            gst = st.text_input("Tax Reg. No (GST)", value=s.get("gst_no", ""))

        col1, col2 = st.columns(2)
        with col1:
            addr1 = st.text_input("Address Line 1", value=s.get("addr1", ""))
            city = st.text_input("City", value=s.get("city", "Chennai"))
            zipcode = st.text_input("ZIP", value=s.get("zip", ""))
        with col2:
            addr2 = st.text_input("Address Line 2", value=s.get("addr2", ""))
            state = st.text_input("State", value=s.get("state", "Tamil Nadu"))
            country = st.text_input("Country", value=s.get("country", "India"))

        if st.button("💾 Save", type="primary"):
            s.update({
                "company_name": name, "company_email": email, "company_phone": phone,
                "company_extra": extra, "abbreviation": abbr, "biz_no": biz_no,
                "gst_no": gst, "addr1": addr1, "addr2": addr2, "city": city,
                "state": state, "zip": zipcode, "country": country
            })
            st.success("✅ Company info saved!")

    # ── 3. SIGNATURE ─────────────────────────────────────────────
    elif section == "✍️ Signature":
        st.markdown("### ✍️ Signature")
        mode = st.radio("Mode", ["✏️ Draw Mode", "📤 Upload Photo", "🔐 Digital Authentication"], horizontal=True)

        if mode == "✏️ Draw Mode":
            st.markdown("""
            <div style="background:#fff;border:2px solid #e5e7eb;border-radius:12px;padding:20px;text-align:center;">
              <div style="color:#6b7280;font-size:14px;margin-bottom:12px;">Draw your signature below</div>
              <canvas id="sigCanvas" width="500" height="150"
                style="border:1px solid #d1d5db;border-radius:8px;cursor:crosshair;background:#fff;max-width:100%;touch-action:none;">
              </canvas>
              <br>
              <button onclick="clearSig()" style="margin-top:10px;padding:6px 16px;border:1px solid #d1d5db;border-radius:6px;cursor:pointer;background:#f9fafb;">
                🗑️ Erase
              </button>
            </div>
            <script>
            const canvas = document.getElementById('sigCanvas');
            const ctx = canvas.getContext('2d');
            let drawing = false;
            canvas.addEventListener('mousedown', e => { drawing=true; ctx.beginPath(); });
            canvas.addEventListener('mousemove', e => {
              if(!drawing) return;
              const r = canvas.getBoundingClientRect();
              ctx.lineWidth=2; ctx.lineCap='round'; ctx.strokeStyle='#0F1923';
              ctx.lineTo(e.clientX-r.left, e.clientY-r.top);
              ctx.stroke(); ctx.beginPath(); ctx.moveTo(e.clientX-r.left, e.clientY-r.top);
            });
            canvas.addEventListener('mouseup', ()=>drawing=false);
            canvas.addEventListener('mouseleave', ()=>drawing=false);
            function clearSig(){ ctx.clearRect(0,0,canvas.width,canvas.height); }
            </script>
            """, unsafe_allow_html=True)

        elif mode == "📤 Upload Photo":
            sig_file = st.file_uploader("Upload Signature Image", type=["png", "jpg", "jpeg"])
            if sig_file:
                st.image(sig_file, width=200)
                st.success("✅ Signature uploaded!")

        else:
            st.markdown("""
            <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px;padding:24px;text-align:center;">
              <div style="font-size:32px;margin-bottom:8px;">🔐</div>
              <div style="font-weight:700;color:#1E40AF;margin-bottom:4px;">Digital Authentication</div>
              <div style="font-size:13px;color:#3B82F6;">Authenticate with your digital certificate</div>
            </div>
            """, unsafe_allow_html=True)

    # ── 4. PAYMENT INSTRUCTIONS ───────────────────────────────────
    elif section == "💳 Payment Instructions":
        st.markdown("### 💳 Payment Instructions")
        instructions = st.text_area(
            "Instructions (up to 500 words)",
            value=s.get("payment_instructions", ""),
            height=150,
            max_chars=3500
        )
        st.caption(f"{len(instructions.split())} / 500 words")

        st.markdown("**Upload Payment QR Code**")
        qr_file = st.file_uploader("QR Code Image", type=["png", "jpg", "jpeg"], key="qr_upload")
        if qr_file:
            st.image(qr_file, width=180)

        if st.button("💾 Save", type="primary"):
            s["payment_instructions"] = instructions
            st.success("✅ Payment instructions saved!")

    # ── 5. TAX ────────────────────────────────────────────────────
    elif section == "🧾 Tax":
        st.markdown("### 🧾 Tax Settings")
        col1, col2 = st.columns(2)
        with col1:
            tax_name = st.text_input("Tax Name", value=s.get("tax_name", "GST"))
            tax_no = st.text_input("Tax Registration Number", value=s.get("gst_no", ""))
        with col2:
            tax_rate = st.number_input("Tax Rate (%)", min_value=0.0, max_value=100.0, value=float(s.get("tax_rate", 18)), step=0.5)

        inclusive = st.checkbox("Prices are tax inclusive", value=s.get("tax_inclusive", False))

        if st.button("💾 Save Tax Settings", type="primary"):
            s.update({"tax_name": tax_name, "tax_rate": tax_rate, "gst_no": tax_no, "tax_inclusive": inclusive})
            st.success("✅ Tax settings saved!")

    # ── 6. TRANSACTIONS ───────────────────────────────────────────
    elif section == "💹 Transactions":
        st.markdown("### 💹 Transaction Accounts")
        accounts = s.get("accounts", ["Cash", "G.M. Account", "Savings Account"])

        for i, acc in enumerate(accounts):
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.markdown(f"""
                <div style="padding:12px 16px;background:#f8f9fa;border:1px solid #e5e7eb;border-radius:8px;font-weight:600;">
                  💰 {acc}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✏️ Edit", key=f"acc_edit_{i}"):
                    st.session_state[f"edit_acc_{i}"] = True
            with col3:
                if st.button("🗑️", key=f"acc_del_{i}"):
                    accounts.pop(i)
                    s["accounts"] = accounts
                    st.rerun()

        st.markdown("---")
        new_acc = st.text_input("New Account Name")
        if st.button("➕ Add Saving Account", type="primary"):
            if new_acc:
                accounts.append(new_acc)
                s["accounts"] = accounts
                st.success(f"✅ '{new_acc}' added!")
                st.rerun()

    # ── 7. CURRENCY & DATE ────────────────────────────────────────
    elif section == "💱 Currency & Date":
        st.markdown("### 💱 Currency & Date Format")
        col1, col2 = st.columns(2)
        with col1:
            currency = st.selectbox("Currency", ["INR", "USD", "EUR", "GBP", "AED"],
                                    index=["INR","USD","EUR","GBP","AED"].index(s.get("currency","INR")))
        with col2:
            date_fmt = st.selectbox("Date Format",
                                    ["DD/MM/YYYY", "MM/DD/YYYY", "YYYY/MM/DD", "19 Jun 2025", "Jun 19, 2025"],
                                    index=["DD/MM/YYYY","MM/DD/YYYY","YYYY/MM/DD","19 Jun 2025","Jun 19, 2025"].index(
                                        s.get("date_format","DD/MM/YYYY")))

        if st.button("💾 Save", type="primary"):
            s.update({"currency": currency, "date_format": date_fmt})
            st.success("✅ Currency & date format saved!")

    # ── 8. THEME ─────────────────────────────────────────────────
    elif section == "🎨 Theme":
        st.markdown("### 🎨 Theme")

        themes = [
            {"id": "default", "label": "Default", "desc": "White background • Black text • Bold headings", "colors": ["#FFFFFF", "#0F1923", "#00C896"]},
            {"id": "classic", "label": "Classic Dark", "desc": "Dark theme • Professional look", "colors": ["#0F1923", "#1A2535", "#00C896"]},
            {"id": "ultra",   "label": "Ultra Level", "desc": "Colourful • Vibrant • Energetic", "colors": ["#FFF8F0", "#1E1B4B", "#F97316"]},
        ]

        cur_theme = s.get("theme", "default")

        for th in themes:
            selected = cur_theme == th["id"]
            border_style = "border:2px solid #00C896;" if selected else "border:1px solid #e5e7eb;"
            check = "✅" if selected else ""

            swatches = "".join([f'<div style="width:24px;height:24px;border-radius:6px;background:{c};border:1px solid rgba(0,0,0,0.1);"></div>' for c in th["colors"]])

            st.markdown(f"""
            <div style="{border_style}border-radius:12px;padding:16px 18px;margin-bottom:10px;cursor:pointer;background:#fff;">
              <div style="display:flex;align-items:center;gap:12px;">
                <div style="display:flex;gap:6px;">{swatches}</div>
                <div style="flex:1;">
                  <div style="font-weight:700;font-size:15px;color:#1a1a2e;">{th['label']} {check}</div>
                  <div style="font-size:12px;color:#6b7280;">{th['desc']}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Apply {th['label']}", key=f"theme_{th['id']}", use_container_width=True):
                s["theme"] = th["id"]
                st.rerun()
