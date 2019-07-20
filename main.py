import base64
import json
import argparse
from urllib.request import urlopen

def getSubscription(url):
  req = urlopen(url)
  return req.read().decode('utf-8')

def decodeSubscription(code):
  encoded = code + "=" * ((8 - len(code) % 8) % 8)
  decoded = base64.b64decode(encoded)
  ssr_link_lines = decoded.decode('utf-8').splitlines()
  ssr_links = []
  for link in ssr_link_lines:
    ssr_links.append(link)
  # print(ssr_links)
  if len(ssr_links) == 0:
    print('Error: no links found!')
    exit(1)
  return ssr_links


def decodeSSRLink(link):
  if (link.find('ssr://') == -1):
    print('Error: link format error, expected "ssr://..."! ')
    exit(2)
  code = link[6:]
  code = code.replace('-', '+')
  encoded = code.replace('_', '/')
  encoded += "=" * ((4 - len(encoded) % 4) % 4)
  decoded = base64.b64decode(encoded).decode('utf-8')
  info = decoded.split(':')
  package = {}
  package['server'] = info[0].strip()
  package['port'] = info[1]
  package['protocal'] = info[2]
  package['method'] = info[3]
  package['obfs'] = info[4]
  password_b64 = info[5][:info[5].find('/?')]
  suffix = info[5][info[5].find('/?')+2:]
  package['password'] = base64.b64decode(password_b64).decode('utf-8')
  s = suffix.split('&')
  suffix = {}
  for item in s:
    suffix[item[:item.find('=')]] = item[item.find('=')+1:]
  for k in suffix.keys():
    if len(suffix[k]) == 0:
      continue
    else:
      suffix[k] = suffix[k].replace('-', '+')
      suffix[k] = suffix[k].replace('_', '/')
      suffix[k] = suffix[k] + "=" * ((4 - len(suffix[k]) % 4) % 4)
      suffix[k] = base64.b64decode(suffix[k]).decode('utf-8')
  package['suffix'] = suffix
  # print(package)
  return package

def generateConfig(package):
  obj = {}
  obj['server'] = package['server']
  obj['local_address'] = '0.0.0.0'
  obj['local_port'] = 12334
  obj['timeout'] = 300
  obj['workers'] = 1
  obj['server_port'] = int(package['port'])
  obj['password'] = package['password']
  obj['method'] = package['method']
  obj['plugin'] = 'obfs-local --obfs http'
  obj['suffix'] = {
    'remarks': package['suffix']['remarks'],
    'group': package['suffix']['group']
  }
  return obj
  # json.dump(obj, indent=4, ensure_ascii=False)

def parseArgument():
  parser = argparse.ArgumentParser(description='Auto sync configurations from SSR subscription.')
  parser.add_argument('--dist', type=str, help='Dist path of configurations.')
  parser.add_argument('--url', type=str, help='Subscription url.')
  return parser
  
def main():
  args = parseArgument().parse_args()
  dist = args.dist
  if dist[-1] != '/':
    dist += '/'
  url = args.url
  code = getSubscription(url)
  ssr_links = decodeSubscription(code)
  t = 1
  for link in ssr_links:
    link_package = decodeSSRLink(link)
    config_package = generateConfig(link_package)
    with open('{}{}.json'.format(dist, t), 'w') as f:
      json.dump(config_package, f, indent=4, ensure_ascii=False)
    t += 1

main()