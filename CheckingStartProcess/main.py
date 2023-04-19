import datetime
import run

plnst = "['8:15']"
nh = 8
nm = 30
plnday = "['1,2,3,4,5']"
tt2 = run.CheckingStartProcess(nh,nm,plnst,plnday).check_start()
print(tt2)