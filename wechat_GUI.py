import numpy as np
import matplotlib.pyplot as plt
import itchat  # itchat documentation -- https://itchat.readthedocs.io/zh/latest/api/
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import re
from wordcloud import WordCloud, ImageColorGenerator
import PIL.Image # pillow
import jieba  # chinese word segementation tool
from matplotlib.font_manager import FontProperties
from tkinter import *

class wechat_display:
    
    
    def __init__(self,master):
        frame= Frame(master,width=600,height=400)
        frame.pack()
        
        self.printbutton1=Button(frame,text='log into wechat',command=self.login)
        self.figurebutton1=Button(frame,text='show gender distribution',command=self.gender)
        self.figurebutton2=Button(frame,text='show district distribution',command=self.district)
        self.figurebutton3=Button(frame,text='generate hot words',command=self.hotwords)
        self.printbutton1.pack(side=LEFT)
        self.figurebutton1.pack(side=LEFT)
        self.figurebutton2.pack(side=LEFT)
        self.figurebutton3.pack(side=LEFT)
        
    def login(self):
        global friends
        itchat.login()
        friends=itchat.get_friends(update=True)[0:]
        print (friends[0])
    
    def gender(self):
        total=len(friends[1:])
        male = 0
        female = 0
        others = 0
        for friend in friends:
            sex = friend['Sex']
            if sex == 1:
                male += 1
            elif sex == 2:
                female += 1
            else:
                others += 1

        print('Male population: {:d}, ratio: {:.4f}'.format(male, male / float(total)))
        print('Female population: {:d}, ratio: {:.4f}'.format(female, female / float(total)))
        print('Others: {:d}, ratio: {:.4f}'.format(others, others / float(total)))
        bar_width = 0.35
        index=np.arange(3)
        genders=(male,female,others)
        plt.figure(figsize=(14, 7))
        plt.figure()
        plt.bar(index, genders, bar_width, alpha=0.6, color='rgb')
        plt.title('Male-Female Population', fontsize=18)  
        plt.xticks(index, ('Male', 'Female', 'Others'), fontsize=14, rotation=20)
        plt.ylim(0,220)
        for idx, gender in zip(index, genders):
            plt.text(idx, gender + 0.1, '%.0f' % gender, ha='center', va='bottom', fontsize=14, color='black')
        plt.show()
    
    def get_features(self):
         features = []
         for friend in friends:
            feature = {'NickName': friend['NickName'], 'Sex': friend['Sex'], 'City': friend['City'], 
                       'Province': friend['Province'], 'Signature': friend['Signature']}
            features.append(feature)
         features=pd.DataFrame(features)
         return features
    def district(self):
         #get features
         features=self.get_features()
         locations = features.loc[:, ['Province', 'City']]
         locations = locations[locations['Province'] != '']
         data = locations.groupby(['Province', 'City']).size().unstack()
         count_subset = data.take(data.sum(1).argsort())[-20:]
         subset_plot = count_subset.plot(kind='bar', stacked=True, figsize=(24, 24))
         # set fonts
         xtick_labels = subset_plot.get_xticklabels()
         font = FontProperties(fname='C:\Windows\Fonts\simhei.ttf', size=14)    #you need to change
         for label in xtick_labels:
             label.set_fontproperties(font)
         legend_labels = subset_plot.legend().texts
         for label in legend_labels:
             label.set_fontproperties(font)
             label.set_fontsize(10)
         plt.xlabel('Province', fontsize=20)
         plt.ylabel('Number', fontsize=20)
         plt.show()
         
    def hotwords(self):
        features=self.get_features()
        sigature_list = []
        for signature in features['Signature']:
            signature = signature.strip().replace('span', '').replace('class', '').replace('emoji', '')
            signature = re.compile('1f\d+\w*|[<>/=]').sub('', signature)
            if (len(signature) > 0):
                sigature_list.append(signature)
        text = ''.join(sigature_list)
        word_list = jieba.cut(text, cut_all=True)
        words = ' '.join(word_list)
        coloring = np.array(PIL.Image.open('C:\\Users\\lenovo\\Desktop\\snipper.jpg'))   #you need to change
        wc = WordCloud(background_color='white', max_words=2000, mask=coloring, max_font_size=60, random_state=42, 
               font_path='C:\Windows\Fonts\simhei.ttf', scale=2).generate(words)   #you need to change
        image_color = ImageColorGenerator(coloring)
        plt.figure(figsize=(32, 16))
        plt.imshow(wc.recolor(color_func=image_color))
        plt.imshow(wc)
        plt.axis('off')
        plt.show()
        
root=Tk()

b=wechat_display(root)


root.mainloop()
