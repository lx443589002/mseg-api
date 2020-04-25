#!/usr/bin/python3

import pdb
from typing import Any, List, Mapping
from mseg.utils.json_utils import read_json_file
from mseg.utils.names_utils import get_dataloader_id_to_classname_map

"""
Interface for semantic labels of COCO Panoptic dataset
"""

class COCOSemanticAPI:

	def __init__(self, coco_dataroot: str) -> None:
		"""
			Args:
			-	coco_dataroot: path to unzipped COCO Panoptic directory

			Returns:
			-	None
		"""
		self.annotations_root = f'{coco_dataroot}/annotations'
		self.fname_to_annot_map_splitdict = {}
		self.categoryid_to_classname_map = get_dataloader_id_to_classname_map(
			dataset_name='coco-panoptic-201'
		)

		for split in ['train', 'val']:
			fname_to_annot_map = self.get_semantic_annotations(split)
			self.fname_to_annot_map_splitdict[split] = fname_to_annot_map


	def get_semantic_annotations(self, split: str):
		""" Get COCO Panoptic semantic annotations from .json file

			Args:
			-	split: string representing training, validation, or testing split of the data

			Returns:
			-	filename_to_annot_map: dictionary mapping (filename)->(json annotation).
		"""
		json_data = read_json_file(f'{self.annotations_root}/panoptic_{split}2017.json')
		# map (filename) -> (json annotation)
		fname_to_annot_map = { annot['file_name']: annot for annot in json_data['annotations'] }
		return fname_to_annot_map


	def get_img_annotation(self, split: str, fname_stem: str) -> Mapping[str,Any]:
		"""
			Args:
			-	split: string representing training, validation, or testing split of the data
			-	fname_stem: 

			Returns:
			-	img_annot: Python dictionary with information about image's annotation
		"""
		img_annot = self.fname_to_annot_map_splitdict[split][fname_stem + '.png']
		return img_annot


	def get_present_classes_in_img(self, split: str, fname_stem: str) -> List[str]:
		"""
			Args:
			-	split: string representing training, validation, or testing split of the data
			-	fname_stem:

			Returns:
			-	list of strings, representing classnames
		"""
		annot = self.get_img_annotation(split, fname_stem)
		classes_present = []
		for segment in annot['segments_info']:
			categoryid = segment['category_id']
			classname = self.categoryid_to_classname_map[categoryid]
			classes_present += [classname]
		return classes_present

