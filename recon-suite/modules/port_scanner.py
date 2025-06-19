import socket #Use for port scanning
from datetime import datetime #To display the time of the scan starts and ends too.
from tqdm import tqdm #To display a progress bar during the port scanning process.

def scan_ports(target, start_port=1, end_port=1024):
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

    try:
        print(f"Scanning {target} from port {start_port} to {end_port}...")
        print(f"Scan started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        for port in tqdm(range(start_port, end_port + 1), desc="Scanning ports", unit="port"):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Set a timeout for the connection attempt
            
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
    except socket.gaierror:  # If the target is not resolvable
        print("Hostname could not be resolved. Please check the target IP or hostname.")
    except socket.error:  # If there is a socket error
        print("Could not connect to server. It might be down.")
    
    print(f"\nScan finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if open_ports:
        print(f"\nOpen ports: {open_ports}")
    else:
        print("No open ports found.")  # Return the list of open ports found during the scan.
    return open_ports

if __name__ == "__main__": # This is the main entry point for the port scanner module.
    target_input = input("Enter the target IP address or hostname: ")
    scan_ports(target_input)