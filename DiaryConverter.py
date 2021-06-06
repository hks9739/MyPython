import tkinter.filedialog
import json
import re
import bs4.element
from bs4 import BeautifulSoup
from datetime import datetime
import html2text


def get_html_bs():
    # infile = tkinter.filedialog.askopenfile(encoding='UTF-8')
    # s = BeautifulSoup(infile, 'html.parser')
    bs = None
    filename = tkinter.filedialog.askopenfilename()
    if filename:
        with open(filename, 'r', encoding='UTF-8') as f:
            bs = BeautifulSoup(f, 'html.parser')
    return bs


def memoires_date_to_timestamp(mdate):
    p = re.compile(r'(\d+)년 (\d+)월 (\d+)일 \w+ at (오전|오후) (\d+):(\d+)')
    m = p.match(mdate)
    if m:
        # locale 설정을 하면 되지만 환경별로 차이가 크기 때문에 24시간 제로 변경
        # locale.setlocale(locale.LC_TIME, "")
        hour = int(m.group(5))
        if hour == 12:
            hour = 0
        if m.group(4) == '오후':
            hour += 12
        date_str = '%s-%02d-%02d %02d:%02d' % (m.group(1), int(m.group(2)), int(m.group(3)), hour, int(m.group(6)))
        res = datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    else:
        res = datetime.now()

    # print(res)
    return int(res.timestamp() * 1000)  # in ms


def memoires_bs_to_json(bs):
    entries = []
    entry = None
    note_maker = html2text.HTML2Text()
    note_maker.ignore_links = True
    note_maker.single_line_break = True

    for e in bs.body.children:
        if not isinstance(e, bs4.element.Tag):
            continue

        if e.name == 'div':
            if entry:
                entries.append(entry)
                entry = None

            entry = {'audio': [], 'createdDate': 0, 'mood': 3, 'moodColor': -16121, 'photos': [], 'starred': 0, 'tags': []}

            create_date = e.find('p', class_='sDateCreated').string
            entry['createdDate'] = memoires_date_to_timestamp(create_date)

            # loc = e.find('p', class_='sLocation')
            # print(loc.a.string)

        elif e.get('class'):
            if 'sExtPara' in e['class']:
                note = e.find(class_='sNote')  # bs4.element.Tag
                # print(note)
                entry['text'] = note_maker.handle(str(note)).strip()

                tags = e.find(class_='sTags').string
                if tags:
                    entry['tags'] = tags.split(', ')

            elif 'imgPara' in e['class']:
                entry['photos'].append(e.img['src'].replace('./images/', ''))
                # print(entry['photos'])

        # print('######################')

    if entry:
        entries.append(entry)

    return entries


def write_json_data(data):
    # print(json.dumps(data, indent=4, ensure_ascii=False))
    filename = tkinter.filedialog.asksaveasfilename()
    with open(filename, 'w', encoding='UTF-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_json_data():
    data = None
    filename = tkinter.filedialog.askopenfilename()
    if filename:
        with open(filename, 'r', encoding='UTF-8') as f:
            data = json.load(f)
    return data


s = get_html_bs()
# print(s.prettify())
new_data = memoires_bs_to_json(s)

# json 포맷 데이타로 출력
write_json_data(new_data)

# print(s.prettify())
# body = s.body.contents
# print(len(body))
