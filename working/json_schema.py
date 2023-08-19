#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import geopandas as gpd

if __name__ == "__main__":

    # ABS LGA layer
    lga = gpd.read_file(
        "data/LGA_2021_AUST_GDA2020_SHP/LGA_2021_AUST_GDA2020.shp"
    ).drop("geometry", axis=1)
    lga["LGA"] = lga.LGA_NAME21.apply(lambda x: x.upper())

    # manual fixes for the LGA names in the heritage centroids file
    concordance = {
        "ALBURY CITY": "ALBURY",
        "BAYSIDE": "BAYSIDE (NSW)",
        "CAMPBELLTOWN": "CAMPBELLTOWN (NSW)",
        "CENTRAL COAST": "CENTRAL COAST (NSW)",
        "CITY OF PARRAMATTA": "PARRAMATTA",
        "LEICHARDT": "INNER WEST",
        "LITHGOW CITY": "LITHGOW",
        "Queanbeyan-Palerang Regional": "QUEANBEYAN-PALERANG REGIONAL",
        "UPPER HUNTER": "UPPER HUNTER SHIRE",
        "WARRUMBUNGLE": "WARRUMBUNGLE SHIRE",
    }

    def update_lga(row):
        if row in concordance.keys():
            return concordance[row]
        else:
            return row

    # SHR centroids file
    heritage_centroids = gpd.read_file(
        "data/heritage_stateheritageregistercentroids/SHR_CENTROIDS.shp"
    )
    heritage_centroids.geometry = heritage_centroids.geometry.to_crs(
        "epsg:4326"
    )

    # Fix errors in LGA names in the SHR centroids file
    heritage_centroids["LGA_updated"] = heritage_centroids["LGA"].apply(
        update_lga
    )

    # Generate the lat long field
    heritage_centroids["longitude"] = heritage_centroids.geometry.x
    heritage_centroids["latitude"] = heritage_centroids.geometry.y
    heritage_centroids["lat_long"] = heritage_centroids.apply(
        lambda df: [df.latitude, df.longitude], axis=1
    )

    # Filtering out rows in the LGA column of the heritage centroids that are not an LGA
    heritage_centroids_filtered = heritage_centroids[
        heritage_centroids.LGA_updated.isin(lga.LGA.tolist())
    ]

    # Prepare file for export
    heritage_centroids_export = heritage_centroids_filtered[
        ["HOITEMID", "ITEMNAME", "ADDRESS", "LGA_updated", "lat_long"]
    ].rename(columns={"LGA_updated": "LGA_NAME21"})

    heritage_centroids_export.to_csv(
        "working/shr_centroids_lat_long.csv", index=False
    )
