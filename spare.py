import json
import argparse
from datetime import datetime

def pretty_print_list(lst, items_per_line=6):
    for i in range(0, len(lst), items_per_line):
        print('\t' + ' '.join(map(str, lst[i:i+items_per_line])))

parser = argparse.ArgumentParser(description="Spare Classroom:")  # )
parser.add_argument('-a', '--area', type=str, help=' choose area: a for A or b for B ')
parser.add_argument('-t', '--time', type=str, help=' choose time: 1~14 ')
parser.add_argument('-r', '--room', type=str, help=' check room ')
args = parser.parse_args()

file_path = "spare_classroom.json"

# 读取 JSON 文件中的数据
with open(file_path, 'r') as json_file:
    data = json.load(json_file)

# 读取星期
today = datetime.today()
day_of_week = today.weekday() + 1


if args.room is None:

    # 判断阶段
    #====================================================================================

    schedule = [
        {"start": "08:00", "end": "08:45", "phase": "1"},
        {"start": "08:55", "end": "09:40", "phase": "2"},
        {"start": "10:00", "end": "10:45", "phase": "3"},
        {"start": "10:55", "end": "11:40", "phase": "4"},
        {"start": "12:00", "end": "12:45", "phase": "5"},
        {"start": "12:55", "end": "13:40", "phase": "6"},
        {"start": "14:00", "end": "14:45", "phase": "7"},
        {"start": "14:55", "end": "15:40", "phase": "8"},
        {"start": "16:00", "end": "16:45", "phase": "9"},
        {"start": "16:55", "end": "17:40", "phase": "10"},
       ]

    # 获取当前时间的小时和分钟
    current_time = datetime.now().time()
    current_hour, current_minute = current_time.hour, current_time.minute

    # 将当前时间转换为分钟
    current_total_minutes = current_hour * 60 + current_minute

    # 判断当前处于哪个阶段
    current_phase = None
    for item in schedule:
        start_time_hour, start_time_minute = map(int, item["start"].split(":"))
        end_time_hour, end_time_minute = map(int, item["end"].split(":"))
        start_total_minutes = start_time_hour * 60 + start_time_minute
        end_total_minutes = end_time_hour * 60 + end_time_minute
        if start_total_minutes <= current_total_minutes <= end_total_minutes:
            current_phase = item["phase"]
            break

    # 如果不处于任何一个阶段，则找出最近的一个阶段
    if current_phase is None:
        nearest_phase = min(schedule, key=lambda x: abs(int(x["start"].replace(":", "")) - current_total_minutes))
        current_phase = nearest_phase["phase"]

    #====================================================================================


    if args.area and args.time:
        print(f'{args.area.upper()}区： ')
        pretty_print_list(data[fr'{day_of_week}'][args.area][args.time])
    elif args.area and args.time is None:
        print(f'{args.area.upper()}区： ')
        pretty_print_list(data[fr'{day_of_week}'][args.area][current_phase])
    elif args.time and args.area is None:
        print("A区： ")
        pretty_print_list(data[fr'{day_of_week}']['a'][args.time])
        print("B区： ")
        pretty_print_list(data[fr'{day_of_week}']['b'][args.time])
    else:
        print("A区： ")
        pretty_print_list(data[fr'{day_of_week}']['a'][current_phase])
        print("B区： ")
        pretty_print_list(data[fr'{day_of_week}']['b'][current_phase])

else:
    sparetime = []
    if args.area:
        for i in range(1,14):
            if args.room in data[fr'{day_of_week}'][args.area][fr'{i}']:
                sparetime.append(f'{i}' + '\t' + '空闲' + '\n')
            else:
                sparetime.append(f'{i}' + '\t' + '有课' + '\n')
        print("教室情况为： ")
        pretty_print_list(sparetime,1)
    else:
        print('请输入区域')
