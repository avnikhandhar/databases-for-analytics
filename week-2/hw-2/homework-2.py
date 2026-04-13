def validate_SQL_insert(query):
    query_parts = query.split(" ")  # breaking up the query

    if len(query_parts) < 5:
        return "Invalid insert"

    cmd = (query_parts[0] + " " + query_parts[1]).upper()

    if cmd == "INSERT INTO"  and query.endswith(';'):
        table_name = query_parts[2]
        values = " ".join(query_parts[4:]).rstrip(';')

        response = f"Inserting {values} into {table_name} table"
    else:
        response = "Invalid insert"

    return response

result1 = validate_SQL_insert("INSERT INTO Students VALUES (1, 'Jane', 'A-');")
print(result1)

result2 = validate_SQL_insert("INSERT Students VALUES (1, 'Jane', B+);")
print(result2)