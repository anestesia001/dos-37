#!/usr/bin/env python3
import argparse
import secrets
import socket
import string
from pathlib import Path

ENV_FILE = Path(".env")
DB_USER = "appuser"
START_PORT = 8000
END_PORT = 9000

def read_env():
  env = {}
  if ENV_FILE.exists():
    with open(ENV_FILE, "r", encoding="utf-8") as file:
      for line in file:
        line = line.strip()
        if not line or line.startswith("#"):
          continue
        if "=" in line:
          key, value = line.split("=", 1)
          env[key] = value
  return env

def find_free_port():
  for port in range(START_PORT, END_PORT + 1):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
      try:
        sock.bind(("0.0.0.0", port))
        return port
      except OSError:
        continue
  raise RuntimeError("Not found free port")

def gen_db_pass(length=12):
  symbols = string.ascii_letters + string.digits
  return "".join(secrets.choice(symbols) for _ in range(length))

def write_env(env):
  with open(ENV_FILE, "w", encoding="utf-8") as file:
    for key, value in env.items():
      file.write(f"{key}={value}\n")

def main():
  parser = argparse.ArgumentParser(description="Gen env python script")
  parser.add_argument(
    "--app-img",
    required=True,
    help="docker image for app"
  )
  parser.add_argument(
    "--db-host",
    required=True,
    help="database host for app"
  )

  args = parser.parse_args()
  env = read_env()

  if "APP_PORT" not in env:
    env["APP_PORT"] = str(find_free_port())

  if "DB_PASS" not in env:
    env["DB_PASS"] = gen_db_pass(24)

  env["APP_IMG"] = args.app_img
  env["DB_HOST"] = args.db_host
  env["DB_USER"] = DB_USER

  write_env(env)

if __name__ == "__main__":
  main()
