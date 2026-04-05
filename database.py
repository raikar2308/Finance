import mysql.connector
from mysql.connector import pooling
from flask import session
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import os

load_dotenv()
# Setup logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
handler = RotatingFileHandler('db.log', maxBytes=2 * 1024 * 1024, backupCount=3)
logging.basicConfig(handlers=[handler], level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# print(os.getenv("HOST")," , ",os.getenv("USER")," , ",os.getenv("PASSWORD")," , ",os.getenv("DATABASE"))

dbconfig = {
    "host": os.getenv("HOST"),
    "user": os.getenv("DBUSER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE")
}

connection_pool = pooling.MySQLConnectionPool(
    pool_name="finance_pool",
    pool_size=10,
    pool_reset_session=True,
    **dbconfig
)

def get_connection():
    try:
        return connection_pool.get_connection()
    except Exception as e:
        logging.error(f"Connection error: {str(e)}")
        raise

def execute_select(query, params=None):
    conn = connection_pool.get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
    finally:
        try:
            cursor.close()
        except:
            pass
        try:
            if conn.is_connected():
                conn.close()   # safely returns to pool
        except:
            pass

def execute_insert(query, params):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Insert error: {str(e)}")
        logging.error(f"Insert error: {str(e)}")
        return False
    finally:
        conn.close()

def execute_insert_return_id(query, params):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        return last_id
    except Exception as e:
        logging.error(f"Insert (return id) error: {str(e)}")
        return None
    finally:
        conn.close()

def execute_update(query, params):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
        return True
    except Exception as e:
        logging.error(f"Update error: {str(e)}")
        return False
    finally:
        conn.close()

def execute_delete(query, params):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        affected = cursor.rowcount > 0
        cursor.close()
        return affected
    except Exception as e:
        logging.error(f"Delete error: {str(e)}")
        return False
    finally:
        conn.close()

def execute_fetchone(query, params=None):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        cursor.execute(query, params or ())
        result = cursor.fetchone()
        cursor.close()
        return result
    except Exception as e:
        logging.error(f"FetchOne error: {str(e)}")
        return None
    finally:
        conn.close()


def execute_fetchall(query, values=None):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, values or ())
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print("❌ FetchAll Error:", e)
        return []
    finally:
        cursor.close()
        conn.close()
