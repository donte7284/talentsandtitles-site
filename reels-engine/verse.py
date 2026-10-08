"""Print scripture verses from the saved texts in scripture/, to check a script against.

usage: python verse.py "2 Kings 4:1-7" ["Luke 14:28-30" ...]
Old and New Testament are the KJV; the Book of Mormon is the 2013 edition text. All public domain.
"""
import os,re,sys
here=os.path.join(os.path.dirname(os.path.abspath(__file__)),'scripture')
lines={}
for f in sorted(os.listdir(here)):
    if f.endswith('.txt'):
        for ln in open(os.path.join(here,f),encoding='utf-8'):
            if not ln.startswith('#'):
                ref,txt=ln.rstrip('\n').split('\t',1);lines[ref]=txt
for q in sys.argv[1:]:
    m=re.fullmatch(r'\s*(.+?)\s+(\d+):(\d+)(?:\s*[-–]\s*(\d+))?\s*',q)
    if not m:raise SystemExit(f'cannot read reference: {q!r} (use "Book C:V" or "Book C:V-V")')
    book,ch,v1,v2=m.group(1),m.group(2),int(m.group(3)),int(m.group(4) or m.group(3))
    found=False
    for v in range(v1,v2+1):
        ref=f'{book} {ch}:{v}'
        if ref in lines:print(f'{ref}  {lines[ref]}');found=True
    if not found:raise SystemExit(f'not found: {q!r} (book names as in the KJV, e.g. "1 Nephi", "Song of Solomon")')
    print()
