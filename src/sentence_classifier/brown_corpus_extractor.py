import re

with open("a01.xml", "r") as f:
    data = f.read().replace("\n", "")

all_sentence_segments = re.findall(r"<p><s n=\"\d+\">(.*?)</s></p>", data)
sentences = []
for segment in all_sentence_segments:
    if "mw pos" not in segment:
        sentences.append(list(map(lambda tup: tup[1], re.findall(r"<w type=\".{0,4}\"( subtype=\".{0,4}\")?>(.*?)</w>", segment))))
