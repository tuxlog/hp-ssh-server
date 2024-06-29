# hp-ssh-server
A honeypot ssh fake server 

One of our VPS got attacked a thousand times per day with brute force ssh attacks. So I wanted to fetch the IPs, user and passwords to see what happened and wanted to have them on a map to know about the countries from where the attacks are started. SO I searched a bit and found two great little projects which I used as a base for my honeypot ssh server, short hp-ssh-server. One is https://github.com/internetwache/SSH-Honeypot and the other https://github.com/pieqq/PyGeoIpMap/. I integrated both and adopted the source to my needs.

# Installation
If you want to have your own real ssh server in parallel you have to change the port of your sshd setup in /etc/ssh/sshd_config.
To run hp-ssh-server on a non root account, you have to redirect connects to ssh port 22 to another port > 1024, e.g. 2222 using something like 
iptables -A PREROUTING -t nat -p tcp --dport 22 -j REDIRECT --to-port 2222

Copy the files to a user directory like /home/myuser/hp-ssh-server
Edit hp-ssh-server and change the directories accordingly
Copy the systemd file to /lib/systemd/system `sudo cp hp-ssh-server.service /lib/systemd/system/hp-ssh-server.service`
Enable the service `systemctl enable hp-ssh-server`
Start the service `sudo service hp-ssh-server start`

The server starts and writeds all the information in a txt file sshlogins.txt looking like
`2024-06-28 07:19:38;180.101.88.221;58235;"root";"silvestre"`
As you can see it logs the date, ip, port, user and password on one line for every attempt.

Now for the fun part.

# Creating a map of the logon attempts
First of all you have to fetch the GeoIPCity.dat from https://mailfud.org/geoip-legacy/ and unzip it in the same directory.
This is the old legacy format of the IP database which can be obtained without a registration.

After this just start ip2map.py. Depending on the number of ips it may take some time to create the image and store it to hackermap.png. 
Which shows red circles at the location which attacked. The more often one IP attacks the bigger the circle gets, to get an impression of the amount of tries from this location.

# License
This piece of software is lincensed under MIT. See LICENSE.md for more information
