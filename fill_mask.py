from fairseq.models.roberta import RobertaModel
import torch

roberta = RobertaModel.from_pretrained('checkpoints', 'checkpoint_last.pt', 'data-bin/assembly-source/')  # modily this line to load the appropriate model
assert isinstance(roberta.model, torch.nn.Module)

# replace the test variable with a token sequence, one token should be replaced by <mask>
test = "50 6a 00 ff 74 24 18 e8 14 00 00 00 48 83 c4 10 59 c3 66 2e 0f 1f 84 00 00 00 00 00 0f 1f 40 00 { <mask> _pkcs_5_alg1_common(password, password_len, salt, iteration_count, hash_idx, out, outlen, 0);}"

res = roberta.fill_mask(test)
for r in res:
    print(r[1:])
