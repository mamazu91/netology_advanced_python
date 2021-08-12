from db import setup
from vk import longpoll


def main() -> None:
    setup.create_users_table()
    setup.create_matches_table()

    longpoll.send_matches()


if __name__ == '__main__':
    main()
