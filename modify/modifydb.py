# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 00:56:12 2026

@author: Meghana
"""

import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Meghana@1703",
    database="rentzy_hackathon"
)

cursor = conn.cursor(dictionary=True)

# ---------- USERS ----------
def add_user(name, mobile, email, aadhar, role):
    sql = """
    INSERT INTO users (name, mobile, email, aadhar, role, trust)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (name.strip(), mobile.strip(), email.strip(), aadhar.strip(), role, 80))
    conn.commit()

def get_user_by_mobile(mobile):
    cursor.execute("SELECT * FROM users WHERE mobile=%s", (mobile,))
    return cursor.fetchone()

def update_trust(name, points):
    cursor.execute("UPDATE users SET trust = LEAST(GREATEST(trust + %s, 0), 100) WHERE name=%s", (points, name))
    conn.commit()

# ---------- ITEMS ----------
def add_item(name, category, location, rent, owner):
    sql = """
    INSERT INTO items (name, category, location, rent, owner)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (name.strip(), category, location, rent, owner))
    conn.commit()

def get_items():
    cursor.execute("SELECT * FROM items")
    return cursor.fetchall()

# ---------- REQUESTS ----------
def add_request(item_id, consumer, owner):
    # Check if request already exists
    cursor.execute("SELECT * FROM requests WHERE item_id=%s AND consumer=%s AND status='Pending'", (item_id, consumer))
    if cursor.fetchone():
        return False  # Already requested
    sql = """
    INSERT INTO requests (item_id, consumer, owner, status)
    VALUES (%s, %s, %s, 'Pending')
    """
    cursor.execute(sql, (item_id, consumer, owner))
    conn.commit()
    return True

def get_requests_for_user(username):
    sql = """
    SELECT r.id, r.status, r.consumer, r.owner,
           i.name, i.category, i.location, i.rent
    FROM requests r
    JOIN items i ON r.item_id = i.id
    WHERE r.owner=%s OR r.consumer=%s
    """
    cursor.execute(sql, (username, username))
    return cursor.fetchall()

def update_request_status(request_id, status):
    cursor.execute("UPDATE requests SET status=%s WHERE id=%s", (status, request_id))
    conn.commit()
