mkdir -p gpt2_bpe
wget -O gpt2_bpe/dict.txt https://dl.fbaipublicfiles.com/fairseq/gpt2_bpe/dict.txt
fairseq-preprocess \
    --only-source \
    --srcdict gpt2_bpe/dict.txt \
    --trainpref assembly-source/assembly-source.train.bpe \
    --validpref assembly-source/assembly-source.valid.bpe \
    --testpref assembly-source/assembly-source.test.bpe \
    --destdir data-bin/assembly-source \
    --workers 60