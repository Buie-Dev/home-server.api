from lib.irrigation import create_automation_command


class TestCreateAutomationCommand:
    def test_basic_command(self):
        zone = {
            "id": 1,
            "name": "Front Lawn",
            "zone": 3,
            "subzones": [
                {"subzone": 10, "name": "Left"},
                {"subzone": 11, "name": "Right"},
            ],
        }
        schedule = {
            "start_time": "06:00",
            "monday": 1,
            "tuesday": 0,
            "wednesday": 1,
            "thursday": 0,
            "friday": 1,
            "saturday": 0,
            "sunday": 0,
            "sort_order": 2,
            "duration": 600,
            "subzone_ids": [10, 11],
        }

        result = create_automation_command(zone, schedule, 42)

        assert result["id"] == 42
        assert result["start_time"] == "06:00"
        assert result["monday"] == 1
        assert result["friday"] == 1
        assert result["tuesday"] == 0
        assert result["command"]["priority"] == 2
        assert result["command"]["duration"] == 600
        assert result["command"]["zone"] == 3
        assert len(result["command"]["subzones"]) == 2
        assert result["command"]["subzones"][0] == {"id": 10, "state": 1}

    def test_no_matching_subzones_returns_none(self):
        zone = {
            "id": 1,
            "name": "Front Lawn",
            "zone": 3,
            "subzones": [{"subzone": 10, "name": "Left"}],
        }
        schedule = {
            "start_time": "06:00",
            "monday": 1,
            "tuesday": 0,
            "wednesday": 0,
            "thursday": 0,
            "friday": 0,
            "saturday": 0,
            "sunday": 0,
            "sort_order": 1,
            "duration": 300,
            "subzone_ids": [99],  # No match
        }

        result = create_automation_command(zone, schedule, 1)

        assert result["command"]["subzones"] is None

    def test_empty_subzone_ids_returns_none(self):
        zone = {
            "id": 1,
            "name": "Front Lawn",
            "zone": 3,
            "subzones": [{"subzone": 10, "name": "Left"}],
        }
        schedule = {
            "start_time": "06:00",
            "monday": 1,
            "tuesday": 0,
            "wednesday": 0,
            "thursday": 0,
            "friday": 0,
            "saturday": 0,
            "sunday": 0,
            "sort_order": 1,
            "duration": 300,
            "subzone_ids": [],
        }

        result = create_automation_command(zone, schedule, 1)

        assert result["command"]["subzones"] is None


class TestIrrigationServicesSchedules:
    def test_formats_schedule_rows(self):
        from unittest.mock import patch

        mock_rows = [
            {
                "id": 1,
                "name": "Morning",
                "zone_id": 2,
                "sort_order": 1,
                "subzoneIds": "[10, 11]",
                "start_time": "06:00",
            }
        ]

        with patch("services.IrrigationServices.IrrigationModels") as mock_models:
            mock_models.schedules.return_value = mock_rows
            from services.IrrigationServices import IrrigationServices

            result = IrrigationServices.schedules()

        assert len(result) == 1
        assert result[0]["zoneId"] == 2
        assert result[0]["sortOrder"] == 1
        assert result[0]["subzoneIds"] == [10, 11]

    def test_empty_subzone_ids(self):
        from unittest.mock import patch

        mock_rows = [
            {
                "id": 1,
                "name": "Morning",
                "zone_id": 2,
                "sort_order": 1,
                "subzoneIds": None,
                "start_time": "06:00",
            }
        ]

        with patch("services.IrrigationServices.IrrigationModels") as mock_models:
            mock_models.schedules.return_value = mock_rows
            from services.IrrigationServices import IrrigationServices

            result = IrrigationServices.schedules()

        assert result[0]["subzoneIds"] == []


class TestIrrigationServicesHistoryTotals:
    def test_formats_totals(self):
        from unittest.mock import patch

        mock_row = {
            "today_litres": 150.5,
            "today_seconds": 3600,
            "today_runs": 3,
            "week_litres": 500.0,
            "week_seconds": 10800,
            "week_runs": 10,
            "month_litres": 2000.0,
            "month_seconds": 43200,
            "month_runs": 40,
        }

        with patch("services.IrrigationServices.IrrigationModels") as mock_models:
            mock_models.fetch_history_totals.return_value = mock_row
            from services.IrrigationServices import IrrigationServices

            result = IrrigationServices.fetch_history_totals()

        assert result["today"]["litres"] == 150.5
        assert result["today"]["minutes"] == 60
        assert result["today"]["runs"] == 3
        assert result["week"]["minutes"] == 180

    def test_empty_totals(self):
        from unittest.mock import patch

        with patch("services.IrrigationServices.IrrigationModels") as mock_models:
            mock_models.fetch_history_totals.return_value = None
            from services.IrrigationServices import IrrigationServices

            result = IrrigationServices.fetch_history_totals()

        assert result["today"] == {"litres": 0, "minutes": 0, "runs": 0}
        assert result["week"] == {"litres": 0, "minutes": 0, "runs": 0}
        assert result["month"] == {"litres": 0, "minutes": 0, "runs": 0}


class TestCreateHistory:
    def test_splits_litres_by_heads(self):
        from unittest.mock import patch, call

        params = {
            "zone_id": 1,
            "subzone_ids": [10, 11],
            "litres": 100.0,
            "start_time": "06:00",
            "end_time": "06:10",
            "date": "2025-06-01",
        }
        subzones = [
            {"id": 10, "heads": 3},
            {"id": 11, "heads": 7},
        ]

        with patch("services.IrrigationServices.IrrigationModels") as mock_models:
            mock_models.fetch_subzones_by_ids.return_value = subzones
            from services.IrrigationServices import IrrigationServices

            IrrigationServices.create_history(params)

        calls = mock_models.create_history.call_args_list
        assert len(calls) == 2
        # 3/10 of 100 = 30.0
        assert calls[0][0][0]["subzone_id"] == 10
        assert calls[0][0][0]["litres"] == 30.0
        # 7/10 of 100 = 70.0
        assert calls[1][0][0]["subzone_id"] == 11
        assert calls[1][0][0]["litres"] == 70.0

    def test_splits_equally_when_no_heads(self):
        from unittest.mock import patch

        params = {
            "zone_id": 1,
            "subzone_ids": [10, 11],
            "litres": 100.0,
            "start_time": "06:00",
            "end_time": "06:10",
            "date": "2025-06-01",
        }
        subzones = [
            {"id": 10, "heads": 0},
            {"id": 11, "heads": 0},
        ]

        with patch("services.IrrigationServices.IrrigationModels") as mock_models:
            mock_models.fetch_subzones_by_ids.return_value = subzones
            from services.IrrigationServices import IrrigationServices

            IrrigationServices.create_history(params)

        calls = mock_models.create_history.call_args_list
        assert len(calls) == 2
        assert calls[0][0][0]["litres"] == 50.0
        assert calls[1][0][0]["litres"] == 50.0

    def test_no_subzones_inserts_zone_level(self):
        from unittest.mock import patch

        params = {
            "zone_id": 1,
            "subzone_ids": [],
            "litres": 100.0,
            "start_time": "06:00",
            "end_time": "06:10",
            "date": "2025-06-01",
        }

        with patch("services.IrrigationServices.IrrigationModels") as mock_models:
            from services.IrrigationServices import IrrigationServices

            IrrigationServices.create_history(params)

        mock_models.create_history.assert_called_once_with(params)
