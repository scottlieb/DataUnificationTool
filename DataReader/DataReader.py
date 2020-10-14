import os, sys, csv, json, argparse
import numpy as np
import pandas as pd
import mygene

import logging
logging.basicConfig(
	filename='DataReader.log',
	level=logging.DEBUG, 
	format='%(asctime)s %(message)s'
	)


import Mappings
import GeneMap

from concurrent.futures import ThreadPoolExecutor

config = json.load(open("config.json"))

PATH_TO_DATASETS = config["PATH_TO_DATASETS"]
FIELDS = config["FIELDS"]
METADATA_CONFIG = "/md_config.json"
metadata_name = "/patients.csv"
mrna_name = "/mrna.csv"

def make_sterile_metadata(path, dataset, write_all):

	#check if new csv needs to be written
	if write_all == False and os.path.isfile(path + dataset + "/UD_metadata.csv"):
		return

	#load config json
	try:
		md_config=json.load(open(path + dataset + METADATA_CONFIG))
	except FileNotFoundError:
		logging.warning("No md_config file found for %s. Continuing...", dataset)
		return

	#read patients.csv
	patients_df = pd.read_csv(
		path + dataset + metadata_name, 
		dtype = object, 
		header = 0, 
		index_col = 0
		)

	#Change pateint ids to dataset#id format
	def map(id):
		return dataset + '#' + id

	patients_df.index = patients_df.index.map(map)

	#Get column names (fields)
	columns = FIELDS

	#make empty DataFrame
	metadata = pd.DataFrame(columns = columns, index = patients_df.index)

	#create columns from config file using Mappings
	for field in columns:
		#if field is not defined in md_config, return NaN column:
		if field not in md_config:
			nan_func = getattr(Mappings, 'NAN')
			metadata[field] = nan_func(patients_df, args = None)
		#if feild is defined, apply map defined in md_config:
		else:
			args = md_config[field]
			map_name = args['MAP']
			map_func = getattr(Mappings, map_name)
			metadata[field] = map_func(patients_df, args)

	#write to ".csv"
	csv_path = path + dataset + "/UD_metadata.csv"
	metadata.to_csv(path_or_buf = csv_path)

def make_sterile_mrna(path, dataset, write_all):

	#check if new csv needs to be written
	if write_all == False and os.path.isfile(path + dataset + "/UD_mrna.csv"):
		return

	#read mrna data into dataframe
	try:
		mrna_df = pd.read_csv(
		path + dataset + mrna_name, 
		header = 0, 
		index_col = 0
		)
	except:
		logging.warning("No mrna file found for %s. Continuing...", dataset)
		return
		
	#Change pateint ids to dataset#id format
	def map(id):
		return dataset + '#' + id

	mrna_df.columns = mrna_df.columns.map(map)

	#get genes list
	genes = list(mrna_df.index)

	#get gene-->entrez_id using mygene
	gene_map = GeneMap.get_gene_map(genes)

	#map gene symbols to entrez_id
	mrna_df.index = mrna_df.index.map(gene_map)

	#remove duplicates (keep only first) and Nan rows, sort dataset
	mrna_df = mrna_df[~mrna_df.index.duplicated(keep='first')]
	mrna_df = mrna_df[mrna_df.index.notnull()]
	mrna_df.sort_index(axis = 'index', inplace = True, kind = 'quicksort')

	#write .csv file
	csv_path = path + dataset + "/UD_mrna.csv"
	mrna_df.to_csv(path_or_buf = csv_path)

def sterilize_datasets(PATH_TO_DATASETS, datasets, write_all = False):

	logging.info("Sterilizing...\nPath to datasets: %s", PATH_TO_DATASETS)

	with ThreadPoolExecutor(max_workers = 50) as executor:
		for dataset in datasets:
			executor.submit(make_sterile_metadata,PATH_TO_DATASETS, dataset, write_all)
			executor.submit(make_sterile_mrna,PATH_TO_DATASETS, dataset, write_all)

	logging.info("*"*10+"DONE"+"*"*10)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-f",
		"--force", 
		help="Force reader to sterlize datasets even if they have already been sterilized.",
		action="store_true"
		)
	parser.add_argument(
		"--datasets",
		"-d",
		help="Specify which datasets to sterilize.",
		action = "store",
		nargs = "*")

	args = parser.parse_args()

	write_all = False
	if args.force:
		write_all = True

	datasets = []

	if args.datasets == None:
		datasets = [dataset_dir for dataset_dir in os.listdir(PATH_TO_DATASETS)]
	else:
		datasets = args.datasets

	sterilize_datasets(PATH_TO_DATASETS, datasets, write_all = write_all)