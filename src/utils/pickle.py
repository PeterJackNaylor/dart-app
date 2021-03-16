import pickle


def save_dic(file_name, dic):
    with open(file_name, 'wb') as handle:
        pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)


def open_dic(file_name):
    with open(file_name, 'rb') as handle:
        b = pickle.load(handle)
    return b
