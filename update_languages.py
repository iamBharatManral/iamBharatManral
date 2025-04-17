import requests
import os
import hashlib
from collections import defaultdict

GITHUB_USERNAME = "iamBharatManral"
README_FILE = "README.md"
START_TAG = "<!--START_LANGUAGES_SECTION-->"
END_TAG = "<!--END_LANGUAGES_SECTION-->"
GITHUB_API = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"

def get_color_for_language(lang):
    # Generate a consistent color hex from the hash of the language name
    hash_object = hashlib.md5(lang.encode())
    hex_digest = hash_object.hexdigest()
    # Use the first 6 characters of the hash as the hex color
    return hex_digest[:6].upper()

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
    badges = []
    for lang, _ in langs:
        color = get_color_for_language(lang)
        badges.append(
            f"![{lang}](https://img.shields.io/badge/{lang.replace(' ', '%20')}-{color}?style=flat&logo={lang.lower()}&logoColor=white)"
        )
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
