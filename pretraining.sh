DATA_DIR=data-bin/assembly-source

fairseq-train \
    --cpu \
    --task masked_lm --criterion masked_lm \
    --arch roberta_base --sample-break-mode complete --tokens-per-sample 4096 \
    --optimizer adam --adam-betas '(0.9,0.98)' --adam-eps 1e-6 --clip-norm 0.0 \
    --lr-scheduler polynomial_decay --lr 0.001 --warmup-updates 1 --total-num-update 5 \
    --dropout 0.1 --attention-dropout 0.1 --weight-decay 0.01 \
    --batch-size 1 \
    --log-format simple --log-interval 1 \
    $DATA_DIR
