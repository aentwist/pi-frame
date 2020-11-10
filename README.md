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
    <div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2020-11-09T03:43:05.091Z\&quot; agent=\&quot;5.0 (Windows)\&quot; etag=\&quot;_aEel1xA7UKKvoFyN6m6\&quot; version=\&quot;13.9.2\&quot; type=\&quot;device\&quot;&gt;&lt;diagram id=\&quot;t2zgoPWlfdpKi9xcir2_\&quot; name=\&quot;Page-1\&quot;&gt;5VpZU9swEP41mWkfYHzmeMwB5YUOM5QCj8IWtgbZciWFJP31lWL5kh0IGcem5AWk1f3tp9XuOgN7Hq1/UJCE18SHeGAZ/npgLwaWZRr2WPyTkk0qcZ1RKggo8lWnQnCL/sJspJIukQ9ZpSMnBHOUVIUeiWPo8YoMUEpW1W7PBFdXTUAAa4JbD+C69B75PEylY9co5FcQBWG2smmolghknZWAhcAnq5LIvhjYc0oIT0vReg6xBC/DJR13uaM13xiFMd9nAJrjKUTjX/FPg1PrNny+myzO1CyvAC/VgQfWEIv5Zk+iEMjCDTp7piCCots9FFJjmiRZJ7Fa3k+dkm8y6ChZxj6UqxuieRUiDm8T4MnWlSCLkIU8wqJm5qNfIeVwvfOAZg6b4BskEeR0I7qoAfZQIa2oZo1VfVUozsy0EZaU5igZUFwJ8qkLOEVBIfoBdK0auncMUtY7Us7IrSDlGHWkhl0CZe+koY9eM4ItUIA4kHPdII8vqWTkpWQmK9Gx1L93mHMCvgGz6XSJs9OAswYSjP2ptJui5mHAGPKquMA14g8SwnPLVdVHhagsL9blyiarxGL3D+XKYzadrBSDtrVsVLo36NcstKYAsX+ypB58n2Ac0ADy9+xhXaElhbkN+spkFGLA0Wt1u01KVCvcECQOUhgwt8oXe6TxID2mGlU29dpEjq1NNNQmSnGoTbTlVH7sw2nmHo1m5p40O3fLRDO6I1rmo7xHNLtPojmmZpjctog27pZowxaIVnBm5H7EOh1kCFtkmvU/mDRHM2mOdSjThv0ybdSeSTMPsWejz27QrD5p5joaOw41aO5Em8jolmbjBpqlvi1LQFzh2/DPkmwDNeC9BFvX9swjmNCBPZWABk/fLFc8xGL/YiuGVv5ejM/jPCK3lzvS6Xo7PGnhE/MquRmn5AXO0w0sYhKLnrNnhLEmAhgFsbwhgohQyGfSw0Yi3p6qhgj5vlym0T+vevCDFmJGcwdxSrxt8tB1M9aahz7pjwDzJd3CJnYYyayIzLSIPz5iCQab06OG/uI0UKPJpB2NGubuZM3RufEbMSSZAeT54dM2a3ZyhDC0rIlTJ8SkU0LU3d9rEKdXd3uFmVw19qU+sEyjhjId+mX1o7uI++rHPpp+enzN5ySKhOrZyd3SWkg6qrOgKbd5vFva45M+kx9AUBycHgv0x7vBFnTq12UTvxVAshAksugDDhgndBdaLWeptRDd2vPC6DnF9qBq8nP2ibWZCM74nsmeSjRdZAvfyfWUQ3c1qpNUj4L6k+d6DO39PTirqCeNOg7CM76VCLhA7OXrWktLt5YNH6q6tZb1D4JX8st94dd+WVU41SDDtuuqGLWjClEtfn2Q3p3iNxz2xT8=&lt;/diagram&gt;&lt;/mxfile&gt;&quot;,&quot;toolbar&quot;:&quot;pages zoom layers lightbox&quot;,&quot;page&quot;:0}"></div>
    <script type="text/javascript" src="https://app.diagrams.net/js/viewer-static.min.js"></script>
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
