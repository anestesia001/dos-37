#!/usr/bin/env python3
"""
Ansible Dynamic Inventory для Yandex Cloud Compute.

Требования:
- yc CLI установлен и авторизован
- Python 3.8+
- Переменная окружения YC_FOLDER_ID

Использование:
  ./yc_inventory.py --list
  ./yc_inventory.py --host <vm-name>
  ansible-inventory -i ./yc_inventory.py --graph
  ansible-playbook -i ./yc_inventory.py playbook.yml

Переменные окружения:
  YC_FOLDER_ID        ID каталога Yandex Cloud. Обязательно.
  YC_USE_PUBLIC_IP    1/true — использовать публичный IP, если он есть.
  YC_ONLY_RUNNING     1/true — включать только VM со статусом RUNNING.
"""

import argparse
import json
import os
import subprocess
import sys


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    sys.exit(1)


def run_yc(args: list[str]) -> dict | list:
    command = ["yc", "compute", "instance", "list", "--format", "json"] + args

    try:
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        fail(
            "Yandex Cloud CLI не найден. "
            "Установите yc и выполните 'yc init'."
        )
    except subprocess.CalledProcessError as exc:
        fail(f"Ошибка выполнения yc:\n{exc.stderr}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        fail(f"Не удалось разобрать JSON от yc: {exc}")


def get_instances(folder_id: str) -> list[dict]:
    args = [
        "--folder-id", folder_id,
        "--limit", "1000",
    ]

    only_running = os.getenv("YC_ONLY_RUNNING", "0").lower() in {
        "1", "true", "yes"
    }

    if only_running:
        args += ["--filter", "status=RUNNING"]

    response = run_yc(args)

    if isinstance(response, list):
        return response

    return response.get("instances", [])


def get_ip(instance: dict) -> str | None:
    interfaces = instance.get("network_interfaces") or []

    use_public = os.getenv("YC_USE_PUBLIC_IP", "0").lower() in {
        "1", "true", "yes"
    }

    for interface in interfaces:
        v4 = interface.get("primary_v4_address") or {}
        private_ip = v4.get("address")
        public_ip = (v4.get("one_to_one_nat") or {}).get("address")

        if use_public and public_ip:
            return public_ip

        if private_ip:
            return private_ip

        if public_ip:
            return public_ip

    return None


def safe_group_name(value: str) -> str:
    return "".join(
        character if character.isalnum() else "_"
        for character in value
    ).lower()


def add_host_to_group(inventory: dict, group: str, host: str) -> None:
    inventory.setdefault(group, {"hosts": []})
    inventory[group].setdefault("hosts", [])

    if host not in inventory[group]["hosts"]:
        inventory[group]["hosts"].append(host)


def build_inventory(instances: list[dict]) -> dict:
    inventory = {
        "_meta": {
            "hostvars": {},
        },
        "all": {
            "children": [],
        },
    }

    for instance in instances:
        name = instance.get("name") or instance.get("id")
        ip = get_ip(instance)
        fqdn = instance.get("fqdn")

        print(
            f"DEBUG: name={name} "
            f"status={instance.get('status')} "
            f"ip={ip} "
            f"fqdn={fqdn}",
            file=sys.stderr,
        )

        if not name:
            continue

        ansible_host = ip or fqdn

        if not ansible_host:
            print(
                f"WARNING: {name}: не найден ни IP, ни FQDN; хост пропущен",
                file=sys.stderr,
            )
            continue

        add_host_to_group(inventory, "ungrouped", name)

        zone_id = instance.get("zone_id")
        if zone_id:
            add_host_to_group(inventory, zone_id, name)

        status = instance.get("status")
        if status:
            add_host_to_group(
                inventory,
                f"status_{safe_group_name(status)}",
                name,
            )

        labels = instance.get("labels") or {}

        for label_key, label_value in labels.items():
            group = (
                f"{safe_group_name(label_key)}"
                f"_{safe_group_name(str(label_value))}"
            )
            add_host_to_group(inventory, group, name)

        inventory["_meta"]["hostvars"][name] = {
            "ansible_host": ansible_host,
            "yc_id": instance.get("id"),
            "yc_name": instance.get("name"),
            "yc_fqdn": fqdn,
            "yc_status": status,
            "yc_zone_id": zone_id,
            "yc_folder_id": instance.get("folder_id"),
            "yc_labels": labels,
            "yc_private_ip": get_private_ip(instance),
            "yc_public_ip": get_public_ip(instance),
        }

    inventory["all"]["children"] = sorted(
        set(inventory.keys()) - {"_meta", "all"}
    )

    return inventory


def get_private_ip(instance: dict) -> str | None:
    for interface in instance.get("network_interfaces") or []:
        v4 = interface.get("primary_v4_address") or {}

        if v4.get("address"):
            return v4["address"]

    return None


def get_public_ip(instance: dict) -> str | None:
    for interface in instance.get("network_interfaces") or []:
        v4 = interface.get("primary_v4_address") or {}
        public_ip = (v4.get("one_to_one_nat") or {}).get("address")

        if public_ip:
            return public_ip

    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Yandex Cloud dynamic inventory for Ansible"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Вывести полный inventory в формате JSON",
    )
    parser.add_argument(
        "--host",
        help="Вывести переменные для одного хоста",
    )
    args = parser.parse_args()

    folder_id = os.getenv("YC_FOLDER_ID")

    if not folder_id:
        fail("Укажите переменную окружения YC_FOLDER_ID.")

    if args.host:
        for instance in get_instances(folder_id):
            current_name = instance.get("name") or instance.get("id")

            if current_name == args.host:
                ip = get_ip(instance)
                print(
                    json.dumps(
                        {"ansible_host": ip} if ip else {}
                    )
                )
                return

        print(json.dumps({}))
        return

    if not args.list:
        parser.print_help()
        sys.exit(1)

    instances = get_instances(folder_id)

    print(
        f"DEBUG: получено инстансов: {len(instances)}",
        file=sys.stderr,
    )

    print(
        json.dumps(
            build_inventory(instances),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
