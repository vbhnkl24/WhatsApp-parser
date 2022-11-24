import csv
import re
import json
import os


def datadump(data, file):
    path = os.path.dirname(__file__)
    filename = os.path.join(path, f"{file}")
    with open(filename, 'w') as Fout:
        json.dump(data, Fout, indent=4, sort_keys=True)


# finding the first two colons in the message, which are used to indicate
# the date of the message and the message author's name
def make_obj(row: str) -> (str, str):
    time_colon = 0
    time = False
    for let in range(len(row)):
        temp = row[let]
        if temp == ':':
            if time:
                return time_colon, let
            else:
                time_colon = let
                time = True
    return None, None


def main():
    # dump messages and some additional stats into csv files
    with open('tsohar.txt', 'r', encoding='utf-8') as file:
        data = file.read().splitlines()
    f = csv.writer(open('tsohar.csv', 'w', encoding='utf-8'))
    f.writerow(['author', 'date', 'text'])
    g = csv.writer(open('tsohar_stats.csv', 'w', encoding='utf-8'))
    # g.writerow(['name', 'number of messages', 'most common word', 'number of appearances'])
    g.writerow(['name', 'number of messages'])
    # check for AM/PM. if they aren't present in a line, it's discarded as
    # not being a message(usually being new line mistakes in the raw file)
    r = re.compile('.*[AP]M*')
    stats = {}
    # sort all messages and their dates according to sender
    print("parsing raw file")
    for row in data:
        if r.match(row) is None:
            continue
        time, author = make_obj(row)
        if (time is None) or (author is None):
            continue
        name = row[time+9:author]
        if name not in stats.keys():
            stats[name] = {
                'num': 1,
                'messages': [{
                    'date' : row[:time+6],
                    'text': row[author+1:]
                }]
            }
        else:
            stats[name]['num'] += 1
            stats[name]['messages'].append({
                'date' : row[:time+6],
                'text': row[author+1:]
            })
        f.writerow([name, row[:time+6], row[author+1:]])

    print("pulling global stats")
    # find number of messages from each member and sort by number,
    # and find most common word used by each member
    user_num = {}
    # user_messages = {}
    # pull used words from stats dictionary
    for user in stats:
        user_num[user] = stats[user]['num']
        """user_messages[user] = []
        [user_messages[user].extend(msg.split()) for msg in [item['text'] for item in stats[user]['messages']]]"""

    print("sorting words and amounts")
    # move words and amounts into sorted dictionaries
    user_num = dict(reversed(sorted(user_num.items(), key= lambda item: item[1])))
    """counted_messages = {}
    for user in user_messages:
        print(f"current user: {user}")
        counted_messages[user] = {item:user_messages[user].count(item) for item in user_messages[user]}
        counted_messages[user] = dict(reversed(sorted(counted_messages[user].items(), key=lambda item: item[1])))
        print([f"{list(counted_messages[user].keys())[i]},"
               f" {list(counted_messages[user].values())[i]}"
               for i in range(2)])"""
    print("finished parsing users")
    print(f"number of overall messages: {sum([stats[item]['num'] for item in stats])}")
    datadump(stats, 'stats.json')
    # datadump(counted_messages, 'counted_messages.json')
    for user in user_num:
        # g.writerow([user, user_num[user],
        #           list(counted_messages[user].keys())[0], list(counted_messages[user].values())[0]])
        g.writerow([user, user_num[user]])

if __name__ == '__main__':
    main()