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

---
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

---

## Project Structure
```bash
   site-checker/
├── site_checker_gui.py     # Main GUI application
├── config.json             # Auto-generated config (created on first use)
├── site_checker.log        # Log file (created automatically)
└── README.md
   ```

---

## Configuration Example (config.json)
```bash
{
  "interval": 5,
  "email": "your@email.com",
  "smtp_server": "smtp.gmail.com",
  "smtp_user": "your@gmail.com",
  "sites": [
    {
      "url": "https://example.com",
      "use_ping": false
    },
    {
      "url": "192.168.1.100",
      "use_ping": true
    }
  ]
}
```

---
## Future Enhancements (Planned)

System tray / minimized mode
Sound alerts
Slack / Discord / Telegram notifications
Dashboard with uptime statistics
Docker support

---

---

### 🤝 Open to Opportunities

- Backend / Full-Stack Internships  
- Freelance web projects  
- AI/ML and productivity-focused collaborations  

---

### 📫 Contact & Socials

<p align="center">
  <a href="mailto:aryanbhalsing7090@gmail.com">
    <img src="https://img.shields.io/badge/Email-aryanbhalsing7090%40gmail.com-red?style=for-the-badge&logo=gmail" />
  </a>
  <a href="https://www.linkedin.com/in/iamaryanbhalsing">
    <img src="https://img.shields.io/badge/LinkedIn-iamaryanbhalsing-blue?style=for-the-badge&logo=linkedin" />
  </a>
  <a href="https://github.com/iamaryanbhalsing">
    <img src="https://img.shields.io/badge/GitHub-iamaryanbhalsing-black?style=for-the-badge&logo=github" />
  </a>
  <a href="https://leetcode.com/iamaryanbhalsing">
    <img src="https://img.shields.io/badge/LeetCode-Profile-orange?style=for-the-badge&logo=leetcode" />
  </a>
</p>

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=iamaryanbhalsing&label=Profile%20views&color=0e75b6&style=flat" alt="Profile views" />
</p>

---
<img src="https://camo.githubusercontent.com/a5dbb660f658cb0ba61949a83a2eac3bde636395a476ecc7c16124d2a1f9d8a0/68747470733a2f2f73746174732e70706861742e746f702f69636f6e733f6e616d653d6170706c652c617263686c696e75782c646f636b65722c646a616e676f2c666173746170692c6769746c61622c6769742c6769746875622c6a736f6e2c6a6176617363726970742c6c696e75782c6d6f6e676f64622c6e656f76696d2c6e67696e782c706f737467726573716c2c707974686f6e2c727573742c72656163742c72656469732c7461696c77696e646373732c26636f6c756d6e733d3230" />

---

