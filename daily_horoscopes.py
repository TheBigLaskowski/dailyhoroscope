import requests
from bs4 import BeautifulSoup
from datetime import datetime
from termcolor import colored

def fetch_and_parse_horoscope(zodiac_sign, url):
    print(colored(f"{zodiac_sign} - {current_date}", "magenta"))

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    blogtexts = soup.find_all("div", class_="blogtext")

    for blogtext in blogtexts:
        text = blogtext.get_text(strip=True)
        if "The Daily Horoscope for" in text:
            print(text)
            print("\n")
            break

def fetch_daily_writeup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    summary_start = soup.find("h3", string="Today's Horoscope Summary...").find_next("br")
    summary = ""

    for sibling in summary_start.next_siblings:
        if sibling == "\n" or isinstance(sibling, str):
            summary += sibling.strip()
        elif sibling.name == "br" and sibling.find_next("br") is not None:
            break
        else:
            summary += sibling.text.strip()

    print(colored("Today's Horoscope Summary...", "magenta"))
    print(summary)
    print("\n")

def main():
    zodiac_signs = {
        "Pisces ♓": "https://weeklyhoroscope.com/horoscopes/daily-horoscope-pisces.php",
        "Scorpio ♏": "https://weeklyhoroscope.com/horoscopes/daily-horoscope-scorpio.php",
        "Taurus ♉": "https://weeklyhoroscope.com/horoscopes/daily-horoscope-taurus.php",
    }

    # Fetch the daily writeup from one of the URLs (the same on each page)
    fetch_daily_writeup(zodiac_signs["Pisces ♓"])

    for zodiac_sign, url in zodiac_signs.items():
        fetch_and_parse_horoscope(zodiac_sign, url)

if __name__ == "__main__":
    current_date = datetime.now().strftime("%B %d, %Y")
    main()
