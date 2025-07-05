import sys

with open("out/syspath.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sys.path))
