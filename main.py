from pprint import pprint
import re
from IO_data import read_data_from_file, write_data_to_file


def fix_full_name_and_phone(contacts_list):
    pattern = (r'(\+7|8)\s*[\(|\s]*(\d{1,3})[\)|\s]*[\-\s]*(\d{1,3})[\-\s]*(\d{1,2})[\-\s]*(\d{1,2})(\s*)[\(\s]*(['
               r'\w\.]*)\s*([\d]*)\)*')
    sub = r'+7(\2)\3-\4-\5\6\7\8'
    for contact_data in contacts_list[1:]:
        initials = " ".join(contact_data[:3])
        initials_list = initials.split(" ")
        for initial in initials_list[:3]:
            contact_data[initials_list.index(initial)] = initial
        contact_data[5] = sub_string(pattern, sub, contact_data[5])
    return contacts_list


def sub_string(pattern, sub, current_str):
    pattern = re.compile(pattern)
    result = pattern.sub(sub, current_str)
    return result


def update_list(person_data, contacts_list, persons_dict, persons_list):
    delete_data = contacts_list.pop(contacts_list.index(person_data))
    # В списке словарей "persons_list" пропущен первый элемент телефонной книги, поэтому индекс увеличивается на 1
    update_data = contacts_list[persons_list.index(persons_dict) + 1]
    for item in delete_data:
        if item != '':
            update_data[delete_data.index(item)] = item


def merge_contacts(fixed_contacts_list):
    persons_list = []
    for person_data in fixed_contacts_list[1:]:
        persons_dict = {'lastname': person_data[0],
                        'firstname': person_data[1]}
        if persons_list.count(persons_dict) > 0:
            update_list(person_data, fixed_contacts_list, persons_dict, persons_list)
        else:
            persons_list.append(persons_dict)

    return fixed_contacts_list


if __name__ == '__main__':
    contacts_list = read_data_from_file()
    fixed_contacts_list = fix_full_name_and_phone(contacts_list)
    final_contacts_list = merge_contacts(fixed_contacts_list)
    write_data_to_file('cooked_phonebook', final_contacts_list)
    pprint(fixed_contacts_list)
