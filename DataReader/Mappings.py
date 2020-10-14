import numpy as np
import pandas as pd

###******** User-Made Maps ********###
###********************************###

# All maps should be functions which take a DataFrame and args dictionary
# as input. All maps should output a single pandas column, matching in length 
# to the columns of the input DataFrame. 

# Template:

# This template an be wrapped in a function to make a custom map. See ID (below)
# as an example of how to create an identity map named "ID".

def __TEMPLATE(dataframe, args, map_func):

	HEADER = args["HEADER"]

	#return none if no col
	rowcount = len(dataframe.index)
	if HEADER not in dataframe.columns:
		res = [pd.NA for _ in range(rowcount)]
		return pd.DataFrame(data=res)

	#apply map to col and return
	array = dataframe[HEADER].apply(map_func)
	return array

# Maps:

def ID(dataframe, args):

	#returns column with no changes

	identity = lambda x: x

	return __TEMPLATE(dataframe, args, map_func=identity)




###******** Built-In Maps ********###
###*******************************###

def NUM(dataframe, args):

	HEADER = args["HEADER"]

	def map(x):
		try:
			return float(str(x).replace(",","."))
		except ValueError:
			return pd.NA
	
	#return none if no col
	rowcount = len(dataframe.index)
	if HEADER not in dataframe.columns:
		res = [pd.NA for _ in range(rowcount)]
		return pd.DataFrame(data=res)

	#apply map to col and return
	array = dataframe[HEADER].apply(map)
	return array

def STR_MAP(dataframe, args):
	
	HEADER = args["HEADER"]

	def map(x):
		try:
			res = args["DATA"][x]
			if res == 'NA':
				return pd.NA
			return str(res)
		except:
			return pd.NA

	#return none if no col
	rowcount = len(dataframe.index)
	if HEADER not in dataframe.columns:
		res = [pd.NA for _ in range(rowcount)]
		return pd.DataFrame(data=res)

	#return col as array
	array = dataframe[HEADER].map(map)
	return array

def NAN(dataframe, args):
	rowcount = len(dataframe.index)
	res = [pd.NA for _ in range(rowcount)]
	return pd.DataFrame(data=res)

