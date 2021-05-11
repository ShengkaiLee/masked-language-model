
**Learning assembly and source code semantics with masked language modeling**.  

Inspired by [Trex](https://arxiv.org/pdf/2012.08680.pdf), we hope to study the effectiveness of language
modeling in learning the direct semantic correlations between assembly and source codes, and ultimately translating assembly codes back to source codes. More detailes were provided in this [paper](https://github.com/ShengkaiLee/masked-language-model/blob/main/Trex_follow_up.pdf)

**Team**  

Team members (ordered alphabetically by last name):
- Weifan Jiang (wj2301@columbia.edu)
- Shengkai Li (sl4685@columbia.edu)
- Zeyu Liu (zl2967@columbia.edu)

## Download data

- Download all source codes: `data/downloadSourceCode.py`.
- Download all compiled binaries: from [Google drive](https://drive.google.com/drive/folders/1FXlrGiZkch9bnAxlrm43IhYGC3r5NveA?usp=sharing), the binaries should be placed inside `data/binary/`.

## Process data

- Disassemble binaries: `data/disassembleAllBinaries.py`
- Match assembly and source functions by name: `data/assemblySourceMatch.py`.
- Format data as token sequences and split to train/validation/test sets: `prepare_data.py`
- Encode data with BPE: `encode_data.sh`
- Preprocess/binarize data: `preprocessing.sh`
- Download a zip of the processed binarized data in [Google drive](https://drive.google.com/file/d/1CTdA73gHtk_P2z8E01J1PgVYB_jqzoUN/view?usp=sharing).

## Training (pre-training)

- `pretraining.sh`. Note that we did not include a script for each configuration of hyperparameters in our study. Manual change of hyperparameters is required. Note that the the output model should be saved in a directory named `checkpoint` under the repository root.
- [Google drive](https://drive.google.com/drive/folders/1y33PZsB3PzvfHcHVijzCkTpxgrLnLnFY?usp=sharing) contains our pre-trained models with different learning rates.

## Evaluation:

- `training_log/` directory contains the standard output of pre-training when using different configurations of hyperparameters.
- Visualize how perplexity changes over number of updates: `plot_loss_perplexity.py`. The output of the command is saved in `plots/` (**Note** that the loss and perplexity plots are almost identical, since we plot perplexity in log scale, and loss = log2(perplexity)). The command to run this script is:

```
python3 plot_loss_perplexity.py training_log/training_log_0.01_learning_rate.txt training_log/training_log_0.005_learning_rate.txt training_log/training_log_0.001_learning_rate.txt
```

- Test the model to fill mask: `fill_mask.py`. Note that we did not include a script for all testing input sequences. Manually changing the checkpoint path and test input (and replacing one token with `<mask>`) in the script is required.

## Other:
- Code used to extract functions from c-language source code is partially adopted from [here](https://github.com/yuedeji/c_func_name_extract/blob/master/func_extract_clang.py).
