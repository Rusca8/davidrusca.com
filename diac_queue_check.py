import requests
from tele import send_message

if __name__ == "__main__":
    lenq = requests.get('https://www.davidrusca.com/hooks/diacriptic/queue_check')

    if lenq.status_code != 200:
        send_message("archi", "yo", "Els diacríptics no em volen dir si n'hi ha, em temo.")
    else:
        lenq = int(lenq.json())

        mins = {"first": 40, "second": 20, "worry": 10, "panic": 5}

        print(f"Checking diac queue length...\nCurrently {lenq} on queue.")
        if lenq == mins["first"]:
            send_message("archi", "yo", f"Hauria de posar Diacríptics nous a la llista, senyoria.\nEn queden {lenq}.")
        elif lenq == mins["second"]:
            send_message("archi", "yo", f"⚠️ Senyoria, no va posar Diacríptics. S'estan gastant.\nEn queden *{lenq}*.")
        elif lenq == mins["worry"]:
            send_message("archi", "yo",
                         f"⚠️ Queden molt pocs diacríptics, excel·lència. *Només {lenq}.*\nPotser que s'espavil·li.")
        elif lenq <= mins["panic"]:
            send_message("archi", "yo",
                         f"🚨⚠⚠️ ELS DIACRÍPTICS S'ESTAN ESGOTANT. FACI ALGUNA COSA, SISPLAU LI HO DEMANO.\nEN QUEDEN {lenq}.")
        else:
            print("No need to wake up Archibald.")
