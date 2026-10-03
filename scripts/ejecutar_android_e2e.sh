#!/usr/bin/env bash
set -euo pipefail
task_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$task_root/scripts/preparar_fixture_android.py"
python3 "$task_root/scripts/asistir_selector_e2e.py" android > "$task_root/artifacts/e2e/selector.log" 2>&1 &
picker_pid=$!
finish() {
  task_status=$?
  kill "$picker_pid" 2>/dev/null || true
  if [ "$task_status" -ne 0 ]; then
    tail -n 30 "$task_root/artifacts/e2e/selector.log"
    timeout 15s adb exec-out screencap -p > "$task_root/artifacts/e2e/android-selector-fallo.png" || true
  fi
}
trap finish EXIT
cd "$task_root/frontend/campusmarket"
timeout --signal=TERM --kill-after=20s 12m flutter drive --driver=test_driver/mvp_driver.dart --target=integration_test/mvp_flow_test.dart -d emulator-5554 --dart-define=CAMPUSMARKET_API_BASE_URL=http://10.0.2.2:8000
