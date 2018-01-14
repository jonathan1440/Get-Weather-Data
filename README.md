# Get-Weather-Data
**Hack into AcuRite from Raspberry Pi to constantly extract weather data**

**vv Instructions below!! vv**

Adapted from this amazing blog series by Dave Thompson: http://www.desert-home.com/2014/11/acurite-weather-station-raspberry-pi.html
`usbexample1.c` and `weatherstation.c` were copied verbatum from that blog and `readWeatherData.py` is based on code from it. Everything else is my own creation.

I didn't have the tools, equipment, desire, or knowledge to ditch the weather station console and go striaght to intercepting the RF signals, or else I would direct you to Dave's GitHub repo for this project. 
I'll link it here anyways: https://github.com/draythomp/Desert-Home-WeatherStation

I had to do quite a few things differntly from Dave when I set it up myself, and it wasn't always clear to a beginner like me what his instructions meant, so I thought I'd put the exact process I follwed in one place.
To be clear, at the time of writing, I am still a beginner. I'm sure there are better ways to do most of what's below, but hopefully this will help someone else who doesn't want to take the time to figure it out themself.


Both of the .py files are throughly commented by me to explain what's going on.
Both of the .c files are commented by Dave Thompson for the same purpose.

**===========================================================**

**A brief overivew of the files involved:**
* `usbexample1.c` allows us to access the USB cord connection the RPi to the AcuRite console.
* `weatherstation.c` accesses the AcuRite console and retrievs the data it collects from the weather station itself. It outputs that data every 15 seconds. You can change the timer interval in the top of the file.
* `readWeatherData.py` collects the output from `weatherstation.c`, formats it how I wanted it, and writes it to a csv file (one file per day) for storage. Also, every midnight, it emails the previous day's file to a specified email address.
* `emailData.txt` stores all the parameters needed for the above email to work. You'll need to update this yourself with info specific to your senario.

**My equipment:**
1. I have the AcuRite weather station model 01536. 
   - You can read all sorts of useful information about it here: https://www.acurite.com/kbase/01536_Weather_Station.html
   - It should come with a power cord and USB cord. 
2. I used a Raspberry Pi 3 B v1.2 to hack into the AcuRite weather station console.
   - You can read details about it here: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
   - You have to order a microUSB power cord separately. I didn't realize this and had to wait a few extra days for it to arrive.
   - It is running Raspbian on a microSD card that has NOOBS v1.9 preinstalled.
     - I bought it from adafruit, which is now selling microSDs with NOOBS v2.1: https://www.adafruit.com/product/1583 
   - I'm using an HDMI monitor and wireless USB mouse and keyboard to control the GUI on the RPi.
     - The mouse and keyboard are something like this: https://www.amazon.com/Logitech-MK270-Wireless-Keyboard-Mouse/dp/B00BP5KOPA
     - It is possible to do this whole thing by SSHing into the pi, but I'm too visual to feel comfortable doing that. Although I run the scripts through SSH now that I've finished, I set it up using the GUI.
     - If you need to use only an SSH connection, you can download WinSCP to transfer files from your windows machine to the RPi over an SSH connection: https://winscp.net/download/WinSCP-5.11.3-Setup.exe
   - Although my RPi has 4 USB ports, I could have done it with 2:
     - One for the wireless USB keyboard and mouse
     - One to connect with the AcuRite sensor
 
 
####**Instructions:**
The first step, obviously, is to plug everything in.
The USB port on the AcuRite is under the panel you have to take off to replace the batteries. 
Plug in the USB cord that comes with the AcuRite to both that port and a USB port on the RPi.

**The below section corresponds to Dave's first related post: http://www.desert-home.com/2014/11/acurite-weather-station-raspberry-pi.html**
We don't have permissions to access the USB cord. 
To see that we don't have permissions:
1. Open terminal in the RPi
2. Type `cd /dev` to go to the directory storing all the USB types. Hit enter (hit enter after each command you enter in terminal).
3. Type `ls -l` to look at all of the permissions.
4. This USB type is something like `hidraw2`. The number could be different.
5. Note that we can't do much to it.
To change permissions so we can access the USB:
1. (Optionally) type `clear`
2. Type `dmesg` 
3. Look for something like this:
   - `[    2.536425] usb 1-1.2: New USB device found, idVendor=24c0, idProduct=0003`
   
      `[    2.538128] usb 1-1.2: New USB device strings: Mfr=0, Product=2, SerialNumber=0`
      
      `[    2.541669] usb 1-1.2: Product: Chaney Instrument`
      
      `[    3.127499] udevd[156]: starting version 175`
      
      `[    5.553287] bcm2708-i2s bcm2708-i2s.0: Failed to create debugfs directory`
      
      `[   12.559829] hid-generic 0003:24C0:0003.0001: usb_submit_urb(ctrl) failed: -1`
      
      `[   12.561497] hid-generic 0003:24C0:0003.0001: timeout initializing reports`
      
      `[   12.563452] input: Chaney Instrument as /devices/platform/bcm2708_usb/usb1/1-1/1-1.2/1-1.2:1.0/input/input0`
      
      `[   12.569076] hid-generic 0003:24C0:0003.0001: input,hidraw0: USB HID v1.11 Device [Chaney Instrument] on usb-bcm2708_usb-1.2/input0`
      
   - It will probably be at the very end, since its the last thing you plugged into the USB ports.
