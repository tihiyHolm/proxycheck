import socks
import socket
import argparse

def test_proxy(proxy, mode):
    ip, port = proxy.split(":")
    port = int(port)

    # Set proxy type
    if mode == "socks4":
        proxy_type = socks.SOCKS4
    elif mode == "socks5":
        proxy_type = socks.SOCKS5
    else:
        print(f"❌ Invalid mode: {mode}")
        return None

    
    socks.set_default_proxy(proxy_type, ip, port)
    socket.socket = socks.socksocket
    try:
        s = socket.socket()
        s.settimeout(6)
        s.connect(("api.ipify.org", 80))
        s.send(b"GET / HTTP/1.1\r\nHost: api.ipify.org\r\nConnection: close\r\n\r\n")
        data = s.recv(4096)
        s.close()
        if b"200 OK" in data:
            return proxy
    except:
        return None

def main():
    parser = argparse.ArgumentParser(description="SOCKS4/5 Proxy Tester")
    parser.add_argument("-proxy", required=True, help="Path to proxy list")
    parser.add_argument("-m", required=True, choices=["socks4", "socks5"], help="Proxy mode (socks4 or socks5)")
    args = parser.parse_args()

    with open(args.proxy, "r") as f:
        proxies = [line.strip() for line in f if line.strip()]

    print(f"\n🔎 Testing {len(proxies)} proxies in {args.m.upper()} mode...\n")

    for proxy in proxies:
        result = test_proxy(proxy, args.m)
        if result:
            print(f"✅ WORKING: {result}")
        else:
            print(f"❌ FAILED:  {proxy}")

if __name__ == "__main__":
    main()
