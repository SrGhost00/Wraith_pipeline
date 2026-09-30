import sqlite3, requests
from datetime import datetime

DB="projeto_wraith.db"
# Brasil inteiro: norte,sul,oeste,leste
BOUNDS="-5,-35,-75,-30"
URL=f"https://data-cloud.flightradar24.com/zones/fcgi/feed.js?bounds={BOUNDS}&faa=1&satellite=1&mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=14400&gliders=1&stats=1"

def init_db():
    con=sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS voos_fr24 (coletado_em TEXT, flight_number TEXT, origin TEXT, destination TEXT, latitude REAL, longitude REAL, altitude INTEGER)")
    con.commit(); con.close()

def coletar():
    headers={
        "User-Agent":"Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36",
        "Accept":"application/json",
        "Origin":"https://www.flightradar24.com",
        "Referer":"https://www.flightradar24.com/"
    }
    print("Buscando...")
    r=requests.get(URL, headers=headers, timeout=20)
    print(f"Status: {r.status_code} | Tamanho: {len(r.text)} bytes")
    data=r.json()
    print(f"Keys: {list(data.keys())[:5]} | full_count: {data.get('full_count')}")

    rows=[]
    for k,v in data.items():
        if k in ["full_count","version","stats"]: continue
        if isinstance(v, list) and len(v)>=12:
            # v[1]=lat, v[2]=lon, v[4]=alt, v[11]=orig, v[12]=dest, v[16]=flight
            flight = str(v[16]) if len(v)>16 else k
            rows.append((datetime.now().isoformat(), flight, v[11], v[12], v[1], v[2], v[4]))

    print(f"{len(rows)} voos no Brasil")
    if rows:
        con=sqlite3.connect(DB)
        con.executemany("INSERT INTO voos_fr24 VALUES (?,?,?,?,?,?,?)", rows[:150])
        con.commit()
        c=con.execute("SELECT COUNT(*) FROM voos_fr24").fetchone()[0]
        con.close()
        print(f"-> {len(rows[:150])} salvos | TOTAL no banco: {c}")
    else:
        print("Veio vazio - provavelmente Cloudflare. Vamos tentar OpenSky (backup)")
        # FALLBACK OPENSKY - funciona 100% no Termux
        r2=requests.get("https://opensky-network.org/api/states/all?lamin=-35&lomin=-75&lamax=-5&lomax=-30", timeout=20)
        j=r2.json()
        states=j.get("states",[]) or []
        print(f"OpenSky: {len(states)} voos")
        if states:
            con=sqlite3.connect(DB)
            for s in states[:150]:
                # s[1]=callsign, s[5]=lon, s[6]=lat, s[7]=alt
                con.execute("INSERT INTO voos_fr24 VALUES (?,?,?,?,?,?,?)", (datetime.now().isoformat(), s[1].strip(), "", "", s[6], s[5], int(s[7] or 0)))
            con.commit(); con.close()
            print("Salvo via OpenSky!")

init_db()
coletar()
