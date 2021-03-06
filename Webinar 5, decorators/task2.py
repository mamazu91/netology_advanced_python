def decorator(log_path):
    from datetime import datetime

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


@decorator(log_path='task2_log.txt')
def task2_func(*args, **kwargs):
    return 'This is my function.'


if __name__ == '__main__':
    task2_func(1, 2, 'a', b='test')
