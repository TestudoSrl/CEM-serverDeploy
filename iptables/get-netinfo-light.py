import socket
import fcntl
import struct
import subprocess
import re

def get_default_gateway_info():
    try:
        result = subprocess.run(['ip', 'route', 'list'], capture_output=True, text=True)
        routes = result.stdout.split('\n')
        for route in routes:
            if 'default' in route:
                parts = route.split()
                for i, part in enumerate(parts):
                    if part == 'dev':
                        interface = parts[i + 1]
                    elif part == 'via':
                        gateway = parts[i + 1]
                return interface, gateway
    except Exception as e:
        print(f"Errore durante il recupero delle informazioni sulla default gateway: {e}")

    return None, None

def get_ip_address(interface):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            ip_address = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', interface[:15].encode("utf-8"))
            )[20:24])
        return ip_address
    except IOError:
        return None

def get_subnet_mask(interface):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            subnet_mask = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x891b,  # SIOCGIFNETMASK
                struct.pack('256s', interface[:15].encode("utf-8"))
            )[20:24])
        return subnet_mask
    except IOError:
        return None

def get_network_address(ip_address, subnet_mask):
    ip_parts = [int(part) for part in ip_address.split('.')]
    subnet_parts = [int(part) for part in subnet_mask.split('.')]
    network_address = '.'.join(str(ip & mask) for ip, mask in zip(ip_parts, subnet_parts))
    return network_address

def get_broadcast_address(network_address, subnet_mask):
    network_parts = [int(part) for part in network_address.split('.')]
    subnet_parts = [int(part) for part in subnet_mask.split('.')]
    broadcast_address = '.'.join(str(network | (255 - mask)) for network, mask in zip(network_parts, subnet_parts))
    return broadcast_address

def main():
    interfaccia_rete, gateway = get_default_gateway_info()

    if interfaccia_rete is None or gateway is None:
        print("Impossibile trovare l'interfaccia di rete con la default gateway.")
        return

    indirizzo_ip = get_ip_address(interfaccia_rete)
    subnet_mask = get_subnet_mask(interfaccia_rete)
    indirizzo_rete = get_network_address(indirizzo_ip, subnet_mask)
    indirizzo_broadcast = get_broadcast_address(indirizzo_rete, subnet_mask)

    file_path = "rc.z-fw"
    with open(file_path, 'r') as file:
        file_content = file.read()

    file_content = re.sub(r'\$IpAdd', indirizzo_ip, file_content)
    file_content = re.sub(r'\$Subnet', subnet_mask, file_content)
    file_content = re.sub(r'\$Gateway', gateway, file_content)
    file_content = re.sub(r'\$NetAdd', indirizzo_rete, file_content)
    file_content = re.sub(r'\$BroadAdd', indirizzo_broadcast, file_content)
    file_content = re.sub(r'\$NetIf', interfaccia_rete, file_content)

    with open(file_path, 'w') as file:
        file.write(file_content)

    print(f"Le informazioni sono state scritte nel file '{file_path}'. Grazie!")

if __name__ == "__main__":
    main()

