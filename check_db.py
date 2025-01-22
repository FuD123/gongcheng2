import sqlite3

def check_database():
    try:
        conn = sqlite3.connect('system.db')
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Tables in database:")
        for table in tables:
            print(f"- {table[0]}")
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table[0]});")
            columns = cursor.fetchall()
            print("  Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # If users table, print sample data
            if table[0] == 'users':
                cursor.execute("SELECT username, role FROM users LIMIT 5")
                users = cursor.fetchall()
                print("\nSample users:")
                for user in users:
                    print(f"- {user[0]} ({user[1]})")
        
        conn.close()
    except Exception as e:
        print(f"Error checking database: {e}")

if __name__ == "__main__":
    check_database()
