# Python program to read
# json file


import json
import pandas

d = {'url': [], 'text': [], 'photo_url': [], 'date': []}
df = pandas.DataFrame(data=d)
# Opening JSON file
with open('result.json', 'r', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)
    name = data['name']
    url = 'https://t.me/fighter_bomber'
    for message in data['messages']:
        date = message['date']
        text = message['text']
        if not text or (isinstance(text, str) and len(text) < 20):
            continue
        if isinstance(text, list):
            cur_text = ''
            for part_text in text:
                if isinstance(part_text, str) and len(text) < 25:
                    cur_text += part_text
            text = cur_text
            if len(text) > 15:
                continue
        photo = message.get('photo_url', '')
        if photo:
            print(photo)
        try:
            df = df.append({'url': url, 'text': text, 'date': date, 'photo_url': photo}, ignore_index=True)
        except Exception as ex:
            print(1)

df.to_csv(name + '.csv')

# Iterating through the json
# list
print(1)
# Closing file
f.close()
