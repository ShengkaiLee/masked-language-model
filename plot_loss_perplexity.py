import sys
import os
import re
import numpy as np
from matplotlib import pyplot as plt

START = "^.*Start iterating over samples$"
END = "^.*begin validation on \"valid\" subset$"


def extract_txt(txt):
  with open(txt, 'rb') as f:
    txt_file = f.readlines()
  text_start = False
  output = []
  for line in txt_file:
    line = line.decode('utf-8')
    if re.match(END, line):
      text_start = False
    if text_start:
      columns = line.split(" ")
      if columns[16][0] != 'l':
        loss, ppl, num_updates = columns[17][5:-1], columns[18][4:-1], columns[23][12:-1]
      else:
        loss, ppl, num_updates = columns[16][5:-1], columns[17][4:-1], columns[22][12:-1]
      if len([loss, ppl, num_updates]):
        output.append([float(loss), float(ppl), float(num_updates)])
    if re.match(START, line):
      text_start = True
  output = np.array(output)
  return output[:,0], output[:,1], output[:,2]

def draw_loss(loss, num_updates):
  label_ = [0.01, 0.005, 0.001]
  color_ = ['red', 'green', 'black']
  loss = np.array(loss, dtype=object)
  num_updates = np.array(num_updates, dtype=object)
  for i in range(len(loss)):
    plt.grid()
    plt.plot(num_updates[i],loss[i],color=color_[i],label=label_[i])
    print("learning rate = {}, minimum loss = {}".format(label_[i], np.amin(loss[i])))
    plt.xlim([0, 400])
  plt.legend(loc="upper right", title="learning rate")
  plt.savefig("plots/loss.png")

def draw_perplexity(ppl, num_updates):
  plt.clf()
  label_ = [0.01, 0.005, 0.001]
  color_ = ['red', 'green', 'black']
  ppl = np.array(ppl, dtype=object)
  num_updates = np.array(num_updates, dtype=object)
  for i in range(len(ppl)):
    plt.grid()
    plt.plot(num_updates[i],np.log2(ppl[i]),color=color_[i],label=label_[i])
    print("learning rate = {}, minimum PPL = {}".format(label_[i], np.amin(ppl[i])))
    plt.xlim([0, 400])
  plt.legend(loc="upper right", title="learning rate")
  plt.xlabel("number of updates")
  plt.ylabel("log2(Perplexity)")
  plt.title("Number of updates vs. log of Perplexity for different learning rates")
  plt.savefig("plots/perplexity.png")

if __name__ == "__main__":
  loss, ppl, num_updates = [], [], []
  for txt in sys.argv[1:]:
    l, p, n = extract_txt(txt)
    loss.append(l)
    ppl.append(p)
    num_updates.append(n)
  draw_loss(loss, num_updates)
  draw_perplexity(ppl, num_updates)
  plt.clf()