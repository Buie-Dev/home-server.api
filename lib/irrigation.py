def create_automation_command(zone, schedule, schedule_id) -> dict:
    # Get subzones from zone that match the subzones in schedule
    subzones = [
        {"id": s["subzone"], "state": 1}
        for s in zone["subzones"]
        if s["subzone"] in schedule["subzone_ids"]
    ]

    return {
        "id": schedule_id,
        "start_time": schedule["start_time"],
        "monday": schedule["monday"],
        "tuesday": schedule["tuesday"],
        "wednesday": schedule["wednesday"],
        "thursday": schedule["thursday"],
        "friday": schedule["friday"],
        "saturday": schedule["saturday"],
        "sunday": schedule["sunday"],
        "command": {
            "priority": schedule["sort_order"],
            "duration": schedule["duration"],
            "zone": zone["zone"],
            "subzones": subzones if len(subzones) > 0 else None,
        },
    }
