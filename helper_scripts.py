import os
import glob
import shutil

base_path = '...\indian_traffic_detection_dataset\IDD_Detection'
folders = os.listdir(base_path)

def count_files(final_path):
	count = 0
	for dir_path,dir_names,file_name in os.walk(final_path):
		count = count + len(file_name)
	return count

for folder in folders:
	if not folder.split('.'):
		final_path = os.path.join(base_path,folder)
		total_count = count_files(final_path)
		print(f' {folder} : {total_count} files')




#checking for unique files
files = glob.glob(base_path+'/*.txt')

train_set = set()
val_set = set()
test_set = set()

sets = [train_set,val_set,test_set]

for i,file in enumerate(files):
    fl = open(file,'r')
    contents = fl.readlines()
    for line in contents:
        folder,sub_folder,file_name = line.split('/')
        sets[i].add(folder)
        sets[i].add(sub_folder)
        sets[i].add(file_name)
    fl.close()

'''
>>> len(train_list),len(val_list),len(test_list)
(4955, 3450, 1509)

'''


#to move files ending without "_r"

t_path = r""
dest_test = r""

for o,p in enumerate(t_path):
	dirs = [d for d in os.listdir(p)]
	n = len(dirs)
	for i in range(n):
		fp = os.path.join(p,dirs[i])
		sub_dirs = [sd for sd in os.listdir(fp)]
		n_sd = len(sub_dirs)
		for b in range(n_sd):
			fip = os.path.join(fp,sub_dirs[b])
			general_files = glob.glob(os.path.join(fip,fmt[o]))
			extension_file_names = [name.split("\\")[-1] for name in general_files]
			for m in range(len(general_files)):
				if (extension_file_names[m].split(".")[0] in required_files):
					shutil.copy(general_files[m],dest_test)
				else:
					continue