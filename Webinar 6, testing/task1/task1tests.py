from task1app import *
import random
import string


class TestBuhApp:

    def setup(self):
        self.doc_type = random.choice([doc['type'] for doc in documents])
        self.doc_number = random.choice([doc['number'] for doc in documents])
        self.doc_owner_name = random.choice([doc['name'] for doc in documents])
        self.random_doc_number = '~'.join(random.choice(string.ascii_letters) for x in range(5))
        self.shelf_number = random.choice(list(directories.keys()))
        self.shelf_max_number = int(max(directories.keys()))
        self.random_shelf_number = str(random.randrange(self.shelf_max_number + 1, self.shelf_max_number + 1000))

    def test_doc_exist(self):
        assert doc_exists(self.doc_number)

    def test_doc_exist_wrong_number(self):
        assert not doc_exists(self.random_doc_number)

    def test_shelf_exist(self):
        assert shelf_exists(self.shelf_number)

    def test_shelf_exist_wrong_shelf(self):
        assert not shelf_exists(self.random_shelf_number)

    def test_doc_add(self):
        assert doc_add(self.shelf_number, self.doc_type, self.doc_number, self.doc_owner_name)

    def test_doc_add_wrong_shelf(self):
        assert not doc_add(self.random_shelf_number, self.doc_type, self.doc_number, self.doc_owner_name)

    def test_shelf_add(self):
        assert shelf_add(self.random_shelf_number)

    def test_shelf_add_wrong_shelf(self):
        assert not shelf_add(self.shelf_number)

    def test_doc_del(self):
        assert doc_del(self.doc_number)

    def test_doc_del_wrong_number(self):
        assert not doc_del(self.random_doc_number)

    def test_get_all_docs(self):
        assert get_all_docs()

    def test_doc_move(self):
        assert doc_move(self.doc_number, self.shelf_number)

    def test_doc_move_wrong_shelf(self):
        assert not doc_move(self.doc_number, self.random_shelf_number)

    def test_doc_move_wrong_doc(self):
        assert not doc_move(self.random_doc_number, self.shelf_number)

    def test_get_doc_owner_name(self):
        assert get_doc_owner_name(self.doc_number)

    def test_get_doc_owner_name_wrong_doc(self):
        assert not get_doc_owner_name(self.random_doc_number)

    def test_get_doc_shelf_number(self):
        assert get_doc_shelf_number(self.doc_number)

    def test_get_doc_shelf_number_wrong_doc(self):
        assert not get_doc_shelf_number(self.random_doc_number)