4. Find the line that says `New USB device found, idVendor=24c0, idProduct=0003` in your terminal. The values for idVendor and idProduct could be different.
   - Take note of what it defines `idVendor` and `idProduct` as. In this example, they are `24c0` and `0003` respectively.
5. To make the USB readable by anything other than root, go to the directory `/etc/udev/rules.d`.
   - Type `cd /etc/udev/rules.d`
6. Create a file named `10-local.rules`
   - There are multiple methods, but one option is to type `nano 10-local.rules`.
7. Make sure it has a line in it that says `SUBSYSTEM=="usb", ATTRS{idVendor}=="XXXX", ATTRS{idProduct}=="YYYY", SYMLINK="weather" MODE="666",GROUP="users"`.
   - Once you've typed it out, replace `XXXX` with the `idVendor` and `YYYY` with the `idProduct` that you found earlier.
   - Then hit `ctrl+x`, type `y`, and hit enter.
8. Now check to see if we have permissions on the USB.
   - Type `cd /dev`
   - Type `ls -l`
   - Look for `weather`. That's what we renamed it in the file.

**This next part corresponds with this post: http://www.desert-home.com/2014/12/acurite-weather-station-raspberry-pi.html**
Next we need to get the ability to connect to the AcuRite console through code:
1. Go to this link and download it on your RPi: https://sourceforge.net/projects/libusb/files/latest/download?source=files
2. Go in terminal to the directory where you put the download. Type `tar xvf filename` (replace filename with the filename of the download)
3. Before you can install the library you need to make sure your RPi is completely up to date.
   - Type `sudo apt-get update`
   - Type `sudo apt-get upgrade`
   - Type `y`
   - This will take a while. IIRC, it took me about an hour, but it will vary based on your CPU and download speed.
4. You also need to get another library first. Type `sudo apt-get install libudev-dev`
5. Now go to the directory where the original download is. Read the `INSTALL` file to get the instructions. They could easily change between when I write this and you read it, but, when I did it, they were:
   1. `sudo ./configure`
   2. `sudo make`
   3. `sudo make install`
   - If it's different for you, make sure you're logged in as root or put `sudo` before the commands. Otherwise it won't work.
6. Now download `usbexample1.c` from this repository and put it somewhere on your RPi. It doesn't matter, but I put mine in a folder on my desktop. Where ever you put it, remember it, because all the other files in this repository need to go to the same place.
7. This particular file needs to be compiled to `/usr/local/lib`. To compile it, type `cc  usbexample1.c -L/usr/local/lib -lusb-1.0`.
8. Compiling it should leave you with an `a.out` file. You need this; leave it there.
9. If you run `a.out`, you'll see output that tells you that it was able to find the device and open it.

**This next part corresponds to this post: http://www.desert-home.com/2014/12/acurite-weather-station-raspberry-pi_3.html**
The AcuRite console gives off two different types of output. The `weatherstation.c` file reads them. Here's how to set it up:
1. Download the `weatherstation.c` file from this repository to the same directory you put `usbexample1.c` in. 
2. Read the comments in `weatherstation.c` if you want. They kind of explain how to use it and what it does. This is optional; I'll tell you everything you need to know here (the bare minimum).
3. `weatherstation.c` needs to be compiled too; type `cc -o weatherstation  weatherstation.c -L/usr/local/lib -lusb-1.0`
4. When you run it, the `stdout` output will be the data from the console in a dictionary. To run it, type `./weatherstation`
5. All the output you see is a combination of the `stderr` and `stdout` output. To narrow it down you can type `./weatherstation 2`

Now we use a python file to put the data into a file for storage.
The file Dave provided was in `python 2.7.9`. I don't know `python 2` and wanted to edit the code, so I changed it to `python 3.4.2`. I also added daily weather updates with all the data from the previous 24 hours via email.

The RPi is naturally set to run `python 2.7.9` even though it has multiple versions installed. 
In order to run the `readWeatherData.py` file we first have to change the default python version to `3.4.2`:
1. First make sure you know what your python version is: `python --version`
2. If it says `2.7.9`, type `update-alternatives --list python` to list the current versions of python. If it returns `3.4.#`, you can skip to step 7.
   - You'll probably get a result saying `update-alternatives: error: no alternatives for python`
3. Type `update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1`
   - This sets python 2.7 as one of the alternatives. Even if you don't want to use it now, you should do it to make switching between versions later easier.
4. Now type `update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2`
   - This sets python 3.4 as another alternative.
