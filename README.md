# Site Checker with Time Scheduling
Site Checker with Time Scheduling - An application that attempts to connect to a website or server every so many minutes or a given time and check if it is up. If it is down, it will notify you by email or by posting a notice on screen.
---

A powerful, easy-to-use website and server monitoring tool with GUI, email alerts, logging, and multi-site support.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- **Graphical User Interface** (Tkinter) — no command line needed
- **Monitor multiple websites/servers** simultaneously
- **Dual Check Methods**: HTTP status + ICMP Ping
- **Email Notifications** on downtime (Gmail and most SMTP providers supported)
- **Config File Support** (`config.json`) — settings are saved automatically
- **Detailed Logging** to console + `site_checker.log`
- **Background Monitoring** with Start/Stop controls
- Lightweight and cross-platform (Windows, macOS, Linux)

## Installation

1. **Clone or download** the project:
   ```bash
   git clone https://github.com/iamaryanbhalsing/Site-Checker-with-Time-Scheduling
   cd site-checker
   ```

2. **Install dependencies:**
   ```bash
   pip install requests
   ```

3. **Run the application:**
   ```bash
   python site_checker_gui.py
   ```

## Usage

Adding Sites

Enter a URL (e.g. https://example.com or google.com)
Check "Use Ping" for server reachability testing
Click Add Site

Starting Monitoring

Set check interval (minutes)
Configure email notifications (optional)
Click Start Monitoring

Email Setup (Recommended)

Use Gmail App Password (not your regular password)
Enable 2-Factor Authentication on your Google account
Generate App Password at: Google Account → Security → App Passwords
