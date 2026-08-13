from pathlib import Path

p = Path('verify_out.txt')
if not p.exists():
    print('verify_out.txt not found')
else:
    print(p.read_text(encoding='utf-16'))
