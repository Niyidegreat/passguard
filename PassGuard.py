#!/usr/bin/env python3
"""
PassGuard
Owner: Niyi De Great the Cyberscientist
"""

import os, json, csv, math, re, base64, hashlib, logging, secrets, string
from datetime import datetime

import requests
from cryptography.fernet import Fernet
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from pyfiglet import Figlet

APP_NAME = "PassGuard"
VERSION = "SOC Edition 1.0"
OWNER = "Niyi De Great, the Cyberscientist"

REPORT_DIR = "reports"
LOG_DIR = "logs"
VAULT_DIR = "vault"
VAULT_FILE = f"{VAULT_DIR}/vault.dat"

for d in (REPORT_DIR, LOG_DIR, VAULT_DIR):
    os.makedirs(d, exist_ok=True)

logging.basicConfig(
    filename=f"{LOG_DIR}/passguard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

console = Console()

COMMON_PASSWORDS = {
    "123456","password","123456789","qwerty",
    "admin","welcome","password123","123123"
}

def banner():
    fig = Figlet(font="slant")
    console.print(f"[cyan]{fig.renderText(APP_NAME)}[/cyan]")
    console.print(Panel.fit(
        f"[bold green]{VERSION}[/bold green]\n"
        f"Owner: {OWNER}\n"
        f"Password Security & Integrity Toolkit",
        border_style="cyan"
    ))

def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^\w]", password): charset += 32
    return 0 if charset == 0 else len(password) * math.log2(charset)

def detect_patterns(password):
    issues = []
    if re.search(r"(.)\1\1", password):
        issues.append("Repeated characters")
    if re.search(r"123|234|345|456|567|678|789", password):
        issues.append("Sequential numbers")
    return issues

def save_report(data):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"{REPORT_DIR}/report_{ts}.json","w") as f:
        json.dump(data,f,indent=4)

def password_strength():
    password = Prompt.ask("Enter password", password=True)
    score = 0
    issues = []

    if len(password) >= 12: score += 25
    elif len(password) >= 8: score += 15
    else: issues.append("Too short")

    if re.search(r"[A-Z]", password): score += 10
    if re.search(r"[a-z]", password): score += 10
    if re.search(r"[0-9]", password): score += 10
    if re.search(r"[^\w]", password): score += 15

    entropy = calculate_entropy(password)

    if entropy > 80:
        score += 25
    elif entropy < 50:
        issues.append("Low entropy")

    if password.lower() in COMMON_PASSWORDS:
        score -= 30

    score = max(0, min(100, score))

    table = Table(title="Password Analysis", box=box.ROUNDED)
    table.add_column("Metric")
    table.add_column("Value")
    table.add_row("Score", str(score))
    table.add_row("Entropy", f"{entropy:.2f}")
    table.add_row("Issues", ", ".join(issues) if issues else "None")
    console.print(table)

def password_generator():
    length = int(Prompt.ask("Length", default="enter the password length e.g 16"))
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(secrets.choice(chars) for _ in range(length))
    console.print(Panel.fit(password, title="Generated Password"))

def hash_generator():
    text = Prompt.ask("Enter text")
    table = Table(title="Hash Generator", box=box.ROUNDED)
    table.add_column("Algorithm")
    table.add_column("Digest")

    for algo in sorted(hashlib.algorithms_guaranteed):
        try:
            h = hashlib.new(algo)
            h.update(text.encode())
            table.add_row(algo.upper(), h.hexdigest())
        except Exception:
            pass

    console.print(table)

def hash_identifier():
    h = Prompt.ask("Enter hash").strip()

    length_map = {
        32:["MD5"],
        40:["SHA1"],
        56:["SHA224"],
        64:["SHA256","SHA3-256"],
        96:["SHA384","SHA3-384"],
        128:["SHA512","SHA3-512"]
    }

    table = Table(title="Hash Identification")
    table.add_column("Property")
    table.add_column("Value")

    table.add_row("Length", str(len(h)))
    table.add_row("Hex", str(bool(re.fullmatch(r"[a-fA-F0-9]+", h))))

    if len(h) in length_map:
        table.add_row("Possible Type(s)", ", ".join(length_map[len(h)]))
    else:
        table.add_row("Possible Type(s)", "Unknown")

    console.print(table)

