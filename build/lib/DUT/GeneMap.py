"""
   Copyright 2020 Pangea

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0
"""

import numpy as np
import pandas as pd
import mygene

def get_gene_map(genes):
	mg = mygene.MyGeneInfo()
	res = mg.querymany(genes, scopes='symbol', fields='entrezgene', species='human', as_dataframe = True)
	res = res['entrezgene']
	gene_map = res.to_dict()
	return gene_map