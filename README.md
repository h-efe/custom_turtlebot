# custom_turtlebot

ESP32-S3 ve Raspberry Pi 4 üzerine, [linorobot2](https://github.com/linorobot/linorobot2) /
[linorobot2_hardware](https://github.com/linorobot/linorobot2_hardware) açık kaynak ekosistemiyle
inşa edilmiş, özel (custom) mekanik parçalara sahip bir diferansiyel sürüşlü mobil robot.

## İçindekiler

- `index.html` — tam yapım kılavuzu: malzeme listesi, güç mimarisi, kablolama şeması, yazılım
  kurulumu, kalibrasyon ve bilinen sorunlar (tarayıcıda açılabilir)
- `TurtleBot_Yapim_Kilavuzu.pdf` — aynı içeriğin PDF hâli
- `esp32s3_config.h` — bu robotta fiilen kullanılan, kalibre edilmiş ESP32-S3 yapılandırma dosyası
- `install_linorobot2.bash` — Raspberry Pi 4 kurulum betiği (proje notuyla)

## Durum

Kılavuz güncel donanım durumunu yansıtır. RPLIDAR A1M8'e geçiş ve şaft-adaptör mekanik düzeltmesi
henüz uçtan uca doğrulanmadı — bkz. `index.html` içindeki ilgili notlar.
