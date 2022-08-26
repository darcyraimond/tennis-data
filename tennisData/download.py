from email.mime import base
from termcolor import colored
import os
import requests


clr = "\033[K"


def requestToFile(request, path: str):

    
    content = str(request.content)
    content = content.replace("\\'", "'").split("\\n")
    out = ""
    for line in content:
        if len(line) < 5: continue
        if line[0:2] == "b'": line = line[2:]
        if line[0:2] == 'b"': line = line[2:]
        out += line
        out += "\n"

    out = out[:-1]

    file = open(path, "w+")
    file.write(out)
    file.close()


def downloadFiles(
    silent=False, 
    players=True, 
    tourSingles=True, 
    amaetur=False, 
    doubles=False, 
    futures=False, 
    qualChall=False, 
    rankings=False
):
    
    try:
        base = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master"
        folder = "tennis_atp-master"

        # Diagnose issues here (run this so network error caught before old data folder can be deleted)
        data = requests.get(f"{base}/atp_players.csv")
        os.system(f"rm -rf {folder}")
        os.system(f"mkdir {folder}")

        # Get player data
        data = requests.get(f"{base}/atp_players.csv")
        if players:
            print(colored(f"{clr}Up to atp_players.csv", "blue"), end="\r")
            requestToFile(data, f"{folder}/atp_players.csv")
            print(colored(f"{clr}Downloaded player data", "green"))

        # Tour singles
        if tourSingles:
            year = 1968
            fileName = f"atp_matches_{year}.csv"
            data = requests.get(f"{base}/{fileName}")
            while data.status_code == 200:
                if not silent:
                    print(colored(f"{clr}Up to file: {fileName}", "blue"), end = "\r")
                requestToFile(data, f"{folder}/{fileName}")
                year += 1
                fileName = f"atp_matches_{year}.csv"
                data = requests.get(f"{base}/{fileName}")
            print(colored(f"{clr}Downloaded main tour match data 1968-{year-1}", "green"))

        # Amateur
        if amaetur:
            print(colored(f"{clr}Up to atp_matches_amateur.csv", "blue"), end="\r")
            requestToFile(data, f"{folder}/atp_matches_amateur.csv")
            print(colored(f"{clr}Downloaded pre-open (amateur) main tour match data", "green"))

        # Doubles
        if doubles:
            year = 2000
            fileName = f"atp_matches_doubles_{year}.csv"
            data = requests.get(f"{base}/{fileName}")
            while data.status_code == 200:
                if not silent:
                    print(colored(f"{clr}Up to file: {fileName}", "blue"), end = "\r")
                requestToFile(data, f"{folder}/{fileName}")
                year += 1
                fileName = f"atp_matches_doubles_{year}.csv"
                data = requests.get(f"{base}/{fileName}")
            print(colored(f"{clr}Downloaded doubles match data 2000-{year-1}", "green"))

        # Futures
        if futures:
            year = 1991
            fileName = f"atp_matches_futures_{year}.csv"
            data = requests.get(f"{base}/{fileName}")
            while data.status_code == 200:
                if not silent:
                    print(colored(f"{clr}Up to file: {fileName}", "blue"), end = "\r")
                requestToFile(data, f"{folder}/{fileName}")
                year += 1
                fileName = f"atp_matches_futures_{year}.csv"
                data = requests.get(f"{base}/{fileName}")
            print(colored(f"{clr}Downloaded futures match data 1991-{year-1}", "green"))

        # Qualifiers/Challengers
        if qualChall:
            year = 1978
            fileName = f"atp_matches_qual_chall_{year}.csv"
            data = requests.get(f"{base}/{fileName}")
            while data.status_code == 200:
                if not silent:
                    print(colored(f"{clr}Up to file: {fileName}", "blue"), end = "\r")
                requestToFile(data, f"{folder}/{fileName}")
                year += 1
                fileName = f"atp_matches_qual_chall_{year}.csv"
                data = requests.get(f"{base}/{fileName}")
            print(colored(f"{clr}Downloaded qualifiers/challengers match data 1978-{year-1}", "green"))


        # Rankings
        if rankings:
            year = 1970
            fileName = f"atp_rankings_{str(year)[2:]}s.csv"
            data = requests.get(f"{base}/{fileName}")
            while data.status_code == 200:
                if not silent:
                    print(colored(f"{clr}Up to file: {fileName}", "blue"), end = "\r")
                requestToFile(data, f"{folder}/{fileName}")
                year += 10
                fileName = f"atp_rankings_{str(year)[2:]}s.csv"
                data = requests.get(f"{base}/{fileName}")

            fileName = "atp_rankings_current.csv"
            if not silent:
                print(colored(f"{clr}Up to file: {fileName}", "blue"), end = "\r")
            data = requests.get(f"{base}/{fileName}")
            requestToFile(data, f"{folder}/{fileName}")
            print(colored(f"{clr}Downloaded rankings data 1970s-{year-10}s", "green"))


        
    except requests.exceptions.ConnectionError:
        raise Exception(colored("Unable to establish connection. Consider using pre-downloaded data if connection is unavailable.", "red"))

