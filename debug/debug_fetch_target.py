from __future__ import annotations

from src.fetch.fetch_target import get_name_and_url
from config.constant import BASE_URL
from config.target import FETCH_TARGET


def main() -> None:
    print("\n\n====== START ======\n\n")
    print(">>> BASE_URL")
    print(f"- {BASE_URL}\n")
    print(">>> FETCH_TARGET")
    for target in FETCH_TARGET:
        print(f"- {target}")

    print("\n>>> get_name_and_url()")
    names, urls = get_name_and_url()
    for name, url in zip(names, urls):
        print(f"- {name} : {url}")

    print("\n\n====== END ======\n\n")


if __name__ == "__main__":
    main()
