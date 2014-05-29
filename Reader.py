import datetime
import Common

log_handle = open('/opt/zfs_perf_tests/logs/derp/results/20140529051756','r')

results_map = {}
prefix = 'start'
for line in log_handle:
    if 'time' in line:
        time = int(float(line[6:]))
        results_map[prefix + 'time'] = time
    elif 'TXG' in line:
        txg = int(line[5:])
        results_map[prefix + 'txg'] = txg
    elif 'size' in line:
        size = int(line[6:])
        results_map[prefix + 'size'] = size
    elif 'END' in line:
        prefix = 'end'
        
delta_time = results_map['endtime'] - results_map['starttime']
delta_txgs = results_map['endtxg'] - results_map['starttxg']
delta_size = results_map['endsize'] - results_map['startsize']
"""
print("time delta was : " + str(delta_time))
print("txg delta was : " + str(delta_txgs))
print("size delta was : " + str(delta_size))
"""
txgs_per_second = float(delta_txgs)/delta_time
bytes_per_second = float(delta_size) / delta_time
mibibytes_per_second = Common.bytes_to_mebibyte(bytes_per_second)

print("Total time : " + str(datetime.timedelta(seconds=delta_time)))
print("MiB/s : " + str(mibibytes_per_second))
print("TXGs per second : " + str(txgs_per_second))
