from typing import TypedDict, Optional, List


class ModelZone(TypedDict):
    id: int
    name: str
    zone: int


class Subzone(TypedDict):
    id: int
    zone_id: int
    name: str
    subzone: int


class Zone(TypedDict):
    id: int
    name: str
    zone: int
    subzones: Optional[List[Subzone]]


class Subzone(TypedDict):
    id: int
    state: int


class CreateScheduleParams(TypedDict):
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    start_time: bool
    duration: bool


class AutomationSchedule(TypedDict):
    id: int
    zone_id: int
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    start_time: str
    duration: int
    subzone_ids: str


class AutomationScheduleFormatted(TypedDict):
    id: int
    zone_id: int
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    sunday: bool
    start_time: str
    duration: int
    subzone_ids: List[int]


class AutomationCommand(TypedDict):
    id: int
    start_time: str
    monday: bool
    tuesday: bool
    wednesday: bool
    thursday: bool
    friday: bool
    saturday: bool
    command: str


class ToggleScheduleParams(TypedDict):
    active: bool


class ZoneType(TypedDict):
    id: int
    type: str
