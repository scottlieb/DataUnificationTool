"""
   Copyright 2020 Pangea

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0
"""

import os, json
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
import mygene

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


config = json.load(open("../config.json"))

DATA_SET_DEFAULT_DIR = config["WORKING_DIR"] + "/DataSets/"

class PatientPool:
	def __init__(self, root_dir, datasets):
		self.root_dir = root_dir
		self.datasets = datasets
		self.patients_set = self.get_all_patients()

	def update_datasets(self, datasets):
		
		self.datasets = datasets
		return


	def get_all_patients(self):

		def get_patients_for_file(dataset):
			try:
				df = pd.read_csv(self.root_dir + dataset + "/UD_metadata.csv", index_col=0)
			except:
				return set()
			return set(df.index)

		patients = set()

		with ThreadPoolExecutor() as executor:
			res = executor.map(get_patients_for_file, self.datasets)

			for s in res:
				patients |= s

			return patients

	def restrict_by_sex(self, sex='M'):

		def restrict_for_file(dataset):
			try:
				df = pd.read_csv(self.root_dir + dataset + "/UD_metadata.csv", index_col=0, header=0)
			except:
				return set()
			df = df[df['sex']==sex]
			df = df[df['sex'].notnull()]
			res = df.index
			return set(res)

		patients = set()

		with ThreadPoolExecutor() as executor:
			res = executor.map(restrict_for_file, self.datasets)

			for s in res:
				patients |= s

			self.patients_set &= patients


	def restrict_by_age(self, min_age = 0, max_age = 120):
		
		def restrict_for_file(dataset):
			try:
				df = pd.read_csv(self.root_dir + dataset + "/UD_metadata.csv", index_col=0, header=0)
			except:
				return set()
			df = df[df['age']>=min_age]
			df = df[df['age']<=max_age]
			res = df.index
			return set(res)

		patients = set()

		with ThreadPoolExecutor() as executor:
			res = executor.map(restrict_for_file, self.datasets)

			for s in res:
				patients |= s

			self.patients_set &= patients

class GenePool:
	def __init__(self, root_dir, datasets):
		self.root_dir = root_dir
		self.datasets = datasets
		self.gene_set = set()
		self.mg = mygene.MyGeneInfo()

	def restrict_by_symbols(self, symbol_list):

		query_res = self.mg.querymany(symbol_list, scopes='symbol', fields='entrezgene', species='human')
		for res in query_res:
			try:
				self.gene_set.add(res['entrezgene'])
			except KeyError:
				print(res['query'] + " not found.")

	def restrict_by_ids(self, id_list):

		for entrezid in id_list:
			self.gene_set.add(entrezid)

	def reset_gene_pool(self):

		self.gene_set = set()

class DataPool:

	def __init__(self, root_dir, datasets):
		self.root_dir = root_dir
		self.datasets = self.__define_datasets(datasets)
		self.PatientPool = PatientPool(root_dir, datasets)
		self.GenePool = GenePool(root_dir, datasets)

	def __define_datasets(self, datasets):
		res = []
		for dataset in datasets:
			if dataset in os.listdir(self.root_dir):
				res.append(dataset)
		return sorted(res)

	def remove_datasets(self, datasets):
		for dataset in datasets:
			try:
				self.datasets.remove(dataset)
			except:
				continue
		self.PatientPool.update_datasets(self.datasets)
		self.PatientPool.get_all_patients()

	def get_genes_set(self):
		return self.GenePool.gene_set

	def get_pateint_set(self):
		return self.PatientPool.patients_set

	def get_gene_set(self):
		return self.GenePool.gene_set

	def get_datasets(self):
		if self.datasets:
			return self.datasets
		return []

class DataExplorer:

	def __init__(self, root_dir = DATA_SET_DEFAULT_DIR):
		self.root_dir = root_dir
		self.all_datasets = self.get_all_datasets()

	def get_all_datasets(self):
		return [dataset for dataset in os.listdir(self.root_dir)]

	def create_data_pool(self, datasets):
		return DataPool(self.root_dir, datasets)

	def get_metadata(self, DataPool):
		
		patient_set = DataPool.get_pateint_set()
		datasets = [self.root_dir + dataset + "/UD_metadata.csv"\
		 for dataset in DataPool.get_datasets()]

		def __read_metadata_csv(filename):

			try:
				df = pd.read_csv(filename,  header=0,  index_col=0)
			except:
				df = pd.DataFrame()
			return df[df.index.isin(patient_set)]

		with ThreadPoolExecutor() as executor:
			dfs = executor.map(__read_metadata_csv, datasets)
			res	= pd.DataFrame()
			
			for df in dfs:
				res = pd.concat([res, df], axis = 0)

			return res

	def get_mrna(self, DataPool):

		gene_set = DataPool.get_gene_set()
		patient_set = DataPool.get_pateint_set()
		datasets = [self.root_dir + dataset + "/UD_mrna.csv"\
		 for dataset in DataPool.get_datasets()]

		def __read_mrna_csv(filename):
			try:
				df = pd.read_csv(filename,  header=0,  index_col=0)
			except:
				df = pd.DataFrame()
			if gene_set:
				df = df[df.index.isin(gene_set)]
				df = df.loc[:, df.columns.isin(patient_set)]
			return df

		with ThreadPoolExecutor(max_workers = 30) as executor:
			dfs = executor.map(__read_mrna_csv, datasets)
			res	= next(dfs)

			for df in dfs:
				res = pd.merge(
					res,
					df, 
					left_index = True,
					right_index = True,
					how ='outer',
					)

			return res



if __name__ == '__main__':

	#Example:


	#create DataExplorer object
	explorer = DataExplorer(DATA_SET_DEFAULT_DIR)

	#get all datasets from default directory
	all_datasets = explorer.all_datasets

	#create a datapool of all datasets
	datapool = explorer.create_data_pool(all_datasets)

	#remove dataset from pool
	datapool.remove_datasets(['GSE1378'])

	#restrict sex of patients
	datapool.PatientPool.restrict_by_sex(sex = 'F')

	#restrict age of patients
	datapool.PatientPool.restrict_by_age(max_age = 42)

	#restrict genes by symbol
	datapool.GenePool.restrict_by_symbols(['AADAT', 'WERT', 'FAT1'])

	#restrict by entrez id
	datapool.GenePool.restrict_by_ids(['15'])
	
	#get mrna and metadata as pandas dataframes
	mrna_df = explorer.get_mrna(datapool)
	meta_df = explorer.get_metadata(datapool)

	print(mrna_df)
	print(meta_df)