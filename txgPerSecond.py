import time
import ZfsApi
import MovingAverage
import TestConfig
import Configs

txg_ma = MovingAverage.moving_average([5, 15, 30])

txg_file = TestConfig.get_txg_history_filename(Configs.main_pool)

while True:
    time.sleep(1)
    txg_ma.insert_value(ZfsApi.linux_get_current_txg(txg_file))
    txg_result_string = ""
    for txg_delta,diff in txg_ma.get_diffs():
        txg_diff = float(diff)/txg_delta
        reasonable_string = '%.3f' % txg_diff
        txg_result_string = txg_result_string + reasonable_string.rjust(9)
    print("TXGs per second, should be .200")
    print(txg_result_string)
 
