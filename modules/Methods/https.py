import os

os.system("sudo -u mitmproxyuser -H bash -c 'mitmdump --mode transparent --showhost --flow-detail 1 \
	--set stream_websocket=true --ssl-insecure -s ./modules/Methods/proxy.py'")