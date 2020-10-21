from mailchimp3 import MailChimp
import csv

API_KEY = 'c7fa7e8c464aeb475d012f0867f0047e-us8'

OUTPUT_FILE = 'members.csv'

client = MailChimp(API_KEY)


def write_to_csv(member_list):
    keys = member_list[0].keys()
    with open(OUTPUT_FILE, 'w', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(member_list)


def get_all_lists():
    return client.lists.all(get_all=True, fields="lists.name,lists.id")['lists']


if __name__ == '__main__':
    lists = get_all_lists()

    members_list = []
    for lst in lists:
        members = client.lists.members.all(lst['id'], get_all=True)['members']
        for member in members:
            if member['status'] == 'subscribed':
                member_dict = {
                    'list name': lst['name'],
                    'email': member['email_address'],
                    'first name': member['merge_fields']['FNAME'],
                    'last name': member['merge_fields']['LNAME'],
                    'average open rate': member['stats']['avg_open_rate'],
                    'average click rate': member['stats']['avg_click_rate']
                }
                members_list.append(member_dict)

    write_to_csv(members_list)
