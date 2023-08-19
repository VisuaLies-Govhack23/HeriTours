#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import geopandas as gpd
import pandas as pd
import numpy as np
import os


def update_lga(row):
    if row in concordance.keys():
        return concordance[row]
    else:
        return row


if __name__ == "__main__":

    lga = gpd.read_file(
        "data/LGA_2021_AUST_GDA2020_SHP/LGA_2021_AUST_GDA2020.shp"
    ).drop("geometry", axis=1)

    lga["LGA"] = lga.LGA_NAME21.apply(lambda x: x.upper())

    # manual fixes for the LGA names in the historic heritage sites file
    concordance = {
        "CENTRAL COAST": "CENTRAL COAST (NSW)",
        "GREATER HUME": "GREATER HUME SHIRE",
        "NAMBUCCA": "NAMBUCCA VALLEY",
        "SUTHERLAND": "SUTHERLAND SHIRE",
        "THE HILLS": "THE HILLS SHIRE",
        "UPPER HUNTER": "UPPER HUNTER SHIRE",
        "WARRUMBUNGLE": "WARRUMBUNGLE SHIRE",
        "UPPER LACHLAN": "UPPER LACHLAN SHIRE",
    }

    heritage_sites = gpd.read_file(
        "data/heritage_historicheritagesites/Heritage_HistoricHeritageSites/HistoricHeritageSites.shp"
    ).drop("geometry", axis=1)

    # Filtering out rows in the LGA column of the heritage centroids that are not an LGA

    heritage_sites["LGA_updated"] = heritage_sites["LGA_ID"].apply(update_lga)

    heritage_sites_not_null = heritage_sites[
        (heritage_sites.LGA_updated.isin(lga.LGA.tolist()))
    ].rename(columns={"LGA_updated": "LGA_NAME21"})

    heritage_sites_group = (
        heritage_sites_not_null.groupby(["LGA_NAME21", "ITEM_STATU"])
        .OBJECT_ID.count()
        .reset_index()
        .rename(columns={"OBJECT_ID": "count"})
    )

    heritage_sites_group.to_csv("working/heritage_data.csv", index=False)
