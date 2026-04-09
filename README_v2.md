# AP Tech Care Invoice App v2 (with Database)

## 🚀 DEPLOYMENT STEPS

### STEP 1: Create New GitHub Repo
1. Go to https://github.com/aptechcarechennai-eng
2. Click **"New repository"**
3. Repository name: `aptechcare-invoice-v2`
4. Description: `AP Tech Care Invoice App v2 with Supabase Database`
5. Select **Public**
6. Click **"Create repository"**

### STEP 2: Upload Files
Upload these 2 files to the new repo:
- `app_v2.py` → rename to `app.py`
- `requirements_v2.txt` → rename to `requirements.txt`

### STEP 3: Streamlit Cloud Deployment
1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Select repository: `aptechcarechennai-eng/aptechcare-invoice-v2`
4. Branch: `main`
5. Main file path: `app.py`
6. Click **"Deploy"**

### STEP 4: Add Supabase Secrets
1. In Streamlit Cloud, go to your app
2. Click ⚙️ **Settings** → **Secrets**
3. Add this (replace with your Supabase credentials):

```toml
[supabase]
url = "https://zibexeqgtajeaujjkwqe.supabase.co"
key = "YOUR_SUPABASE_ANON_KEY_HERE"
```

4. Click **"Save"**
5. App will restart automatically

### STEP 5: Test
1. Open your new app URL: `https://aptechcare-invoice-v2.streamlit.app`
2. Create an invoice
3. Refresh the page (F5)
4. Invoice should still be there! ✅

---

## 📱 TWO APPS RUNNING

You will now have 2 separate apps:

1. **Old App (No Database):**
   - URL: `https://aptechcare-invoice.streamlit.app`
   - Use for: Daily invoice generation (no saving)
   - Repo: `aptechcare-invoice`

2. **New App (With Database):**
   - URL: `https://aptechcare-invoice-v2.streamlit.app`
   - Use for: Permanent data storage
   - Repo: `aptechcare-invoice-v2`

Both apps work independently!

---

## 🔧 SUPABASE DATABASE SETUP

If you haven't created the Supabase table yet:

1. Go to https://supabase.com/dashboard
2. Select your project
3. Go to **Table Editor**
4. Click **"New table"**
5. Table name: `ap_settings`
6. Add columns:
   - `id` (int8, primary key, auto-increment)
   - `key` (text)
   - `value` (text)
   - `created_at` (timestamp with time zone, default: now())
7. Click **"Save"**

---

## ✅ FEATURES IN v2

- ✅ Full database persistence (Supabase)
- ✅ Auto-save on every action
- ✅ Data survives app restarts
- ✅ Clean, simple UI
- ✅ Invoice generation with preview
- ✅ Customer management
- ✅ Items/services catalog
- ✅ Company settings & logo
- ✅ Mobile responsive

---

## 🎯 USAGE

### Daily Workflow:
1. Open app
2. Add customer (if new)
3. Create invoice
4. Preview → Print to PDF
5. Share with customer

Data stays saved permanently in database!

---

**Created for: AP Tech Care, Chennai**
**Developer: T.Arunprasad, BE., MBA.**
