from pint import UnitRegistry
from pint.facets.plain import PlainQuantity
from pyvisa import ResourceManager
from pyvisa.resources import TCPIPInstrument
from termcolor import colored
from typing import Literal

from .types import Channel, Coupling, AcquireType, StatisticsItem, StatisticsType
from .types import acquire_type, statistics_item, statistics_type

TIME_SCALES = (
    (2e-9, 5e-9, 10e-9, 20e-9, 50e-9, 100e-9, 200e-9, 500e-9)
    + (1e-6, 2e-6, 5e-6, 10e-6, 20e-6, 50e-6, 100e-6, 200e-6, 500e-6)
    + (1e-3, 2e-3, 5e-3, 10e-3, 20e-3, 50e-3, 100e-3, 200e-3, 500e-3)
    + (1, 2, 5, 10, 20, 50)
)

ureg = UnitRegistry()
Q = ureg.Quantity  # type: ignore


class Scope(TCPIPInstrument):

    channel: Channel = 1
    ureg: UnitRegistry

    def __init__(self) -> None:
        rm = ResourceManager("@py")
        try:
            name = rm.list_resources()[0]
        except IndexError:
            raise Exception(colored("No instruments found", "red"))
        super().__init__(rm, name)
        super().open()
        print(colored(f"Found resource '{self.resource_name}'", "green"))
        print(f"LAN status: {self.get_lan_status()}")

    # =========================
    # ======== Acquire Commands
    # =========================

    def set_acquire_type(self, type: AcquireType):
        self.write(f":ACQuire:TYPE {acquire_type[type]}")

    def set_average_number(self, count: int):
        assert count in [2**n for n in range(1, 11)], "count = 2^n, n = 1, ..., 10"
        self.write(f":ACQuire:TYPE AVERages")
        self.write(f":ACQuire:AVERages {count}")

    # =========================
    # ======== Channel Commands
    # =========================

    def set_coupling(self, coupling: Coupling):
        self.write(f":CHANnel{self.channel}:COUPling {coupling}")
        print(f"Set voltage scale at {self.get_coupling()}")

    def get_coupling(self) -> str:
        return self.query(f":CHANnel{self.channel}:COUPling?")

    def set_voltage_scale(self, scale: PlainQuantity):
        _scale = scale.to("volts").magnitude
        self.write(f":CHANnel{self.channel}:SCALe {_scale}")
        print(f"Set voltage scale at {self.get_voltage_scale()}")

    def get_voltage_scale(self) -> PlainQuantity:
        m = float(self.query(f":CHANnel{self.channel}:SCALe?"))
        return Q(m, "volts")

    # =========================
    # ======== Measure Commands
    # =========================

    def query_voltage_average(self) -> PlainQuantity:
        m = float(self.query(f":MEASure:ITEM? VAVG,CHANnel{self.channel}"))
        return Q(m, "volts")

    def measure_stat(self, typ: StatisticsType, item: StatisticsItem) -> float:
        self.write(":MEASure:STATistic:DISPlay ON")
        try:
            m = self.query(
                f":MEAS:STAT:ITEM? {statistics_type[typ]},{statistics_item[item]}"
            )
            return float(m)
        except KeyError:
            raise KeyError(
                f"'type' must be one of {statistics_type.keys} and 'item' must be one of {statistics_item.keys}"
            )

    def clear_stat_item(self, item: Literal[1, 2, 3, 4, 5, 6]):
        assert (
            isinstance(item, int) and 1 <= item <= 6
        ), "'item' must be one of '1, 2, 3, 4, 5, 6"
        self.write(f":MEASure:CLEar ITEM{item}")

    # =========================
    # ======= Timebase Commands
    # =========================

    def set_time_scale(self, scale: PlainQuantity):
        _scale = scale.to("seconds").magnitude
        assert _scale in TIME_SCALES, f"scale must be one of {TIME_SCALES} seconds"
        self.write(f":TIMebase:MAIN:SCALe {_scale}")

    def get_time_scale(self) -> PlainQuantity:
        m = float(self.query(f":TIMebase:MAIN:SCALe?"))
        return Q(m, "seconds")

    # =========================
    # ============ LAN Commands
    # =========================

    def get_lan_status(self) -> str:
        return self.query(":LAN:STATus?")

    def get_ip(self) -> str:
        return self.query(":LAN:IPADdress?")

    # =========================
    # ======== Trigger Commands
    # =========================

    def trigger(self):
        self.write(":TFORce")
