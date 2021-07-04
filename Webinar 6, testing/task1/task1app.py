documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}


def doc_exists(doc_number):
    for doc in documents:
        if doc['number'] == doc_number:
            return True

    return False


def shelf_exists(shelf_number):
    if shelf_number in directories.keys():
        return True

    return False


def doc_add(shelf_number, doc_type, doc_number, doc_owner_name):
    if not shelf_exists(shelf_number):
        print('There is no shelf with this number.', end='\n\n')
        return False

    documents.append({
        'type': doc_type,
        'number': doc_number,
        'name': doc_owner_name
    })
    directories[shelf_number].append(doc_number)
    print(f'The document {doc_type} "{doc_number}" "{doc_owner_name}" was successfully added '
          f'to the shelf {shelf_number}.', end='\n\n')
    return True


def shelf_add(shelf_number):
    if shelf_exists(shelf_number):
        print(f'The shelf {shelf_number} already exists.', end='\n\n')
        return False

    directories[shelf_number] = []
    print(f'The shelf {shelf_number} was successfully added.', end='\n\n')
    return True


def doc_del(input_doc_number):
    if not doc_exists(input_doc_number):
        print('There is no document with this number.', end='\n\n')
        return False

    for shelf_number, doc_number in directories.items():
        if input_doc_number in doc_number:
            doc_number.remove(input_doc_number)
            print(f'The document "{input_doc_number}" was successfully removed from the shelf {shelf_number}')
    for document in list(documents):
        if document['number'] == input_doc_number:
            documents.remove(document)
            print(f'The document "{input_doc_number}" was successfully removed from the documents list.')
    print('')
    return True


def get_all_docs():
    all_docs = [list(doc.values()) for doc in documents]
    print('Available documents:')
    for doc_type, doc_number, doc_owner_name in all_docs:
        print(f'- {doc_type} "{doc_number}" "{doc_owner_name}"')
    print('')
    return True


def doc_move(input_doc_number, input_shelf_number):
    if not shelf_exists(input_shelf_number):
        print('There is no shelf with this number.', end='\n\n')
        return False
    if not doc_exists(input_doc_number):
        print('There is no document with this number.', end='\n\n')
        return False

    for shelf_number, doc_number in directories.items():
        if input_doc_number in doc_number and shelf_number != input_shelf_number:
            doc_number.remove(input_doc_number)
            directories[input_shelf_number].append(input_doc_number)
            print(f'The document "{input_doc_number}" was successfully moved from the shelf {shelf_number} '
                  f'to the shelf {input_shelf_number}', end='\n\n')
    return True


def get_doc_owner_name(doc_number):
    if not doc_exists(doc_number):
        print('There is no document with this number.', end='\n\n')
        return False

    doc_owners = [doc['name'] for doc in documents if doc['number'] == doc_number]
    print(f'The document "{doc_number}" belongs to the following person(s): {", ".join(doc_owners)}.',
          end='\n\n')
    return True


def get_doc_shelf_number(input_doc_number):
    if not doc_exists(input_doc_number):
        print('There is no document with this number.', end='\n\n')
        return False

    doc_shelves = [shelf_number for shelf_number, doc_number in directories.items() if
                   input_doc_number in doc_number]
    print(f'The document "{input_doc_number}" can be found on the following shelve(s): {", ".join(doc_shelves)}.',
          end='\n\n')
    return True

# def main():
#     print('Please enter a command, or type "help" for the commands list: ', end='')
#     user_input = input()
#     if user_input == 'help':
#         print('List of available commands:\n'
#               'a (add) - add a new document.\n'
#               'as (add shelf) - add a new shelf.\n'
#               'd (delete document) - delete the document.\n'
#               'l (list) - print the list of available documents.\n'
#               'm (move document) - move the document to another shelf.\n'
#               'p (people) - print the document owner(s).\n'
#               'q (quit) - quit the application.\n'
#               's (shelf) - print the document shelf', end='\n\n')
#     elif user_input == 'a':
#         doc_add()
#     elif user_input == 'as':
#         shelf_add()
#     elif user_input == 'd':
#         doc_del()
#     elif user_input == 'l':
#         get_all_docs()
#     elif user_input == 'm':
#         doc_move()
#     elif user_input == 'p':
#         get_doc_owner_name()
#     elif user_input == 'q':
#         print('Quitting the application.')
#         quit()
#     elif user_input == 's':
#         get_doc_shelf_number()
#
#
# while True:
#     main()
