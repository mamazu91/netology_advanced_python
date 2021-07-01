from datetime import datetime
import hashlib


def param_decorator(log_path):
    def __decorator(func):
        def new_func(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(log_path, 'a') as log_file:
                log_file.write(
                    f"[{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}] Function '{func.__name__}' was called "
                    f"with the following args: '{args}', and kwargs: '{kwargs}'. "
                    f"Return value: '{result}'" + '\n')
            return result

        return new_func

    return __decorator


@param_decorator(log_path='task3_log.txt')
def lines_md5_generator(file):
    with open(file, 'r') as f:
        lines = f.readlines()

    for line in lines:
        yield hashlib.md5(line.encode('UTF-8')).hexdigest()


def main():
    for item in lines_md5_generator('countries.json'):
        print(item)


param_decorator(lines_md5_generator)

main()
