import textwrap
import Adafruit_DHT
import argparse
import configparser
from influxdb_client import InfluxDBClient
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Pushes a Dir to a remote Host via SCP',
        prog='ProgramName',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
                 sudo python3 ./main.py -m [11|22|2302] -p <GPIO pin number>
                 sudo python3 ./main.py -m 2302 -p 4 - Read from an AM2302 connected to GPIO pin #4
                 '''))

    parser.add_argument('-m', type=str, default='2302', help='module')
    parser.add_argument('-p', type=int, default=2, help='GPIO Data Pin')
    parser.add_argument('-c', type=str, default='./config.ini', help='Config File')
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.c)

    sensor = ""
    match args.m:
        case '11':
            sensor = Adafruit_DHT.DHT11
        case '22':
            sensor = Adafruit_DHT.DHT22
        case '2302':
            sensor = Adafruit_DHT.AM2302

    humidity, temperature = Adafruit_DHT.read_retry(sensor, args.p)

    client = InfluxDBClient(
                        url=f"http://{config['INFLUXDB']['ip']}:{config['INFLUXDB']['port']}",
                        token=config['INFLUXDB']['token'],
                        org=config['INFLUXDB']['org'])

    write_api = client.write_api()
    write_api.write(config['INFLUXDB']['bucket'],
                config['INFLUXDB']['org'],
                [f"{config['INFLUXDB']['measurement']},location=sleep temperature={temperature},humidity={humidity}"])
    write_api.flush()
    write_api.close()
