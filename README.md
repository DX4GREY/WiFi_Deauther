# Wireless Network Scanner and Deauthentication Tool

This Python script serves as a wireless network scanner and deauthentication tool. It allows users to scan for available access points, select a target access point, and perform deauthentication attacks against it. Below is a breakdown of its functionalities:

## Features:

### 1. Interface Selection:
   - Users can select a wireless interface from available options for scanning and deauthentication.

### 2. Mode Configuration:
   - The script automatically switches the selected wireless interface to monitor mode using `airmon-ng`.

### 3. Access Point Scanning:
   - It continuously scans for nearby access points and displays them in real-time.
   - Access point information is saved in CSV format.

### 4. Access Point Selection:
   - Upon user interruption (Ctrl+C), the script presents a list of scanned access points for selection.

### 5. Channel Configuration:
   - Users can set the wireless interface channel based on the selected access point.

### 6. Deauthentication Attack:
   - Users can choose an access point to target and launch deauthentication attacks against it using `aireplay-ng`.

### 7. Clean-up:
   - Temporary CSV files generated during the scanning process are automatically removed.

## Implementation:

The script utilizes various Linux command-line tools such as `iwconfig`, `airmon-ng`, `airodump-ng`, and `aireplay-ng` to achieve its functionalities. It leverages Python's `subprocess` module for executing shell commands and `multiprocessing` for parallel processing.

The script also provides user-friendly interaction through console-based menus and prompts. Additionally, it utilizes the `colorama` library for adding colors to the console output to enhance readability.

## Usage:

Users need to run the script with administrative privileges (sudo) to access wireless interfaces and execute certain commands. Upon execution, users are guided through the interface selection, scanning, access point selection, and deauthentication process.

## Note:

- The script is designed for educational and testing purposes only. Unauthorized use against networks you don't own or have permission to test is illegal and unethical.
- It's essential to use this tool responsibly and in compliance with applicable laws and regulations.
