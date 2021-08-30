import numpy as np


def split(file_path="40sentences.txt"):
    f = open(file_path, "r")
    sent_list = []
    for (index, sent) in enumerate(f):
        curr_sent = sent.replace(" ", "+").strip()
        curr_sent = ' '.join(curr_sent.upper())
        curr_sent = curr_sent.replace("+", "Spc")

        # add enter
        curr_sent = ''.join(('Nois Act ', curr_sent, ' Ent Act Nois'))
        sent_list.append(curr_sent)
        # curr_sent = split(" ".join(cur_sent))
    return sent_list


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(split())

# if __name__ == '__main__':
#     f = open("40sentences.txt", "r")
#     long_text = np.empty([1,1])
#     for (index, sent) in enumerate(f):
#         curr_sent = split(sent)
#         long_text += np.add(long_text, curr_sent, out=long_text, casting="unsafe")
#     print(long_text)
