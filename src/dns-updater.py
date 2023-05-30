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

def update_dns_records(domain, subdomains, current_ip):
  # Update DNS records for the given domain and subdomains
  try:
    records = domain.get_records()
    for record in records:
      # Only update A records
      if record.type == 'A':
        # Check record is in subdomains list
        if record.name in subdomains:
          if record.data != current_ip:
            record.data = current_ip
            record.save()
            logger.info("IP changed to %s for %s", current_ip, record.name)
          else:
            logger.info("IP not changed for %s", record.name)
  except Exception as e:
    logger.error("DNS UPDATE ERROR: %s". str(e))


def main():
  # DigitalOcean TOKEN
  TOKEN = "TOKEN"

  # Get domain from DO
  domain = digitalocean.Domain(token=TOKEN, name="DOMAIN")

  # Subdomains list
  subdomains = ['@', 'subdomain1', 'subdomain2']

  # Get current IP
  current_ip = get_current_ip()

  # Changing to current IP
  update_dns_records(domain, subdomains, current_ip)

  quit()

if __name__ == "__main__":
  main()