import argparse
import concurrent.futures #For threading and multiprocessing
import dns.resolver # dnspython does the DNS lookups
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

def resolve_domain(sub: str, domain: str, resolver_obj: dns.resolver.Resolver): #Function to resolve a subdomain if it has an A record
    full_domain = f"{sub}.{domain}"
    try:
        #We only care if an "A" record exists for the subdomain
        answers = resolver_obj.resolve(full_domain, "A", lifetime=2)
        ips = [rdata.address for rdata in answers] #If resolve didnt raise an exception, the subdomain has an A record
        return full_domain, ips
    except (dns.resolver.NXDOMAIN,  #Domain does not exist
            dns.resolver.NoAnswer,  #No A record found
            dns.resolver.Timeout,
            dns.exception.DNSException): #Invalid DNS response
      return None

if __name__ == "__main__": # Main entry point for the subdomain enumerator module
    from pathlib import Path
    wordlist_path = Path(__file__).parent.parent / "utils" / "wordlists" / "subdomain.txt"
    subdomains = load_wordlist(wordlist_path)
    # Test resolve_domain on the first subdomain (if any)
    if subdomains:
        test_domain = "google.com"  # Change to a real domain for real results
        resolver = dns.resolver.Resolver()
        result = resolve_domain(subdomains[0], test_domain, resolver)
        if result:
            full_domain, ips = result
            print(f"[+] {full_domain} resolves to: {ips}")
        else:
            print(f"[-] {subdomains[0]}.{test_domain} did not resolve.")