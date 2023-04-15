# pip install -r requirements.txt
import sys
import pandas as pd
import numpy as np
import csv
import requests
from bs4 import BeautifulSoup
import json
import statsmodels.api as sm
from scipy import stats
import time 
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt
# import all the other libraries you need
# make sure to explain in the readme any special libraries the TAs might need

def default_function():
    #default mode
    #add the functions/code you need to scrape all your data
    #print all the data you scrape/request but and if it's huge, show the dimensions and a sample


    reviews_df = pd.read_csv("Traffic_Collision_Data_from_2010_to_Present-2.csv")
    #for lines in reviews_df:
    #    print(lines)
    col_list = ["DR Number","Date Reported","Date Occurred","Time Occurred","Area ID",
                "Area Name","Reporting District","Crime Code","Crime Code Description",
                "MO Codes","Victim Age","Victim Sex","Victim Descent","Premise Code",
                "Premise Description","Address","Cross Street","Location"]
    y = open("myfile.csv", "w")
    df = pd.read_csv("Traffic_Collision_Data_from_2010_to_Present-2.csv", usecols=col_list)
    for items in df["Location"]:
        a = items.replace('(', '')
        a = a.replace(')', '')
        #print(a.split(', '))
        #print(a.split(', ')[0] + ',' + a.split(', ')[1])
        y.write(a.split(', ')[0] + ',' + a.split(', ')[1])
        y.write('\n')
    y.close()
    n = open("myfile.csv", "r")
    print(n.read())


    f = open("myfile.csv", "r")
    csvreader = csv.reader(f)
    rows = []
    for x in csvreader:
        rows.append(x)
    #print(len(rows))
    #print(rows[0])
    zipcode_file = open("zipcode.csv", "w")
    index = 0
    while index < len(rows):
        if index + 20 > len(rows):
            for value in rows[index:len(rows)]:
                url = 'http://dev.virtualearth.net/REST/v1/Locations/' + value[0] + ',' + value[1] + '?&key=AtwP2GlmjNkx5aHfJwdZkQa4WJZl2w3WjAYbDmshUmmaEbHhOny1ZdKzQUBH7KR2'
                content1 = requests.get(url)
                content2 = content1.json() ['resourceSets'][0]['resources'][0]['address']['postalCode']
                print(content2)
                zipcode_file.write(content2)
                zipcode_file.write('\n')
        else:
            for value in rows[index:(index + 20)]:
                url = 'http://dev.virtualearth.net/REST/v1/Locations/' + value[0] + ',' + value[1] + '?&key=AtwP2GlmjNkx5aHfJwdZkQa4WJZl2w3WjAYbDmshUmmaEbHhOny1ZdKzQUBH7KR2'
                content1 = requests.get(url)
                content2 = content1.json() ['resourceSets'][0]['resources'][0]['address']['postalCode']
                print(content2)
                zipcode_file.write(content2)
                zipcode_file.write('\n')
        index += 20
        time.sleep(3)
    
    zipcode_file.close()
    #z = open("zipcode.csv", "r")
    #print(z.read())


    a = open("zipcode.csv", "r")
    csvreader = csv.reader(a)
    zipcode_list = []
    #print(a.read())
    for x in csvreader:
#        print(x[0])
        zipcode_list.append(x[0])
    c = Counter(zipcode_list)
    top_10_zip = c.most_common(10)
    #print(top_10_zip)
    avg_dict = {} 
    for tuples in top_10_zip:
        #print(tuples[0])
        content = requests.get('https://losangeles.craigslist.org/search/apa?postal='+ tuples[0] +
        '&min_bedrooms=2&max_bedrooms=2&min_bathrooms=2&max_bathrooms=2&availabilityMode=0&housing_type=1&sale_date=all+dates')
        soup = BeautifulSoup(content.content, 'html.parser')
        price_list = []
        for link in soup.find_all('span',{'class': 'result-price'}):
            price_list.append(link.text.replace('$', '').strip())
        price_list = [int(item.replace(",", "")) for item in price_list]
        avg_price = sum(price_list) / len(price_list)
        avg_dict[tuples[0]] = avg_price
