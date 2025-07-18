import argparse
import socket
import dns.resolver
import whois

def get_whois_info(domain): #Function to get WHOIS information for a given domain
  try:
    w = whois.whois(domain) #Use the whois library to get WHOIS information
    return w
  except Exception as e:
    print(f"[!] WHOIS lookup failed for {domain}; {e}")
    print("[!] This may be due to network issues, TLD restrictions, or rate limiting.")
    return None
  
def get_dns_records(domain):  # Function to get DNS records for a given domain
    records = {}
    record_types = ["A", "AAAA", "MX", "NS", "CNAME", "TXT", "SOA"]
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            if rtype == "SOA":
                soa = answers[0]
                # Convert rname to email format
                rname = soa.rname.to_text().replace('.', '@', 1)
                records[rtype] = [soa.to_text(), f"SOA email: {rname}"]
            else:
                records[rtype] = [ans.to_text() for ans in answers]
        except Exception as e:
            print(f"[!] DNS lookup failed for {domain} ({rtype}); {e}")
            records[rtype] = [f"Error: {e}"]
    return records

def main():
  parser = argparse.ArgumentParser(description="WHOIS and DNS Recon Tool")
  parser.add_argument("domain", type=str, help="Target domain (example.com)")
  args = parser.parse_args()

  domain = args.domain
  if domain.startswith("www."):
      domain = domain[4:]

  print(f"\n[*] WHOIS information for  {domain}:")
  whois_info = get_whois_info(domain)
  if whois_info:
    for key, value in whois_info.items():
      print(f"{key}: {value}")

  print(f"\n[*] DNS records for  {domain}:")
  dns_info = get_dns_records(domain)
  for rtype, records in dns_info.items():
    print(f"{rtype}:")
    for rec in records:
        print(f" {rec}")

if __name__ == "__main__":
  main()



