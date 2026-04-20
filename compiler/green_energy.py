from __future__ import annotations

from typing import Dict, Any

try:
    from codecarbon import EmissionsTracker
except Exception:
    EmissionsTracker = None


class GreenEnergyTracker:
    def __init__(self):
        self.tracker = None
        self.enabled = False

    def start(self) -> None:
        if EmissionsTracker is None:
            return

        try:
            self.tracker = EmissionsTracker(
                measure_power_secs=1,
                log_level="error",
                save_to_file=False
            )
            self.tracker.start()
            self.enabled = True
        except Exception:
            self.enabled = False

    def stop(self) -> Dict[str, Any]:
        if not self.enabled or self.tracker is None:
            return {
                "co2_kg": None,
                "energy_kwh": None
            }

        try:
            emissions = self.tracker.stop()
            return {
                "co2_kg": float(emissions),
                "energy_kwh": None
            }
        except Exception:
            return {
                "co2_kg": None,
                "energy_kwh": None
            }