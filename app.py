from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)
app.secret_key = "change-this-development-secret"
DB_PATH = Path(__file__).with_name("paisapilot.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL CHECK(kind IN ('income', 'expense')),
                amount REAL NOT NULL CHECK(amount > 0),
                category TEXT NOT NULL,
                note TEXT DEFAULT '',
                transaction_date TEXT NOT NULL
            )
        """)

TRANSLATIONS = {
    "en": {
        "app_name": "PaisaPilot", "tagline": "Your money, made clearer.",
        "balance": "Net balance", "income": "Income", "expense": "Expenses",
        "add": "Add transaction", "type": "Transaction type", "amount": "Amount (₹)",
        "category": "Category", "note": "Note (optional)", "date": "Date",
        "save": "Save transaction", "recent": "Recent transactions",
        "all": "All", "delete": "Delete", "empty": "No transactions yet. Add your first one!",
        "income_option": "Income", "expense_option": "Expense",
        "language": "Language", "required": "Please enter a valid amount and category.",
        "saved": "Transaction saved.", "deleted": "Transaction deleted.",
        "warning": "Prototype only: use sample data, not bank credentials or sensitive financial information."
    },
    "gu": {
        "app_name": "પૈસાપાઇલટ", "tagline": "તમારા પૈસાનો સરળ હિસાબ.",
        "balance": "ચોખ્ખી બાકી રકમ", "income": "આવક", "expense": "ખર્ચ",
        "add": "વ્યવહાર ઉમેરો", "type": "વ્યવહારનો પ્રકાર", "amount": "રકમ (₹)",
        "category": "શ્રેણી", "note": "નોંધ (વૈકલ્પિક)", "date": "તારીખ",
        "save": "વ્યવહાર સાચવો", "recent": "તાજેતરના વ્યવહારો",
        "all": "બધા", "delete": "કાઢી નાખો", "empty": "હજુ કોઈ વ્યવહાર નથી. પહેલો ઉમેરો!",
        "income_option": "આવક", "expense_option": "ખર્ચ",
        "language": "ભાષા", "required": "કૃપા કરીને યોગ્ય રકમ અને શ્રેણી દાખલ કરો.",
        "saved": "વ્યવહાર સાચવાયો.", "deleted": "વ્યવહાર કાઢી નાખ્યો.",
        "warning": "આ માત્ર પ્રોટોટાઇપ છે: નમૂનાનો ડેટા વાપરો; બેંક પાસવર્ડ અથવા સંવેદનશીલ માહિતી નહીં."
    },
    "hi": {
        "app_name": "पैसापायलट", "tagline": "अपने पैसों का हिसाब आसान बनाएं।",
        "balance": "कुल शेष", "income": "आय", "expense": "खर्च",
        "add": "लेन-देन जोड़ें", "type": "लेन-देन का प्रकार", "amount": "राशि (₹)",
        "category": "श्रेणी", "note": "नोट (वैकल्पिक)", "date": "तारीख",
        "save": "लेन-देन सेव करें", "recent": "हाल के लेन-देन",
        "all": "सभी", "delete": "हटाएं", "empty": "अभी कोई लेन-देन नहीं है। पहला जोड़ें!",
        "income_option": "आय", "expense_option": "खर्च",
        "language": "भाषा", "required": "कृपया सही राशि और श्रेणी दर्ज करें।",
        "saved": "लेन-देन सेव हो गया।", "deleted": "लेन-देन हटा दिया गया।",
        "warning": "यह केवल एक प्रोटोटाइप है: नमूना डेटा इस्तेमाल करें; बैंक पासवर्ड या संवेदनशील जानकारी नहीं।"
    }
}

@app.route("/", methods=["GET"])
def index():
    lang = request.args.get("lang", "en")
    if lang not in TRANSLATIONS:
        lang = "en"
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM transactions ORDER BY transaction_date DESC, id DESC"
        ).fetchall()
        totals = conn.execute("""
            SELECT
              COALESCE(SUM(CASE WHEN kind='income' THEN amount ELSE 0 END), 0) AS income,
              COALESCE(SUM(CASE WHEN kind='expense' THEN amount ELSE 0 END), 0) AS expense
            FROM transactions
        """).fetchone()
    return render_template(
        "index.html", t=TRANSLATIONS[lang], lang=lang, rows=rows,
        income=totals["income"], expense=totals["expense"],
        balance=totals["income"] - totals["expense"], today=date.today().isoformat()
    )

@app.route("/add", methods=["POST"])
def add_transaction():
    lang = request.form.get("lang", "en")
    if lang not in TRANSLATIONS:
        lang = "en"
    kind = request.form.get("kind", "")
    category = request.form.get("category", "").strip()
    note = request.form.get("note", "").strip()
    tx_date = request.form.get("transaction_date", "")
    try:
        amount = float(request.form.get("amount", "0"))
    except ValueError:
        amount = 0

    if kind not in ("income", "expense") or amount <= 0 or not category or not tx_date:
        flash(TRANSLATIONS[lang]["required"], "error")
        return redirect(url_for("index", lang=lang))

    with get_db() as conn:
        conn.execute("""
            INSERT INTO transactions (kind, amount, category, note, transaction_date)
            VALUES (?, ?, ?, ?, ?)
        """, (kind, amount, category, note, tx_date))
    flash(TRANSLATIONS[lang]["saved"], "success")
    return redirect(url_for("index", lang=lang))

@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    lang = request.form.get("lang", "en")
    if lang not in TRANSLATIONS:
        lang = "en"
    with get_db() as conn:
        conn.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    flash(TRANSLATIONS[lang]["deleted"], "success")
    return redirect(url_for("index", lang=lang))

 init_db()
if __name__ == "__main__":
    app.run(debug=True)
