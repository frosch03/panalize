# -*- coding: utf-8 -*-
"""Panalize - a simple script to draw infection data into diagrams

Filename   : panalize.py
Author     : Matthias Brettschneider
Date       : 2020-04

Details    : Read the data from the CSSE dataset of the Johns Hopkins
             University. The dataset is distributed via git [1].

             [1] https://github.com/CSSEGISandData/COVID-19.git
"""

DATASET = "/home/frosch03/Programming/DataSets/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"  # noqa
US_DATASET = "/home/frosch03/Programming/DataSets/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"  # noqa

from IDS import IDS

world = IDS(DATASET)
de = world['Germany']
fr = world['France']
fr.setRegions(['France'])
es = world['Spain']
it = world['Italy']
cn = world['China']
cn.setRegions(['Hubei'])

us = IDS(US_DATASET, data_offset=11, pos_country=6, pos_region=5)
ny = us['New York']
ny.setRegions(['New York'])
