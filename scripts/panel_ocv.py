import time
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from accurate_timed_loop import accurate_wait

from scope import Scope, Q

plt.rcParams["text.usetex"] = True


TIME_TO_MEASURE = Q("300 seconds").to("seconds")
TRIGGER_FREQUENCY = Q("1 per second").to("Hz")

MEASUREMENTS = TIME_TO_MEASURE * TRIGGER_FREQUENCY
SLEEP_TIME = 1 / TRIGGER_FREQUENCY

scope = Scope()


#########
# SETUP #
#########

scope.set_coupling("DC")
scope.set_time_scale(Q(20, "milliseconds"))
scope.set_voltage_scale(Q(100, "volts"))
scope.set_acquire_type("HighResolution")

# ================================================================================================


def plot():
    plt.plot(times, measurements)
    plt.xlabel("$Time[s]$")
    plt.ylabel("$Voltage[Volts]$")

    plt.show()


# ================================================================================================

time.sleep(1)
start = time.time()

measurements, times = [], []


pbar = tqdm(total=int(MEASUREMENTS))
try:
    for elapsed, start_time in accurate_wait(TIME_TO_MEASURE.m, SLEEP_TIME.m):
        voltage = scope.query_voltage_average()
        pbar.set_description(str(voltage))
        if voltage.m < 200:
            measurements.append(voltage.m)
            times.append(time.time() - start)
        pbar.update()
except:
    pass


np.savez("solar_dump.npz", measurements=measurements, times=times)
print("saved")
