#!/usr/bin/python3
import digitalocean
import requests
import logging
import os

# Logging configurations
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'dyndns.log')

logging.basicConfig(filename=filename, format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_current_ip():
  # Get the current IP address
  try:
    response = requests.get('https://api.my-ip.io/ip.json')
    # Raise exception if request not successful
    response.raise_for_status()
    data = response.json()
    return data['ip']
  except requests.exceptions.RequestException as e:
    logger.error("REQUEST ERROR: %s", str(e))
  except Exception as e:
    logger.error("ERROR RETRIEVING IP: %s". str(e))

def update_dns_records(domain, hostname, current_ip):
  # Update DNS records for the given domain and subdomains
  try:
    records = domain.get_records()
  except Exception as e:
    logger.error("ERROR RETRIEVING RECORDS: {}".format(str(e)))

  for record in records:
    # Only update A records
    if record.type == 'A' and record.name == hostname:
      if record.data != current_ip:
        previousData = record.data
        try:
          record.data = current_ip
          record.save()
          logger.info("IP changed from {} to {}".format(previousData, current_ip))
        except Exception as e:
          logger.error("ERROR CHANGING IP: {}".format(str(e)))
      else:
        logger.info("IP not changed")
      break

if __name__ == "__main__":
  # DigitalOcean TOKEN
  TOKEN = "DigitalOcean Token"
  # Get domain from DO
  domain = digitalocean.Domain(token=TOKEN, name="example.com")
  # Hostname to change IP
  hostname = "@"
  # Get current IP
  current_ip = get_current_ip()
  # Update DNS records
  update_dns_records(domain, hostname, current_ip)
  quit()