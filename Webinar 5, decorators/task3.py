from datetime import datetime
import hashlib


def decorator(log_path):
    def __decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(log_path, 'a') as log_file:
                log_file.write(
                    f"[{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}] Function '{func.__name__}' was called "
                    f"with the following args: '{args}', and kwargs: '{kwargs}'. "
                    f"Return value: '{result}'" + '\n')
            return result

        return wrapper

    return __decorator


@decorator(log_path='task3_log.txt')
def lines_md5_generator(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        yield hashlib.md5(line.encode('UTF-8')).hexdigest()


def task3_main():
    for item in lines_md5_generator('countries.json'):
        print(item)


if __name__ == '__main__':
    task3_main()