5. You should now be set to `3.4.2` for your default. 
6. If, at any time in the future, you want to change between python versions, type `update-alternatives --config python` and follow the instructions shown in terminal.
   - You can read more about changing python versions here: https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux
7. Now go ahead and download `readWeatherData.py` into the same directory as the previous two files.
8. You'll need to update lines 62 and 67 to match the filepath to the directory you're using for this project.
9. `readWeatherData.py` sends email updates based on the content of a file called `emailData.txt` in the same directory as `readWeatherData.py`.
10. Download `emailData.txt` into the appropriate directory and edit its contents to be specific to you wants.
11. Now, to store the data, go to that same directory and create a folder called `Data`. The file `readWeatherData.py` is coded to use it. You can go into the code and change it in line 62 if you don't like the name.
12. To run the file, type `./weatherstation.c 2| python readWeatherData.py`.
   - This takes the `stdout` output of `weatherstaion.c` and pipes it into `readWeatherData.py` as the input.
   - `readWeatherData.py` takes that input and writes it into a file it creates in `./Data` named for the date.

   
**Great! Now you have the data being collected and stored in a directory where you can access it. This is as far as I went in following Dave's blogs.**
The rest of his blogs on this topic are linked here:
* http://www.desert-home.com/2014/12/acurite-weather-station-raspberry-pi_13.html
* http://www.desert-home.com/2014/12/acurite-weather-station-raspberry-pi_16.html
* http://www.desert-home.com/2014/12/acurite-weather-station-and-barometric.html
* http://www.desert-home.com/2014/12/acurite-weather-station-raspberry-pi_29.html
* http://www.desert-home.com/2015/01/acurite-weather-station-raspberry-pi.html
* http://www.desert-home.com/2015/02/reading-acurite-5n1-sensor-set-this.html
* http://www.desert-home.com/2015/05/yet-another-update-to-acurite-5n1.html


It is unrealistic to have your monitor permantently connected to the RPi which has to be connected to the AcuRite weather station console to work.
Therefore, you'll probably want to run the files via SSH.
Here's how to set it up: (adapted from http://www.instructables.com/id/Use-ssh-to-talk-with-your-Raspberry-Pi/)
1. Before disconnecting your monitor, you need to enable SSH on your RPi.
2. At some point, you'll probably be prompted to login. The default username is `Pi` and the default password is `raspberry`.
3. Type `sudo raspi-config`.
4. Navigate to `Interfacing Options` > `SSH` > `Yes`
5. Hit the right arrow key twice to navigate to `Finish`
6. Now you need to reboot to save the changes. After making sure all your files are saved, type `reboot`.
7. After it restarts, open terminal and type `ifconfig` to find the IP address.
8. You're looking for `inet addr: ###.###.###.###`, probably under the `wlan0` heading. Write it down.
9. Now you need to install PuTTY on the computer you're going to SSH from. 
10. Download it from here: `http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html`
11. Install it by running the .exe
12. Run PuTTY.
13. In the field marked `Host Name (or IP address)` enter the `inet addr` you wrote down earlier.
14. Click `open`.
15. A window will pop open. I would choose "no" the first time so that you can make sure everything works as expected.
16. A black screen will appear and, after a possible (short) wait, you'll be prompted to login. Login using the user credentials for you pi.
    - Remember that the default username is `pi` and the default password is `raspberry`.
17. If everything went correctly, you're in the terminal in your RPi!


Now we need to make the two scripts executable over SSH. It isn't practical to have it running in the SSH terminal, as it would prevent you from doing anything else. The solution I chose was to make it a service. Services can be set to run at certain points. I set it up to start every time the RPi turns on. 
1. Download the check-weather.sh file into your directory. This file executes the `weatherstation.c` file and pipes its output into `readWeatherData.py` and runs it too.
2. Now we need to make the service. Type in `cd /lib/systemd/system`.
3. We're going to make a file called `check-weather.service` that controlls what (the `check-weather.sh` file) and when it is run. Type `sudo nano check-weather.service`.
4. Type the following: 
  `[Unit]`

   `Description=Hello World`

   `After=multi-user.target`

   ``

   `[Service]`

   `Type=simple`

   `ExecStart=/usr/bin/python /home/pi/hello_world.py`

   `Restart=on-abort`

   ``

   `[Install]`

   `WantedBy=multi-user.target`


5. Hit `ctrl+x`, `y`, and enter.
6. Now execute the following commands to set the permissions, make the file executable, and start the service:

   `sudo chmod 644 /lib/systemd/system/check-weather.service`

   `chmod +x <filepath to your directory with the weather stuff in it>`

   `sudo systemctl daemon-reload`

   `sudo systemctl enable check-weather.service`

   `sudo systemctl start check-weather.service`

7. The script should now be running. If you want to check it for stderr (errors and logs), type `sudo systemctl status check-weather.service`.
8. If you want to make sure its working right, you can go to the /Data folder and make sure the right file has been created and that it has the right content.

