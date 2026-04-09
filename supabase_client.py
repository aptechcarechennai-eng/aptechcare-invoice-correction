import os
from supabase import create_client, Client
import streamlit as st

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://zibexeqgtajeaujjkwqe.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

@st.cache_resource
def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# ── AUTH ────────────────────────────────────────────────────────
def sign_in(email, password):
    try:
        sb = get_supabase()
        res = sb.auth.sign_in_with_password({"email": email, "password": password})
        return res.user, None
    except Exception as e:
        return None, str(e)

def sign_up(email, password, full_name):
    try:
        sb = get_supabase()
        res = sb.auth.sign_up({"email": email, "password": password, "options": {"data": {"full_name": full_name}}})
        return res.user, None
    except Exception as e:
        return None, str(e)

def sign_out():
    try:
        get_supabase().auth.sign_out()
    except:
        pass
    for k in ["user", "access_token"]:
        st.session_state.pop(k, None)

def reset_password(email):
    try:
        get_supabase().auth.reset_password_email(email)
        return True, None
    except Exception as e:
        return False, str(e)

# ── INVOICES ────────────────────────────────────────────────────
def get_invoices(user_id):
    try:
        sb = get_supabase()
        res = sb.table("invoices").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return res.data or []
    except:
        return []

def create_invoice(data):
    try:
        sb = get_supabase()
        res = sb.table("invoices").insert(data).execute()
        return res.data[0] if res.data else None, None
    except Exception as e:
        return None, str(e)

def update_invoice(inv_id, data):
    try:
        sb = get_supabase()
        res = sb.table("invoices").update(data).eq("id", inv_id).execute()
        return res.data[0] if res.data else None, None
    except Exception as e:
        return None, str(e)

def delete_invoice(inv_id):
    try:
        get_supabase().table("invoices").delete().eq("id", inv_id).execute()
        return True
    except:
        return False

# ── CUSTOMERS ───────────────────────────────────────────────────
def get_customers(user_id):
    try:
        sb = get_supabase()
        res = sb.table("customers").select("*").eq("user_id", user_id).order("name").execute()
        return res.data or []
    except:
        return []

def create_customer(data):
    try:
        sb = get_supabase()
        res = sb.table("customers").insert(data).execute()
        return res.data[0] if res.data else None, None
    except Exception as e:
        return None, str(e)

def update_customer(cust_id, data):
    try:
        sb = get_supabase()
        res = sb.table("customers").update(data).eq("id", cust_id).execute()
        return res.data[0] if res.data else None, None
    except Exception as e:
        return None, str(e)

# ── ITEMS ───────────────────────────────────────────────────────
def get_items(user_id):
    try:
        sb = get_supabase()
        res = sb.table("items").select("*").eq("user_id", user_id).order("name").execute()
        return res.data or []
    except:
        return []

def create_item(data):
    try:
        sb = get_supabase()
        res = sb.table("items").insert(data).execute()
        return res.data[0] if res.data else None, None
    except Exception as e:
        return None, str(e)

def update_item(item_id, data):
    try:
        sb = get_supabase()
        res = sb.table("items").update(data).eq("id", item_id).execute()
        return res.data[0] if res.data else None, None
    except Exception as e:
        return None, str(e)

def delete_item(item_id):
    try:
        get_supabase().table("items").delete().eq("id", item_id).execute()
        return True
    except:
        return False

# ── SETTINGS ────────────────────────────────────────────────────
def get_settings(user_id):
    try:
        sb = get_supabase()
        res = sb.table("settings").select("*").eq("user_id", user_id).single().execute()
        return res.data or {}
    except:
        return {}

def save_settings(user_id, data):
    try:
        sb = get_supabase()
        existing = get_settings(user_id)
        if existing:
            sb.table("settings").update(data).eq("user_id", user_id).execute()
        else:
            sb.table("settings").insert({**data, "user_id": user_id}).execute()
        return True
    except:
        return False

# ── CASHFLOW ────────────────────────────────────────────────────
def get_transactions(user_id):
    try:
        sb = get_supabase()
        res = sb.table("transactions").select("*").eq("user_id", user_id).order("date", desc=True).execute()
        return res.data or []
    except:
        return []

def create_transaction(data):
    try:
        sb = get_supabase()
        res = sb.table("transactions").insert(data).execute()
        return res.data[0] if res.data else None, None
    except Exception as e:
        return None, str(e)

# ── FILE UPLOAD ─────────────────────────────────────────────────
def upload_file(bucket, path, file_bytes, content_type="image/png"):
    try:
        sb = get_supabase()
        sb.storage.from_(bucket).upload(path, file_bytes, {"content-type": content_type, "upsert": "true"})
        url = sb.storage.from_(bucket).get_public_url(path)
        return url, None
    except Exception as e:
        return None, str(e)
