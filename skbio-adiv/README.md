# skbio-adiv

## Setup
This script was tested using Python 3.4, scikit-bio 0.4.1, and biom-format
2.1.5.

Create a new `conda` environment, activate it, and install the required
dependencies:

```
conda create -n skbio-adiv python=3.4
source activate skbio-adiv
conda install -c https://conda.anaconda.org/biocore scikit-bio
pip install biom-format
```

## What it does
skbio-adiv.py takes a BIOM file and
[scikit-bio alpha diversity metric](http://scikit-bio.org/docs/latest/generated/skbio.diversity.alpha.html)
as input and produces a TSV file containing alpha diversity results for each
sample in the BIOM file. The output file matches the format used by
[QIIME](http://qiime.org)'s alpha_diversity.py script.

This script is useful, for example, if you need to use an alpha diversity
metric in scikit-bio that is not available via QIIME's alpha_diversity.py
script.

## How to use it
Download the skbio-adiv.py script included in this repository and run it on a
BIOM file, providing an output filepath and a scikit-bio alpha diversity
metric:

```shell
python skbio-adiv.py <input BIOM file> <output filepath> <alpha diversity metric>
```

For example:

```shell
python skbio-adiv.py table.biom results.txt pielou_e
```

The BIOM file is ``table.biom``, the results will be written to
``results.txt``, and the alpha diversity metric is `pielou_e`.
