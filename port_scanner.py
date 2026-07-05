import requests
import time
import smtplib
import json
import subprocess
import logging
from datetime import datetime
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("site_checker.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SiteCheckerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Site Checker - Monitor & Alert")
        self.root.geometry("900x700")
        
        self.monitoring = False
        self.thread = None
        self.sites = []
        
        self.create_widgets()
        self.load_config()
    
    def create_widgets(self):
        # === Top Frame - Controls ===
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")
        
        ttk.Label(top_frame, text="Check Interval (minutes):").pack(side="left")
        self.interval_var = tk.IntVar(value=5)
        ttk.Entry(top_frame, textvariable=self.interval_var, width=5).pack(side="left", padx=5)
        
        self.start_btn = ttk.Button(top_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_btn.pack(side="right", padx=5)
        
        self.stop_btn = ttk.Button(top_frame, text="Stop", command=self.stop_monitoring, state="disabled")
        self.stop_btn.pack(side="right")
        
        # === Sites Management ===
        sites_frame = ttk.LabelFrame(self.root, text="Monitored Sites", padding=10)
        sites_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Add site
        add_frame = ttk.Frame(sites_frame)
        add_frame.pack(fill="x", pady=5)
        
        ttk.Label(add_frame, text="URL:").pack(side="left")
        self.url_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.url_var, width=40).pack(side="left", padx=5)
        
        self.use_ping_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(add_frame, text="Use Ping", variable=self.use_ping_var).pack(side="left", padx=5)
        
        ttk.Button(add_frame, text="Add Site", command=self.add_site).pack(side="right")
        
        # Sites list
        self.sites_list = tk.Listbox(sites_frame, height=8)
        self.sites_list.pack(fill="both", expand=True, pady=5)
        
        ttk.Button(sites_frame, text="Remove Selected", command=self.remove_site).pack(pady=2)
        
        # === Email Settings ===
        email_frame = ttk.LabelFrame(self.root, text="Email Notifications", padding=10)
        email_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(email_frame, text="Notify Email:").grid(row=0, column=0, sticky="w")
        self.email_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.email_var, width=40).grid(row=0, column=1, padx=5)
        
        ttk.Label(email_frame, text="SMTP Server:").grid(row=1, column=0, sticky="w")
        self.smtp_server_var = tk.StringVar(value="smtp.gmail.com")
        ttk.Entry(email_frame, textvariable=self.smtp_server_var).grid(row=1, column=1, padx=5, sticky="ew")
        
        ttk.Label(email_frame, text="SMTP User:").grid(row=2, column=0, sticky="w")
        self.smtp_user_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.smtp_user_var).grid(row=2, column=1, padx=5, sticky="ew")
        
        ttk.Label(email_frame, text="SMTP Pass:").grid(row=3, column=0, sticky="w")
        self.smtp_pass_var = tk.StringVar()
        ttk.Entry(email_frame, textvariable=self.smtp_pass_var, show="*").grid(row=3, column=1, padx=5, sticky="ew")
        
        # === Log Area ===
        log_frame = ttk.LabelFrame(self.root, text="Live Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15)
        self.log_text.pack(fill="both", expand=True)
    
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        full_msg = f"[{timestamp}] {message}"
        self.log_text.insert(tk.END, full_msg + "\n")
        self.log_text.see(tk.END)
        logger.info(message)
    
    def add_site(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Warning", "URL cannot be empty")
            return
        use_ping = self.use_ping_var.get()
        self.sites.append({"url": url, "use_ping": use_ping})
        self.sites_list.insert(tk.END, f"{'[PING] ' if use_ping else ''}{url}")
        self.url_var.set("")
        self.save_config()
    
    def remove_site(self):
        selection = self.sites_list.curselection()
        if selection:
            index = selection[0]
            self.sites.pop(index)
            self.sites_list.delete(index)
            self.save_config()
    
    def check_site(self, site):
        url = site["url"]
        use_ping = site.get("use_ping", False)
        
        if use_ping:
            try:
                # Ping check
                param = "-n" if os.name == "nt" else "-c"
                result = subprocess.run(["ping", param, "1", "-W", "5", url.replace("https://", "").replace("http://", "").split("/")[0]],
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                success = result.returncode == 0
                status = "Ping OK" if success else "Ping failed"
                return success, status
            except:
                return False, "Ping error"
        else:
            # HTTP check
            try:
                response = requests.get(url, timeout=10, allow_redirects=True)
                success = response.status_code == 200
                return success, f"HTTP {response.status_code}"
            except requests.RequestException as e:
                return False, str(e)
    
    def send_email(self, url, status):
        try:
            to_email = self.email_var.get().strip()
            if not to_email or not self.smtp_user_var.get():
                return False
            
            msg = MIMEText(f"Site {url} is DOWN!\nStatus: {status}\nTime: {datetime.now()}")
            msg['Subject'] = f"🚨 Site Down: {url}"
            msg['From'] = self.smtp_user_var.get()
            msg['To'] = to_email
            
            with smtplib.SMTP(self.smtp_server_var.get(), 587) as server:
                server.starttls()
                server.login(self.smtp_user_var.get(), self.smtp_pass_var.get())
                server.sendmail(self.smtp_user_var.get(), to_email, msg.as_string())
            self.log(f"📧 Email alert sent for {url}")
            return True
        except Exception as e:
            self.log(f"❌ Email failed: {e}")
            return False
    
    def monitoring_loop(self):
        interval = self.interval_var.get() * 60
        while self.monitoring:
            for site in self.sites:
                is_up, status = self.check_site(site)
                url = site["url"]
                
                if is_up:
                    self.log(f"✅ {url} is UP ({status})")
                else:
                    self.log(f"❌ {url} is DOWN ({status})")
                    self.send_email(url, status)
            
            time.sleep(interval)
    
    def start_monitoring(self):
        if not self.sites:
            messagebox.showwarning("Warning", "Add at least one site to monitor")
            return
        if self.monitoring:
            return
        
        self.monitoring = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.log("🚀 Monitoring started...")
        
        self.thread = threading.Thread(target=self.monitoring_loop, daemon=True)
        self.thread.start()
    
    def stop_monitoring(self):
        self.monitoring = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log("⏹️ Monitoring stopped.")
    
    def save_config(self):
        config = {
            "interval": self.interval_var.get(),
            "email": self.email_var.get(),
            "smtp_server": self.smtp_server_var.get(),
            "smtp_user": self.smtp_user_var.get(),
            "sites": self.sites
        }
        try:
            with open("config.json", "w") as f:
                json.dump(config, f, indent=2)
        except:
            pass
    
    def load_config(self):
        if os.path.exists("config.json"):
            try:
                with open("config.json") as f:
                    config = json.load(f)
                self.interval_var.set(config.get("interval", 5))
                self.email_var.set(config.get("email", ""))
                self.smtp_server_var.set(config.get("smtp_server", "smtp.gmail.com"))
                self.smtp_user_var.set(config.get("smtp_user", ""))
                self.sites = config.get("sites", [])
                for site in self.sites:
                    prefix = "[PING] " if site.get("use_ping") else ""
                    self.sites_list.insert(tk.END, f"{prefix}{site['url']}")
            except:
                pass
    
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()
    
    def on_close(self):
        self.stop_monitoring()
        self.save_config()
        self.root.destroy()

if __name__ == "__main__":
    app = SiteCheckerApp()
    app.run()
