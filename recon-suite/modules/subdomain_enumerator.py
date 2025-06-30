import argparse
import concurrent.futures #For threading and multiprocessing
import dns.resolver # dnspython does the DNS lookups
from pathlib import Path  #For file path handling
from tqdm import tqdm #Progress bar for the enumeration process

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

def enumerate_domain(domain: str, prefixes: list[str], threads: int = 50): #Function to enumerate subdomains for a given domain
    found = {}
    resolver_obj = dns.resolver.Resolver() #Create a resolver object
    resolver_obj.timeout = 2
    resolver_obj.lifetime = 2

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as pool: #Make a thread pool to resolve subdomains
        tasks = {
            pool.submit(resolve_domain, sub, domain, resolver_obj): sub for sub in prefixes
        }
        for future in tqdm(concurrent.futures.as_completed(tasks), total=len(tasks), desc="Enumerating"):
            result = future.result()
            if result:
                host, ips = result
                found[host] = ips
                tqdm.write(f"[*] Found: {host} -> {', '.join(ips)}") # Print the found subdomain and its IPs addresses
    return found

def main(): #Main function to parse arguments and run the subdomain enumeration
    parser =argparse.ArgumentParser(description="Subdomain Enumerator")
    parser.add_argument("domain", type=str, nargs="?", help="Root domain (e.g., example.com )")
    parser.add_argument(
        "-w", "--wordlist",
        type=Path,
        help="Path to subd-domain wordlist (default: utils/wordlists/subdomain.txt)",
    )
    parser.add_argument( #Argument for number of threads to use.Threads are used to speed up the enumeration process
        "-t", "--threads",
        type=int, default=50,
        help="Number of threads to use for enumeration (default:50)"
    )
    args = parser.parse_args()

    if not args.domain:
        args.domain = input("Enter the root domain (e.g., example.com): ").strip()

    if args.wordlist is None:
        args.wordlist = Path(__file__).parent.parent / "utils" / "wordlists" / "subdomain.txt"

    if not args.wordlist.exists():
        print(f"[!] Wordlist file not found: {args.wordlist}")
        return

    prefixes = load_wordlist(args.wordlist)  # Load the wordlist
    print(f"[*] Loaded {len(prefixes)} subdomains prefixes")
    print(f"[*] Enumerating subdomains for: {args.domain}\n")

    enumerate_domain(args.domain, prefixes, threads=args.threads)

if __name__ == "__main__":
    main()