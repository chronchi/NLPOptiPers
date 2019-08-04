import numpy as np

def file_to_index(gen_file):
    """
    Return the coordinates (uniquely) from a cycle given a
    persistence diagram
    """
    # open the file
    f = open(gen_file)
    # split into lines
    lines = f.read().splitlines()
    # list for pd points (tuples)
    pd_points = []
    # list for index of vertices (unique list)
    idx_vertices = []
    for counter, line in enumerate(lines):
        # get the pd line
        if ';' in line:
            elements_line = line.split()
            # append the pd points
            pd_points.append([np.float(bd) for bd in elements_line[1:]])
            # tmp vector to append idx
            tmp_idx = []
            # iterate over the subsequent lines to get the idx
            for sublines in lines[counter+1:]:
                # if it finds another ';', break
                if ';' in sublines:
                    break
                else:
                    # split the subline and get only the string numbers (including coefficient)
                    splitted_subline = [x.split()[0] for x in sublines.split(',')]
                    # get only the index of vertices
                    idx = [np.int(x) for x in splitted_subline[1:]]
                    tmp_idx.extend(idx)
        # transform the list in unique vertices
        tmp_idx = np.unique(tmp_idx)
        # append to the original list of index vertices
        idx_vertices.append(tmp_idx)
    # return the index of coordinates
    return pd_points, idx_vertices


def idx_to_coord(i2p_file, idx_vertices):
    """
    Convert the coord list from file_to_index to a list of 3d coordinates
    """
    # load index two point file
    i2p_data = np.loadtxt(i2p_file)
    # convert the first column to integer
    indices_i2p = [int(elem) for elem in i2p_data[:,0]]
    # initialize empty list to add the respective coordinates
    coordinates_ = []
    for elem in idx_vertices:
        # find the index in indices_i2p for elem
        position_index = indices_i2p.index(elem)
        # append the coordinate
        coordinates_.append(i2p_data[position_index,1:])
    # return numpy array
    coordinates_ = np.array(coordinates_)
    return coordinates_

def find_true_index(embedded_dataset, idx_vertice, i2p_file):
    """
    Find the index in the original embedded dataset of each point in the cycle for the respective
    persistence diagram point.

    idx_vertices is just a sublist of idx_vertice. embedded_dataset is the embedded dataset
    given by UMAP.
    """
    coordinates = idx_to_coord(i2p_file, idx_vertice)
    # empty list to append the coordinate indices in the embedded dataset
    idx_embedded = []
    for coord in coordinates:
        coord = [i for i in coord]
        # find the index where coord is in the embedded dataset
        index_coord = np.where((coord[:-1] == embedded_dataset[:,:-1]).all(axis=1))
        idx_embedded.append(index_coord[0][0])
    return idx_embedded
