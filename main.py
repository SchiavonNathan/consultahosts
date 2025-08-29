#Created by Nathan Schiavon-2025
import os
from pyzabbix import ZabbixAPI, ZabbixAPIException
from dotenv import load_dotenv
import json

load_dotenv()

ZABBIX_SERVER = os.getenv("ZABBIX_SERVER")
ZABBIX_USER = os.getenv("ZABBIX_USER")
ZABBIX_PASSWORD = os.getenv("ZABBIX_PASSWORD")

def get_zabbix_stats(as_json=False):
    if not all([ZABBIX_SERVER, ZABBIX_USER, ZABBIX_PASSWORD]):
        print("Erro: As variáveis de ambiente ZABBIX_SERVER, ZABBIX_USER, e ZABBIX_PASSWORD não foram definidas.")
        print("Certifique-se de que o arquivo .env está correto e na mesma pasta do script.")
        return

    try:
        zapi = ZabbixAPI(ZABBIX_SERVER)
        zapi.session.verify = False
        zapi.login(ZABBIX_USER, ZABBIX_PASSWORD)

        total_hosts = zapi.host.get(countOutput=True)
        online_hosts = zapi.host.get(filter={'available': 1}, countOutput=True)
        offline_hosts = zapi.host.get(filter={'available': 2}, countOutput=True)

        detailed_group_stats = {}
        host_groups = zapi.hostgroup.get(output=['groupid', 'name'])

        for group in host_groups:
            group_id = group['groupid']
            group_name = group['name']

            online_in_group = zapi.host.get(
                groupids=[group_id],
                filter={'available': 1},
                countOutput=True
            )

            offline_in_group = zapi.host.get(
                groupids=[group_id],
                filter={'available': 2},
                countOutput=True
            )

            total_in_group = int(online_in_group) + int(offline_in_group)
            if total_in_group > 0:
                detailed_group_stats[group_name] = {
                    'online': int(online_in_group),
                    'offline': int(offline_in_group),
                    'total': total_in_group
                }

        if as_json:
            stats_dict = {
                "total_hosts": total_hosts,
                "online_hosts": online_hosts,
                "offline_hosts": offline_hosts,
                "groups": detailed_group_stats
            }
            print(json.dumps(stats_dict, ensure_ascii=False, indent=4))
        else:
            print("--- Estatísticas Gerais ---")
            print(f"Total de Hosts Cadastrados: {total_hosts}")
            print(f"Hosts Online (Disponíveis): {online_hosts}")
            print(f"Hosts Offline (Indisponíveis): {offline_hosts}")
            print("\n--- Detalhes por Grupo ---")

            for group_name in sorted(detailed_group_stats.keys()):
                stats = detailed_group_stats[group_name]
                print(f"- {group_name} (Total: {stats['total']})")
                print(f"  Online:  {stats['online']}")
                print(f"  Offline: {stats['offline']}")

    except ZabbixAPIException as e:
        print(f"Erro ao conectar ou consultar a API do Zabbix: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        if 'zapi' in locals() and zapi.user.loggedin:
            zapi.user.logout()

if __name__ == "__main__":
    # Para exibir em JSON, passe as_json=True
    get_zabbix_stats(as_json=False)