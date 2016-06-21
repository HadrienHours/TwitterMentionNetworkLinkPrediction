import matplotlib.pyplot as plt
import matplotlib
import csv
import datetime

f = open('numberTweetsMentionPerMonth.csv','r')

lv = [[int(el[0]),int(el[1])] for el in csv.reader(f,delimiter=',')]
xTweets = range(len(lv))
xMentions = [0.1 + i for i in range(len(lv))]
fig,ax = plt.subplots()
listTweets = [el[0] for el in lv]
listMentions = [el[1] for el in lv]
listDates1 = [datetime.datetime(2014,6,1),datetime.datetime(2014,7,1),datetime.datetime(2014,8,1),datetime.datetime(2014,9,1),datetime.datetime(2014,10,1),datetime.datetime(2014,11,1),datetime.datetime(2014,12,1),datetime.datetime(2015,1,1),datetime.datetime(2015,2,1),datetime.datetime(2015,3,1),datetime.datetime(2015,4,1),datetime.datetime(2015,5,1)]
listDates2 = [datetime.datetime(2014,6,5),datetime.datetime(2014,7,5),datetime.datetime(2014,8,5),datetime.datetime(2014,9,5),datetime.datetime(2014,10,5),datetime.datetime(2014,11,5),datetime.datetime(2014,12,5),datetime.datetime(2015,1,5),datetime.datetime(2015,2,5),datetime.datetime(2015,3,5),datetime.datetime(2015,4,5),datetime.datetime(2015,5,5)]
plt.bar(listDates1,listTweets,color='blue',alpha=0.75,width=8,label='Number of Tweets')
plt.bar(listDates2,listMentions,color='green',alpha=0.75,width=8,label='Number of Mentions')
plt.xaxis_date()
plt.yscale('log')
plt.legend(loc='upper left')
plt.grid()
matplotlib.rcParams.update({'font.size': 22})
fig.autofmt_xdate()
plt.show(block=False)


