def decorator(func):
    from datetime import datetime

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('task1_log.txt', 'a') as log_file:
            log_file.write(
                f"[{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}] Function '{func.__name__}' was called "
                f"with the following args: '{args}', and kwargs: '{kwargs}'. "
                f"Return value: '{result}'" + '\n')
        return result

    return wrapper


@decorator
def task1_func(*args, **kwargs):
    return 'This is my function.'


if __name__ == '__main__':
    task1_func(1, 2, 'a', b='test')
