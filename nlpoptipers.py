import os, sys
import subprocess

import numpy as np
import umap

sys.path.insert(0, os.path.abspath('.'))
import utils

def convert_and_save(dataset, save_path, n_components=3, dataset_name=None):
    """
    Convert dataset using UMAP and save it
    """
    # initialize umap
    fit = umap.UMAP(n_components=n_components)
    # embedding of dataset to R^n_components
    embedding_ = fit.fit_transform(dataset)
    # add a zero column to embedding (the radius to be used with optiperslp)
    embedding = np.zeros((embedding_.shape[0], embedding_.shape[1]+1))
    embedding[:,:-1] = embedding_
    embedding = np.around(embedding, 3)
    # save dataset. if not specified it saves in the current folder
    # if save_path was not created
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    if dataset_name == None:
        np.savetxt(os.path.join(save_path, 'embedded_dataset.txt'), embedding,
                delimiter=',', fmt='%.3f')
    else:
        np.savetxt(os.path.join(save_path, dataset_name + '.txt'), embedding,
                delimiter=',', fmt='%.3f')
    return embedding

def call_optiperslp(dimension_pd='1', save_path='.', dataset_name=None, output_path='.'):
    """
    Call optiperslp to calculate the persistence diagrams
    """
    # check dataset_name
    if dataset_name == None:
        dataset_name = 'embedded_dataset.txt'
    # path to dataset used in optiperslp
    path_to_dataset = os.path.join(save_path, dataset_name)
    # define output path for optiperslp. Where the files will be saved. Use dataset_name to create
    # folder
    if dataset_name == 'embedded_dataset.txt':
        output_path = os.path.join(output_path, dataset_name[:-4])
    else:
        output_path = os.path.join(output_path, dataset_name)
    # create folder if it does not exit
    print(output_path)
    if not os.path.isdir(output_path):
        os.makedirs(output_path)
    # call optiperslp in python
    bash_command = 'bash nlpoptipers.sh ' + output_path + ' ' + dimension_pd + ' ' +\
                    dataset_name[:-4] + ' ' + path_to_dataset
    process = subprocess.run(bash_command.split())

def most_important_points(embedded_dataset, output_path, dimension_pd='1',
                          dataset_name = None, n_points=5):
    """
    Return the indices of the n_points most important points in cycles in the embedded dataset
    """
    # check if .txt is in name
    if dataset_name == None:
        dataset_name = 'embedded_dataset'
    else:
        if '.txt' in dataset_name:
            dataset_name = dataset_name[:-4]
    # path to gen file with cycles
    gen_file = os.path.join(output_path, 'gen_' + dataset_name + '_' + dimension_pd + '.txt')
    # path to i2p file
    i2p_file = os.path.join(output_path, 'gen_' + dataset_name + '_i2p.txt')
    # get pd_points and their indexed cycles
    pd_points, idx_vertices = utils.file_to_index(gen_file)
    # iterate over pd points to get the non negative points
    for counter, pd_p in enumerate(pd_points):
        if pd_p[0] >= 0:
            break
    pd_points = np.array(pd_points[counter:])
    idx_vertices = idx_vertices[counter:]
    bp_points = pd_points; bp_points[:,1] -= bp_points[:,0]
    # get the top n_points points with most persistence
    # check if there is enough points to select
    if bp_points.shape[0] >= n_points:
        idx_ = np.argpartition(bp_points[:,1], -n_points)[-n_points:]
    else:
        print('There are not enough points in the persistence diagram to be selected')
    # now we can get n_points lists for each index in idx_
    top_idx_vertices = [idx_vertices[i] for i in idx_]
    embedded_indices = []
    for list_vertices in top_idx_vertices:
        idx_embedded = utils.find_true_index(embedded_dataset, list_vertices, i2p_file)
        embedded_indices.append(idx_embedded)
    return embedded_indices

def run_nlpoptipers(dataset, save_path = '.', output_path = '.', dimension_pd = '1',
                    dataset_name = None, n_points = 5, n_components = 3):
    """
    Wrap all 3 functiosn above.
    """
    embedded_dataset = convert_and_save(dataset, save_path, n_components=n_components,
                        dataset_name=dataset_name)
    call_optiperslp(dimension_pd = dimension_pd, save_path = save_path,
                    dataset_name = dataset_name, output_path = output_path)
    if dataset_name == None:
        output_path = os.path.join(output_path, 'embedded_dataset')
    else:
        output_path = os.path.join(output_path, dataset_name)
    embedded_indices = most_important_points(embedded_dataset,
                output_path, dimension_pd = dimension_pd,
                dataset_name = dataset_name, n_points = n_points)
    return embedded_indices, embedded_dataset
