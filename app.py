from flask import Flask
import psycopg2

GITHUB_URL = "https://github.com/viljarvi/viikko2"

app = Flask(__name__)

def db():
    return psycopg2.connect(dbname="viikko2", user="viikko2")

def kasvata():
    conn = db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS laskuri (id int PRIMARY KEY, maara bigint NOT NULL DEFAULT 0)")
    cur.execute("INSERT INTO laskuri (id, maara) VALUES (1, 0) ON CONFLICT (id) DO NOTHING")
    cur.execute("UPDATE laskuri SET maara = maara + 1 WHERE id = 1 RETURNING maara")
    maara = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return maara

PAGE = """<!DOCTYPE html>
<html lang="fi"><head><meta charset="UTF-8">
<title>Viikko 2 — Python ja tietokanta</title>
<style>
body { max-width: 700px; margin: 40px auto; padding: 0 20px;
       font-family: sans-serif; line-height: 1.6; background: #f0f4f8; color: #203040; }
h1, h2 { color: #005a8d; }
.laskuri { background: #fff; border: 2px solid #005a8d; border-radius: 8px;
           padding: 16px; text-align: center; font-size: 1.3em; }
.laskuri strong { font-size: 1.6em; color: #005a8d; }
code { background: #fff; padding: 2px 6px; border-radius: 4px; }
a { color: #005a8d; }
</style></head><body>
<h1>Viikko 2: Python-verkkosovellus ja tietokanta</h1>
<p class="laskuri">Tämä sivu on ladattu <strong>{{LASKURI}}</strong> kertaa.</p>
<h2>Tietokanta ja laskurin tallennus</h2>
<p>Käytetty tietokanta on <strong>PostgreSQL</strong>. Laskurin arvo on taulussa
<code>laskuri</code> sarakkeessa <code>maara</code>, ja jokainen sivun lataus
kasvattaa sitä komennolla <code>UPDATE laskuri SET maara = maara + 1</code>.
Koska arvo on tietokannassa levyllä, se säilyy uudelleenkäynnistyksistä.</p>
<h2>Uudelleenkäynnistystesti</h2>
<p>Virtuaalikone käynnistettiin uudelleen komennolla <code>sudo reboot</code>,
minkä jälkeen laskuri jatkoi aiemmasta arvostaan.</p>
<h2>Lähdekoodi</h2>
<p><a href="{{GITHUB}}">{{GITHUB}}</a></p>
</body></html>"""

@app.route("/")
def index():
    return PAGE.replace("{{LASKURI}}", str(kasvata())).replace("{{GITHUB}}", GITHUB_URL)
