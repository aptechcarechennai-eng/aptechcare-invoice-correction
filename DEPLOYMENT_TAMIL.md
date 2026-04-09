# AP Tech Care Invoice App v2 - Deployment Guide (Tamil)

## 🚀 DEPLOYMENT PANNURADHU EPPADI

### STEP 1: Pudhu GitHub Repo Create Pannu
1. https://github.com/aptechcarechennai-eng ku po
2. **"New repository"** button click pannu
3. Repository name type pannu: `aptechcare-invoice-v2`
4. Description: `AP Tech Care Invoice App v2 with Database`
5. **Public** select pannu
6. **"Create repository"** click pannu

### STEP 2: Files Upload Pannu
Intha 2 files-a upload pannu:
- `app_v2.py` → rename pannu `app.py` nu
- `requirements_v2.txt` → rename pannu `requirements.txt` nu

**Upload pannuradhu eppadi:**
1. New repo page-la **"uploading an existing file"** link click pannu
2. Files-a drag and drop pannu
3. **"Commit changes"** click pannu

### STEP 3: Streamlit Cloud-la Deploy Pannu
1. https://share.streamlit.io ku po
2. **"New app"** button click pannu
3. Repository select pannu: `aptechcarechennai-eng/aptechcare-invoice-v2`
4. Branch: `main`
5. Main file path: `app.py`
6. **"Deploy"** click pannu
7. 2-3 minutes wait pannu - app deploy aagidum!

### STEP 4: Supabase Secrets Add Pannu
1. Streamlit Cloud-la unga app page-ku po
2. ⚙️ **Settings** click pannu → **Secrets** click pannu
3. Intha code-a paste pannu (unga Supabase key-oda):

```toml
[supabase]
url = "https://zibexeqgtajeaujjkwqe.supabase.co"
key = "YOUR_SUPABASE_ANON_KEY_PASTE_HERE"
```

4. **"Save"** click pannu
5. App auto-restart aagidum

**Supabase key edukuradhu eppadi:**
1. https://supabase.com/dashboard ku po
2. Unga project select pannu
3. Settings icon click pannu (gear icon)
4. **API** section-ku po
5. **"anon" "public"** key-a copy pannu
6. Streamlit secrets-la paste pannu

### STEP 5: Test Pannu! 🎉
1. Unga new app URL open pannu: `https://aptechcare-invoice-v2.streamlit.app`
2. Invoice onnu create pannu
3. Page-a refresh pannu (F5 press pannu)
4. **Invoice innum irukka check pannu** - data saved! ✅

---

## 📱 IPPO RENDU APPS IRUKKUM

### App 1: Old App (Database Illa)
- **URL:** `https://aptechcare-invoice.streamlit.app`
- **Use:** Daily invoice generate panna mattum (saving illa)
- **Repo:** `aptechcare-invoice`
- **Status:** Safe-aa irukku, disturb pannala

### App 2: New App (Database Irukku) ⭐
- **URL:** `https://aptechcare-invoice-v2.streamlit.app`
- **Use:** Permanent data storage
- **Repo:** `aptechcare-invoice-v2`
- **Status:** Database-la data save aagidum!

**Rendu apps-um separately run aagidum!** ✅

---

## 🔧 SUPABASE TABLE CREATE PANNALA NA

Intha steps follow pannu:

1. https://supabase.com/dashboard ku po
2. Unga project select pannu
3. **Table Editor** click pannu (left sidebar-la)
4. **"New table"** green button click pannu
5. Table name type pannu: `ap_settings`
6. Intha columns add pannu:
   - `id` → int8 → primary key → auto-increment on
   - `key` → text
   - `value` → text  
   - `created_at` → timestamp → default: now()
7. **"Save"** click pannu

Table ready! ✅

---

## ✅ v2-LA ENNA FEATURES IRUKKU

- ✅ Database-la full data save aagidum (Supabase)
- ✅ Every action-kum auto-save
- ✅ App restart aanalum data safe
- ✅ Clean, simple UI
- ✅ Invoice generate + preview
- ✅ Customer management
- ✅ Items/services catalog  
- ✅ Company settings & logo upload
- ✅ Mobile la kooda nalla work aagidum

---

## 🎯 DAILY USAGE

### Work Pannuradhu Eppadi:
```
Morning → App open pannu
       → Customer add pannu (pudhusu-na)
       → Invoice create pannu
       → Preview check pannu
       → Print/PDF save pannu
       → Customer-ku send pannu

Data permanent-aa database-la save aagidum! 🎉
```

---

## ⚠️ IMPORTANT NOTES

1. **Old app touch pannala** - adhu appa irukku same place-la
2. **New app separate URL** - testing easy
3. **Rendu apps-um parallel-aa run aagidum**
4. **Database credentials secret-aa vechuko** - public-aa share pannaadhinga

---

## 🆘 PROBLEM VANTHAA

### Error 1: "Supabase connection error"
**Solution:** Secrets correct-aa add panninga-na check pannu

### Error 2: App deploy aaagala
**Solution:** File names check pannu - `app.py` and `requirements.txt` correct-aa irukka

### Error 3: Data save aagala
**Solution:** Supabase table create panninga-na check pannu (`ap_settings`)

---

**Built for: AP Tech Care, Chennai** ⚡
**Developer: T.Arunprasad, BE., MBA.**
**Version: 2.0 with Database Support**
