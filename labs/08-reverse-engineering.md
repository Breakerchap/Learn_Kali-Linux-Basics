# Lesson 08 — Reverse Engineering Basics

**Reverse engineering** (RE) means taking a finished program apart to understand
how it works — and, in a CTF, to recover a secret it's hiding. You don't need to
be a programmer to start: the easiest flags fall to `strings` before you ever
open a disassembler.

> [!IMPORTANT]
> Only analyse binaries from a challenge or that you compiled yourself.
> See [Lesson 00](00-ethics-and-safety.md).

## Learning goals

- Identify a binary's type and architecture.
- Pull readable text and secrets out of a binary.
- Read a disassembly and explore functions with `radare2`.

## Part A — Identify the binary

```bash
file /usr/bin/python3
```

Expected output (an ELF is a Linux executable):

```
/usr/bin/python3: ELF 64-bit LSB ... x86-64 ...
```

```bash
objdump -f /usr/bin/python3 | head -4
```

Expected output:

```
/usr/bin/python3:     file format elf64-x86-64
architecture: i386:x86-64, flags 0x00000112:
EXEC_P, HAS_SYMS, D_PAGED
```

## Part B — Easy wins first: strings

Most beginner RE challenges store the flag as plain text. Always try this first:

```bash
strings /usr/bin/python3 | grep -i "version" | head -3
```

In a real challenge you'd run `strings ./program | grep -i pecan`.

## Part C — Disassemble

`objdump -d` turns machine code back into assembly. You're looking for compared
strings, suspicious constants or function names:

```bash
objdump -d /usr/bin/python3 | head -20    # press q if you pipe to less
```

You'll see lines like `mov`, `cmp`, `call` — the CPU instructions the program runs.

## Part D — Interactive analysis with radare2

`radare2` is a full reverse-engineering toolkit. Confirm it's installed:

```bash
radare2 -v | head -1
```

Expected output (version may differ):

```
radare2 6.0.5 0 @ linux-x86-64
```

A typical session (a sample binary `./crackme`):

```bash
radare2 -A ./crackme      # -A analyses the whole binary on load
```

Then at the `[0x...]>` prompt:

| Command             | What it does                                                 |
| ------------------- | ------------------------------------------------------------ |
| `afl`               | **a**nalyse **f**unction **l**ist — show all functions       |
| `s main` then `pdf` | seek to `main` and **p**rint **d**isassembly of **f**unction |
| `izz ~pecan`        | search all strings for `pecan`                               |
| `q`                 | quit                                                         |

> Prefer a GUI? **Ghidra** does the same job with a graphical decompiler. For
> beginner CTFs, `strings` + `radare2` is usually enough.

## ✅ Challenge

1. Run `file` on `/bin/ls` and `/usr/bin/python3`. Are they both ELF?
2. Use `strings ... | grep` to find the Python version string in the binary.
3. Try **Reverse Engineering → _Love letter_** at
   [practice.pecanplus.org](https://practice.pecanplus.org/?page=challenges).

➡️ Next: [Lesson 09 — Network Scanning with Nmap](09-network-scanning-nmap.md)
