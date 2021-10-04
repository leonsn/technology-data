#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to convert the transport data assumptions of the Fraunhofer ISE Study
"Wege zu einem klimaneutralen Energiesystem" (see pdf in folder docu) into a
.csv format.
"""
import pandas as pd
import numpy as np
import camelot

#import pdb; pdb.set_trace()

## Read PDF and parse tables
tables = camelot.read_pdf(snakemake.input.fraunhofer, pages="9-12")
#tables = camelot.read_pdf("docu/Anhang-Studie-Wege-zu-einem-klimaneutralen-Energiesystem.pdf", pages="9-12")

df = pd.concat([tables[0].df, tables[1].df, tables[2].df[1:], tables[3].df])

## Forward fill values.
df.replace(r'', np.NaN, inplace=True)
df.ffill(inplace=True)

## Replace line breaks
df.replace(to_replace=r'( \n|\n |\n)', value=' ', regex=True, inplace=True)
df.replace('\u20ac/PKW', 'EUR/car', inplace=True)
df.replace('\u20ac/LKW', 'EUR/truck', inplace=True)

## Rename columns
df.columns = df.iloc[0]
df = df[1:]
## Set index
df.set_index(df.columns[0:3].tolist(), inplace=True)

## Save output
df.to_csv(snakemake.output.costs, encoding='iso-8859-15')
#df.to_csv("inputs/Fraunhofer_ISE_transport_costs.csv", encoding='iso-8859-15')

