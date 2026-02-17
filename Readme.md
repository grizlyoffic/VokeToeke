# Free Fire Access Token Tool

A simple tool to generate or use Free Fire (FF) access tokens — mainly used for guest ID banning or similar automation tasks.

> **Disclaimer**  
> This tool is for **educational purposes only**.  
> Using it to harm accounts, violate Garena's terms of service, or perform unauthorized actions may result in permanent bans or legal consequences.  
> Use at your own risk.

## Features

- Generate access token using `access.py` (for guest IDs / alternate method)
- Use your own **already generated access token** directly in `main.py`
- Simple command-line interface

## Requirements

- Termux (recommended) or Linux / any Python-supported environment
- Python 3.8+

## Installation

Open Termux (or your terminal) and run these commands one by one:

```bash
# Update & upgrade packages (optional but recommended)
pkg update && pkg upgrade -y

# Install Python
pkg install python -y

# Install git (if you haven't cloned yet)
pkg install git -y

# Clone this repository (change URL to your actual repo)
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name

# Install all required Python packages
pip install -r requirements.txt