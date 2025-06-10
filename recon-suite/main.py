# Import the argparse module to handle command-line arguments
import argparse
import subprocess
import os

#importing the tools to the main file
from modules import (password_checker) 

def launch_tool(tool_scripts):
  #Launch a tool script from the modules directory
  tool_path = os.path.join("modules", tool_scripts)
  try:
    subprocess.run(["python3", tool_path])
  except Exception as e:
    print(f"Could not run tool: {e}")

def main():
  # Create the argument parser
  parser = argparse.ArgumentParser(description="🛠️ Recon Suite - Cybersecurity Tools")
  subparsers = parser.add_subparsers(dest="tool", help="Available tools")
  
  # Add subparsers for each tool
  subparsers.add_parser("password_checker", help="Run the  password strength checker tool")

  args = parser.parse_args()


  if args.tool == "password_checker":
    # Call the password checker tool
    launch_tool("password_checker.py")
  else:
    print("Please specify a valid tool. Available tools: password_checker")

if __name__ == "__main__":
    main()
# This is the main entry point for the Recon Suite application.