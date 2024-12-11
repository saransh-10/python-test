from databricks import sql

def execute_databricks_sql_query(query):
    try:
        conn = sql.connect(
            server_hostname="adb-1707235376781494.14.azuredatabricks.net",
            http_path="/sql/1.0/warehouses/a38993babbf6581b",
            access_token="dapi5e687e69ca8a1e490a12946b35b9989e-2"
        )


        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()  # Fetch all rows
            columns = [desc[0] for desc in cursor.description]  # Get column names

        result_dict = [dict(zip(columns, row)) for row in result]
        return result_dict
    

    except Exception as e:
        print(f"Databricks SQL Execution Error: {e}")
        return {}
 
    