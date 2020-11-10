# Pi-frame
Pi-frame is a digital picture frame implementation for the Raspberry Pi.
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Download](#download)
  - [Configuration](#configuration)
- [Getting Started](#getting-started)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Overview
Pi-frame provides a web interface to:
- Upload, download, and manage pictures
- Start and stop slideshows

For now, due to the lack of documentation I will outline the general
architecture of the project here. Note that the web server should have cheap
access to the image storage. I do not recommend using network drives as
depending on how it is done, the continuous transfer of uncompressed images can
put significant load on your router (images are continuously transferred over
the network from where they are stored to the web app, where they are then
compressed and served to frame clients).

<div align="center">
    ![Architecture block diagram](src/static/arch-clear.png?raw=true "Architecture")
</div>

Architecture Options:
1. All on one Pi (1 frame, 1 Pi)
2. Web app and storage on one frame's Pi, with additional frames (<var>n</var>
   frames, <var>n</var> Pis)
3. Web app and storage on one Pi not driving a frame, with frames (<var>n</var>
   frames, <var>n</var> + 1 Pis)
4. Web app and storage in cloud, with frames (<var>n</var> frames, 1 remote
   machine, <var>n</var> Pis)

Your choice of setup mostly depends on whether you would like to store images
on a Raspberry Pi that drives a frame, on other disks, or in the cloud.

**Without using a setup where image data has the redundance and routine backups
necessary to be safe, you *CANNOT* rely on storing images on Pi-frame alone.**
That is to say, with the simplest setup all images are stored on a Pi's micro
SD card, and in this case I **do not** recommend saving images only on Pi-frame
as this could result in data loss if the card is corrupted. If you would like
to use Pi-frame as a safe method for storing images, then you might consider
either 3. or 4.

Storing images on a Pi driving a frame has the obvious advantage of requiring
one less Pi, lowering the barrier for entry to just one Pi. On the other hand,
using a different Pi can be advantageous if you would like to use physically
larger storage devices (e.g. SSDs in a RAID setup with a `chron` job for
backups) and would prefer not to keep said disks plugged into a Pi driving a
frame.

The local options 1., 2., and 3. have the advantages of being one-time costs
instead of a subscription and working with no internet access (LAN-based). The
remote/cloud option 4. has every other benefit including less setup and data
backups that are not location-dependent.

## Requirements
The minimum bill of materials is as follows:
- 1x Raspberry Pi Zero W
- 1x micro SD card
- 1x 5V 1A micro USB power supply
- 1x display
- 1x cable to connect the Pi to the display (male mini HDMI to ?). Most likely
  to male HDMI, DVI, or VGA. You probably want this to be as short as possible
  while still allowing room for connection; adapters *might* be possible to use
  instead of cables.

This is good to set up a web interface with one digital picture frame. For each
additional digital picture frame you will need another set of these materials.

##### Optional
- 1x Pi 3B+ or 4 (with micro SD and appropriate power supply)
- 2x+ disk (RAID, backups)
- Cables to connect the disks to the Pi?

OR:
- A cloud-based machine with sufficient compute and storage

## Installation
`# TODO: Write an install script.`

### Download
Download the project using [`git clone`][1] or as a compressed file ([.zip][2],
[.tar.gz][3]).

[1]: https://git-scm.com/docs/git-clone "Git - git-clone Documentation"
[2]: https://github.com/andersonentwistle/full-frame/archive/master.zip
[3]: https://github.com/andersonentwistle/full-frame/archive/master.tar.gz

### Configuration
Navigate to the project's root directory. Set the environment variable
`FLASK_APP`.
```bash
export FLASK_APP=$pwd/src/app.py
```

##### Optional
- Use Pi-hole or set up a local DNS server to create a local DNS entry for the
  web interface (e.g. http://frame.local -> http://192.168.1.???)
- Use NGINX as a reverse proxy for the Flask app
- Configure the frame client Pis to open the frame client webpage in a browser
  in full-screen on boot

## Getting Started
Run the web interface using `flask run --host=0.0.0.0 &`. The web app will be
available at the IP of the machine it is running on at port 5000. Note that
devices must be on the same network as the device running the web app in order
to access it.

## Documentation
`return this`

## Contributing
