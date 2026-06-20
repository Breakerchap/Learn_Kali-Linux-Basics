# Lesson 09 — Network Scanning with Nmap

**Nmap** ("Network Mapper") finds devices on a network and the **ports** they
have open. Open ports are doors into a computer — knowing which are open is the
first step in both attacking _and_ defending.

> [!IMPORTANT]
> We only scan **`scanme.nmap.org`**, which Nmap provides for legal practice.
> Do not scan anything else without permission. (See [Lesson 00](00-ethics-and-safety.md).)

## Ports in 30 seconds

A computer has 65,535 ports. Common ones:

| Port | Service                 |
| ---- | ----------------------- |
| 22   | SSH (remote login)      |
| 80   | HTTP (websites)         |
| 443  | HTTPS (secure websites) |
| 25   | SMTP (email)            |

## Your first scan

```bash
# Is the target alive? (a "ping" scan)
nmap -sn scanme.nmap.org
```

```bash
# Scan the most common ports
nmap scanme.nmap.org
```

Read the output: each line shows a port, whether it's `open`/`closed`, and the
likely service.

## Going deeper

```bash
# -sV  = detect the version of software behind each open port
nmap -sV scanme.nmap.org
```

```bash
# -O   = guess the operating system (needs sudo)
sudo nmap -O scanme.nmap.org
```

```bash
# Scan a specific list of ports only
nmap -p 22,80,443 scanme.nmap.org
```

## Save your results

```bash
nmap -sV scanme.nmap.org -oN my_scan.txt
cat my_scan.txt
```

## How it works

```mermaid
sequenceDiagram
    participant You as Kali (you)
    participant T as scanme.nmap.org
    You->>T: Is port 80 open?
    T-->>You: Yes (SYN/ACK)
    You->>T: Is port 23 open?
    T-->>You: No reply / closed
```

## ✅ Challenge

1. How many ports did Nmap report as `open` on `scanme.nmap.org`?
2. What service and version is running on port 22?
3. What does the `-sV` flag add compared to a plain scan?
4. Save a version scan to a file and open it in the VS Code editor.

➡️ Next: [Lesson 10 — Password & Hash Basics](10-passwords-and-hashes.md)
