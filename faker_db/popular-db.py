from faker import Faker
import sqlite3
import random
from datetime import datetime, timedelta

faker = Faker('pt_BR')

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 25)

conn = sqlite3.connect('Guaratingueta.db')
c = conn.cursor()

c.execute("SELECT * FROM cepaberto WHERE Rua is NOT NULL")
guaratinguetDB = c.fetchall()
c.close()

appDB = sqlite3.connect("app.db")
c = appDB.cursor()

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 25)

lastID = c.execute("SELECT MAX(id) FROM occurrences").fetchone()[0]

if lastID == None:
    lastID = 0

for i in range(800):
    nome = faker.name()
    telefone = faker.msisdn().replace('55', '')
    create_date = faker.date_time_between(
        start_date=start_date, end_date=end_date)
    numero_rua = faker.random_int(min=1, max=999)
    email = faker.email()

    tipomanifest = random.choice(['denuncia', 'contaminacao', 'visita'])
    if tipomanifest == 'contaminacao':
        valortipomanifest = random.choices(
            ['dengue', 'zika', 'chikungunya', 'febreamarela'], [0.85, 0.1, 0.05, 0.005])[0]
    elif tipomanifest == 'visita':
        valortipomanifest = random.choices(['manha', 'tarde'], [0.8, 0.2])[0]
    else:
        valortipomanifest = ""

    address = random.choice(guaratinguetDB)
    cep = address[0]
    rua = address[1]
    bairro = address[2]
    lat = address[3]
    long = address[4]

    sms = random.choice([1, 0])

    c.execute('INSERT INTO occurrences (id, create_date, name, email, tel, tipomanifest, valortipomanifest, rua, numero, bairro, cep, sms, lat, long) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
              (lastID+i+1, create_date, nome, email, telefone, tipomanifest, valortipomanifest, rua, numero_rua, bairro, cep, sms, lat, long))

    appDB.commit()

c.close()
