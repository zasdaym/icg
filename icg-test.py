'''
    IOU CONFIG GENERATOR FOR GNS3 in Python
    Author: Zasda Yusuf Mikail
     
    Automate basic ip and ipv6 addressing, example R1 to R2:
   
    R1
    ipv4 = 192.168.12.1/24
    ipv6 = 2001:10:1:12::1/64
    ipv4Lo = 1.1.1.1
    ipv6Lo = 2001::1/128

    R2
    ipv4 = 192.168.12.2/24
    ipv6 = 2001:10:1:12::2/64
    ipv4Lo = 2.2.2.2
    ipv6Lo = 2001::2/128

    ONLY SUPPORT POINT TO POINT LINK

    HOW TO USE
    1. Create topology, save project.
    2. Run the script. If using the VM don't use the -bd or --base-dir argument.
    3. Boot up, start labbing!

    MINIMAL ARGUMENTS (NATIVE)
        python icg.py -bd /home/zasda/GNS3/projects/lab1 -t lab1.gns3

    MINIMAL ARGUMENTS (VM)
        python icg.py -vm -srv 192.168.56.101 -t /home/zasda/GNS3/projects/lab1/lab1.gns3

    DEBUG ONLY
        python icg.py -bd /home/zasda/GNS3/projects/lab1 -t lab1.gns3 -d

    CHANGE IPV4 BASE PREFIX TO 172.16
        python icg.py -bd /home/zasda/GNS3/projects/lab1 -t lab1.gns -4 172.16
    
    IDN STYLE ( ipv4 = R1 TO R2 Becomes 12.12.12.X )
        python icg.py -bd /home/zasda/GNS3/projects/lab1 -t lab1.gns3 -idn
'''

import json
import os
import itertools
import sys
import argparse
#import paramiko

#PARSE ARGUMENT FROM SCRIPT
def parse():

    parser = argparse.ArgumentParser(description='iou_auto_ip')

    parser.add_argument("--debug", "-d",
                        action="store_true",
                        default=False,
                        help="enable debugging")

    parser.add_argument("--base-dir", "-bd",
                        type=str,
                        default='/opt/gns3/projects/',
                        dest='base_dir',
                        help="base directory for GNS3 project")
    
    parser.add_argument("--project-files", "-pf",
                         type=str,
                         default='project-files/iou/',
                         dest='project_files',
                         help="iou project files dir")

    parser.add_argument("--topology", "-t",
                        type=str,
                        dest='topology_file',
                        help="GNS3 topology file")

    parser.add_argument("--v4", "-4",
                        type=str,
                        default='192.168',
                        dest='ipv4_base',
                        help="IPv4 base prefix")

    parser.add_argument("--v6", "-6",
                        type=str,
                        default='2001:10:1',
                        dest='ipv6_base',
                        help="IPv6 base prefix")

    parser.add_argument("--idn", "-idn",
                        action="store_true",
                        default=False,
                        help="Special IDN mode")

    parser.add_argument("--vm", "-vm",
                        action="store_true",
                        default=False,
                        help="Special VM mode")

    parser.add_argument("--srv", "-srv",
                        type=str,
                        default='192.168.56.101',
                        dest='srv',
                        help="VM IP address")




    args = parser.parse_args()

    return args
#END OF PARSE FUNCTION

