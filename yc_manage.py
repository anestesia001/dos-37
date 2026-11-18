#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import requests

API_URL = "https://compute.api.cloud.yandex.net/compute/v1"
TIMEOUT = 15

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s | %(levelname)s | %(message)s",
  handlers=[
    logging.FileHandler("yc_vm.log"),
    logging.StreamHandler(sys.stdout)
  ]
)

def api_request(method, endpoint, token, **kwargs):
  url = f"{API_URL}/{endpoint}"

  headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
  }

  try:
    response = requests.request(
      method,
      url,
      headers=headers,
      timeout=TIMEOUT,
      **kwargs
    )

    response.raise_for_status()
    return response.json()
  except requests.exceptions.HTTPError as err:
    logging.error(err.response.status_code, err.response.text)
  except requests.exceptions.Timeout as err:
    logging.error(err)

  return None

def list_vms(token, folder_id):
  logging.info("Get vms list")

  vms = []
  page_token = None

  while True:
    params = {
      "folderId": folder_id,
      "pageSize": 100
    }
    if page_token:
      params["pageToken"] = page_token

    data = api_request(
      "GET",
      "instances",
      token,
      params=params
    )

    #print(data)

    if data is None:
      return None
    vms.extend(data.get("instances", []))
    page_token = data.get("nextPageToken")
    if not page_token:
      break
  #print(vms[0].get('name'))
  return vms

def find_vm(token, folder_id, name):
  vms = list_vms(token, folder_id)

  if vms is None:
    return None

  matches = []
  for vm in vms:
    if vm.get("name") == name:
      matches.append(vm)

  if not matches:
    logging.error(f"VM {name} not found")
    return None

  return matches[0]

def start_vm(token, folder_id, name):
  vm = find_vm(token, folder_id, name)
  if vm is None:
    return False
  vm_id = vm["id"]
  status = vm["status"]

  if status == "RUNNING":
    logging.warning(f"VM {name} already running")
    return True

  if status != "STOPPED":
    logging.error(f"Unable to start {name}")
    return False

  logging.info(f"Starting {name}")

  response = api_request(
    "POST",
    f"instances/{vm_id}:start",
    token,
    json={}
  )

  if response is None:
    return False

  return True

def stop_vm(token, folder_id, name):
  vm = find_vm(token, folder_id, name)
  if vm is None:
    return False
  vm_id = vm["id"]
  status = vm["status"]

  if status == "STOPPED":
    logging.warning(f"VM {name} already stopped")
    return True

  if status != "RUNNING":
    logging.error(f"Unable to stop {name}")
    return False

  logging.info(f"Stopping {name}")

  response = api_request(
    "POST",
    f"instances/{vm_id}:stop",
    token,
    json={}
  )

  if response is None:
    return False

  return True

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "action",
    choices=["list", "stop", "start"]
  )
  parser.add_argument(
    "--name"
  )
  args = parser.parse_args()
  token = os.getenv("YC_TOKEN")
  folder_id = os.getenv("FOLDER_ID")

  if not token or not folder_id:
    logging.error("YC_TOKEN or FOLDER_ID is not set")
    return 1

  if args.action in ("start", "stop") and not args.name:
    parser.error("Need vm name (--name)")

  if args.action == "list":
    vms = list_vms(token, folder_id)
    #print(vms)

    if vms is None:
      return 1

    for vm in vms:
      #print(f"{vm.get('name')}")
      print(f"{vm.get('name')}\t{vm.get('status')}")
    return 0

  if args.action == "start":
    result = start_vm(token, folder_id, args.name)
  else:
    result = stop_vm(token, folder_id, args.name)

  if result:
    return 0
  return 1

if __name__ == "__main__":
  sys.exit(main())
