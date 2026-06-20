# Lesson 11 — Compete in the PECAN+ CTF 🏁

This is what everything has been building towards. A **Capture The Flag (CTF)**
is a competition where you solve security puzzles to uncover hidden **flags** —
short strings in the form `pecan{...}`. You now have a tool and a method for
every category. Time to play.

> [!IMPORTANT]
> Only attack the official practice challenges and your own machines.
> See [Lesson 00](00-ethics-and-safety.md).

**Play here ➜ https://practice.pecanplus.org/?page=challenges**

## How a CTF works

1. Each challenge gives you a file, a link or a clue.
2. You find the hidden flag, e.g. `pecan{y0u_f0und_me}`.
3. You submit the flag for points. Harder challenges = more points.
4. Difficulty is shown with locks: 🔓 Beginner · 🔓🔓 Intermediate · 🔓🔓🔓 Advanced.

## Pick your tool by category

| Category            | First things to try                               | Lesson                                           |
| ------------------- | ------------------------------------------------- | ------------------------------------------------ |
| Cryptography        | CyberChef _Magic_, `base64 -d`, ROT13 brute force | [02](02-cyberchef.md) · [03](03-cryptography.md) |
| OSINT               | `whois`, `exiftool`, Wayback Machine              | [04](04-osint-wayback.md)                        |
| Web exploits        | view source, `robots.txt`, `gobuster`             | [05](05-web-recon.md)                            |
| Steganography       | `exiftool`, `strings`, `steghide`, `binwalk`      | [06](06-steganography.md)                        |
| Forensics           | `file`, `xxd`, `binwalk -e`, `tshark`             | [07](07-forensics.md)                            |
| Reverse Engineering | `strings`, `file`, `radare2`                      | [08](08-reverse-engineering.md)                  |

## A flag-hunting checklist

When you're stuck, work through these quick wins:

```bash
# Is the flag just sitting there?
grep -ri "pecan{" .

# Hidden in a binary or image?
strings -n 6 file | grep -i pecan

# Encoded? Try Base64.
cat file | base64 -d 2>/dev/null | grep -i pecan

# Hidden in metadata?
exiftool file | grep -i pecan

# A file inside a file?
binwalk -e file && grep -ri pecan _file.extracted/
```

## Suggested first solves (all Beginner 🔓)

Work these in order — each maps directly to a lesson you've finished:

1. **Cryptography → _Encoded_** — decode with CyberChef.
2. **Steganography → _Head in the clouds_** — `exiftool` / `strings`.
3. **Web exploits → _Bite my shiny metal_** — check `robots.txt`.
4. **OSINT → _Kidnapped part 1_** — search public info + Wayback.
5. **Forensics → _3D flag_** — identify and open the file.
6. **Reverse Engineering → _Love letter_** — `strings` the binary.

## Keep a write-up

For every flag you capture, note:

- The challenge name and category.
- The commands that worked.
- The flag.

Write-ups are the single best way to revise — and they look great in a portfolio.

## Compete for real

When you're landing Beginner and Intermediate flags, enter the live competition:

- **Register:** [pecanplus.org/register.html](https://pecanplus.org/register.html)
- **Choose a division:** [Division Decision Guide](https://pecanplus.org/assets/DivisionDecisionGuide.pdf)

## Keep levelling up

- [picoCTF](https://picoctf.org/) · [TryHackMe](https://tryhackme.com/) ·
  [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/)
- Bonus skills: [Python for Security](12-python-scripting.md) to automate your solves.

🎉 **You've completed the course. Go capture some flags!**

⬅️ Back to the [Course Plan](../COURSE_PLAN.md) · [README](../README.md)
