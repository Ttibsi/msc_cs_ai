import re

def main() -> int:
    with open("The_Raven.txt") as f:
        text = f.read()

    print(f"shrieked: {bool(re.search(r'[sS]hrieked', text))}")
    print(f"bleak: {bool(re.search(r'[bB]leak', text))}")
    print(f"pp count: {len(re.findall(r'[pP]{2}', text))}")
    print(re.sub(f"!", "#", text))
    print(f"t..e count: {len(re.findall(r'\s[tT]\w+[eE]\s', text))}")
    return 0 

if __name__ == "__main__":
    raise SystemExit(main())
