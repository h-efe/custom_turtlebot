#!/usr/bin/env bash
set -e

ORBIROB_USER="${USER}"
USER_HOME="${HOME}"

BRINGUP_SERVICE="/etc/systemd/system/linorobot2_bringup.service"
ROS_SETUP="/opt/ros/humble/setup.bash"
LINOROBOT2_SETUP="${USER_HOME}/linorobot2_ws/install/setup.bash"

echo "=============================================="
echo " linorobot2_bringup.service kurulumu"
echo "=============================================="
echo "Kullanici: ${ORBIROB_USER}"
echo "Ev dizini: ${USER_HOME}"
echo

if [ ! -f "${ROS_SETUP}" ]; then
    echo "HATA: ROS2 Humble bulunamadi: ${ROS_SETUP}"
    exit 1
fi

if [ ! -f "${LINOROBOT2_SETUP}" ]; then
    echo "HATA: linorobot2_ws derlenmemis: ${LINOROBOT2_SETUP}"
    exit 1
fi

echo "Servis dosyasi yaziliyor: ${BRINGUP_SERVICE}"

sudo tee "${BRINGUP_SERVICE}" >/dev/null <<EOF
[Unit]
Description=linorobot2 temel sistemi (micro-ROS agent + EKF + robot tanimi)
After=network.target

[Service]
Type=simple
User=${ORBIROB_USER}
Group=${ORBIROB_USER}
Environment=HOME=${USER_HOME}
ExecStart=/bin/bash -lc 'unset LINOROBOT2_LASER_SENSOR; source ${ROS_SETUP} && source ${LINOROBOT2_SETUP} && exec ros2 launch linorobot2_bringup bringup.launch.py micro_ros_baudrate:=921600'
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

echo "systemd yeniden yukleniyor..."
sudo systemctl daemon-reload

echo "linorobot2_bringup.service etkinlestiriliyor (acilista otomatik baslasin diye)..."
sudo systemctl enable linorobot2_bringup.service

echo "Servis simdi baslatiliyor..."
sudo systemctl restart linorobot2_bringup.service

sleep 3

echo
echo "=============================================="
echo " Kurulum tamamlandi"
echo "=============================================="
echo -n "Durum: "
systemctl is-enabled linorobot2_bringup.service
echo
echo "Detayli durumu gormek icin:"
echo "  systemctl status linorobot2_bringup.service"
echo "Canli loglari izlemek icin:"
echo "  journalctl -u linorobot2_bringup.service -f"
