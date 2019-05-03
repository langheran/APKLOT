import warnings
warnings.filterwarnings('ignore')
import numpy as np

def computeIoU(y_pred_batch, y_true_batch):
    results1=np.asarray([pixelAccuracy(y_pred_batch[i], y_true_batch[i]) for i in range(len(y_true_batch))])
    results2=np.asarray([pixelAccuracy(y_pred_batch[i], y_true_batch[i],1) for i in range(len(y_true_batch))])
    return np.mean(results1[(results1!=-1)]), results1, results2

def pixelAccuracy(y_pred, y_true,dlib=None):
    y_pred = np.asarray(y_pred); y_pred=y_pred>0
    y_true = np.asarray(y_true); y_true=y_true>0
    num_right=y_true[(y_true==y_pred)].shape[0]
    num_wrong=y_true[(y_true!=y_pred)].shape[0]
    if(dlib is None):
        return float(y_true[(y_true==y_pred) & (y_true)].shape[0] / y_true[(y_pred) | (y_true)].shape[0]) if (y_true[(y_pred) | (y_true)].shape[0]>0) else -1
    else:
        return float(num_right/(num_right+num_wrong))

import argparse, sys
if __name__ == '__main__' and type(__builtins__).__name__=='module' or ( type(__builtins__).__name__=='dict' and 'get_ipython' not in __builtins__):
    parser = argparse.ArgumentParser(description = 'Evaluate IoU.')
    parser.add_argument('-t', '--true_batch_folder', help = 'True batch folder')
    parser.add_argument('-p', '--pred_batch_folder', help = 'Predicted batch folder')
    args = parser.parse_args(sys.argv[1:])
    
    true_batch_folder = args.true_batch_folder
    pred_batch_folder = args.pred_batch_folder
    
    from scipy import misc
    import os
    y_true_batch=[]
    y_pred_batch=[]
    for f in os.listdir(true_batch_folder):
        true_mask = misc.imread(os.path.join(true_batch_folder,f), mode='L')
        y_true_batch.append(true_mask)
        pred_mask = misc.imread(os.path.join(pred_batch_folder,f), mode='L')
        y_pred_batch.append(pred_mask)
    print(computeIoU(y_true_batch, y_pred_batch))
    os.system("pause")
