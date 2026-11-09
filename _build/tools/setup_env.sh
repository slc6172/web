#!/bin/sh
# 還原驗證環境(容器重置後執行一次):AVR 工具鏈、官方 ArduinoCore-avr、simavr 模擬腳本
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
apt-get update >/dev/null 2>&1 || true
apt-get install -y --no-install-recommends gcc-avr avr-libc binutils-avr simavr libsimavr-dev libelf-dev >/dev/null
[ -d /tmp/ArduinoCore-avr ] || git clone --depth 1 https://github.com/arduino/ArduinoCore-avr.git /tmp/ArduinoCore-avr
INC=/usr/include/simavr
gcc -O1 -I$INC -I$INC/avr "$HERE/simpin.c" -o "$HERE/simpin" -lsimavr -lelf
echo "環境就緒:avr-gcc、ArduinoCore-avr、simpin"
