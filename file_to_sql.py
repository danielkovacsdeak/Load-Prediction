import pandas as pd
import datetime

xls = pd.ExcelFile("Stark Anonymised Data Pack 1.xlsx")
sheet_to_df_map = {}
for sheetName in xls.sheet_names:
    if 'Site' in sheetName:
        sheet_to_df_map[sheetName] = xls.parse(sheetName)
'''now we have a dict containing site name -
- the data of that site in dataframe data pairs'''

'''
output format: .sql
output like:
    insert into meter_reading ('<site name>', '<leave it empty>', '<datetime>', '<value>');
    insert into meter_reading ('<site name>', '<leave it empty>', '<datetime>', '<value>');
    insert into meter_reading ('<site name>', '<leave it empty>', '<datetime>', '<value>');
    ...
'''

f = open('data.sql', 'a+')

for sheet in sheet_to_df_map.keys():
    d = sheet_to_df_map[sheet]
    checkTimeDifference(d)
    times = getTimes(d)
    for j in range(d.shape[0]):
        for i in range(1, len(times) + 1):
            value = d.iat[j, i]

            col = times[i - 1]
            seconds = (col.hour * 60 + col.minute) * 60 + col.second
            Datetime = d['Date'][j] + datetime.timedelta(0, seconds)
            nextLine = 'insert into meter_reading values (\'' + str(
                sheet) + '\', \'\', \'' + str(Datetime) + '\', \'' + str(value) + '\', \'\', \'\');'
            f.write(nextLine + '\n')

f.close()


# -------------------- Functions ------------------

def getTimes(d):
    '''
    Returns a list of the time columns of
    the sheet.
    '''
    times = d.columns.tolist()
    for i in times:
        if type(i) != datetime.time:
            times.remove(i)
    # somehow it skips the last column ->
    # have to manage it separately
    if type(times[-1]) != datetime.time:
        times.remove(times[-1])
    return times


def checkTimeDifference(d):
    '''
    For every site we call this function. 
    First it checks if the time step between
    columns is correct (30 mins).
    It also returns the number of columns with data
    (note: the first column is date, and the last 
    few is rubbish.) -> later we can iterate this long.
    '''
    last = 0
    numberOfDataColumns = 0
    # use this to check if we have data for every 30 mins
    check = datetime.datetime(100, 1, 1, 0, 30, 0)
    for col in d.columns:
        if type(col) == datetime.time:
            numberOfDataColumns += 1
        if type(last) == datetime.time and type(col) == datetime.time:
            # timedelta only works with date-s but our columns are time-s
            # need to create a date variable to check (might  be a bit
            # confusing)
            seconds = (col.hour * 60 + col.minute) * 60 + col.second
            current = datetime.datetime(
                100, 1, 1, 0, 0, 0) + datetime.timedelta(0, seconds - 30 * 60)
            if last != current.time():
                print(f'ERROR! Difference between columns "{col}" and "{last}" is NOT 30 mins.')
                breakti
        last = col
    return numberOfDataColumns
