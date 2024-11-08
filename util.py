import ipaddress



def is_in_lan(ip_address, subnet):
    return ipaddress.ip_address(ip_address) in ipaddress.ip_network(subnet)



#IP 패킷을 컨버팅
def convert_ip_with_zero(ip):
    parts = ip.split('.')
    converted_parts = [part.zfill(3) for part in parts]

    return '.'.join(converted_parts)


#컨버팅 되돌리기
def revert_ip(ip):
    parts = ip.split('.')
    reverted_parts = [str(int(part)) for part in parts]
    return '.'.join(reverted_parts)


#네트워크 주소 되돌리기
def revert_ipv4_subnet(ip_with_mask):
    ip, mask = ip_with_mask.split('/')

    ip_parts = [int(part) for part in ip.split('.')]

    return ".".join(str(part) for part in ip_parts) + "/" + mask


def convert_ipv4_subnet(new_ip_with_mask):
    new_ip, mask = new_ip_with_mask.split('/')

    new_ips = [str(part.zfill(3)) for part in new_ip.split('.')]

    return '.'.join(new_ips) + '/' + mask