def verify_hash():
    text = Prompt.ask("Enter plaintext")
    target = Prompt.ask("Enter hash").lower()

    matches = []

    for algo in sorted(hashlib.algorithms_guaranteed):
        try:
            h = hashlib.new(algo)
            h.update(text.encode())
            if h.hexdigest().lower() == target:
                matches.append(algo.upper())
        except Exception:
            pass

    if matches:
        console.print(f"[green]Match found:[/green] {', '.join(matches)}")
    else:
        console.print("[red]No match found[/red]")

def breach_checker():
    password = Prompt.ask("Enter password", password=True)
    sha1 = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    try:
        r = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            timeout=10
        )
        r.raise_for_status()
    except Exception as e:
        console.print(f"[red]{e}[/red]")
        return

    for line in r.text.splitlines():
        h, count = line.split(":")
        if h == suffix:
            console.print(f"[red]Found in breaches {count} times[/red]")
            return

    console.print("[green]Not found in known breaches[/green]")

def get_cipher(master):
    key = hashlib.sha256(master.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def load_vault(master):
    cipher = get_cipher(master)
    if not os.path.exists(VAULT_FILE):
        return [], cipher

    try:
        with open(VAULT_FILE, "rb") as f:
            data = f.read()
        return json.loads(cipher.decrypt(data).decode()), cipher
    except Exception:
        return [], cipher

def save_vault(vault, cipher):
    with open(VAULT_FILE, "wb") as f:
        f.write(cipher.encrypt(json.dumps(vault).encode()))

def password_vault():
    master = Prompt.ask("Master Password", password=True)
    vault, cipher = load_vault(master)

    while True:
        console.print("\n1 Add | 2 View | 3 Delete | 0 Exit")
        c = Prompt.ask("Choice")

        if c == "1":
            vault.append({
                "site": Prompt.ask("Site"),
                "user": Prompt.ask("Username"),
                "pass": Prompt.ask("Password", password=True)
            })
            save_vault(vault, cipher)

        elif c == "2":
            table = Table(title="Vault")
            table.add_column("ID")
            table.add_column("Site")
            table.add_column("User")

            for i, v in enumerate(vault):
                table.add_row(str(i), v["site"], v["user"])

            console.print(table)

        elif c == "3":
            idx = int(Prompt.ask("Index"))
            if 0 <= idx < len(vault):
                vault.pop(idx)
                save_vault(vault, cipher)

        elif c == "0":
            break

def file_integrity_checker():
    path = Prompt.ask("File path")

    if not os.path.exists(path):
        console.print("[red]File not found[/red]")
        return

    with open(path, "rb") as f:
        data = f.read()

    table = Table(title="File Integrity Hashes")
    table.add_column("Algorithm")
    table.add_column("Digest")

    for algo in ["md5","sha1","sha256","sha512"]:
        h = hashlib.new(algo)
        h.update(data)
        table.add_row(algo.upper(), h.hexdigest())

    console.print(table)

def menu():
    table = Table(title="PassGuard SOC Edition 2.0", box=box.DOUBLE_EDGE)
    table.add_column("Option")
    table.add_column("Function")
    table.add_row("1","Password Analysis")
    table.add_row("2","Password Generator")
    table.add_row("3","Hash Generator (All Algorithms)")
    table.add_row("4","Hash Identifier")
    table.add_row("5","Breach Checker")
    table.add_row("6","Password Vault")
    table.add_row("7","Hash Verification Lab")
    table.add_row("8","File Integrity Checker")
    table.add_row("0","Exit")
    console.print(table)

def main():
    banner()
    while True:
        menu()
        c = Prompt.ask("Select")

        if c == "1": password_strength()
        elif c == "2": password_generator()
        elif c == "3": hash_generator()
        elif c == "4": hash_identifier()
        elif c == "5": breach_checker()
        elif c == "6": password_vault()
        elif c == "7": verify_hash()
        elif c == "8": file_integrity_checker()
        elif c == "0": break

if __name__ == "__main__":
    main()
