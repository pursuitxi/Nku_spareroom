import json
import argparse
from datetime import datetime

def pretty_print_list(lst, items_per_line=6):
    for i in range(0, len(lst), items_per_line):
        print('\t' + ' '.join(map(str, lst[i:i+items_per_line])))
        
def find_current_phase(schedule):
    current_time = datetime.now().strftime("%H:%M")
    closest_phase = None
    min_difference = float('inf')

    for item in schedule:
        start_time = item["start"]
        end_time = item["end"]
        phase = item["phase"]

        # 计算当前时间与阶段开始时间的差值
        start_difference = (datetime.strptime(start_time, "%H:%M") - datetime.strptime(current_time, "%H:%M")).total_seconds()
        # 计算当前时间与阶段结束时间的差值
        end_difference = (datetime.strptime(end_time, "%H:%M") - datetime.strptime(current_time, "%H:%M")).total_seconds()

        # 如果当前时间在阶段的时间范围内，则直接返回该阶段
        if start_difference <= 0 <= end_difference:
            return phase
        # 如果当前时间比当前最小差值更接近阶段开始时间，则更新最接近阶段的信息
        elif abs(start_difference) < min_difference:
            min_difference = abs(start_difference)
            closest_phase = phase
        # 如果当前时间比当前最小差值更接近阶段结束时间，则更新最接近阶段的信息
        elif abs(end_difference) < min_difference:
            min_difference = abs(end_difference)
            closest_phase = phase

    return closest_phase


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

    current_phase = find_current_phase(schedule) 

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
