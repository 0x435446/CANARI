#forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables --table nat --append POSTROUTING --out-interface ens33 -j MASQUERADE
iptables --append FORWARD --in-interface ens38 -j ACCEPT
iptables --append FORWARD -i ens33 -j ACCEPT


#mitmproxy
sysctl -w net.ipv6.conf.all.forwarding=1
sysctl -w net.ipv4.conf.all.send_redirects=0
iptables -A FORWARD -i ens38 -o ens33 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i ens33 -o ens38 -j ACCEPT
iptables -t nat -A POSTROUTING -o ens38 -j MASQUERADE
iptables -t nat -A PREROUTING -i ens33 -p tcp -m tcp --dport 80 -j REDIRECT --to-ports 8080
iptables -t nat -A PREROUTING -i ens33 -p tcp -m tcp --dport 443 -j REDIRECT --to-ports 8080
#sudo -u mitmproxyuser -H bash -c 'mitmdump --mode transparent --showhost --flow-detail 1 --set stream_websocket=true --ssl-insecure -s proxy.py'
