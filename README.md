# DUT (Dataset Unification Tool)

## Overview:

DUT is a tool for unifying sets of dirty genomic data and metadata. DUT has two modules: DUT.DataReader; which sterilizes new datasets, and DUT.DataExplorer; which allows the user to explore sterilzed datasets as pandas dataframes.

## Dependencies:

* Python 3.6 or above
* numpy for python
* pandas for python
* mygene for python (optional)

## Quickstart

1. Install DUT using pip

```bash
pip3 install -i https://test.pypi.org/simple/ DUT==0.1
```

2. In your working directory, save the "DataSets" example directory from https://github.com/scottlieb/DataUnificationTool. (Alternativeley, create your own directory and config file and save them both into your working directory. If no config file exists, DUT will automatically read datasets from the DataSets folder in your current directory.)

3. Create a new python file. Copy the following code:

```python
import pandas as pd
import numpy as np

import DUT.DataReader as DR
import DUT.DataExplorer as DE

#this will create new sterilized datasets in the dataset directory
DR.sterilize_datasets() 

#create DataExplorer object
explorer = DR.DataExplorer(DATA_SET_DEFAULT_DIR)

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

print(meta_df)
print(mrna_df)
```

4. Run the code. The output will be two pandas dataframes. The first is metadata for all patients that match restrictions. The second is mRNA expression for all patients in the metadata and all the genes in the gene pool.

## Configuring the DUT

DUT will look for datasets in the "DataSets" directory in the defined path. By default, the path is defined to be the working directory In addition, DUT will create sterilized metadata with the fields "age", "sex" and "response". To change either the path to datasets, or the fields to be created, create a new file called "config.json" in the working directory. The file should be edited as follows:
> ###### config.json
```json
{
	"WORKING_DIR": "/path/to/working/directory",
	"FIELDS": [
		"any",
		"field",
		"you",
		"wish"
	]
}
```

Datasets within the "DataSet" directory should be laid out in the following format:
```
DataSets  
│
└───dataset_1
│   │   md_config.json
│   │   mrna.csv
|	|	metadata.csv
│   
└───dataset_2
│   │   md_config.json
│   │   mrna.csv
|	|	metadata.csv
etc...
```
Please refer to the example datasets. The file 'md_config.json' is DATASET SPECIFIC. This means each dataset requires its own unique config file. The file defines a set of fields to read. For each field, HEADER defines how the field is named in this specific dataset, MAP defines which mapping function to use to map the field, and DATA passes arguments to the mapping function, if necessary.    
  
As as example, the following 'md_config.json' file defines that DUT should only read the field 'Sex'. In this dataset, age is called "gender of patient". The file defines to map this field using the 'STR_MAP' function where "male" maps to "M" and "female" maps to "F".
> ###### md_config.json
```
{ 
	"sex": {
		"HEADER": "",
		"MAP": "STR_MAP",
		"DATA": {
			"male":"M",
			"female":"F",
			"":"NA"
		}
	}
}
```
**Note: in this case, "sex" must also be defined as a field in the 'config.json' file, otherwise it will be ignored.*

**For more information on mapping functions such as 'STR_MAP', see the official DUT documentation.**

## Using the DataReader

The DataReader, which reads and sterilizes data, can be implemented using a single function on the following way:
```python
import DUT.DataReader as DR
DR.sterilize_datasets(PATH_TO_DATASETS = PATH_TO_DATASETS, datasets = DATASETS, force = False)
```
#### Arguments:
- **PATH_TO_DATASETS:** *Default: Working directory defined in config.* Defines a path to 'DataSets' directory from which to read.
- **datasets:** *Default: All datasets in defined directory.* List of datasets to sterilize.
- **force:** *Default: Flase.* If true, will sterilize all defined datasets, even if they have already been sterilized. This is useful after adjusting configurations.

## Unresolved Issues
- [] Genes are currently only identifiable by entrez id. We would like to add functionality for identification by symbol.
- [] DataReader.log should be more informative. For instance, it should log duplicate genes or unreadable files or datatypes.
- [] A functionality to autogenrate md_config files for each dataset should be added.
- [] MyGene currently dumps info to stdout. This should be avoided (quick fix).




