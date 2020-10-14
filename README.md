<<<<<<< HEAD:README
tutuDUT (Dataset Unification Tool)
=======
# DUT (Dataset Unification Tool)
>>>>>>> README:README.md

## Overview:

DUT is a tool for unifying sets of dirty genomic data and metadata. DUT has two major components: DataReader; which sterilizes new datasets, and DataExplorer; which allows the user to explore sterilzed datasets as pandas dataframes.

## Dependencies:

Python 3.x
numpy for python
pandas	for python
mygene for python (optional)

## Setup:
Each Dataset should be saved as a directory at the apropriate path. The path to all datasets can be changed in the config.json file in the DataReader directory. In each directory genomic and meta data should be saved in csv format as mrna.csv and patients.csv respectivley (see example for correct format). Along with these files a file named md_config.json should be saved in each dataset directory. DataReader uses the md_config file to parse each dataset. A detailed explanation of md_config can be found below.
Along with this, a list of all fields the DataReader should parse should be defined in the config.json file in the DataReader directory.
In the given example, a selection of datasets are saved in the approprite format, each with its own md_config file. The fields defined for parsing are "age", "sex", and "response". To sterilize all the datasets, run DataReader.py. An in-depth explanation of DataReader will be given below.

## DataReader:
The DataReader reads and sterilizes datasets. As mentioned above, the path to datasets and fields to sterilize can be set via the config.json file. After steralizing genomic and meta data, DataReader will save them alongside the origional data in csv format under the names UD_mrna and UD_metadata. DataReader should be run from the command line as a python3 file and takes the following optional arguments:
--force, -f: Force reader to sterlize datasets even if they have already been sterilized.
--datasets, -d: specify a list of datasets to sterilize, if argument is not passed, all datasets will be sterilized.

## DataExplorer:
After data has been sterilized, it can be explored via the data explorer. In short, one can create a DataExplorer object, which can then be used to filter through data by common parameters and retirve data as a pandas dataframe for further processing. An encompassing example exists in the DataExplorer.py file.
DataExplorer is very fast, and therefore should be used to filter down data to a manageable size for further processing downstream.

## md_config:
The md_config (metadata configuration) file in each dataset allows easy controll over the normalization of data per dataset per field. The file is in dictionary format where the keys are fields defined in the general config.json file. If a field appears in a md_config file but is not defined in the general config file, it will be ignored.

## The keys for each field is also a dictionary in the following format:
	HEADER -> [name of feild in dataset]
	MAP -> [name of function used to map feild*]
	DATA -> [optional data to pass to MAP function]
	
	*more information below

More keys can be added as needed, but every feild MUST contain a HEADER and MAP key. See given examples.

# # Mapping Functions:
Mapping function are lambda-like function used to normalize data in datasets. Often these will be simple maps such as "Male" -> M or "Female" -> F but often these functions will need to be more complex to accuratley normalize data. DataReader allows for the creation of such functions with minimal coding.
The mapping functions STR_MAP and NUM are given. NUM reads numeric input in several format and STR_MAP does simple string mapping as in "Male" -> M. The mapping to use is defined in DATA (see above and examples).
To write a custom mapping function, one must write their own in the Mappings.py python file in DataReader. A Template exists to write functions in a lambda-style format. See Mappings.py for a detailed example.


 




