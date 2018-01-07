import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
%matplotlib inline
import matplotlib.dates as mdates

# read data from csv
df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
df['Data_Value'] = df['Data_Value'] * 0.1
df.set_index('Date',inplace=True)
df = df.sort_index()
df.index = pd.to_datetime(df.index)

# seperate the dataset for 2 time frames, 2005-2014 and 2005 and drop the leap days
df_previous = df.loc['2005':'2014',:]
df_previous = df_previous.groupby([df_previous.index.month, df_previous.index.day]).agg({'Data_Value': ['min', 'max']})
df_previous = df_previous.drop((2,29))
# load 2015 data
df_2015 = df['2015']


# group by date and calculate max and min
df_2015 = df_2015.groupby([df_2015.index.month, df_2015.index.day]).agg({'Data_Value': ['min', 'max']})
min_2015 = df_2015.loc[:, (slice(None),'min')].values.ravel()
max_2015 = df_2015.loc[:, (slice(None),'max')].values.ravel()
min_previous = df_previous.loc[:, (slice(None),'min')].values.ravel()
max_previous = df_previous.loc[:, (slice(None),'max')].values.ravel()

# create date list for x-axis
datelist = pd.date_range('2015-1-1','2015-12-31')
# plot 2005-2014 data and fill the lines
plt.plot(datelist, min_previous, color='gray', label='Temperature range, 2005-2014')
plt.plot(datelist, max_previous, color='gray')
plt.fill_between(datelist ,min_previous, max_previous, color='grey', alpha='0.25')
# scatter plot extreme hot and cold days for 2015
plt.scatter(datelist[min_2015 < min_previous], min_2015[min_2015 < min_previous], label='Extrem cold days, 2015')
plt.scatter(datelist[max_2015 > max_previous], max_2015[max_2015 > max_previous], label='Extrem hot days, 2015')

# set the dates on x-axis
days = mdates.DayLocator()   # every day
months = mdates.MonthLocator()  # every month
plt.gcf().autofmt_xdate()
xfmt = mdates.DateFormatter('%b')
plt.gca().xaxis.set_major_formatter(xfmt)
# format the ticks
plt.gca().xaxis.set_major_locator(months)
plt.gca().xaxis.set_minor_locator(days)

# make the plot looks nicer 
plt.gca().set_xlim(datelist[0], datelist[-1])
for line in plt.gca().get_lines():
    line.set_linewidth(0.5)
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.gca().spines["bottom"].set_visible(False)
plt.gca().spines["left"].set_visible(False)



# plot title
plt.title('Extreme Weather, 2015')
# set labels
plt.gca().set_xlabel('Month')
plt.gca().set_ylabel('Temperature (celsius)')
# update y-axis so it doens't look clumsy 
plt.yticks([-30, 0, 40])
# put the legend
plt.legend(loc=4)