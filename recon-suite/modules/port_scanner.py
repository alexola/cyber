import socket #Use for port scanning
from datetime import datetime #To display the time of the scan starts and ends too.
from tqdm import tqdm #To display a progress bar during the port scanning process.
import warnings

warnings.filterwarnings("ignore", message="resource_tracker: There appear to be .* leaked semaphore objects")

def scan_ports(target, start_port=1, end_port=1024, mode="normal"):
    """
    Scans a range of ports on the target selected IP or hostname.
    
    Args:
    target (str): The target IP address or hostname to scan.
    start_port (int): The starting port number (default is 1).
    end_port (int): The ending port number (default is 1024).
    
    Returns:
    list: A list of open ports found during the scan.
    """

    open_ports = []

    if mode == "stealth":
        try:
            from scapy.all import IP, TCP, sr1, conf
            conf.verb = 0 # Suppres Scapy's output
        except ImportError: # If Scapy is not installed, we will print an error message and return an empty list.
            print("Scapy is required for stealth mode. Please install it with 'pip install scapy'.")
            return []
        

        print(f"Stealth scanning (SYN) scanning {target} from port {start_port} to {end_port}...")
        print(f"Stealth scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            for port in tqdm(range(start_port, end_port + 1), desc="Scanning ports", unit="port"):
                # Create an IP packet with a TCP SYN flag
                pkt = IP(dst=target)/TCP(dport=port, flags='S') # Create a TCP packet with SYN flag
                resp = sr1(pkt, timeout=1, verbose=0)  # Send the packet and wait for a response
                if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12: # If the response has a TCP layer and the flags indicate SYN-ACK
                    tqdm.write(f"Port {port} is open stealthily")  # Display the open port
                    open_ports.append(port)
        except KeyboardInterrupt: # User interrupts the scan
            print("\nStealth scan aborted by user. (Ctrl+C)")
            if open_ports: # If there are any open ports found before the scan was aborted will show up.
                print(f"\nOpen ports found so far: {open_ports}")
            else:
                print("No open ports found before the scan was aborted.")
            return open_ports  # Return the list of open ports found so far.
        print(f"\nStealth scan finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        if open_ports:
            print(f"\nOpen ports found stealthily: {open_ports}")
        else:
            print("No open ports found stealthily.")
        return open_ports

    #Normal mode port scanning
    try:
        print(f"Scanning {target} from port {start_port} to {end_port}...")
        print(f"Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        for port in tqdm(range(start_port, end_port + 1), desc="Scanning ports", unit="port"):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)  # Set a timeout for the connection attempt
            
            result = sock.connect_ex((target, port))  # Attempt to connect to the port

            if result == 0:  # If the connection was successful
                tqdm.write(f"Port {port} is open") #Display the open port
                open_ports.append(port)  # Saves the open port to the list

            sock.close()  # Close the socket connection

    except KeyboardInterrupt: # User interrupts the scan
        print("\nScan aborted by user. (Ctrl+C)") 
        if open_ports: # If there are any open ports found before the scan was aborted will show up.
            print(f"\nOpen ports found so far: {open_ports}")
        else:
            print("No open ports found before the scan was aborted.")
        return open_ports  # Return the list of open ports found so far.
    except socket.gaierror:  # If the target is not resolvable0
        print("Hostname could not be resolved. Please check the target IP or hostname.")
    except socket.error:  # If there is a socket error
        print("Could not connect to server. It might be down.")
    
    print(f"\nScan finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if open_ports:
        print(f"\nOpen ports: {open_ports}")
    else:
        print("No open ports found.")  # Return the list of open ports found during the scan.
    return open_ports


if __name__ == "__main__":
    target_input = input("Enter the target IP address or hostname: ").strip()
    while not target_input:
        target_input = input("Target cannot be empty. Enter the target IP address or hostname: ").strip()
    mode_input = input("Select scan mode - normal or stealth [n/s]: ").strip().lower()
    while mode_input not in ('n', 's'):
        mode_input = input("\nInvalid input. Select scan mode - normal or stealth [n/s]: ").strip().lower()
    if mode_input == 's':
        scan_ports(target_input, mode="stealth")
    else:
        scan_ports(target_input, mode="normal")
