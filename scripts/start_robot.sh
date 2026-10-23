#!/bin/bash

LOG_DIR="$HOME/robot_logs"
mkdir -p "$LOG_DIR"

cleanup() {
  echo ""
  echo "Kapatiliyor (LIDAR + SLAM)..."
  kill $(jobs -p) 2>/dev/null
  wait 2>/dev/null
  echo "Temel sistem (micro-ROS koprusu) temiz durum icin yeniden baslatiliyor..."
  sudo systemctl restart linorobot2_bringup.service
  sleep 3
  echo "Tamam. Koprunu tekrar ayakta, joystick/cmd_vel calismali."
}
trap cleanup EXIT INT TERM

source /opt/ros/humble/setup.bash
source "$HOME/linorobot2_ws/install/setup.bash"

echo "[0/2] Temel sistemin (linorobot2_bringup.service) hazir olmasi bekleniyor..."
if ! systemctl is-active --quiet linorobot2_bringup.service; then
  echo "  Servis aktif degil, baslatiliyor..."
  sudo systemctl start linorobot2_bringup.service
fi

for i in $(seq 1 20); do
  if ros2 topic list 2>/dev/null | grep -q "^/odom/unfiltered$"; then
    echo "  Temel sistem hazir (/odom/unfiltered goruluyor)."
    break
  fi
  sleep 1
  if [ "$i" -eq 20 ]; then
    echo "  UYARI: 20 saniyede /odom/unfiltered gorulemedi, yine de devam ediliyor."
    echo "  Kontrol icin: systemctl status linorobot2_bringup.service"
  fi
done

echo "[1/2] LIDAR surucusu baslatiliyor (LDS-01 / hls_lfcd_lds_driver)..."
ros2 launch hls_lfcd_lds_driver hlds_laser.launch.py \
  > "$LOG_DIR/lidar.log" 2>&1 &
sleep 3

echo "[2/2] SLAM + Nav2 baslatiliyor..."
ros2 launch linorobot2_navigation slam.launch.py \
  > "$LOG_DIR/slam.log" 2>&1 &

echo ""
echo "Hepsi baslatildi. Loglar: $LOG_DIR/ (lidar.log, slam.log)"
echo "Temel sistemin loglari icin: journalctl -u linorobot2_bringup.service -f"
echo "Durdurmak icin Ctrl+C'ye bas."
echo ""

wait
