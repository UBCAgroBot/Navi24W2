# Isaac Sim

## How to run Isaac Sim on the CS servers
The lovely computer science departement happens to have a 
few lovely servers with RTX 3070 Tis, which are capable of running
Isaac Sim.

### Connecting to the lin servers
This part assumes you have a working UBC CS account.
If you don't, either take a computer science course or find 
someone who does.

The servers we want are only available to computers on the UBC network.

First, `ssh` into any one of the normal servers, then `ssh` into the lin server.
```bash
ssh -X -C <your-cwl>@gambier.students.cs.ubc.ca
ssh -X -C <your-cwl>@lin03.students.cs.ubc.ca # Run this on Gambier
```
You can choose whichever lin server you want (lin01-lin25),
but I use `lin03` so it may already have IsaacSim on it.

Test to make sure everything is working by running `xeyes`. If you
don't see a pair of eyes, something is wrong. Make sure you're on 
a system with a working X server.

### Check if it's installed already
Navigate to `/scratch-ssd`. If there's an nvidia folder, skip to the last step.

### Install NVIDIA Omniverse
First download the AppImage:
```bash
wget https://install.launcher.omniverse.nvidia.com/installers/omniverse-launcher-linux.AppImage
```
It won't just run because permissions, so extract it:
```bash
./omniverse-launcher-linux.AppImage --appimage-extract
cd squashfs-root/
```
Now run it with:
```bash
./omniverse-launcher --no-sandbox
```

### Signing in to NVIDIA Omniverse
This is the hardest part.

Make sure you have an NVIDIA account.

Next, run omniverse (as described above).
Then close it. Right now the sign in won't work because it relies on
special links, which currently don't work. So we'll make them work.

Navigate to `~/.local/share/applications`.
Open `nvidia-omniverse.desktop`. It should look like this:
```desktop
[Desktop Entry]
Name=omniverse-launcher
Exec="undefined" --no-sandbox %u
Type=Application
Terminal=false
MimeType=x-scheme-handler/omniverse
```
Replace `undefined` with the full path to `onmiverse-launcher`.
It should look something like this:
```desktop
[Desktop Entry]
Name=omniverse-launcher
Exec="/home/f/fbainbri/squashfs-root/omniverse-launcher" --no-sandbox %u
Type=Application
Terminal=false
MimeType=x-scheme-handler/omniverse
```
Now do exactly the same thing to `nvidia-omniverse-launcher.desktop`.

Now you should be able to launch omniverse and sign in normally.

### Installing Isaac Sim
Up until this point, we installed omniverse on your home directory.
Func fact: The CS departement only lets
you store 4gb on your home directory (I found out the hard way). 
So Isacc Sim has to be stored somewhere else.

The best place is the individual computer's ssd, which is located at `/scratch-ssd`.
This means that isaac sim has to be installed seperately on each computer,
but that's not too big of a problem since your omniverse settings and installation
is global.

Create a folder called `nvidia` at `/scratch-ssd/nvidia`.
Next, open NVIDIA omniverse's settings. Make all the three paths point to
`/scratch-ssd/nvidia`.

Now, simply install IsaacSim through Omniverse.

### Running Isaac Sim
Run
```bash
/scratch-ssd/nvidia/isaac-sim-4.2.0/isaac-sim.sh
```
You can also run it from omniverse if you so please.

The first time you run it there might be a message about IOMMU or something.
Just ignore it.
