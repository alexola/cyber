![alt text](logo.png)


A powerful, modular suite of Python-based cybersecurity tools. Built for learning, testing, and enhancing both offensive and defensive security skills that I have been learning and turning into a real-life project.


> ⚙️ This project was created as a hands-on journey to sharpen coding skills and to gain the confidence and capability to build custom cybersecurity tools from scratch.

---

## ✅ Completed Tools
  - [x] **Password Strength Checker**
  - [x] **Checks password complexity**
  - [x] **Optional entropy scoring**
  - [x] **Port Scanner /Normal & Stealth mode**
  - [X] **Subdomain Enumerator Working on Stealth mode**
  - [X] **Whois + DNS Recon Tool**

## 🚧 Tools in Progress
- [ ] **Simple Packet Sniffer**
- [ ] **IP Rotator / IP Hider**
- [ ] **Brute-Force Login Tool**
- [ ] **Malware Analysis Sandbox**
- [ ] **Log Analyzer for Intrusion Detection**
- [ ] **Simple Honeypot**
- [ ] **Payload Generator**

## 🛠️ Installation

Clone the repo:

```bash
git clone https://github.com/alexola/cyber.git
cd cyber
```

Install dependencies:

```bash
pip install -r requirements.txt
```
---

## 🔐 Password Strength Checker

✨ Features
ls

- Modular design: easily add new tools
- Menu-driven interface for easy tool selection
- Password strength checker with entropy scoring
- Clean codebase and repository hygieneevaluates the strength of user-provided passwords based on length, character variety, and more.

### Usage

```bash
python3 recon-suite/main.py
```
### Output Example

```
Enter your password: P@ssw0rd123!
Password Strength: Strong
Feedback: Good job! Try not to reuse this password across sites.
```

---

## 🌐 Subdomain Enumerator

Supports both normal and stealth modes.  
You can use your own wordlist with `-w` or `--wordlist`.

### Usage

```bash
python3 [subdomain_enumerator.py](http://_vscodecontentref_/1) example.com
```

### Output Example

```
[*] Loaded 1000 subdomain prefixes
[*] Enumerating subdomains for: example.com

[*] Found: www.example.com -> 93.184.216.34
[*] Found: mail.example.com -> 93.184.216.34
...
```

# Enhanced WHOIS and DNS Recon Tool

This tool is designed for performing WHOIS lookups and DNS reconnaissance on specified domains. It provides detailed information about domain registration and DNS records, making it useful for security assessments and domain investigations for educational purposes.

## Features

- WHOIS information retrieval, including registrar, creation date, expiration date, and name servers.
- DNS record lookup for various record types (A, AAAA, MX, NS, CNAME, TXT, SOA, SRV, CAA, NAPTR).
- Reverse DNS lookup for IP addresses.
- Option to output results in JSON format.

## Output in JSON Format

The tool can output results in JSON format, which is useful for integration with other tools or for easier data processing.

### How to Output Results in JSON

To output the results in JSON format, use the `--json` flag when running the tool. The output will include the domain information, WHOIS details, and DNS records structured in a JSON format.

### Example

1. **Run the tool with JSON output**:

   ```bash
   python dns-whois.py example.com --json

---

## 🧼 Repository Hygiene

To maintain a clean, efficient project, we’ve included a `.gitignore` file to exclude:

- Python bytecode & cache  
- Environment folders (`env/`, `venv/`)  
- OS clutter files (`.DS_Store`, `Thumbs.db`)  
- IDE configs (`.vscode/`, `.idea/`)  
- Logs, temp files, and backups  

> ➡️ See `.gitignore` for the full list

### 🤝 Contributing

As this is a learning-focused open project. Pull requests, issues, and suggestions are welcome the idea is to keep on growing this toolset .

So please feel free to fork the project, work on a feature/tool, and open a pull request. Even simple feedback is appreciated!

---

## 📜 License

MIT License — see the [`LICENSE`](LICENSE) file for full details.

---

### 👩‍💻 Author

**GitHub**: [alexola](https://github.com/alexola)

> ⚠️ **Note:**  
> To use the port scanner in **stealth mode**, you must run the program with administrator privileges:
> - On macOS/Linux: use `sudo python3 recon-suite/main.py`
> - On Windows: run your terminal as Administrator
>
> This is required for sending raw packets (SYN scans) with Scapy.
