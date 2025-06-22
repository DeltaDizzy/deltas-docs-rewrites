import unicodeit, os
from glob import glob

if __name__ == "__main__":
    prefix = "docs/system-id"
    result = [y for x in os.walk(prefix) for y in glob(os.path.join(x[0], '*.md'))]
    for f in result:
        with open(f, 'r') as file:
            content = file.read()
        with open(f, 'w') as file:
            file.write(unicodeit.replace(content))
        