from flask import Flask, render_template, request   #Importa Flask base program in render template za "podajanje/prikazovanje" html datotek ter request featurje
import sqlite3 # Importa Sqlite3

app = Flask(__name__)

@app.route('/hello/')           
def hello_world():
    return "Hello world! Stran deluje."

def setup_databaseFUN(): #Funkcija za povezavo na test.db file sqlite 
    conn = sqlite3.connect("test.db") 
    cursor = conn.cursor()
    
    # SQL ukaz za ustvarjanje tabele contacts, če ta še ne obstaja. Ker navodila sem geslo pustil kot last_name
    create_table = """
    CREATE TABLE IF NOT EXISTS uporabniki (
     contact_id INTEGER PRIMARY KEY,
     first_name TEXT NOT NULL,
     last_name TEXT NOT NULL
    );
    """
    cursor.execute(create_table)
    conn.commit()
    conn.close()

@app.route('/login/') #Network path za logiranje in funkcija zanj. Vrne corresponding html file.
def loginFUN():
    return render_template('/login.html/')

@app.route('/login-submit/') #network path in funkcija, ki se odpre ko submittamo podatke na login filepathu
def form_submitFUN():
    uporabnisko_ime = request.args.get("username") # Pobere podatke
    geslo = request.args.get("geslo")
    
    conn = sqlite3.connect("test.db") # Se poveže na test.db sqlite fil
    cursor = conn.cursor()
    
    query = "SELECT contact_id FROM uporabniki WHERE first_name = ? AND last_name = ?;" # Poišče ujemajoči name in last_name (password)
    
    cursor.execute(query, (uporabnisko_ime, geslo)) #Dejansko executa query ukaz zgoraj in poslje podatke preko spremenljivk 
    
    match = cursor.fetchone() # Če najde rezultat oz. več njih vrne prvega
    
    conn.close() # Zapre povezavo z bazo
    
    if match: # If stavek ki javi da je ali ni uspelo glede na če se najde zgoraj match
        return "<h1>Prijava USPELA! Dobrodošel/a!</h1>"
    else:
        return render_template("login.html", info_text="Prijava NI uspela. Preverite podatke in poizkusite znova.") # Damo nazaj isti page samo z dodanim tekstom da ni slo skozi.

@app.route('/register/') #Network path za registracijo in funkcija zanj. Vrne corresponding html file.
def registerFUN():
    return render_template("register.html")

@app.route('/register-submit/') #Network path za submit registracije. Pošlje podatke v podatkovno bazo.
def register_submit():
    uporabnisko_ime = request.args.get("username")
    geslo = request.args.get("geslo")
    insert_command = 'INSERT INTO uporabniki(first_name, last_name) VALUES(?, ?);'
    
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(insert_command, (uporabnisko_ime, geslo)) #Poda vnesena atributa up. ime in geslo dejansko v tabelo preko execute ukaza, ki excuta vsebino spremenljivke "insert_command" 
    conn.commit()
    conn.close()
    
    return f"<h1>Registracija USPELA!</h1><p>Uporabnik '{uporabnisko_ime}' je shranjen. Zdaj se lahko prijavite na <a href='/login/'>Prijavni strani</a></p>" #Izpise sporocilo da se registracija uspesna.



@app.route('/view_db/')     #Network filepath za ogled podatkov v podatkovni bazi in funkcija zanj
def view_dbFUN():
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute("select * from uporabniki;") # Skratka "Pokaži vse podatke z vseh stolpcev tabele uporabniki"
    
    rezultati = cursor.fetchall()  #fetchall() vrne tuples, Flask jih prikaže kot tekst
    conn.close()
    
    return str(rezultati)







if __name__ == '__main__':
    setup_databaseFUN() # Klic za pripravo baze!
    app.run(debug=True)
