from openai import OpenAI
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from schema import SCHEMA
from examples import EXAMPLES
from validator import sql_yoxla
import os
import pyodbc

load_dotenv()

client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def db_baglan():
    return pyodbc.connect(os.getenv("DB_CONNECTION"))

def mehsul_adlarini_al():
    conn = db_baglan()
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Products WHERE IsDeleted = 0")
    adlar = [r[0] for r in cursor.fetchall()]
    conn.close()
    return ", ".join(adlar)

@app.get("/")
def index():
    return {"status": "QResto AI işləyir!"}

@app.post("/sual")
def sual_ver(data: dict):
    sual = data["sual"]
    tarix = data.get("tarix", [])
    kontekst = "\n".join(tarix) if tarix else ""
    mehsul_siyahisi = mehsul_adlarini_al()

    cavab = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": f"""Sən QResto restoranının SQL Server ekspertisən.
Sualı SQL-ə çevir. YALNIZ SQL yaz, ``` yazma, LIMIT yazma.
Mövcud məhsul adları: {mehsul_siyahisi}
Sual səhv yazılmış məhsul adı ehtiva edə bilər. Ən yaxın uyğun adı tap.

Əvvəlki söhbət (kontekst üçün):
{kontekst}

Əgər indiki sual əvvəlki sualın davamıdırsa (məs: "bəs X?"), kontekstdən mövzunu tap.

Qaydalar:
- Məhsul adı: LIKE '%ad%'
- Tarix: CAST(sütun AS DATE) = CAST(GETDATE() AS DATE)
- Sıralama: SELECT TOP N ... ORDER BY ... DESC/ASC
- Səhv yazılmış sualları da anla

{SCHEMA}

{EXAMPLES}"""},
            {"role": "user", "content": sual}
        ]
    )

    sql = cavab.choices[0].message.content.strip()
    sql = sql.replace("SQL:", "").strip()

    kecdi, xeta = sql_yoxla(sql)
    if not kecdi:
        return {"cavab": f"Bu sorğu icazə verilmir: {xeta}", "sql": sql}

    try:
        conn = db_baglan()
        cursor = conn.cursor()
        cursor.execute(sql)
        sutunlar = [s[0] for s in cursor.description]
        satirlar = [dict(zip(sutunlar, satir)) for satir in cursor.fetchall()]
        conn.close()
    except Exception as e:
        return {"cavab": f"Sorğu xətası: {str(e)}"}

    izah = client_ai.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": "Sən restoran idarəetmə sisteminin AI assistantısan. Verilən məlumatı qısa, oxunaqlı və Azərbaycanca izah et. YALNIZ verilən nəticəyə əsaslan, heç vaxt məlumat uydurma. Nəticə TAMAMILƏ boşdursa (heç sətir yoxdursa), 'Məlumat tapılmadı' de. Əgər nəticədə sətir var, amma dəyər False/0/boşdursa, bunu normal nəticə kimi izah et (məsələn: 'Xeyr, mövcud deyil'). Sütun adlarına diqqət et: 'Total' sözü ƏDƏD deməkdir, pul deyil — manat yazma. JSON və kod yazma, yalnız sadə mətn yaz."},
            {"role": "user", "content": f"Sual: {sual}\nNəticə: {satirlar}"}
        ]
    )
    #""
    return {"cavab": izah.choices[0].message.content, "sql": sql}