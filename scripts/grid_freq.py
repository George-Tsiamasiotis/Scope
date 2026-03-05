import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from datetime import datetime
from accurate_timed_loop import accurate_wait

from scope import Scope, Q

plt.rcParams["text.usetex"] = True


TIME_TO_MEASURE = Q("48 hours").to("seconds")
MEASURE_FREQUENCY = Q("1 per second").to("Hz")

MEASUREMENTS = TIME_TO_MEASURE * MEASURE_FREQUENCY
SLEEP_TIME = 1 / MEASURE_FREQUENCY

scope = Scope()


#########
# SETUP #
#########

scope.set_coupling("AC")
scope.set_time_scale(Q(5, "milliseconds"))
scope.set_voltage_scale(Q(50, "volts"))
scope.set_acquire_type("HighResolution")
scope.enable_frequency_count(channel=1)

# ================================================================================================

time.sleep(3)


measurements = []
times = []


pbar = tqdm(total=int(MEASUREMENTS), smoothing=0.01)
try:
    for elapsed, start_time in accurate_wait(TIME_TO_MEASURE.m, SLEEP_TIME.m):
        frequency = scope.query_frequency_count()
        pbar.set_description(str(frequency))
        if frequency.m > 40 and frequency.m < 60:
            measurements.append(frequency.m)
            times.append(np.datetime64(datetime.now()))
        pbar.update()
except:
    pass


np.savez("freq_dump.npz", measurements=measurements, times=times)
scope.close()
