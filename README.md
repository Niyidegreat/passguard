# PASSGUARD

**Passguard** is a cybersecurity toolkit designed to help users analyze, generate secure, and validate passwords and cryptographic data. It combines multiple security utilities into one lightweight and practical tool for learners, developers, and security enthusiasts.

---

## FEATURES

### Password Analysis

Evaluate password strength based on complexity, entropy, patterns, and common vulnerabilities.

### PASSWORD GENERATOR

Generate strong, random, and customizable passwords with options for:

* Length control
* Symbols, numbers, uppercase/lowercase toggles
* High-entropy generation

### HASH GENNERATOR (All Algorithms)

Generate hashes using multiple cryptographic algorithms such as:

* MD5
* SHA-1
* SHA-256
* SHA-512
* (and other supported algorithms depending on implementation)

### HASH IDENTIFIER

Identify the likely hashing algorithm used based on hash structure, length and pattern recognition.

### BREACH CHECKER

Check if a password has appeared in known data breaches using external datasets or APIs.

### PASSWORD VAULT

Securely store and manage passwords locally with encryption and quick retrieval features.

### HASH VERIFICATION

Compare original data against hashes to verify integrity and authenticity. Generate and verify file hashes to detect unauthorized modifications or corruption.

---

## Tech Stack

Python
Hashlib / Cryptography libraries
CLI-based architecture

---

## Use Cases

* Cybersecurity learning and practice
* SOC analyst training labs
* Password security auditing
* Cryptography experimentation
* File integrity verification
* Personal password management

---

## ⚙️ Installation

```bash
git clone https://github.com/Niyidegreat/passguard.git
cd passguard
pip install -r requirements.txt
```

*(Adjust based on your actual stack: Python, Node.js, etc.)*

---

## Usage

```bash
python passguard.py
```

Then follow the interactive menu to access different modules.

---

## Project Structure 

```
Passguard/
│
├── modules/
│   ├── password_analysis.py
│   ├── password_generator.py
│   ├── hash_generator.py
│   ├── hash_identifier.py
│   ├── breach_checker.py
│   ├── password_vault.py
│   ├── hash_lab.py
│   └── exit.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Security Note

Passguard is built for educational and defensive security purposes. It should not be used for malicious activities or unauthorized data access.

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to improve.

---

## License

MIT License (or specify your license here)

## AUTHOR

Adeniyi Ojedele (Niyi de Great, the cyberscientist(
