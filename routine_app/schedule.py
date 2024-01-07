import random as rnd

import pandas as pd


class _Class:
    section_title = None
    course_id = None
    instructor = None
    room = None
    duration = None
    preferred_slot = None
    start_slot = None

    def set_section(self, title):
        self.section_title = title

    def set_course(self, course_id):
        self.course_id = course_id

    def set_instructor(self, faculty):
        self.instructor = faculty

    def set_room(self, room_no):
        self.room = room_no

    def set_duration(self, duration):
        self.duration = duration

    def set_preferred_slot(self, feasible_slots):
        self.preferred_slot = feasible_slots


class Schedule:
    slot_pref = {
        1: [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 1, 2, 4, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23, 25, 26, 28, 29],
        2: [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29],
        3: [4, 10, 16, 22, 28, 1, 7, 13, 19, 25]
    }

    def __init__(self, data, resource_data):
        self.data = data
        self.resources = resource_data
        self.classes = []
        self.unallocated = []
        self.schedule = {}
        # self.class_no = 0
        # self.conflicts=-1
        # self.fitness=0
        # self.is_fitness_changed=True

    def suffle_n_sort(self):
        temp1 = {}
        temp2 = []

        for _class in self.classes:
            if _class.duration in temp1:
                temp1[_class.duration].append(_class)
            else:
                temp1[_class.duration] = [_class]

        for k in temp1:
            rnd.shuffle(temp1[k])

        temp1 = dict(sorted(temp1.items(), key=lambda x: x[0], reverse=True))

        for k in temp1:
            temp2.extend(temp1[k])

        self.classes = temp2

    def create_classes(self):
        sections = self.data.sections
        for section in sections:

            title = section.get_title()
            courses = section.get_courses()
            section_classes = []

            # total_required_slots=section.get_courses()['HOUR'].sum()

            for course in courses.itertuples():
                for i in list(map(int, str(course.SLOT_BREAK_UP).split(','))):
                    new_class = _Class()
                    new_class.set_section(title)
                    new_class.set_course(course.SUBJECT_CODE)
                    new_class.set_instructor([i for i in str(course.FACULTY).split(',')])
                    new_class.set_room([x for x in str(course.ROOM).split(',')])
                    new_class.set_duration(i)
                    new_class.set_preferred_slot(self.slot_pref[i])
                    section_classes.append(new_class)

            # section_classes.sort(lambda x:x.duration, reverse=True)
            self.classes.extend(section_classes)
        self.classes.sort(key=lambda x: (x.duration, x.section_title), reverse=True)

    def generate(self):
        self.suffle_n_sort()

        def check_engagement(cl, slt):
            a = []
            b = []
            c = []

            def is_free(key, df, sl):
                sl = sl - 1
                schedule = df.loc[df['RESOURCE_ID'] == key]["SLOT_AVAILIBILITY"]
                schedule = str(schedule.max()).split('.')
                req_day = [*str(bin(int(schedule[sl // 6], 16)))[2:].rjust(6, '0')]
                return req_day[-int(sl % 6) - 1] == '0'

            for t in range(slt, slt + cl.duration):
                a.append(is_free(cl.section_title, self.resources.Section_data, t))
                b.append(all(is_free(inst, self.resources.Faculty_data, t) for inst in cl.instructor))
                c.append(all(is_free(rm, self.resources.Room_data, t) for rm in cl.room))

            return all(a) and all(b) and all(c)

        def engage(cl, slt):

            def engage_resource(key, df, sl):
                sl = sl - 1
                schedule = df.loc[df['RESOURCE_ID'] == key]["SLOT_AVAILIBILITY"]
                schedule = str(schedule.max()).split('.')
                req_day = [*str(bin(int(schedule[sl // 6], 16)))[2:].rjust(6, '0')]
                req_day[-int(sl % 6) - 1] = '1'
                schedule[sl // 6] = str(hex(int('0b' + ''.join(req_day), 2)))[2:]
                schedule = '.'.join(schedule)
                df.loc[df['RESOURCE_ID'] == key, "SLOT_AVAILIBILITY"] = schedule

            for t in range(slt, slt + cl.duration):
                engage_resource(cl.section_title, self.resources.Section_data, t)
                [engage_resource(inst, self.resources.Faculty_data, t) for inst in cl.instructor]
                [engage_resource(rm, self.resources.Room_data, t) for rm in cl.room]

        for i in range(len(self.classes)):
            flag = False
            for slot in self.classes[i].preferred_slot:
                if check_engagement(self.classes[i], slot):
                    self.classes[i].start_slot = slot
                    engage(self.classes[i], slot)
                    flag = True
                    break
            if not flag:
                self.unallocated.append(self.classes[i])

        self.arrange_schedule()

    def arrange_schedule(self):
        self.classes.sort(key=lambda x: (x.section_title, x.start_slot))
        for _class in self.classes:
            if _class.section_title in self.schedule:
                self.schedule[_class.section_title].append(_class)
            else:
                self.schedule[_class.section_title] = [_class]

    def display(self):
        for section in self.schedule:
            print(section)
            print("time\tsubject\tinstructor\troom\tduration")
            for _cl in self.schedule[section]:
                print(f"{_cl.start_slot}\t{_cl.course_id}\t{_cl.instructor}\t{_cl.room}\t{_cl.duration}")
            print("\n\n")

        print("Unallocated:", self.unallocated)

    def save_schedule(self, path):
        writer = pd.ExcelWriter(path)
        for section in self.schedule:
            routine = {}
            for cl in self.schedule[section]:
                for sl in range(cl.start_slot, cl.start_slot + cl.duration):
                    i = (sl - 1) // 6
                    j = (sl - 1) % 6
                    if "Day" + str(i) in routine:
                        routine["Day" + str(i)][j] = f'{cl.course_id}'
                    else:
                        routine["Day" + str(i)] = {j: f'{cl.course_id}'}
            routine = pd.DataFrame(routine).T
            routine.to_excel(writer, section)
        writer.close()

# s=Schedule(data.data,data.resource_data)
# s.create_classes()
# s.generate()
# s.save_schedule("..//Databases//routine.xlsx")
# s.display()
# #print(data.resource_data.Room_data)
