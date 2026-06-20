"""Validate that every command taught in the course works in this codespace.

Run all checks:           python3 -m pytest -v
Skip internet checks:     python3 -m pytest -m "not network" -v

Each test runs a real command with subprocess and asserts on its output, so a
green run proves the lessons in COURSE_PLAN.md and labs/ are reproducible here.
"""

import hashlib
import shutil
import socket
import subprocess

import pytest


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def run(cmd, **kwargs):
    """Run a shell command and return the CompletedProcess (text mode)."""
    return subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=kwargs.pop("timeout", 60),
        **kwargs,
    )


def have_internet(host="archive.org", port=443, timeout=5):
    try:
        socket.create_connection((host, port), timeout=timeout).close()
        return True
    except OSError:
        return False


requires_net = pytest.mark.skipif(
    not have_internet(), reason="no internet connectivity available"
)


# --------------------------------------------------------------------------- #
# Lesson 0/1 — the tools exist (every command used in the course)
# --------------------------------------------------------------------------- #
TOOLS = [
    # Core shell
    "bash", "ls", "cat", "grep", "find", "man", "tr",
    # Encoding / crypto (Lessons 2 & 3)
    "base64", "base32", "xxd", "openssl", "md5sum", "sha256sum",
    # OSINT / network (Lessons 4 & 9)
    "curl", "whois", "dig", "nmap", "nc",
    # Web (Lesson 5)
    "whatweb", "gobuster", "nikto", "sqlmap",
    # Steganography / forensics (Lessons 6 & 7)
    "file", "strings", "exiftool", "steghide", "binwalk", "foremost",
    "pngcheck", "convert", "tshark", "tcpdump",
    # Reverse engineering (Lesson 8)
    "objdump", "gdb", "radare2",
    # Passwords (Lesson 10)
    "john", "hashid",
]


@pytest.mark.parametrize("tool", TOOLS)
def test_tool_installed(tool):
    assert shutil.which(tool) is not None, f"{tool} is not installed/on PATH"


# --------------------------------------------------------------------------- #
# Lesson 2 — Encoding / decoding (CyberChef equivalents)
# --------------------------------------------------------------------------- #
def test_base64_decode():
    r = run('echo -n "cGVjYW57aGVsbG99" | base64 -d')
    assert r.stdout == "pecan{hello}"


def test_base64_encode():
    r = run('echo -n "pecan{hello}" | base64')
    assert r.stdout.strip() == "cGVjYW57aGVsbG99"


def test_hex_decode():
    r = run('echo -n "70 65 63 61 6e" | xxd -r -p')
    assert r.stdout == "pecan"


def test_rot13():
    r = run("echo \"Uryyb\" | tr 'A-Za-z' 'N-ZA-Mn-za-m'")
    assert r.stdout.strip() == "Hello"


def test_base32_round_trip():
    r = run('echo -n "pecan" | base32 | base32 -d')
    assert r.stdout == "pecan"


# --------------------------------------------------------------------------- #
# Lesson 3 — Cryptography / hashing
# --------------------------------------------------------------------------- #
def test_md5sum_known_value():
    r = run('echo -n "password123" | md5sum')
    assert r.stdout.split()[0] == "482c811da5d5b4bc6d497ffa98491e38"


def test_openssl_sha256_matches_python():
    expected = hashlib.sha256(b"secret").hexdigest()
    r = run('echo -n "secret" | openssl dgst -sha256')
    assert expected in r.stdout


def test_openssl_encrypt_decrypt_round_trip(tmp_path):
    msg = tmp_path / "msg.txt"
    enc = tmp_path / "msg.enc"
    msg.write_text("pecan{crypto}")
    run(
        f"openssl enc -aes-256-cbc -pbkdf2 -salt -pass pass:test123 "
        f"-in {msg} -out {enc}"
    )
    r = run(
        f"openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:test123 -in {enc}"
    )
    assert r.stdout == "pecan{crypto}"


# --------------------------------------------------------------------------- #
# Lesson 6 — Steganography
# --------------------------------------------------------------------------- #
def test_exiftool_read_comment(tmp_path):
    img = tmp_path / "img.jpg"
    run(f"convert -size 32x32 xc:red {img}")
    run(f'exiftool -overwrite_original -Comment="pecan{{exif}}" {img}')
    r = run(f"exiftool -Comment {img}")
    assert "pecan{exif}" in r.stdout


