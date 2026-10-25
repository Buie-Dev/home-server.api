from models.IrrigationModels import IrrigationModels
from lib.irrigation import create_automation_command
from ObjectTypes import (
    Zone,
    CreateScheduleParams,
    AutomationCommand,
    ToggleScheduleParams,
    ZoneType,
)
from typing import List, Optional
import json


class IrrigationServices:
    @staticmethod
    def schedules(zone_id: Optional[int] = None, subzone_id: Optional[int] = None):
        rows = IrrigationModels.schedules(zone_id, subzone_id)
        result = []
        for row in rows:
            raw = row.get("subzoneIds")
            if raw:
                ids = json.loads(raw) if isinstance(raw, str) else raw
                subzone_ids = [i for i in (ids or []) if i is not None]
            else:
                subzone_ids = []
            result.append({**row, "zoneId": row["zone_id"], "subzoneIds": subzone_ids, "sortOrder": row["sort_order"]})
        return result

    @staticmethod
    def update_schedule(id: int, params: CreateScheduleParams):
        schedule_data = {
            "name": params["name"],
            "start_time": params["start_time"],
            "duration": params["duration"],
            "monday": params["monday"],
            "tuesday": params["tuesday"],
            "wednesday": params["wednesday"],
            "thursday": params["thursday"],
            "friday": params["friday"],
            "saturday": params["saturday"],
            "sunday": params["sunday"],
            "zone_id": params["zone_id"],
        }
        IrrigationModels.update_schedule(id, schedule_data)
        IrrigationModels.delete_subzone_schedules(id)
        if len(params["subzone_ids"]) > 0:
            IrrigationModels.create_subzone_schedules(id, params["subzone_ids"])

    @staticmethod
    def create_schedule(params: CreateScheduleParams):
        schedule_data = {
            "duration": params["duration"],
            "name": params["name"],
            "start_time": params["start_time"],
            "monday": params["monday"],
            "tuesday": params["tuesday"],
            "wednesday": params["wednesday"],
            "thursday": params["thursday"],
            "friday": params["friday"],
            "saturday": params["saturday"],
            "sunday": params["sunday"],
            "zone_id": params["zone_id"],
        }

        schedule_result = IrrigationModels.create_schedule(schedule_data)
        schedule_id = schedule_result["inserted_id"]

        if len(params["subzone_ids"]) > 0:
            IrrigationModels.create_subzone_schedules(schedule_id, params["subzone_ids"])

        return schedule_id

    @staticmethod
    def delete_schedule(id: int):
        return IrrigationModels.delete_schedule(id)

    @staticmethod
    def fetch_zones(zone_type_id: Optional[int] = None) -> List[Zone]:
        try:
            zones_model = IrrigationModels.fetch_zones(zone_type_id)
            subzones = IrrigationModels.fetch_subzones()

            zones: List[Zone] = [
                {
                    "id": zm["id"],
                    "name": zm["name"],
                    "zone": zm["zone"],
                    "type": zm["type"],
                }
                for zm in zones_model
            ]
            for subzone in subzones:
                zone_id = subzone["zone_id"]
                zone = next((zone for zone in zones if zone["id"] == zone_id), None)
                if zone is None:
                    continue
                if "subzones" not in zone or zone["subzones"] is None:
                    zone["subzones"] = []

                zone["subzones"].append(subzone)

            return zones
        except Exception as e:
            print(e)
            print("Error Fetching Zones in Service", e)
            raise e

    @staticmethod
    def fetch_zone(id: int) -> Zone:
        try:
            zone_model = IrrigationModels.fetch_zone(id)
            subzones = IrrigationModels.fetch_subzones(id)

            zone: Zone = {
                "id": zone_model["id"],
                "name": zone_model["name"],
                "zone": zone_model["zone"],
                "subzones": subzones,
            }

            return zone
        except Exception as e:
            print(e)
            print("Error Fetching Zones in Service", e)
            raise e

    @staticmethod
    def fetch_automation_schedule(id: int) -> AutomationCommand:
        automation_schedule = IrrigationModels.fetch_automation_schedule(id)
        automation_schedule_formatted = {
            **automation_schedule,
            "subzone_ids": json.loads(automation_schedule["subzone_ids"]),
        }
        zone = IrrigationServices.fetch_zone(automation_schedule["zone_id"])
        return create_automation_command(zone, automation_schedule_formatted, id)

    @staticmethod
    def fetch_automation_schedules(exclude_inactive=False, include_deleted=False) -> List[AutomationCommand]:
        automation_schedules = IrrigationModels.fetch_automation_schedules(
            exclude_inactive=exclude_inactive, include_deleted=include_deleted
        )
        print(f"---------------------------automation_schedules: {automation_schedules}")
        automation_schedules_formatted = [
            {
                **automation_schedule,
                "subzone_ids": json.loads(automation_schedule["subzone_ids"]),
            }
            for automation_schedule in automation_schedules
        ]

        return [
            create_automation_command(
                IrrigationServices.fetch_zone(automation_schedule["zone_id"]),
                automation_schedule,
                automation_schedule["id"],
            )
            for automation_schedule in automation_schedules_formatted
        ]

    @staticmethod
    def fetch_active_automation_schedules():
        """Returns full automation commands for all active (non-deleted) schedules."""
        rows = IrrigationModels.fetch_active_automation_schedules()
        result = []
        for row in rows:
            formatted = {
                **row,
                "subzone_ids": (
                    json.loads(row["subzone_ids"])
                    if isinstance(row["subzone_ids"], str)
                    else (row["subzone_ids"] or [])
                ),
            }
            formatted["subzone_ids"] = [i for i in formatted["subzone_ids"] if i is not None]
            zone = IrrigationServices.fetch_zone(row["zone_id"])
            command = create_automation_command(zone, formatted, row["id"])
            result.append(command)
        return result

    @staticmethod
    def compare_sync(automation_schedules: list) -> dict:
        """Compare automation service state against DB active schedules field-by-field."""
        db_schedules = IrrigationServices.fetch_active_automation_schedules()

        automation_by_id = {s["id"]: s for s in automation_schedules}
        db_by_id = {s["id"]: s for s in db_schedules}

        missing_from_automation = []
        mismatched = []
        extra_in_automation = []

        for db_id, db_s in db_by_id.items():
            if db_id not in automation_by_id:
                missing_from_automation.append(db_id)
            else:
                diffs = IrrigationServices._diff_schedule(db_s, automation_by_id[db_id])
                if diffs:
                    mismatched.append({"id": db_id, "diffs": diffs})

        for auto_id in automation_by_id:
            if auto_id not in db_by_id:
                extra_in_automation.append(auto_id)

        return {
            "in_sync": not missing_from_automation and not mismatched and not extra_in_automation,
            "missing_from_automation": missing_from_automation,
            "mismatched": mismatched,
            "extra_in_automation": extra_in_automation,
        }

    _DAY_KEYS = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    @staticmethod
    def _diff_schedule(db_s: dict, auto_s: dict) -> list:
        """Return list of human-readable diff strings between expected (DB) and actual (automation) schedule."""
        diffs = []

        if db_s.get("start_time") != auto_s.get("start_time"):
            diffs.append(f"start_time: db={db_s.get('start_time')} auto={auto_s.get('start_time')}")

        for day in IrrigationServices._DAY_KEYS:
            db_val = bool(db_s.get(day))
            auto_val = bool(auto_s.get(day))
            if db_val != auto_val:
                diffs.append(f"{day}: db={db_val} auto={auto_val}")

        db_cmd = db_s.get("command", {})
        auto_cmd = auto_s.get("command", {})

        if db_s.get("sort_order") != auto_cmd.get("priority"):
            diffs.append(f"priority: db={db_s.get('sort_order')} auto={auto_cmd.get('priority')}")

        if db_cmd.get("duration") != auto_cmd.get("duration"):
            diffs.append(f"duration: db={db_cmd.get('duration')} auto={auto_cmd.get('duration')}")

        if db_cmd.get("zone") != auto_cmd.get("zone"):
            diffs.append(f"zone: db={db_cmd.get('zone')} auto={auto_cmd.get('zone')}")

        db_subzones = sorted([sz["id"] for sz in (db_cmd.get("subzones") or [])])
        auto_subzones = sorted([sz["id"] for sz in (auto_cmd.get("subzones") or [])])
        if db_subzones != auto_subzones:
            diffs.append(f"subzones: db={db_subzones} auto={auto_subzones}")

        return diffs

    @staticmethod
    def reorder_schedules(ids: List[int]):
        IrrigationModels.reorder_schedules(ids)

    @staticmethod
    def is_schedule_active(id: int) -> bool:
        return IrrigationModels.is_schedule_active(id)

    @staticmethod
    def toggle_schedule(id: int, data: ToggleScheduleParams):
        return IrrigationModels.toggle_schedule(id, data)

    @staticmethod
    def fetch_zone_types() -> List[ZoneType]:
        return IrrigationModels.fetch_zone_types()

    @staticmethod
    def fetch_history_totals(zone_id: int = None, subzone_id: int = None):
        row = IrrigationModels.fetch_history_totals(zone_id=zone_id, subzone_id=subzone_id)
        if not row:
            empty = {"litres": 0, "minutes": 0, "runs": 0}
            return {"today": empty, "week": empty, "month": empty}
        return {
            "today": {
                "litres": float(row["today_litres"]),
                "minutes": round(row["today_seconds"] / 60),
                "runs": row["today_runs"],
            },
            "week": {
                "litres": float(row["week_litres"]),
                "minutes": round(row["week_seconds"] / 60),
                "runs": row["week_runs"],
            },
            "month": {
                "litres": float(row["month_litres"]),
                "minutes": round(row["month_seconds"] / 60),
                "runs": row["month_runs"],
            },
        }

    @staticmethod
    def fetch_history(
        limit: int = 100,
        offset: int = 0,
        zone_id: int = None,
        subzone_id: int = None,
        start_date: str = None,
        end_date: str = None,
    ):
        rows = IrrigationModels.fetch_history(
            limit=limit,
            offset=offset,
            zone_id=zone_id,
            subzone_id=subzone_id,
            start_date=start_date,
            end_date=end_date,
        )
        result = []
        for row in rows:
            date = row["date"]  # datetime.date from MySQL
            start_td = row["start_time"]  # datetime.timedelta from MySQL
            end_td = row["end_time"]  # datetime.timedelta from MySQL

            def td_to_hms(td):
                total_s = int(td.total_seconds())
                h = total_s // 3600
                m = (total_s % 3600) // 60
                s = total_s % 60
                return f"{h:02d}:{m:02d}:{s:02d}"

            duration_s = max(0, int((end_td - start_td).total_seconds()))
            result.append(
                {
                    "id": row["id"],
                    "zoneName": row["zone_name"] or "Unknown",
                    "zoneType": row["zone_type"] or "unknown",
                    "subzoneName": row.get("subzone_name"),
                    "startedAt": f"{date.isoformat()}T{td_to_hms(start_td)}",
                    "endedAt": f"{date.isoformat()}T{td_to_hms(end_td)}",
                    "durationSeconds": duration_s,
                    "totalLitres": float(row["litres"] or 0),
                }
            )
        return result

    @staticmethod
    def delete_history(id: int):
        return IrrigationModels.delete_history(id)

    @staticmethod
    def create_history(params):
        subzone_ids = params.get("subzone_ids") or []
        print(
            f"[history] create_history: zone_id={params.get('zone_id')}, subzone_ids={subzone_ids}, litres={params.get('litres')}"
        )
        if subzone_ids:
            subzones = IrrigationModels.fetch_subzones_by_ids(subzone_ids)
            print(f"[history] fetched subzones: {subzones}")
            total_heads = sum(sz.get("heads", 0) for sz in subzones)
            print(f"[history] total_heads={total_heads}")
            if total_heads > 0:
                for sz in subzones:
                    sz_params = {
                        **params,
                        "subzone_id": sz["id"],
                        "litres": round(params["litres"] * (sz.get("heads", 0) / total_heads), 2),
                    }
                    print(f"[history] inserting subzone record: {sz_params}")
                    IrrigationModels.create_history(sz_params)
                return
            # No heads defined: divide equally among subzones (1 subzone = full volume)
            print(f"[history] total_heads=0, dividing equally among {len(subzones)} subzone(s)")
            equal_litres = round(params["litres"] / len(subzones), 2)
            for sz in subzones:
                sz_params = {
                    **params,
                    "subzone_id": sz["id"],
                    "litres": equal_litres,
                }
                print(f"[history] inserting subzone record: {sz_params}")
                IrrigationModels.create_history(sz_params)
            return
        print(f"[history] inserting zone-level record")
        return IrrigationModels.create_history(params)
