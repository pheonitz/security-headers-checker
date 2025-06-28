import requests
from urllib.parse import urlparse
from colorama import Fore, Style

# Recommended Security Headers List
required_headers = {
    "Content-Security-Policy": "Helps prevent XSS attacks",
    "X-Frame-Options": "Prevents Clickjacking",
    "X-Content-Type-Options": "Prevents MIME type sniffing",
    "Strict-Transport-Security": "Enforces HTTPS",
    "Referrer-Policy": "Controls referrer information sent",
    "Permissions-Policy": "Restricts browser features (like camera/mic)"
}

def is_valid_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ("http", "https") and parsed_url.netloc != ""

def check_headers(url):
    print(f"\nScanning: {url}\n")
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        score = 0
        total = len(required_headers)

        for header, desc in required_headers.items():
            if header in headers:
                print(Fore.GREEN + f"[✔] {header}: Present")
                score += 1
            else:
                print(Fore.RED + f"[✘] {header}: Missing -- ({desc})")

        grade = calculate_grade(score, total)
        print(Style.RESET_ALL + f"\nSecurity Grade: {grade} ({score}/{total} headers present)")

    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"\nError: Could not connect to {url}\nReason: {e}")

def calculate_grade(score, total):
    percentage = (score / total) * 100
    if percentage == 100:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 60:
        return "B"
    elif percentage >= 40:
        return "C"
    else:
        return "F"

if __name__ == "__main__":
    print(Style.BRIGHT + "\n=== Website Security Headers Checker ===\n")
    target_url = input("Enter target URL (e.g., https://example.com): ").strip()

    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    if is_valid_url(target_url):
        check_headers(target_url)
    else:
        print(Fore.RED + "\nInvalid URL format. Please enter a valid URL like https://example.com\n")
