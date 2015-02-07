#!/usr/bin/python

import helper

"""
This class is node class which contains the node in decision tree.
"""
class Node:
	"""
	Constructor
	
	Keyword arguments:
	dictionary_attribute_keys -- is the attributes list for the input data.
	found_attribute --  is the attributes list used so far for run.
	parent_property -- is the catalog from the parent.
	list_of_dna_strands_in_node  -- is the list of samples to separate.
	classification_key -- is the attribute name used for concept definition.
	confidence_interval -- is the p-value for testing.
	"""
	def __init__(self, attribute_list, found_attribute, parent_property, current_list, concept_string, compare_value, isMisclassification):
		self.attribute_list = attribute_list
		self.found_attribute = found_attribute
		self.current_list = current_list
		self.child_list = {}
		self.parent_property = parent_property
		self.concept_string = concept_string
		self.parent_entropy = helper.get_set_entropy(current_list, concept_string)
		self.pre_attribute = ""
		self.cal_gain = 0
		self.cat_list_final = {}
		self.positive = 0
		self.negative = 0
		self.compare_value = compare_value
		self.isMisclassification = isMisclassification
	
	"""
	This method is used to calculate which attribute to choose.
	
	return true if there is an attribute for run, otherwise, return false.
	"""
	def calculate_new_attribute_fromEntropy(self):
		temp_list = list(set(self.attribute_list) - set(self.found_attribute))
		temp_list.remove(self.concept_string)

		if len(temp_list) == 0:
			return False;

		for attr in temp_list:
			ini_gain = self.parent_entropy
			cat_list = {}

			for item in self.current_list:
				if item.get_value(attr) in cat_list.keys():
					cat_list[item.get_value(attr)].append(item)
				else:
					cat_list[item.get_value(attr)] = [item]
			
			for sublist in cat_list.values():
				ini_gain -= (len(sublist)/len(self.current_list) * helper.get_set_entropy(sublist, self.concept_string))
			
			if helper.cal_chi_square(cat_list.values(), self.concept_string, self.compare_value) and ini_gain > self.cal_gain:
				self.cal_gain = ini_gain 
				self.pre_attribute = attr
				self.cat_list_final = cat_list
		
		return True
	
	"""
	This method is called to calculate new attribute from misclassification rate
	"""
	def cal_new_attribute_fromMis(self):
		temp_list = list(set(self.attribute_list) - set(self.found_attribute))
		temp_list.remove(self.concept_string)
		low_misclassificationrate = 1.0
		
		if len(temp_list) == 0:
			return False;
		
		for attr in temp_list:
			cal_result = 1.0
			
			cat_list = {}

			for item in self.current_list:
				if item.get_value(attr) in cat_list.keys():
					cat_list[item.get_value(attr)].append(item)
				else:
					cat_list[item.get_value(attr)] = [item]
			
			cal_result = helper.cal_error(self.concept_string, cat_list.values())
			
			if helper.cal_chi_square(cat_list.values(), self.concept_string, self.compare_value) and cal_result < low_misclassificationrate: 
				self.pre_attribute = attr
				self.cat_list_final = cat_list
		
		return True
	
	
	"""
	This method is used to prepare children nodes for calculation.
	"""
	def preChildren(self):
		for key in self.cat_list_final.keys():
			new_attribute_list = list(self.found_attribute)
			new_attribute_list.append(self.pre_attribute)
			self.child_list[key] = Node(self.attribute_list, new_attribute_list, key, self.cat_list_final[key], self.concept_string, self.compare_value, self.isMisclassification)

	"""
	This method is called to calculate all children nodes.
	"""
	def runChildren(self):
		for child in self.child_list.values():
			child.run_build_tree()

	"""
	This method is called to calculate this node.
	"""
	def run(self):
		#check if the sample is pure, if it is pure, just end it
		result = helper.calculate_stat(self.current_list, self.concept_string)
# 		print self.found_attribute
		self.positive = result["positive"]
		self.negative = result["negative"]
		
		if helper.isPure(self.current_list, self.concept_string):
			return
		
		if int(self.isMisclassification) is 1:
			if self.cal_new_attribute_fromMis() == False:
				return
		else:
			if self.calculate_new_attribute_fromEntropy() == False:
				return
		
		self.preChildren()

		self.runChildren()
