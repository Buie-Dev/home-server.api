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
