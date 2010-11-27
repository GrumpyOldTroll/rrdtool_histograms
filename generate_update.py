import random

update_file = open('/cygdrive/c/Documents and Settings/Educator/Desktop/Jonathan/mysite/update1', 'w')

accel_open = [0 for x in range(128)]
accel_closed = [0 for x in range(128)]
unaccel_open = [0 for x in range(128)]
unaccel_closed = [0 for x in range(128)]

print len(accel_open)

for num in range(1000000001, 1000100000, 3):
    line = 'update count_per_rtt.rrd ' + str(num)
    for val in range(len(accel_open)):
        accel_open[val] += random.randrange(50)
        line += ':' + str(accel_open[val])
    for val in range(len(accel_closed)):
        accel_closed[val] += random.randrange(50)
        if accel_closed[val] > accel_open[val]:
            accel_closed[val] = accel_open[val]
        line += ':' + str(accel_closed[val])
    for val in range(len(unaccel_open)):
        unaccel_open[val] += random.randrange(50)
        line += ':' + str(unaccel_open[val])
    for val in range(len(unaccel_closed)):
        unaccel_closed[val] += random.randrange(50)
        if unaccel_closed[val] > unaccel_open[val]:
            unaccel_closed[val] = unaccel_open[val]
        line += ':' + str(unaccel_closed[val])
    line += '\n'
    update_file.writelines(line)
    if (num % 100) == 0 : print num
