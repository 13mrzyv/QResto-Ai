import re

QADAGAN_SOZLER = ["DROP", "DELETE", "UPDATE", "INSERT", "TRUNCATE", "ALTER", "CREATE"]

def sql_yoxla(sql: str) -> tuple[bool, str]:
    sql_upper = sql.upper()

    for soz in QADAGAN_SOZLER:
        if re.search(r'\b' + soz + r'\b', sql_upper):
            return False, f"Təhlükəli əməliyyat aşkarlandı: {soz}"

    if not sql_upper.strip().startswith("SELECT"):
        return False, "Yalnız SELECT sorğularına icazə verilir"

    return True, ""