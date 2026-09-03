import sqlite3

conn = sqlite3.connect("data/ecommerce.db")
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [row[0] for row in cursor.fetchall()]

lines = ["erDiagram"]

# --- 1) Each table with all its columns ---
for table in tables:
    lines.append(f"    {table} {{")
    cursor.execute(f"PRAGMA table_info({table});")
    for col in cursor.fetchall():
        col_name = col[1]
        col_type = col[2] if col[2] else "TEXT"
        is_pk = col[5]  # 1 if this column is part of the primary key
        key_tag = " PK" if is_pk else ""
        lines.append(f"        {col_type} {col_name}{key_tag}")
    lines.append("    }")

# --- 2) Relationships from foreign keys ---
for table in tables:
    cursor.execute(f"PRAGMA foreign_key_list({table});")
    for fk in cursor.fetchall():
        target_table = fk[2]   # the table this FK points to
        lines.append(f"    {target_table} ||--o{{ {table} : has")

conn.close()

# --- 3) Write the Mermaid diagram to a file ---
diagram = "\n".join(lines)
with open("docs/er_diagram.md", "w", encoding="utf-8") as f:
    f.write("# Entity-Relationship Diagram\n\n")
    f.write("```mermaid\n")
    f.write(diagram)
    f.write("\n```\n")

print("Diagram generated in docs/er_diagram.md\n")
print(diagram)