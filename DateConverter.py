import time
from datetime import datetime
import locale
import re

s = '2013년 4월 12일 금요일 at 오전 12:38'
date = re.findall(r'(\d{4})년 (\d+)월 (\d+)일 \w+ at (오전|오후) (\d+):(\d+)', s)
print(re.findall(r'(\d{4})년 (\d+)월 (\d+)일 \w+ at (오전|오후) (\d+):(\d+)', s))

p = re.compile(r'(\d+)년 (\d+)월 (\d+)일 \w+ at (오전|오후) (\d+):(\d+)')
m = p.match(s)
if m:
    # locale 설정을 하면 되지만 환경별로 차이가 크기 때문에 24시간 제로 변경
    # locale.setlocale(locale.LC_TIME, "")
    hour = int(m.group(5))
    if hour == 12:
        hour = 0
    if m.group(4) == '오후':
        hour += 12

    s = '%s-%02d-%02d %02d:%02d' % (m.group(1), int(m.group(2)), int(m.group(3)), hour, int(m.group(6)))
    print(s)

new_time = datetime.strptime(s, '%Y-%m-%d %H:%M')

print(new_time)
print(new_time.timetuple())
print(new_time.timestamp())  # From python 3.3

# 현재 timestamp 값, local 이 반영된 값이다.
print(datetime.now().timestamp())