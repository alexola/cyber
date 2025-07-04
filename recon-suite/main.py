import subprocess
import os

#importing the tools to the main file
from modules import (password_checker) 

def launch_tool(tool_scripts):
    # Corrected path to modules inside recon-suite
    tool_path = os.path.join("recon-suite", "modules", tool_scripts)
    try:
        subprocess.run(["python3", tool_path])
    except Exception as e:
        print(f"Could not run tool: {e}")

def main():
  # Print ASCII art banner
  print(r"""
  [*] Initializing interface...
  [*] Loading modules...
  [*] Welcome back, operator. Time to recon.
      
██████   █████  ██    ██ ███████ ███    ██     ██████  ██    ██ ██      ███████ ███████ 
██   ██ ██   ██ ██    ██ ██      ████   ██     ██   ██ ██    ██ ██      ██      ██      
██████  ███████ ██    ██ █████   ██ ██  ██     ██████  ██    ██ ██      ███████ █████   
██   ██ ██   ██  ██  ██  ██      ██  ██ ██     ██      ██    ██ ██           ██ ██      
██   ██ ██   ██   ████   ███████ ██   ████     ██       ██████  ███████ ███████ ███████ 
        
            🛡️  Recon Suite - Aegis Hunter Toolkit 🔓                                                                                  
  """)
  while True:
    print("\nAvailable tools:")
    print("1. Password Checker - Check the strength of your passwords")
    print("2. Port Scanner - Scan for open ports on a target / stealth scan")
    print("3. Subdomain Enumerator - Enumerate subdomains for a given domain")
    print("0. Exit")

    #we should add a loop to keep the menu running until the user decides to exit
    choice = input("\nSelect a tool you want to run or type '0' to exit: ")
    try:
        if choice == '1':
            launch_tool("password_checker.py")
        elif choice == '2':
            launch_tool("port_scanner.py")
        elif choice == '3':
            launch_tool("subdomain_enumerator.py")
        elif choice == '0':
            print("Exiting Recon Suite. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Returning to menu...")

if __name__ == "__main__":
    main()

# This is the main entry point for the Recon Suite application.

