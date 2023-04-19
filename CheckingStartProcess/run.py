import datetime

'''
Модуль для определения запуска задачи по расписанию с учетом времени лага планировщика
Пример вызова:
plnst = "['8:15']"
nh = 8
nm = 30
plnday = "['1,2,3,4,5']"
tt2 = run.CheckingStartProcess(nh,nm,plnst,plnday).check_start()
print(tt2)
''' 

class CheckingStartProcess(object):
    list_minute = []
    list_minute_fix = []
    lst_part_1 = []
    lst_part_2 = []
    lst_part_2_fix = []
    all_list_times = []

    def __init__(self,nh,nm,plnst,plnday):
        self.nh = nh        #текущий час старта
        self.nm = nm        #текущая минута старта
        self.plnst = plnst      #плановое время старта
        self.plnday = plnday        #плановый номер дня недели старта
        self.start_timeout = 15     #сколько минусуем минут от минуты старта (лаг)
        self.hour_lag = 1
        self.res_day = False        #результирующая переменная вычисления дня старта
        self.res_time = False       #результирующая переменная вычисления времени старта
        self.nowday = datetime.datetime.now().weekday()+1       #текущий день старта
        self.plnst_cl = str(self.plnst.replace("']","").replace("['",""))
        self.plnday_cl = str(self.plnday.replace('"',"").replace(','," "))


    def check_start(self):
        prev_nm = self.nm-self.start_timeout
        prev_nh = self.nh
        if self.nm <= self.start_timeout:       #сформируем список минут
            prev_nm = (60+nm)-self.start_timeout
            prev_nh = self.nh-self.hour_lag
        for i in list(range(prev_nm,self.nm+1)):
            self.list_minute.append(str(i).zfill(2))
        if self.nm <= self.start_timeout:
            for i in list(range(prev_nm,(61+self.nm))):
                self.list_minute.append(str(i).zfill(2))

        for i in self.list_minute:      #сформируем 2 списка в формате ч:мин за прошлый и текущий час
            if i < '60':
                self.lst_part_1.append(i)
        for i in self.list_minute:
            if i >= '60':
                self.lst_part_2.append(i)
        self.list_minute_fix.append(self.lst_part_1)
        for ii, val in enumerate(self.lst_part_2):
            if val >= '60':
                val = val.replace(val,str(ii))
                self.lst_part_2_fix.append(val) 
        self.list_minute_fix.append(self.lst_part_2_fix)                 
        for i in self.lst_part_1:
            self.all_list_times.append(str(prev_nh)+":"+i)
        for i in self.lst_part_2_fix:
            self.all_list_times.append(str(self.nh)+":"+i.zfill(2))

        if self.plnst_cl in self.all_list_times:        #выполним проверку вхождения параметра в сформированный список ч:мин
            self.res_time = True

        if str(self.nowday) in str(self.plnday_cl):     #выполним проверку вхождения параметра номер дня недели
            self.res_day = True

        if self.res_day == True and self.res_time == True: #выполним итоговую проверку полученных результатов
            return True
        else:
            return False