#print(avg_dict)

    (pd.DataFrame.from_dict(data=avg_dict, orient='index')
        .to_csv('avg_price.csv', header=False))
    z = open("avg_price.csv", "r")

    print(z.read())


        ###############analysis part################
    a = open('zipcode.csv',"r")
    csvreader = csv.reader(a)
    zipcode_list = []
    for x in csvreader:
        zipcode_list.append(x[0])
        c = Counter(zipcode_list)
        top_10_zip = c.most_common(10)
#print(top_10_zip)
    b = open('avg_price.csv',"r")
    reader2 = csv.reader(b)
#print(b.read())
    dict_avg = []
    for row in reader2:
        dict_avg.append(float(row[1]))
#print(dict_avg)
    frequency_accident = []
    for value in top_10_zip:
        frequency_accident.append(int(value[1]))
#print(frequency_accident)
    correlation, p_value = stats.pearsonr(frequency_accident, dict_avg)
    print("The correlation coefficient for traffic collisions and house prices is " + str(correlation))
    Y = frequency_accident
    X = dict_avg
    X = sm.add_constant(X)
    est=sm.OLS(Y, X)
    est = est.fit()
    print(est.summary())
    new_dataset = open("new.csv", "w")
    final = [("frequency of collision","average house price")]
    for x in range(len(dict_avg)):
        final.append((frequency_accident[x],dict_avg[x]))
#print(final)
    for n in final:
        for y in n:
            new_dataset.write(str(y)+',')
        new_dataset.write('\n')
    new_dataset.close()
#z = open("new.csv", "r")
#print(z.read())
    con = pd.read_csv('new.csv')
#print(con)
    con.rename(columns={'frequency of collision':'frequency of collision','average house price':'average house price','Unnamed: 2':'N/A'}, inplace=True)
#print(con.head())


    print(sns.scatterplot(x="frequency of collision", y="average house price", data=con))






    pass

def scrape_function():
    #scrape mode
    #add the functions/code you need to scrape SOME (5 rows per dataset) of your data and print
    #this might be very similar to the default mode
    #you can hard code inputs if need be

    reviews_df = pd.read_csv("Traffic_Collision_Data_from_2010_to_Present-2.csv")
    #for lines in reviews_df:
    #    print(lines)
    col_list = ["DR Number","Date Reported","Date Occurred","Time Occurred","Area ID",
                "Area Name","Reporting District","Crime Code","Crime Code Description",
                "MO Codes","Victim Age","Victim Sex","Victim Descent","Premise Code",
                "Premise Description","Address","Cross Street","Location"]
    y = open("myfile_scrape.csv", "w")
    df = pd.read_csv("Traffic_Collision_Data_from_2010_to_Present-2.csv", usecols=col_list)
    for items in df["Location"][:5]:
        a = items.replace('(', '')
        a = a.replace(')', '')
        #print(a.split(', '))
        #print(a.split(', ')[0] + ',' + a.split(', ')[1])
        y.write(a.split(', ')[0] + ',' + a.split(', ')[1])
        y.write('\n')
    y.close()
    n = open("myfile_scrape.csv", "r")
    print(n.read())


    f = open("myfile_scrape.csv", "r")
    csvreader = csv.reader(f)
    rows = []
    for x in csvreader:
        rows.append(x)
    #print(len(rows))
    #print(rows[0])
    zipcode_file = open("zipcode_scrape.csv", "w")
    index = 0
    while index < len(rows):
        if index + 20 > len(rows):
            for value in rows[index:len(rows)]:
                url = 'http://dev.virtualearth.net/REST/v1/Locations/' + value[0] + ',' + value[1] + '?&key=AtwP2GlmjNkx5aHfJwdZkQa4WJZl2w3WjAYbDmshUmmaEbHhOny1ZdKzQUBH7KR2'
                content1 = requests.get(url)
                content2 = content1.json() ['resourceSets'][0]['resources'][0]['address']['postalCode']
                print(content2)
                zipcode_file.write(content2)
                zipcode_file.write('\n')
        else:
            for value in rows[index:(index + 20)]:
                url = 'http://dev.virtualearth.net/REST/v1/Locations/' + value[0] + ',' + value[1] + '?&key=AtwP2GlmjNkx5aHfJwdZkQa4WJZl2w3WjAYbDmshUmmaEbHhOny1ZdKzQUBH7KR2'
                content1 = requests.get(url)
                content2 = content1.json() ['resourceSets'][0]['resources'][0]['address']['postalCode']
                print(content2)
                zipcode_file.write(content2)
                zipcode_file.write('\n')
        index += 20
        time.sleep(3)
    
    zipcode_file.close()
    #z = open("zipcode.csv", "r")
    #print(z.read())


    a = open("zipcode_scrape.csv", "r")
    csvreader = csv.reader(a)
    zipcode_list = []
    #print(a.read())
    for x in csvreader:
