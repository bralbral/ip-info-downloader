import os
import zipfile
import ipaddress
from typing import Optional
import csv
import netaddr as netaddr
import numpy as np
import pandas as pd
from multiprocessing import Pool


def ip_int_to_str(ip: int) -> str:
    return str(ipaddress.ip_address(ip))


def ip_str_to_int(ip: str) -> int:
    return int(ipaddress.ip_address(ip))


def ip_int_range_to_cidr(ip_low, ip_high) -> Optional[str]:
    cidr = None
    try:
        # convert to str
        ip_low_s = ip_int_to_str(ip_low)
        # convert to str
        ip_high_s = ip_int_to_str(ip_high)

        # netaddr.iprange_to_cidrs(ip_low_s, ip_high_s) -> returns list of cidr
        cidrs = [
            ipaddress.ip_network(cidr)
            for cidr in netaddr.iprange_to_cidrs(ip_low_s, ip_high_s)
        ]
        # collapse into one
        cidr = next(ipaddress.collapse_addresses(cidrs))
    finally:
        return cidr


def preprocess(task: dict):
    filename = task["filename"]
    header = task["header"]

    base_dir = os.path.dirname(filename)

    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)

    if os.path.exists(filename):

        with zipfile.ZipFile(filename, "r") as f:
            for name in f.namelist():
                if name.lower().endswith(".csv"):
                    with f.open(name) as zd:
                        df = pd.read_csv(
                            zd,
                            encoding="latin1",
                            sep=",",
                            header=None,
                            index_col=False,
                            names=header,
                        )

                        if "cidr" not in header:
                            df["cidr"] = np.vectorize(ip_int_range_to_cidr)(
                                df["ip_low"], df["ip_high"]
                            )

                        # change order of columns
                        new_order = ["cidr"]
                        new_order.extend(
                            [col for col in list(df.columns.values) if col != "cidr"]
                        )
                        df = df[new_order]

                        df.to_csv(
                            path_or_buf=os.path.join(base_dir, f"converted_{name}.zip"),
                            index=None,
                            header=True,
                            sep=",",
                            doublequote=True,
                            quotechar='"',
                            escapechar="\\",
                            compression="zip",
                            quoting=csv.QUOTE_ALL,
                        )


if __name__ == "__main__":

    tasks = [
        {
            "filename": "./temp/DB11LITECSV.zip",
            "header": [
                "ip_low",
                "ip_high",
                "country_code",
                "country_name",
                "region_name",
                "city_name",
                "latitude",
                "longitude",
                "zip_code",
                "time_zone",
            ],
        },
        {
            "filename": "./temp/DBASNLITE.zip",
            "header": [
                "ip_low",
                "ip_high",
                "cidr",
                "autonomous_system_number",
                "autonomous_system",
            ],
        },
        {
            "filename": "./temp/PX11LITECSV.zip",
            "header": [
                "ip_low",
                "ip_high",
                "proxy_type",
                "country_code",
                "country_name",
                "region_name",
                "internet_service_provider",
                "domain",
                "usage_type",
                "autonomous_system_number",
                "autonomous_system",
                "last_seen",
                "security_threat",
                "provider",
            ],
        },
    ]

    with Pool(3) as p:
        p.map(preprocess, tasks)
