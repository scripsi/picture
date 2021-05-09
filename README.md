# picture

**P**i **C**amera **T**aking **U**tility **Re**adings

## Introduction

A tiny project for a remote camera to take regular pictures of utility meter readings and send them by email. This would be an ideal use for PiCore Linux, but because of time constraints I'm using an easier setup with a Raspberry Pi OS Lite read-only file system. The aim is to minimise writing to the microSD card on the Pi unless you ask it to, so the card is unlikely to become corrupted over long term use or by sudden power failures.

## Hardware

- Raspberry Pi Zero W
- Pimoroni Pi Zero Camera - wide-angle version
- microSD card
- LED backlight panel

## OS installation

Download the latest [Raspberry Pi OS Lite](https://www.raspberrypi.org/software/operating-systems/) and image it to the microSD card using Etcher, Raspberry Pi Imager or Ubuntu Startup Disk Creator in the normal way. While the microSD card is still in your PC, enable networking and ssh by making the following in the `/boot` partition:

- Create a file called `wpa_supplicant.conf`, changing the `ssid` and `psk` parameters for your network:

```conf
country=GB
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="[wireless network name]"
    scan_ssid=1
    psk="[wireless network password]"
    key_mgmt=WPA-PSK
}
```

- Create an empty file called `ssh` - eg `touch /media/$USER/boot/ssh`

Eject the microSD card from the PC, insert it into the Raspberry Pi and connect a power supply. After it has booted up, search for it's IP address on the network and SSH to it using the username `pi` and password `raspberry`.
