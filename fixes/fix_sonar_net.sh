#nmcli connection show
#sudo nmcli connection modify d0f82096-a5b2-378d-87c8-c3212879ec36 connection.interface-name usb0 connection.autoconnect yes
#sudo nmcli connection up d0f82096-a5b2-378d-87c8-c3212879ec36
nmcli connection show
sudo nmcli con up USB
nmcli connection show