def test_strings_finds_flag(tmp_path):
    blob = tmp_path / "blob.bin"
    blob.write_bytes(b"\x00\x01\x02pecan{strings}\xff\xfe")
    r = run(f"strings {blob} | grep pecan")
    assert "pecan{strings}" in r.stdout


def test_steghide_embed_and_extract(tmp_path):
    cover = tmp_path / "cover.bmp"
    secret = tmp_path / "secret.txt"
    stego = tmp_path / "stego.bmp"
    out = tmp_path / "revealed.txt"
    run(f"convert -size 120x120 xc:skyblue BMP3:{cover}")
    secret.write_text("pecan{stego}")
    embed = run(
        f"steghide embed -cf {cover} -ef {secret} -sf {stego} "
        f"-p hunter2 -q"
    )
    assert embed.returncode == 0, embed.stderr
    run(f"steghide extract -sf {stego} -p hunter2 -xf {out} -q")
    assert out.read_text() == "pecan{stego}"


def test_binwalk_detects_embedded_gzip(tmp_path):
    png = tmp_path / "img.png"
    gz = tmp_path / "hidden.gz"
    combo = tmp_path / "combo.png"
    run(f"convert -size 16x16 xc:green {png}")
    run(f'echo "pecan{{hidden}}" | gzip > {gz}')
    run(f"cat {png} {gz} > {combo}")
    r = run(f"binwalk {combo}")
    assert "gzip" in r.stdout.lower()


# --------------------------------------------------------------------------- #
# Lesson 7 — Forensics
# --------------------------------------------------------------------------- #
def test_file_identifies_png(tmp_path):
    png = tmp_path / "pic.png"
    run(f"convert -size 8x8 xc:black {png}")
    r = run(f"file {png}")
    assert "PNG image data" in r.stdout


def test_pngcheck_valid_png(tmp_path):
    png = tmp_path / "pic.png"
    run(f"convert -size 8x8 xc:white {png}")
    r = run(f"pngcheck {png}")
    assert "OK" in r.stdout


# --------------------------------------------------------------------------- #
# Lesson 8 — Reverse engineering
# --------------------------------------------------------------------------- #
def test_objdump_reads_elf():
    # python3 is a known ELF binary on Kali.
    py = shutil.which("python3")
    r = run(f"objdump -f {py}")
    assert "architecture:" in r.stdout


def test_radare2_version():
    r = run("radare2 -v")
    assert "radare2" in r.stdout.lower()


# --------------------------------------------------------------------------- #
# Lesson 10 — Passwords & hashes
# --------------------------------------------------------------------------- #
def test_hashid_identifies_md5():
    r = run("hashid 482c811da5d5b4bc6d497ffa98491e38")
    assert "MD5" in r.stdout


# --------------------------------------------------------------------------- #
# Lessons 4/5/9 — Internet-dependent commands (legal targets only)
# --------------------------------------------------------------------------- #
@pytest.mark.network
@requires_net
def test_wayback_machine_api():
    # Lesson 4: the Wayback Machine availability API returns archived snapshots.
    r = run(
        'curl -s "http://archive.org/wayback/available?url=example.com"'
    )
    assert "archived_snapshots" in r.stdout


@pytest.mark.network
@requires_net
def test_practice_ctf_reachable():
    # Lesson 11: the PECAN+ practice CTF is online.
    r = run(
        'curl -s -o /dev/null -w "%{http_code}" '
        "https://practice.pecanplus.org/"
    )
    assert r.stdout.strip() == "200"


@pytest.mark.network
@requires_net
def test_curl_fetches_page():
    # Lessons 4 & 5: fetching a page with curl (recon basics).
    r = run('curl -s --max-time 20 https://example.com')
    assert "Example Domain" in r.stdout


@pytest.mark.network
@requires_net
def test_dig_resolves():
    # Lesson 9: DNS lookup of a legal practice host.
    r = run("dig +short scanme.nmap.org")
    assert r.stdout.strip() != ""


@pytest.mark.network
@requires_net
def test_nmap_scans_scanme():
    # Lesson 9: Nmap's official legal scanning target (TCP connect scan).
    r = run("nmap -sT -Pn -p 80 scanme.nmap.org", timeout=120)
    assert "scanme.nmap.org" in r.stdout
