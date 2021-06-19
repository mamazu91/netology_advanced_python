import csv
import re


def get_contacts():
    with open('phonebook_raw.csv', encoding='utf-8') as phonebook:
        rows = csv.reader(phonebook, delimiter=',')
        contacts = list(rows)

        return contacts


def fix_contacts(contacts_raw):
    pattern = r'(\+?\d)\s?\(?(\d{3})\)?[\s|\-]?(\d{3})\-?(\d{2})\-?(\d{2})\s?\(?(\w*\.?)\s?(\d*)\)?'
    sub = r'+7(\2)\3-\4-\5 \6\7'
    contacts_clean = {}

    for contact in contacts_raw:
        contact_name = ' '.join(contact[0:3]).split(' ')
        key = (contact_name[0], contact_name[1])
        contact_to_append = [
            contact_name[0],
            contact_name[1],
            contact_name[2],
            contact[3],
            contact[4],
            re.sub(pattern, sub, contact[5]).strip(),
            contact[6]
        ]

        if not contacts_clean.get(key):
            contacts_clean[key] = contact_to_append
        else:
            for i in range(0, len(contact_to_append)):
                if not contacts_clean[key][i]:
                    contacts_clean[key][i] += contact_to_append[i]

    return contacts_clean


def save_contacts(contacts_clean):
    with open('phonebook_clean.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(contacts_clean)


def main():
    contacts_raw = get_contacts()
    contacts_clean = fix_contacts(contacts_raw)
    save_contacts(contacts_clean.values())


main()
