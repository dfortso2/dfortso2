#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 10:00:35 2021

@author: katherinedelgado and Erin Barnhart
"""
import csv
import numpy

def read_csv_file(filename, header=True):
	data = []
	with open(filename, newline='') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for row in csvreader:
			data.append(row)
	if header==True:
		out_header = data[0]
		out = data[1:]
		return out, out_header
	else:
		return out

def write_csv(data,header,filename):
	with open(filename, "w") as f:
		writer= csv.writer(f)
		writer.writerow(header)
		for row in data:
			writer.writerow(row)

