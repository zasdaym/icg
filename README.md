IOU Config Generator (ICG) for GNS3

Zasda Yusuf Mikail

This script used for automating basic ip address and line configuration for IOU device on GNS3.

Warning: ALL CONFIGURATION ON THE DEVICE WILL BE DELETED BEFORE CONFIGURED BY THIS SCRIPT

# How to use:
1. Create topology, save, shutdown all devices.
2. Run the script
3. Boot up

# Addressing:
Example = R1--R2--R3

R1 interface to R2 	= 192.168.12.1/24 
			  		  12.12.12.1/24 (IDN Mode)
			  		  2001:10:1:12::1/64

R1 loopback			= 1.1.1.1/32
			      	  2001::1/64

# Arguments:

-bd,	--base-dir	= Base directory for the GNS3 project.	(REQUIRED IF NOT USING VM)

-t,		--topology	= Location of topology file (.gns3).	(REQUIRED)

-4,		--v4 		= IPv4 Base prefix.						(Default=192.168)

-6,		--v6		= IPv6 Base prefix.						(Default=2001:10:1)

-d,		--debug		= Debug, print what will be configured.

-vm,	--vm		= Use this if you're using GNS3 VM.

-srv,	--srv		= GNS3 VM IP address.					(Default=192.168.56.101)

-idn,	--idn		= IDN addressing style

# Usage Examples:

1. MINIMAL ARGUMENTS (NATIVE IOU,LINUX ONLY) 
    
	python icg.py -bd /home/zasda/GNS3/projects/lab1 -t lab1.gns3

2. MINIMAL ARGUMENTS (VM)
    
	python icg.py -vm -srv 192.168.56.111 -t /home/zasda/GNS3/projects/lab1/lab1.gns3
	
    icg.exe -vm -srv 192.168.56.111 -t C:/users/zasda/GNS3/projects/lab1/lab1.gns3

3. DEBUG ONLY
    
	python icg.py -bd /home/zasda/GNS3/projects/lab1 -t lab1.gns3 -d

4. CHANGE IPV4 BASE PREFIX TO 172.16
    
	python icg.py -bd /home/zasda/GNS3/projects/lab1 -t lab1.gns -4 172.16
    
5. IDN STYLE ( ipv4 = R1 TO R2 Becomes 12.12.12.X )
    
	python icg.py -bd /home/zasda/GNS3/projects/lab1 -t lab1.gns3 -idn
