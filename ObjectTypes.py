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
