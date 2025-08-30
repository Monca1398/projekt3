"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Monika Mendlíková
email: mendlikova.monika@gmail.com
"""

import requests
from bs4 import BeautifulSoup
import csv
import sys
import time


#základní adresa webu
BASE_URL = "https://www.volby.cz/pls/ps2017nss/"


#najde odkazy na obce z úvodní stránky okresu
def get_municipality_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # vrací dvojice (kód obce, odkaz na obec)
    return [(a.text.strip(), BASE_URL + a["href"]) for a in soup.select(".cislo a")]


#z detailu obce vytáhne název obce
def extract_location_name(soup):
    h3_tags = soup.select("h3")
    for h3 in h3_tags:
        text = h3.get_text(strip=True)
        if text.startswith("Obec:"):
            return text.replace("Obec:", "").strip()
    return "NO VILLAGE FOUND"


#z detailu obce vytáhne počty voličů, obálek a platných hlasů
def extract_main_numbers(soup):
    voters = soup.select_one('td[headers="sa2"]').text.strip()
    envelopes = soup.select_one('td[headers="sa3"]').text.strip()
    valid_votes = soup.select_one('td[headers="sa6"]').text.strip()
    return voters, envelopes, valid_votes


#z detailu obce vytáhne hlasy pro jednotlivé strany
def extract_party_votes(soup):
    # první tabulka stran
    party_names = soup.select(".overflow_name")
    vote_counts = soup.select('[headers="t1sa2 t1sb3"]')

    #druhá tabulka stran
    party_names2 = soup.select('td[headers="t2sa1 t2sb2"]')
    vote_counts2 = soup.select('td[headers="t2sa2 t2sb3"]')

    #spojení obou tabulek
    all_party_names = party_names + party_names2
    all_vote_counts = vote_counts + vote_counts2

    result = {}
    order = []

    #vytvoří slovník {název_strany: počet_hlasů}
    for party, votes in zip(all_party_names, all_vote_counts):
        name = party.get_text().strip()
        count = votes.get_text().strip()
        result[name] = count
        order.append(name)

    return result, order


#stáhne a zpracuje data pro konkrétní obec
def parse_municipality_data(code, link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, "html.parser")

    name = extract_location_name(soup)
    voters, envelopes, valid = extract_main_numbers(soup)
    party_votes, parties = extract_party_votes(soup)

    #vytvoření řádku pro CSV
    row = {
        "code": code,
        "location": name,
        "registered": voters,
        "envelopes": envelopes,
        "valid": valid,
    }
    row.update(party_votes)  #přidání hlasů pro strany
    return row, parties


#uloží výsledky do CSV souboru
def save_to_csv(data_list, parties_order, output_filename):
    with open(output_filename, mode="w", newline="", encoding="windows-1250") as file:
        fieldnames = ["code", "location", "registred", "envelopes", "valid"] + parties_order
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data_list:
            writer.writerow(row)


#hlavní funkce pro stažení a uložení výsledků
def get_url(url, output_filename):
    print("CHECKING URL AND FILE NAME")
    print(f"DOWNLOADING DATA FROM GIVEN URL: {url}")

    start_time = time.time()

    links = get_municipality_links(url)  #odkazy na všechny obce v okrese
    data_list = []
    all_parties = []

    #zpracování všech obcí
    for code, link in links:
        row, parties = parse_municipality_data(code, link)
        data_list.append(row)
        for p in parties:
            if p not in all_parties:  #zachová pořadí stran
                all_parties.append(p)

    #uložení výsledků do CSV
    save_to_csv(data_list, all_parties, output_filename)

    end_time = time.time()
    print(f'DATA SUCCESSFULLY DOWNLOADED AND SAVED TO \"{output_filename}\"')
    print(f"DOWNLOAD TOOK {round(end_time - start_time, 2)} SECONDS")
    print("CLOSING main.py")


#spuštění programu z příkazové řádky
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python main.py <URL> <název_souboru.csv>")
        sys.exit(1)

    input_url = sys.argv[1]
    output_file = sys.argv[2]
    get_url(input_url, output_file)
