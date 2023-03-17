import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from termcolor import colored

def fetch_and_parse_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def fetch_daily_writeup(url):
    soup = fetch_and_parse_url(url)
    if soup is None:
        return

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

def fetch_and_parse_horoscope(zodiac_sign, url):
    print(colored(f"{zodiac_sign} - {current_week}", "magenta"))

    soup = fetch_and_parse_url(url)
    if soup is None:
        return

    blogtexts = soup.find_all("div", class_="blogtext")

    for blogtext in blogtexts:
        text = blogtext.get_text(strip=True)
        if "The Weekly Horoscope for" in text:
            print(text)
            print("\n")
            break

def main():
    zodiac_signs = [
        ("Pisces ♓", "https://weeklyhoroscope.com/horoscopes/weekly-horoscope-pisces.php"),
        ("Scorpio ♏", "https://weeklyhoroscope.com/horoscopes/weekly-horoscope-scorpio.php"),
        ("Taurus ♉", "https://weeklyhoroscope.com/horoscopes/weekly-horoscope-taurus.php"),
    ]

    # Fetch the daily writeup from one of the URLs (the same on each page)
    fetch_daily_writeup(zodiac_signs[0][1])

    for zodiac_sign, url in zodiac_signs:
        fetch_and_parse_horoscope(zodiac_sign, url)

if __name__ == "__main__":
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    current_week = f"Week of {week_start.strftime('%B %d')} through {week_end.strftime('%d')}"
    main()