#        print(x[0])
        zipcode_list.append(x[0])
    c = Counter(zipcode_list)
    top_10_zip = c.most_common(10)
    #print(top_10_zip)
    avg_dict = {} 
    for tuples in top_10_zip:
        #print(tuples[0])
        content = requests.get('https://losangeles.craigslist.org/search/apa?postal='+ tuples[0] +
        '&min_bedrooms=2&max_bedrooms=2&min_bathrooms=2&max_bathrooms=2&availabilityMode=0&housing_type=1&sale_date=all+dates')
        soup = BeautifulSoup(content.content, 'html.parser')
        price_list = []
        for link in soup.find_all('span',{'class': 'result-price'}):
            price_list.append(link.text.replace('$', '').strip())
        price_list = [int(item.replace(",", "")) for item in price_list]
        avg_price = sum(price_list) / len(price_list)
        avg_dict[tuples[0]] = avg_price
#print(avg_dict)

    (pd.DataFrame.from_dict(data=avg_dict, orient='index')
        .to_csv('avg_price_scrape.csv', header=False))
    z = open("avg_price_scrape.csv", "r")

    print(z.read())



    pass

def static_function(path_to_static_data):
    #static mode
    #add the functions/code you need to open and print the static copies of your data
    #you can use the path provided in the command line argument to open the data
    f = open(path_to_static_data,"r")
    print(f.read())
    ####################analysis part######################
    a = open('zipcode.csv',"r")
    csvreader = csv.reader(a)
    zipcode_list = []
    for x in csvreader:
        zipcode_list.append(x[0])
        c = Counter(zipcode_list)
        top_10_zip = c.most_common(10)
    #print(top_10_zip)
    b = open('avg_price.csv',"r")
    reader2 = csv.reader(b)
#print(b.read())
    dict_avg = []
    for row in reader2:
        dict_avg.append(float(row[1]))
    #print(dict_avg)
    frequency_accident = []
    for value in top_10_zip:
        frequency_accident.append(float(value[1]))
    #print(frequency_accident)
    correlation, p_value = stats.pearsonr(dict_avg, frequency_accident)
    print("The correlation coefficient for traffic collisions and house prices is " + str(correlation))
    Y = frequency_accident
    X = dict_avg
    X = sm.add_constant(X)
    est=sm.OLS(Y, X)
    est = est.fit()
    print(est.summary())
    new_dataset = open("new.csv", "w")
    final = [("frequency of collision","average house price")]
    for x in range(len(dict_avg)):
        final.append((frequency_accident[x],dict_avg[x]))
#print(final)
    for n in final:
        for y in n:
            new_dataset.write(str(y)+',')
        new_dataset.write('\n')
    new_dataset.close()
#z = open("new.csv", "r")
#print(z.read())
    con = pd.read_csv('new.csv')
#print(con)
    con.rename(columns={'frequency of collision':'frequency of collision','average house price':'average house price','Unnamed: 2':'N/A'}, inplace=True)
#print(con.head())


    print(sns.scatterplot(x="frequency of collision", y="average house price", data=con))





if __name__ == '__main__': #for your purpose, you can think of this line as the saying "run this chunk of code first"
    if len(sys.argv) == 1: # this is basically if you don't pass any additional arguments to the command line
        #default mode
        #print eveything or the dimensions and a sample 
        print("default")
        default_function()

    elif sys.argv[1] == '--scrape': # if you pass '--scrape' to the command line
        #scrape mode
        #print a sample of the data you retrieve from your sources
        print("scrape")
        scrape_function()

    elif sys.argv[1] == '--static': # if you pass '--static' to the command line
        #static mode
        #print a sample of the static datasets you have built from your scraping
        print("static")
        path_to_static_data = sys.argv[2]
        static_function(path_to_static_data)
