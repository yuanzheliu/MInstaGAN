import argparse
import numpy as np
import scipy.io as sio
from pathlib import Path
from tqdm import tqdm
from PIL import Image


def main():
	parser = create_argument_parser()
	args = parser.parse_args()
	generate_ccp_dataset(args)

def create_argument_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('--data_root', type=str, default='datasets/clothing-co-parsing')
	parser.add_argument('--save_root', type=str, default='datasets/jeans2skirt_ccp')
	# change cat 1_1 to cat 1_2
	parser.add_argument('--cat11', type=str, default='jeans', help='category 11')
	parser.add_argument('--cat12', type=str, default='skirt', help='category 12')
	# change cat 2_1 to cat 2_2
	parser.add_argument('--cat21', type=str, default='coat', help='category 21')
	parser.add_argument('--cat22', type=str, default='blouse', help='category 22')
	# add more labeled data
	parser.add_argument('--cat11_', type=str, default='pants', help='category 11_')
	parser.add_argument('--cat12_', type=str, default='skirt', help='category 12_')

	parser.add_argument('--cat21_', type=str, default='jacket', help='category 21_')
	parser.add_argument('--cat22_', type=str, default='shirt', help='category 22_')
	return parser

def generate_ccp_dataset(args):
	"""Generate COCO dataset (train/val, A/B)"""
	args.data_root = Path(args.data_root)
	args.img_root = args.data_root / 'photos'
	args.pix_ann_root = args.data_root / 'annotations' / 'pixel-level'
	args.img_ann_root = args.data_root / 'annotations' / 'image-level'
	args.pix_ann_ids = get_ann_ids(args.pix_ann_root)
	args.img_ann_ids = get_ann_ids(args.img_ann_root)

	args.label_list = sio.loadmat(str(args.data_root / 'label_list.mat'))['label_list'].squeeze()

	args.save_root = Path(args.save_root)
	args.save_root.mkdir()

	generate_ccp_dataset_train(args, 'A', args.cat11, args.cat21, args.cat11_, args.cat21_)
	generate_ccp_dataset_train(args, 'B', args.cat12, args.cat22, args.cat12_, args.cat22_)
	generate_ccp_dataset_val(args, 'A', args.cat11, args.cat21, args.cat11_, args.cat21_)
	generate_ccp_dataset_val(args, 'B', args.cat12, args.cat22, args.cat12_, args.cat22_)

def generate_ccp_dataset_train(args, imset, cat1, cat2):
	img_path = args.save_root / 'train{}'.format(imset)
	seg_path = args.save_root / 'train{}_seg'.format(imset)
	img_path.mkdir()
	seg_path.mkdir()

	cat_id_1 = get_cat_id(args.label_list, cat1)
	cat_id_2 = get_cat_id(args.label_list, cat2)

	pb = tqdm(total=len(args.pix_ann_ids))
	pb.set_description('train{}'.format(imset))
	for ann_id in args.pix_ann_ids:
		ann = sio.loadmat(str(args.pix_ann_root / '{}.mat'.format(ann_id)))['groundtruth']
		if np.isin(ann, cat_id_1).sum() > 0:
			if np.isin(ann, cat_id_2).sum() > 0:
				img = Image.open(args.img_root / '{}.jpg'.format(ann_id))
				img.save(img_path / '{}.png'.format(ann_id))
				seg = (ann == cat_id_1 or ann == cat_id_2).astype('uint8')  # get segment of given category
				seg = Image.fromarray(seg * 255)
				seg.save(seg_path / '{}_0.png'.format(ann_id))
		pb.update(1)
	pb.close()

def generate_ccp_dataset_val(args, imset, cat1,cat2):
	img_path = args.save_root / 'val{}'.format(imset)
	seg_path = args.save_root / 'val{}_seg'.format(imset)
	img_path.mkdir()
	seg_path.mkdir()

	cat_id_1 = get_cat_id(args.label_list, cat1)
	cat_id_2 = get_cat_id(args.label_list, cat2)

	pb = tqdm(total=len(args.img_ann_ids))
	pb.set_description('val{}'.format(imset))
	for ann_id in args.img_ann_ids:
		ann = sio.loadmat(str(args.img_ann_root / '{}.mat'.format(ann_id)))['tags']
		if np.isin(ann, cat_id_1).sum() > 0:
			if np.isin(ann, cat_id_2).sum() > 0:
				img = Image.open(args.img_root / '{}.jpg'.format(ann_id))
				img.save(img_path / '{}.png'.format(ann_id))
		pb.update(1)
	pb.close()

def get_ann_ids(anno_path):
	ids = list()
	for p in anno_path.iterdir():
		ids.append(p.name.split('.')[0])
	return ids

def get_cat_id(label_list, cat):
	for i in range(len(label_list)):
		if cat == label_list[i][0]:
			return i

if __name__ == '__main__':
	main()