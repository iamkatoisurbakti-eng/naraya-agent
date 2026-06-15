"""
select_provider.py — Pemilih provider LLM untuk Naraya-Agent.

Interaktif :  python core/select_provider.py
Langsung   :  python core/select_provider.py naraouter
Status     :  python core/select_provider.py --list
Uji koneksi:  python core/select_provider.py --test [nama]
"""

from __future__ import annotations

import sys
import providers


def interactive() -> None:
    names = providers.ORDER
    active = providers.current_name()
    print("Pilih provider:\n")
    for i, name in enumerate(names, 1):
        cfg = providers.resolve(name)
        mark = "●" if name == active else "○"
        keyst = "key✓" if cfg["api_key"] else "key✗"
        print(f"  {i:>2}. {mark} {providers.REGISTRY[name]['title']:<40} [{name}] {keyst}")
    print()
    try:
        choice = input("Nomor / nama (ENTER batal): ").strip()
    except EOFError:
        return
    if not choice:
        print("Dibatalkan.")
        return
    if choice.isdigit() and 1 <= int(choice) <= len(names):
        choice = names[int(choice) - 1]
    print(providers.set_provider(choice))


def main() -> None:
    args = sys.argv[1:]
    if not args:
        interactive()
    elif args[0] == "--list":
        print(providers.list_providers())
    elif args[0] == "--test":
        print(providers.test_provider(args[1] if len(args) > 1 else None))
    else:
        print(providers.set_provider(args[0]))


if __name__ == "__main__":
    main()
