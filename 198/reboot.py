from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List
from typing import Tuple

from dateutil.parser import parse


@dataclass(order=True)
class Uptime:
    uptime: int
    timestamp: datetime = field(compare=False)

    def astuple(self) -> Tuple[int, str]:
        return (self.uptime, str(self.timestamp.date()))


def parse_dates(last_reboot: str) -> List[datetime]:
    tstamps = []
    for line in last_reboot.strip().splitlines():
        _, _, _, *timestamp = line.split()
        tstamps.append(parse(" ".join(timestamp)))
    return tstamps


def calculate_diff(tstamps: List[datetime]) -> List[Uptime]:
    uptimes = []
    for last_reboot, reboot_before_that in zip(tstamps, tstamps[1:]):
        uptime = (last_reboot - reboot_before_that).days
        uptimes.append(Uptime(uptime, last_reboot))
    return uptimes


def calc_max_uptime(reboots: str):
    """Parse the passed in reboots output,
    extracting the datetimes.

    Calculate the highest uptime between reboots =
    highest diff between extracted reboot datetimes.

    Return a tuple of this max uptime in days (int) and the
    date (str) this record was hit.

    For the output above it would be (30, '2019-02-17'),
    but we use different outputs in the tests as well ...
    """
    dates = parse_dates(last_reboot=reboots)
    longest_uptime = max(calculate_diff(dates))
    return longest_uptime.astuple()
