from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import random

from wordcloud import WordCloud, STOPWORDS

#words color, set to flamingo theme
def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(%d, 100%%, 68%%)" % random.randint(0, 30)


d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

#import text and pictures
text = open(path.join(d, 'out.txt')).read()

pic_mask = np.array(Image.open(path.join(d, "target.png")))

#parse the pharse, NEED A BETTER WAY TO DO IT
stopwords = set(STOPWORDS)
stopwords.add("not")

wc = WordCloud(background_color="white", max_words=20000, mask=pic_mask,
               stopwords=stopwords, contour_width=0, contour_color='pink',max_font_size=200)

wc.generate(text)


default_colors = wc.to_array()
wc.recolor(color_func=grey_color_func, random_state=3)
wc.to_file(path.join(d, "result.png"))
