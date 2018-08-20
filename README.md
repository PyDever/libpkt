## Installation
libpkt can be installed using Make. 
```
$ make build
```
NOTE: libpkt only runs on UNIX systems!

## About libpkt
libpkt is a simple packet manipulation library for Python. It is specially designed to
efficiently handle TCP/IP packets. 

  * ***fast*** packet capture algorithm
  * ***fast*** packing and unpacking
  * efficient data injection
  * ***faster*** THAN SCAPY!
  
 libpkt ***only*** has ***standard library*** dependencies!
 
  * `socket` for obvious reasons
  * `struct` for C-esk functionality
  * `random` for byte generation
  * `time` for plotting delays
  * `array` for low-level structures
  * `fcntl` for low-level file control

### Contributions
Contributions are welcome, however please read the [guidlines](google.com).

### Small API Documentation

#### ***SHIT GETS NERDY HERE! KNOW YOUR STUFF BEFORE READING ON!*** ####

libpkt has smaller sub-modules that do specific things. 

 * `ifs` for low-level newtwork interface control
 * `pkt` for packet manipulation
 * `psocket` for sniffing and sending packets

Let us learn the `ifs` module first. As you may know, every computer
has a network card that houses multiple interfaces. All internet and TCP/IP
connections are made through one of those interfaces. 
