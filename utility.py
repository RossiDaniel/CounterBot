from datetime import timedelta, datetime, tzinfo

def concat(words):
    args_str = '('
    for word in range(len(words)-1):
        args_str+=str(words[word])+','
    args_str+=str(words[len(words)-1])
    args_str+=')'

    return args_str

def now():
    now = datetime.now()
    minutes = now.hour*60 + now.minute
    best = [(minutes /15)*15,((minutes/15)+1)*15]
    result = min(best, key=lambda x:abs(x-minutes))
    hours = (result / 15) / 4
    minutes = (result - hours*60)
    return str(hours)+":"+str(minutes)+"-"+str(now.year)+"/"+str(now.day)+"/"+str(now.month)

def str_time(elapsed_time):
        return str(elapsed_time/60)+" ore, "+str(elapsed_time%60)+" minuti"

def difference(date1,date2):
    strstart = str(date1).split('-')
    strstop = str(date2).split('-')

    hourstart=str(strstart[0]).split(':')
    datestart=[int(x) for x in str(strstart[1]).split('/')]

    hourstop=str(strstop[0]).split(':')
    datestop=[int(x) for x in str(strstop[1]).split('/')]
    
    difference_day = datetime(datestart[0],datestart[2],datestart[1]) - datetime(datestop[0],datestop[2],datestop[1])

    start = int(hourstart[0])*60 + int(hourstart[1])
    stop = int(hourstop[0])*60 + int(hourstop[1]) + difference_day.days*1440

    elapsed_time = stop-start
    return elapsed_time