#CREATE AND WRITE NEW CONFIG FUNCTION
def configure_nodes(node):
    #CREATE LOOPBACK IP
    node_id = node['node_id']
    config = ['! config added by ICG !', '!']
    host = node['node_name']
    lo_cfg = [lo.format(node_id) for lo in (lo0_v4, lo0_v6)]
    loopback = 'interface Loopback0\n {}\n {}'.format(*lo_cfg)
    hostname = 'hostname {}'.format(host)
    config.extend(hostname.splitlines())
    config.extend(line_cfg.splitlines())
    config.extend(loopback.splitlines())

    
    #CREATE INTERFACE IP
    for port in node['ports']:
        src, dst = links[port['link_id']]
        if src > dst:
            base = ''.join(map(str, (dst, src)))
        else:
            base = ''.join(map(str, (src, dst)))

        if options.idn:
            po_cfg = [po.format(base, node_id) for po in (idn_v4, base_v6)]
            int_config = 'interface {}\n {} \n {}\n no shut'.format(port['name'], *po_cfg)
            config.extend(int_config.splitlines())
        else:
            po_cfg = [po.format(base, node_id) for po in (base_v4, base_v6)]
            int_config = 'interface {}\n {} \n {}\n no shut'.format(port['name'], *po_cfg)
            config.extend(int_config.splitlines())

    cfg_file = os.path.join(CFG_DIR, node['vm_id'], node['config']).replace("\\","/")
    #WRITE OR DEBUG LOGIC
    if options.vm:
    	user = 'gns3'
    	passwd = 'gns3'
    	t = paramiko.Transport((srv, 22))
    	t.connect(username=user,password=passwd)
    	sftp = paramiko.SFTPClient.from_transport(t)
    	if options.debug:
            with sftp.open(cfg_file, 'r+') as fh:
            	new_cfg = fh.read().splitlines()[:-1]
            	new_cfg.extend(config)
            	print('\n'.join(new_cfg))
    	else:
            with sftp.open(cfg_file, 'w+') as fh:
                fh.write('\n'.join(config))

    else:
        with open(cfg_file, 'r+') as fh:
            new_cfg = fh.read().splitlines()[:-1]
            new_cfg.extend(config)
            if options.debug:
                print('\n'.join(new_cfg))
            else:
                fh.seek(0)
                fh.write('\n'.join(new_cfg))
                fh.truncate()

#END OF CREATE AND WRITE FUNCTION

#MAIN FUNCTION
if __name__ == '__main__':

    options = parse()

    #BASE PREFIX AND DATA
    base_v4 = 'ip address {ipv4_base}.{{0}}.{{1}} 255.255.255.0'
    idn_v4 = 'ip address {0}.{0}.{0}.{1} 255.255.255.0'
    base_v6 = 'ipv6 address {ipv6_base}:{{0}}::{{1}}/64'
    lo0_v4 = 'ip address {0}.{0}.{0}.{0} 255.255.255.255'
    lo0_v6 = 'ipv6 address 2001::{0}/128'
    line_cfg = 'line con 0 \n exec-timeout 0 0 \n privilege level 15 \n logging sync'
    
    
    

    if options.vm:
        TOPO_FILE = options.topology_file
        data = json.load(open(TOPO_FILE))
        project_id = data['project_id']
        BASE_DIR = os.path.join(options.base_dir, project_id)
        srv = options.srv
    else:
        BASE_DIR = options.base_dir
        TOPO_FILE = os.path.join(BASE_DIR, options.topology_file)
        data = json.load(open(TOPO_FILE))

    CFG_DIR = os.path.join(BASE_DIR, options.project_files)
    IPV4_BASE = options.ipv4_base.strip('.')
    IPV6_BASE = options.ipv6_base.strip(':')
    base_v4 = base_v4.format(ipv4_base=IPV4_BASE)
    base_v6 = base_v6.format(ipv6_base=IPV6_BASE)
    
    

    nodes = [dict(node_id   = node['id'],
                  vm_id     = node['vm_id'],
                  node_name = node['label']['text'],
                  config    = node['properties']['startup_config'],
                  ports     = [{'port_id' : port['id'],
                                'link_id' : port['link_id'],
                                'name'    : port['name']}
                                for port in node['ports'] if 'link_id' in port])
                                    for node in data['topology']['nodes']]

    links = {link['id'] : (link['source_node_id'], link['destination_node_id'])
                 for link in data['topology']['links']}

    for node in nodes:
        configure_nodes(node)

    '''if options.debug:
        print(json.dumps(nodes, indent=4))
        print(json.dumps(links, indent=4))'''
