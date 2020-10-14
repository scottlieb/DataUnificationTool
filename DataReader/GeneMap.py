import numpy as np
import pandas as pd
import mygene

def get_gene_map(genes):
	mg = mygene.MyGeneInfo()
	res = mg.querymany(genes, scopes='symbol', fields='entrezgene', species='human', as_dataframe = True)
	res = res['entrezgene']
	gene_map = res.to_dict()
	return gene_map