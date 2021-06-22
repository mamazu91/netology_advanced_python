import hashlib


def lines_md5_generator(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        yield hashlib.md5(line.encode('UTF-8')).hexdigest()


def main():
    for item in lines_md5_generator('countries.json'):
        print(item)


main()
