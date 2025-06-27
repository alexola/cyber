import argparse
import concurrent.futures #For threading and multiprocessing
#import dns.resolver # dnspython does the DNS lookups
from pathlib import Path 

#Load the wordlist of the subdomain prefixes

def load_wordlist(wordlist_path) -> list[str]: #expect a list of subdomains
    """
    Read a file containing subdomains, one per line.
    """
    subs = []
    with wordlist_path.open("r", encoding="utf-8") as f:  
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                subs.append(line)
    return subs

if __name__ == "__main__": # Main entry point for the subdomain enumerator module
    wordlist_path = Path("../utils/wordlists/subdomain.txt")
    subdomains = load_wordlist(wordlist_path)
    print(f"Loaded {len(subdomains)} subdomains from {wordlist_path}")
    for sub in subdomains:
        print(f"Subdomain: {sub}")