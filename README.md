# Multi-echo fMRI overview

## Background
This is the code base for the Dash app deployed at https://me-fmri-overview.herokuapp.com/

This application provides an interactive overview of parameters implemented in multi-echo functional magnetic resonance imaging (fMRI) studies and acquisition sequences. The study database, coded parameters and visualizations were curated and built by the tedana community. For more information about multi-echo fMRI, open source algorithms to process such data, and the community itself, please visit: [tedana.readthedocs.io](https://tedana.readthedocs.io/)

## Running the Dash app locally

### STEP 1:

Clone the `git` repository:

```
git clone https://github.com/jsheunis/me-fmri-overview.git
```
or use green Code button above to download the code to your device.

Afterwards, navigate to this repository in the command line.

### STEP 2:

Create and activate a virtual environment (below named `me-fmri-overview`) within which to set up and run the application, for example using [miniconda](https://docs.conda.io/en/latest/miniconda.html):

```
conda create -n me-fmri-overview python
conda activate me-fmri-overview
```

### STEP 3:

Install the required Python packages:
```
pip install requirements.txt
```

### STEP 4:

Run the application
```
python index.py
```

Then navigate in your browser to [http://127.0.0.1:8050/](http://127.0.0.1:8050/), where the Dash app should be running.


## Contribute

Contributions in the form of [issues](https://github.com/jsheunis/me-fmri-overview/issues) or [pull requests](https://github.com/jsheunis/me-fmri-overview/pulls) are very welcome!

If you have added to the code base, please test your additions locally, using the instructions above, before sending a pull request.