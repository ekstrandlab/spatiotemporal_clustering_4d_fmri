#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Author: Chelsea Ekstrand <chelsea.ekstrand@uleth.ca>


# In[1]:


# import functions

import numpy as np
import scipy.stats as stats
import mne
import nibabel as nib
from os.path import join
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


# In[3]:


# Parse command line arguments

parser = ArgumentParser(description='Perform 4D spatiotemporal clustering using paired t-test',
                       formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('c1data',help='Restructured data for condition 1')
parser.add_argument('c2data',help='Restructured data for condition 2')
parser.add_argument('save_dir',help='Directory to save results')
parser.add_argument('-c1','--c1name',default='cond1',help='Name of condition 1')
parser.add_argument('-c2','--c2name',default='cond2',help='Name of condition 2')
parser.add_argument('-p','--pval',default=.05,help='P-value for thresholding')
parser.add_argument('-n','--nPerms',default=5000,type=int,help='Number of permutations')
parser.add_argument('-t','--tail',default=0,help='Tail for t-test, two-tailed test, 1 = one-tailed test, thresholded above 0, -1 = one-tailed test, thresholded below 0')
args = vars(parser.parse_args())

# Set up parameters

cond1data = args['c1data']
cond2data = args['c2data']
saveDir = args['save_dir']
cond1name = args['c1name']
cond2name = args['c2name']
pval = args['pval']
n_permutations = args['nPerms']
tail = args['tail']


# In[11]:


def save_nifti(filename, affine, data):
    img = nib.Nifti1Image(data, affine)
    nib.save(img, filename)

# Load functional data
print('Loading fMRI data for condition 1: ' + cond1name)
load_c1_data = nib.load(cond1data)
c1_data = load_c1_data.get_fdata()

print(np.shape(c1_data))

print('Loading fMRI data for condition 2: ' + cond2name)
c2_data = nib.load(cond2data).get_fdata()

N1, t, x, y, z = c1_data.shape
N2, _, _, _, _ = c2_data.shape

# Create adjacency matrices for spatial dimensions
adjacency = mne.stats.combine_adjacency(x, y, z)

print('Running paired samples t-test for ' + str(N1) + ' participants')

df = N1 - 1
if tail == 0:
    thresh = stats.t.ppf(1 - pval / 2, df)
elif tail == 1:
    thresh = stats.t.ppf(1 - pval, df)
elif tail == -1:
    thresh = stats.t.ppf(pval, df)

contrast = c1_data - c2_data
print('t-threshold: ' + str(thresh))

# Perform t-test
t_obs, clusters, cluster_pv, _ = mne.stats.spatio_temporal_cluster_1samp_test(
    X=contrast,
    stat_fun=None,
    adjacency=adjacency,
    threshold=thresh,
    tail=tail,
    n_permutations=n_permutations,
    out_type='mask',
    max_step=1
)

# Save results
print('Saving results to ' + saveDir)
contrast_ave = contrast.mean(axis=0)
signs = np.sign(contrast_ave)

T_obs_plot = np.full_like(t_obs, np.nan)
clust_fill = np.full_like(t_obs, np.nan)

i = 1
for c, p_val in zip(clusters, cluster_pv):
    if p_val <= 0.05:
        T_obs_plot[c] = t_obs[c]
        clust_fill[c] = signs[c] * i
        i += 1

T_obs_plot = np.transpose(T_obs_plot, (1, 2, 3, 0))
clust_fill = np.transpose(clust_fill, (1, 2, 3, 0))
contrast_ave = np.transpose(contrast_ave, (1, 2, 3, 0))

# Save results as NIfTI files
affine_mat = load_c1_data.affine
t_file = join(saveDir, f'4d_spatiotemporal_cluster_results_pairedt_{cond1name}_vs_{cond2name}_n_perm-{n_permutations}_pval-{pval}_tstat.nii.gz')
clust_file = join(saveDir, f'4d_spatiotemporal_cluster_results_pairedt_{cond1name}_vs_{cond2name}_n_perm-{n_permutations}_pval-{pval}_clusters.nii.gz')
ave_file = join(saveDir, f'4d_spatiotemporal_cluster_results_pairedt_{cond1name}_vs_{cond2name}_n_perm-{n_permutations}_pval-{pval}_contrast_average.nii.gz')

save_nifti(t_file, affine_mat, T_obs_plot)
save_nifti(clust_file, affine_mat, clust_fill)
save_nifti(ave_file, affine_mat, contrast_ave)

print('Done!')


# In[ ]:




