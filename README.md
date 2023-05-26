# 4D Spatiotemporal Clustering for fMRI Data

## Overview

This project focuses on analyzing fMRI data to understand the spatiotemporal dynamics of activation associated with stimulus events. The project involves two main steps: data restructuring and spatiotemporal clustering. The goal is to gain insights into the fMRI response amplitude and identify significant activation patterns across time and space.

## Data Restructuring

In the first step, the fMRI data is restructured to facilitate subsequent analysis using the code provided in 'restructure_data_for_spatiotemporal_clustering'. The following process is followed:

1. Restructuring into 4D Volumes: The fMRI data is restructured into 4D volumes associated with specific experimental events in a stimulus. This restructuring occurs over a timescale chosen by the researcher (e.g., 10 seconds).
2. Amplitude Averaging: For each participant, the fMRI response amplitudes are averaged across events at each time point. This provides an estimate of the fMRI response amplitude for each time point for each participant.
3. Averaged responses for each participant are concatonated into a 5D file for the second step of the analysis, spatiotemporal clustering.

## Spatiotemporal Clustering

In the second step, spatiotemporal clustering is performed using the code provided in 'perform_spatiotemporal_clustering_4d_fmri_t_test'. This code performs permutation testing implemented using spatiotemporal cluster tests from the stats module of MNE (https://mne.tools/stable/index.html#). The clustering is carried out across time and space using one-sample, paired, or independent t-tests, as specified by the user. This analysis helps identify significant activation patterns and understand the spatiotemporal dynamics of fMRI activation at each timepoint.

## Requirements

- Python 3.x
- Numpy
- nibabel
- re
- glob
- os
- mne

## Usage

Please see *Required Data Structure* section below for an example of data should be structured. To use this project, follow these steps:
1. Ensure your fMRI data is in compressed NIfTI format and organized according to the following BIDS specification. The code allows you to provide a suffix for preprocessed fMRI data. For data with sessions or runs assigned, please modify the code accordingly. For example:
      ```
      sub-01
         anat
            sub-01_T1w.nii.gz
         func
            sub-01_task-Movie_bold.nii.gz
            sub-01_task-Movie_bold.json
            sub-01_task-Movie_events.tsv
     ```
2. Ensure you have timing files for the events of interest for each participant. The first column should represent the onset of the specific event in seconds, and the second column should represent the duration of the event. For each event, place timing files in a separate folder. Timing files should start with the subject number in BIDS format and be saved as .txt files. For example: ~/Condition1Timing/sub-001_task-condition1.txt
3. Open 'restructure_data_for_spatiotemporal_clustering.ipynb' in a Jupyter Notebook. See [Data Restructuring Code Summary](#data-restructuring-code-summary) for full details for running this code.
4. 

## Required Data Structure

```
- data_struc_example/ # Example of required data structure
   - sub-001/
      - func/
         - sub-001_task-Movie_bold.nii.gz # Example fMRI data file
   - Condition1_event_files/
      - sub-001_task-Movie_condition1.txt # Example event timing file
   - Condition2_event_files/
      - sub-001_task-Movie_condition2.txt # Example event timing file
- src/
   - restructure_data_for_spatiotemporal_clustering.ipynb # Code for data restructuring
   - perform_spatiotemporal_clustering_4d_fmri_t_test.ipynb  # Code for spatiotemporal clustering
- results/
   - 20sub_average_task-Movie_cond-condition1_TRtimepoints-10.nii.gz # Output file for condition 1 after data restructuring
   - 20sub_average_task-Movie_cond-condition2_TRtimepoints-10.nii.gz # Output file for condition 2 after data restructuring
   - clustering_results/ # Directory for clustering results
- README.md # Project overview and instructions
- LICENSE # License information
```

## Data Restructuring Code Summary

To use the 'restructure_data_for_spatiotemporal_clustering.ipynb' code, follow these steps:
1. Set parameters in the # Set parameters block, a description of each parameter is as follows:
   - fmri_path : path to the subject MRI directories in BIDS formater
   - cond1_path : path to the timing files for each participant for condition 1. Timing files should start with the participant number and end in .txt
   - cond1_path : path to the timing files for each participant for condition 2. Timing files should start with the participant number and end in .txt
   - cond1name : the name of the event you are modeling in your first condition (e.g., 'FaceOnset')
   - cond2name : the name of the event you are modeling in your second condition (e.g., 'FaceOffset')
   - task : BIDS task name for the fMRI data
   - suffix : the end of the fMRI filename after the task (e.g., bold)
   - saveDir : path to save the restructured data
   - time : the number of timepoints you are interested in modeling. The number of timepoints must be divisible by your fMRI repetition time
   - TR : the fMRI repetition time of your data
   - saveSubs : 'y' = yes, 'n' = no, option to save the averaged fMRI volumes for each participant related to each event


## License
