from DB_Connect import create_connection

def execute_sql_file(sql_file_path):
    conn = create_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        # Execute each non-empty SQL statement
        for statement in sql_script.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt + ';')

        conn.commit()
        print("SQL script executed successfully.")

    except Exception as e:
        print(f"SQL execution error: {e}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    execute_sql_file("SQL/Initialization.sql")
