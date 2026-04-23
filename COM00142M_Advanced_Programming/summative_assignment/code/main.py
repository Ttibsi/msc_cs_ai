from __future__ import annotations

from ui import start_gui


def main(argv: list[str] | None = None) -> int:
    start_gui()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
