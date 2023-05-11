import netmiko
import textfsm
from pprint import pprint
from tabulate import tabulate
from time import sleep, time
import csv
import sqlite3
from sqlalchemy import create_engine, text
from concurrent.futures import ThreadPoolExecutor


def main():
    devices = [
    {
        "ip": "192.168.1.15",
        "device_type": "huawei",
        "username": "lahcen",
        "password": "@Azerty2024"
    },
    {
        "ip": "192.168.1.16",
        "device_type": "huawei",
        "username": "lahcen",
        "password": "@Azerty2024"
    }
    ]

    interface_list = list()

    def get_interfaces(device):
        

       
        try:
            print(f'|------ connecting to {device["ip"]}', end='')
            connection = netmiko.ConnectHandler(**device)

            output = connection.send_command(
                "display interface", use_textfsm=True, textfsm_template="inetr_info.textfsm")
            hostname = connection.base_prompt
            for host in output:
                host["hostname"] = hostname
                if host['description'] == "":
                    host['description'] = "--"
                if host['ip'] == "":
                    host['ip'] = "--"
                if host['mac'] == "":
                    host['mac'] = "--"
                    
            for interface in output:
                interface_list.append(interface)
            

            connection.disconnect()
            print("\tDone.\n")
        except netmiko.exceptions.NetmikoAuthenticationException:
            print("\tFailed.\n")
        except netmiko.exceptions.NetmikoTimeoutException:
            print("\tFailed.\n")
        except netmiko.exceptions.ReadTimeout:
            print("\tFailed.\n")
        except ConnectionResetError:
            print("\tFailed.\n")
        except TimeoutError:
            print("\tFailed.\n")
        except OSError:
            print("\tFailed.\n")


    #-------------------- threading ---------------
    time_start = time()
    
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(get_interfaces, devices)

    # counte time it taks to finish the task
    totale_time = time() - time_start
    print(f'|------ total time : {totale_time} sec\n')
    #----------------------------------------------

    if interface_list != []:
        with open("report_interface.csv", "w", newline='') as report:
            report.write(
                f"Hostname,InterfaceName,Description,IP,MAC,InterfaceState,ProtocolState,LinkQuality,InputRate,OutputRate\n")
            for interface in interface_list:
                report.write(f'{interface["hostname"]},{interface["interfacename"]},{interface["description"]},{interface["ip"]},{interface["mac"]},{interface["interfacestate"]},{interface["protocolstate"]},{interface["linkquality"]},{interface["inputrate"]},{interface["outputrate"]}\n')

    # -------------SQLAlchemy----------------------------
    database_path = "sqlite:///interface_hw.db"
    engine = create_engine(database_path)
    connection = engine.connect()

    sql_query = text("DELETE FROM list_interface")
    if interface_list != []:
        connection.execute(sql_query)
        connection.commit()

    # insert data to database
    if interface_list != []:
        sql_insert = text('INSERT INTO list_interface ("Hostname","InterfaceName","Description","IP","MAC","InterfaceState","ProtocolState","LinkQuality","InputRate","OutputRate") VALUES (:hostname, :interfacename, :description, :ip, :mac, :interfacestate, :protocolstate, :linkquality, :inputrate, :outputrate)')
        connection.execute(sql_insert, interface_list)
        connection.commit()


if __name__ == "__main__":
    try:
        while True:
            main()
            for remaining in range(15, 0, -1):
                print(
                    f"\r  Refresh: {remaining:3d} seconds remaining.", end="\r")
                sleep(1)
    except KeyboardInterrupt:
        print("\n\nExiting host-monitor")
        exit()
