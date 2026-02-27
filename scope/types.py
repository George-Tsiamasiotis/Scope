from typing import TypeAlias, Literal

AcquireType: TypeAlias = Literal["Normal", "Averages", "Peak", "HighResolution"]
Coupling: TypeAlias = Literal["AC", "DC"]
Channel: TypeAlias = Literal[1, 2]

StatisticsType: TypeAlias = Literal[
    "Maximum",
    "Minimum",
    "Current",
    "Average",
    "Deviation",
]
StatisticsItem: TypeAlias = Literal[
    "Vmax",
    "Vmin",
    "Vpp",
    "Vtop",
    "Vbase",
    "Vamp",
    "Vavg",
    "Vrms",
    "Oversoot",
    "Preshoot",
    "Marea",
    "MParea",
    "Period",
    "Frequenc",
    "Rtime",
    "Ftime",
    "Pwidth",
    "Nwidth",
    "Pduty",
    "Nduty",
    "Rdelay",
    "Fdelay",
    "Rphase",
    "Fphase",
    "Tvmax",
    "Tvmin",
    "Pslewrate",
    "Nslewrate",
    "Vupper",
    "Vmid",
    "Vlower",
    "Variance",
    "Pvrms",
    "Ppulses",
    "Npulses",
    "Pedges",
    "Nedges",
]

# ================================================================================================

acquire_type = {
    "Normal": "NORMal",
    "Averages": "AVERages",
    "Peak": "PEAK",
    "HighResolution": "HRESolution",
}

statistics_type = {
    "Maximum": "MAXimum",
    "Minimum": "MINimum",
    "Current": "CURRent",
    "Average": "AVERages",
    "Deviation": "DEViation",
}

statistics_item = {
    "Vmax": "VMAX",
    "Vmin": "VMIN",
    "Vpp": "VPP",
    "Vtop": "VTOP",
    "Vbase": "VBASe",
    "Vamp": "VAMP",
    "Vavg": "VAVG",
    "Vrms": "VRMS",
    "Oversoot": "OVERshoot",
    "Preshoot": "PREShoot",
    "Marea": "MARea",
    "MParea": "MPARea",
    "Period": "PERiod",
    "Frequenc": "FREQuency",
    "Rtime": "RTIMe",
    "Ftime": "FTIMe",
    "Pwidth": "PWIDth",
    "Nwidth": "NWIDth",
    "Pduty": "PDUTy",
    "Nduty": "NDUTy",
    "Rdelay": "RDELay",
    "Fdelay": "FDELay",
    "Rphase": "RPHase",
    "Fphase": "FPHase",
    "Tvmax": "TVMAX",
    "Tvmin": "TVMIN",
    "Pslewrate": "PSLEWrate",
    "Nslewrate": "NSLEWrate",
    "Vupper": "VUPper",
    "Vmid": "VMID",
    "Vlower": "VLOWer",
    "Variance": "VARIance",
    "Pvrms": "PVRMS",
    "Ppulses": "PPULses",
    "Npulses": "NPULses",
    "Pedges": "PEDGes",
    "Nedges": "NEDGes",
}
