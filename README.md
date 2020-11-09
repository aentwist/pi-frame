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
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="306px" height="201px" viewBox="-0.5 -0.5 306 201" content="&lt;mxfile host=&quot;app.diagrams.net&quot; modified=&quot;2020-11-09T03:43:22.581Z&quot; agent=&quot;5.0 (Windows)&quot; etag=&quot;q20ZH7k-fpTmNAXYXLWR&quot; version=&quot;13.9.2&quot; type=&quot;device&quot;&gt;&lt;diagram id=&quot;t2zgoPWlfdpKi9xcir2_&quot; name=&quot;Page-1&quot;&gt;5VpZU9swEP41mWkfYHzmeMwB5YUOM5QCj8IWtgbZciWFJP31lWL5kh0IGcem5AWk1f3tp9XuOgN7Hq1/UJCE18SHeGAZ/npgLwaWZRr2WPyTkk0qcZ1RKggo8lWnQnCL/sJspJIukQ9ZpSMnBHOUVIUeiWPo8YoMUEpW1W7PBFdXTUAAa4JbD+C69B75PEylY9co5FcQBWG2smmolghknZWAhcAnq5LIvhjYc0oIT0vReg6xBC/DJR13uaM13xiFMd9nAJrjKUTjX/FPg1PrNny+myzO1CyvAC/VgQfWEIv5Zk+iEMjCDTp7piCCots9FFJjmiRZJ7Fa3k+dkm8y6ChZxj6UqxuieRUiDm8T4MnWlSCLkIU8wqJm5qNfIeVwvfOAZg6b4BskEeR0I7qoAfZQIa2oZo1VfVUozsy0EZaU5igZUFwJ8qkLOEVBIfoBdK0auncMUtY7Us7IrSDlGHWkhl0CZe+koY9eM4ItUIA4kHPdII8vqWTkpWQmK9Gx1L93mHMCvgGz6XSJs9OAswYSjP2ptJui5mHAGPKquMA14g8SwnPLVdVHhagsL9blyiarxGL3D+XKYzadrBSDtrVsVLo36NcstKYAsX+ypB58n2Ac0ADy9+xhXaElhbkN+spkFGLA0Wt1u01KVCvcECQOUhgwt8oXe6TxID2mGlU29dpEjq1NNNQmSnGoTbTlVH7sw2nmHo1m5p40O3fLRDO6I1rmo7xHNLtPojmmZpjctog27pZowxaIVnBm5H7EOh1kCFtkmvU/mDRHM2mOdSjThv0ybdSeSTMPsWejz27QrD5p5joaOw41aO5Em8jolmbjBpqlvi1LQFzh2/DPkmwDNeC9BFvX9swjmNCBPZWABk/fLFc8xGL/YiuGVv5ejM/jPCK3lzvS6Xo7PGnhE/MquRmn5AXO0w0sYhKLnrNnhLEmAhgFsbwhgohQyGfSw0Yi3p6qhgj5vlym0T+vevCDFmJGcwdxSrxt8tB1M9aahz7pjwDzJd3CJnYYyayIzLSIPz5iCQab06OG/uI0UKPJpB2NGubuZM3RufEbMSSZAeT54dM2a3ZyhDC0rIlTJ8SkU0LU3d9rEKdXd3uFmVw19qU+sEyjhjId+mX1o7uI++rHPpp+enzN5ySKhOrZyd3SWkg6qrOgKbd5vFva45M+kx9AUBycHgv0x7vBFnTq12UTvxVAshAksugDDhgndBdaLWeptRDd2vPC6DnF9qBq8nP2ibWZCM74nsmeSjRdZAvfyfWUQ3c1qpNUj4L6k+d6DO39PTirqCeNOg7CM76VCLhA7OXrWktLt5YNH6q6tZb1D4JX8st94dd+WVU41SDDtuuqGLWjClEtfn2Q3p3iNxz2xT8=&lt;/diagram&gt;&lt;/mxfile&gt;"><defs/><g><rect x="115" y="10" width="120" height="40" fill="#ffffff" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 118px; height: 1px; padding-top: 30px; margin-left: 116px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; "><b>Pi-frame Web App</b></div></div></div></foreignObject><text x="175" y="34" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Pi-frame Web App</text></switch></g><rect x="230" y="130" width="60" height="40" fill="#ffffff" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 150px; margin-left: 231px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; ">Users</div></div></div></foreignObject><text x="260" y="154" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Users</text></switch></g><rect x="35" y="130" width="140" height="40" fill="#ffffff" stroke="#000000" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 138px; height: 1px; padding-top: 150px; margin-left: 36px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; "><div>Digital Picture Frames</div></div></div></div></foreignObject><text x="105" y="154" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Digital Picture Frames</text></switch></g><path d="M 70 130 L 111.88 55.55" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 114.45 50.97 L 114.07 58.79 L 111.88 55.55 L 107.97 55.36 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 145 50 L 107.85 124.3" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 105.5 129 L 105.5 121.17 L 107.85 124.3 L 111.76 124.3 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 245 130 L 207.85 55.7" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 205.5 51 L 211.76 55.7 L 207.85 55.7 L 205.5 58.83 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 235 50 L 272.15 124.3" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 274.5 129 L 268.24 124.3 L 272.15 124.3 L 274.5 121.17 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><rect x="65" y="80" width="40" height="20" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 38px; height: 1px; padding-top: 90px; margin-left: 66px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; "><span style="background-color: rgb(255 , 255 , 255)">Poll</span></div></div></div></foreignObject><text x="85" y="94" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Poll</text></switch></g><rect x="115" y="80" width="50" height="20" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 48px; height: 1px; padding-top: 90px; margin-left: 116px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; "><span style="background-color: rgb(255 , 255 , 255)">Current image to display</span></div></div></div></foreignObject><text x="140" y="94" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Current...</text></switch></g><rect x="60" y="170" width="90" height="20" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 88px; height: 1px; padding-top: 180px; margin-left: 61px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; "><span style="background-color: rgb(255 , 255 , 255)">Visit a webpage</span></div></div></div></foreignObject><text x="105" y="184" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Visit a webpage</text></switch></g><rect x="215" y="170" width="90" height="30" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 88px; height: 1px; padding-top: 185px; margin-left: 216px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; ">Manage images and slideshows</div></div></div></foreignObject><text x="260" y="189" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Manage images a...</text></switch></g><rect x="185" y="100" width="60" height="20" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 58px; height: 1px; padding-top: 110px; margin-left: 186px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; "><span style="background-color: rgb(255 , 255 , 255)">Commands</span></div></div></div></foreignObject><text x="215" y="114" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Commands</text></switch></g><rect x="215" y="70" width="40" height="20" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 38px; height: 1px; padding-top: 80px; margin-left: 216px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; "><span style="background-color: rgb(255 , 255 , 255)">Browsing</span></div></div></div></foreignObject><text x="235" y="84" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Browsi...</text></switch></g><path d="M 5 8 C 5 -2.67 65 -2.67 65 8 L 65 52 C 65 62.67 5 62.67 5 52 Z" fill="#ffffff" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 5 8 C 5 16 65 16 65 8 M 5 12 C 5 20 65 20 65 12 M 5 16 C 5 24 65 24 65 16" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 71.37 30 L 108.63 30" fill="none" stroke="#000000" stroke-miterlimit="10" pointer-events="stroke"/><path d="M 66.12 30 L 73.12 26.5 L 71.37 30 L 73.12 33.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><path d="M 113.88 30 L 106.88 33.5 L 108.63 30 L 106.88 26.5 Z" fill="#000000" stroke="#000000" stroke-miterlimit="10" pointer-events="all"/><rect x="15" y="30" width="40" height="20" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 38px; height: 1px; padding-top: 40px; margin-left: 16px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; ">Disk</div></div></div></foreignObject><text x="35" y="44" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Disk</text></switch></g><rect x="0" y="60" width="70" height="20" fill="none" stroke="none" pointer-events="all"/><g transform="translate(-0.5 -0.5)"><switch><foreignObject style="overflow: visible; text-align: left;" pointer-events="none" width="100%" height="100%" requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"><div xmlns="http://www.w3.org/1999/xhtml" style="display: flex; align-items: unsafe center; justify-content: unsafe center; width: 68px; height: 1px; padding-top: 70px; margin-left: 1px;"><div style="box-sizing: border-box; font-size: 0; text-align: center; "><div style="display: inline-block; font-size: 12px; font-family: Helvetica; color: #000000; line-height: 1.2; pointer-events: all; white-space: normal; word-wrap: normal; ">Hold images</div></div></div></foreignObject><text x="35" y="74" fill="#000000" font-family="Helvetica" font-size="12px" text-anchor="middle">Hold images</text></switch></g></g><switch><g requiredFeatures="http://www.w3.org/TR/SVG11/feature#Extensibility"/><a transform="translate(0,-5)" xlink:href="https://desk.draw.io/support/solutions/articles/16000042487" target="_blank"><text text-anchor="middle" font-size="10px" x="50%" y="100%">Viewer does not support full SVG 1.1</text></a></switch></svg>
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
