
# Volební scraper

Skript pro stažení výsledků voleb z [volby.cz](https://www.volby.cz) a jejich uložení do CSV.

---

## Instalace

```bash
# Stažení repozitáře
git clone <adresa-repozitare>
cd projekt-volebni-scraper

# Instalace závislostí
pip install -r requirements.txt

Soubor requirements.txt obsahuje:
requests
beautifulsoup4

Spuštění skriptu
python main.py <URL> <soubor.csv>

Parametry
URL – odkaz na okres z webu volby.cz (např. Prostějov, Brno-město, …)
soubor.csv – název výstupního CSV souboru

Příklad použití
Stažení výsledků pro okres Prostějov:
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7106" vysledky_prostejov.csv

Ukázka výstupu
code,location,registred,envelopes,valid,Občanská demokratická strana,Česká str.sociálně demokrat.,...
589309,Atlachov,531,321,318,54,102,...
589317,Bedihošť,943,633,628,84,176,...
