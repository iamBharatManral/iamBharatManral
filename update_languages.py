import requests
import os
from collections import defaultdict

GITHUB_USERNAME = "iamBharatManral"
README_FILE = "README.md"
START_TAG = "<!--START_LANGUAGES_SECTION-->"
END_TAG = "<!--END_LANGUAGES_SECTION-->"
GITHUB_API = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

def fetch_languages():
    repos = requests.get(GITHUB_API).json()
    language_counts = defaultdict(int)

    for repo in repos:
        if repo["fork"]:
            continue
        lang_url = repo["languages_url"]
        langs = requests.get(lang_url).json()
        for lang, count in langs.items():
            language_counts[lang] += count

    sorted_langs = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_langs


def format_languages(langs):
    language_colors = {
        "Go": "00ADD8",
        "Rust": "000000",
        "JavaScript": "F7DF1E",
        "Python": "306998",
        "Java": "007396",
        "TypeScript": "3178C6",
        "C": "A8B9CC",
        "C++": "00599C",
        "HTML": "E34F26",
        "CSS": "1572B6",
        "Ruby": "D9136A",
        "Haskell": "5e4b8b",
        "PHP": "8993be",
        "Swift": "F05138",
        "Kotlin": "7F52FF",
        "GoCache": "00ADD8",
        "Vim": "019733",
        "Linux": "FCC624"
    }

    badges = []
    for lang, _ in langs:
        color = language_colors.get(lang, "informational")  # Default color
        badges.append(f"![{lang}](https://img.shields.io/badge/{lang.replace(' ', '%20')}-{color}?style=flat&logo={lang.lower()}&logoColor=white)")

    return "\n" + " ".join(badges) + "\n"

def update_readme(new_section):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(START_TAG)
    end = content.find(END_TAG)

    if start == -1 or end == -1:
        raise ValueError("Tag section not found")

    updated = content[:start + len(START_TAG)] + "\n" + new_section + "\n" + content[end:]
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

if __name__ == "__main__":
    langs = fetch_languages()
    section = format_languages(langs)
    update_readme(section)
