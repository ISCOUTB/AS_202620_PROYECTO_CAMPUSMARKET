#!/usr/bin/env bash
set -euo pipefail
task_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
adb push "$task_root/artifacts/e2e/campusmarket-e2e.png" /sdcard/Download/campusmarket-e2e.png
python3 "$task_root/scripts/asistir_selector_e2e.py" android > "$task_root/artifacts/e2e/selector.log" 2>&1 &
picker_pid=$!
trap 'kill "$picker_pid" 2>/dev/null || true' EXIT
cd "$task_root/frontend/campusmarket"
flutter drive --driver=test_driver/mvp_driver.dart --target=integration_test/mvp_flow_test.dart -d emulator-5554 --dart-define=CAMPUSMARKET_API_BASE_URL=http://10.0.2.2:8000
