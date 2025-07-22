import argparse
import socket
import dns.resolver
import whois
import subprocess
import json

def get_whois_info(domain):
    if domain.endswith(".es"):
        print("[!] WHOIS lookup skipped for .es domains.")
        print(f"    https://www.whois.com/whois/{domain}")
        return {"domain": domain, "whois": "(WHOIS skipped — restricted TLD)"}
    try:
        w = whois.whois(domain)
        if all(v is None for v in w.values()):
            print("[!] WHOIS module returned no data. Trying CLI fallback...")
            return fallback_whois_cli(domain)
        return filter_whois_fields(w)
    except Exception as e:
        print(f"[!] WHOIS module failed: {e}")
        return fallback_whois_cli(domain)

def filter_whois_fields(whois_data):
    fields = ["domain_name", "registrar", "creation_date", "expiration_date", "updated_date", "status", "name_servers"]
    result = {}
    for field in fields:
        val = whois_data.get(field)
        if val:
            if isinstance(val, list):
                val = list(set(str(v) for v in val if v))
            elif not isinstance(val, str):
                val = str(val)
            result[field] = val
    return result

def fallback_whois_cli(domain):
    try:
        output = subprocess.check_output(["whois", domain], stderr=subprocess.DEVNULL).decode()
        parsed = {}
        for line in output.splitlines():
            if "Registrar:" in line:
                parsed["registrar"] = line.split(":", 1)[1].strip()
            elif "Creation Date:" in line or "Created On:" in line:
                parsed["creation_date"] = line.split(":", 1)[1].strip()
            elif "Expiration Date:" in line or "Registry Expiry Date" in line:
                parsed["expiration_date"] = line.split(":", 1)[1].strip()
            elif "Updated Date:" in line:
                parsed["updated_date"] = line.split(":", 1)[1].strip()
            elif "Name Server:" in line:
                ns = line.split(":", 1)[1].strip()
                parsed.setdefault("name_servers", []).append(ns)
        parsed["domain"] = domain
        return parsed
    except Exception as e:
        return {"domain": domain, "whois": f"(WHOIS CLI lookup failed: {e})"}

def get_dns_records(domain):
    records = {}
    record_types = ["A", "AAAA", "MX", "NS", "CNAME", "TXT", "SOA", "SRV", "CAA", "NAPTR"]
    resolver = dns.resolver.Resolver()
    resolver.timeout = 3
    resolver.lifetime = 3
    resolver.nameservers = ["8.8.8.8", "1.1.1.1"]

    for rtype in record_types:
        try:
            answers = resolver.resolve(domain, rtype)
            recs = [ans.to_text() for ans in answers]
            if rtype == "SOA" and recs:
                rname = answers[0].rname.to_text().replace('.', '@', 1)
                recs.append(f"SOA Email: {rname}")
            records[rtype] = recs
        except Exception:
            records[rtype] = []

    # Add reverse DNS lookup for A and AAAA
    reverse_dns = {}
    for ip in records.get("A", []) + records.get("AAAA", []):
        rev = reverse_dns_lookup(ip)
        if rev:
            reverse_dns[ip] = rev
    if reverse_dns:
        records["REVERSE_DNS"] = reverse_dns

    return records

def reverse_dns_lookup(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None

def clean_for_json(data):
    if isinstance(data, dict):
        return {k: clean_for_json(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_for_json(i) for i in data]
    elif hasattr(data, 'isoformat'):
        return data.isoformat()
    else:
        return data

def main():
    parser = argparse.ArgumentParser(description="Enhanced WHOIS and DNS Recon Tool")
    parser.add_argument("domain", nargs='?', type=str, help="Target domain (example.com)")
    parser.add_argument("--json", action="store_true", help="Print output in JSON format")
    args = parser.parse_args()

    # If no domain is provided as an argument, prompt the user for input
    if not args.domain:
        args.domain = input("Please enter the target domain (example.com): ")

    # Remove 'www.' if present for root domain lookups
    domain = args.domain
    if domain.startswith("www."):
        domain = domain[4:]
    print(f"\n[*] Recon for: {domain}")

    # Get WHOIS and DNS info
    whois_info = get_whois_info(domain)
    dns_info = get_dns_records(domain)

    # Output results
    if args.json:
        output = {
            "domain": domain,
            "whois": clean_for_json(whois_info),
            "dns": dns_info
        }
        print(json.dumps(output, indent=2))
    else:
        print("\n[+] WHOIS Information:")
        for key, value in whois_info.items():
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  {item}")
            else:
                print(f"{key}: {value}")

        print("\n[+] DNS Records:")
        for rtype, recs in dns_info.items():
            if isinstance(recs, dict):  # reverse DNS
                print(f"{rtype}:")
                for ip, host in recs.items():
                    print(f"  {ip} => {host}")
            elif recs:
                print(f"{rtype}:")
                for rec in recs:
                    print(f"  {rec}")
            else:
                print(f"{rtype}: (No records found)")

if __name__ == "__main__":
    main()
