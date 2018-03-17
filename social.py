import requests
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import urllib
import pandas as pd
import re, time, random
from nltk.stem.wordnet import WordNetLemmatizer
import jellyfish
import numpy as np

def cryptomiso():
    '''
    Returns a list of github repo links from Cryptomiso.com
    '''
    coin_dict = {}
    r = requests.get("https://www.cryptomiso.com/")
    soup = BeautifulSoup(r.text, "html.parser")
    commits_info= soup.find_all("small")
    commits_info = commits_info[:-2]
    github_list = []
    for tag in commits_info:
        github_url = tag.find("a")["href"]
        if github_url is not None:
            if github_url[-22:] ==  "graphs/commit-activity":
                github_list.append(github_url[:-23])
    return github_list

def coin_list():
    '''
    Returns a list of coins that are included on cryptomiso
    '''
    r = requests.get("https://www.cryptomiso.com/")
    soup = BeautifulSoup(r.text, "html.parser")
    coins = soup.find_all("h4")
    all_coins = []
    for i in range(len(coins)):
        coin = re.search("\.(.*?)\·", coins[i].text)[1][1:-1].lower()
        all_coins.append(coin)
    return all_coins

def coin_descriptions():
    '''
    Returns a simple description of all the coins 
    '''
    lmtzr = WordNetLemmatizer()
    r = requests.get("https://www.cryptomiso.com/")
    soup = BeautifulSoup(r.text, "html.parser")
    desc_list = soup.find_all("h6")
    prev_counter = 0
    ordered_desc_list = []
    coin_list = []
    for i in range(len(desc_list)):
        coin = desc_list[i].find_previous("h4").text
        coinname = re.search("\.(.*?)\·", coin)[1][1:-1].lower()
        counter = int(re.search(r'\d+', coin).group(0))
        desc = lmtzr.lemmatize(desc_list[i].text)
        if desc[-1] == " ":
            desc = desc[:-1]
        ordered_desc_list.append(desc)
        if prev_counter != counter - 1:
            # print(prev_counter, counter)
            for i in range(counter - prev_counter - 1):
                ordered_desc_list.append("")
        prev_counter = counter                
    return ordered_desc_list

def occur():
    '''
    Returns two dictionaries: a counter of all the occurances 
    second dictionary is of only the repeat occurances
    '''
    ordered_desc_list = coin_descriptions()
    desc_dict = {}
    mult_dict = {}
    for desc in ordered_desc_list:
        if desc not in desc_dict:
            desc_dict[desc] = 1
        else:
            desc_dict[desc] += 1
    for items in desc_dict:
        if desc_dict[items] > 1:
            mult_dict[items] = desc_dict[items]
    return desc_dict, mult_dict

def description_distance():
    '''
    Returns Jaro Winkler Descriptions of different coins
    '''
    ordered_desc_list = coin_descriptions()
    coinlist = coin_list()
    desc_dict = occur()[0]
    lists_of_i_lists = []
    avg_list = []
    for i in range(len(ordered_desc_list)):
        i_list = []
        for j in range(len(ordered_desc_list)):
            jw = jellyfish.jaro_distance(ordered_desc_list[i], ordered_desc_list[j])
            i_list.append(jw)
        lists_of_i_lists.append(i_list)
        avg_list.append(np.mean(i_list))
    distance_df = pd.DataFrame(lists_of_i_lists)
    distance_df.index = coinlist
    distance_df["avg"] = avg_list
    column_list = coinlist
    column_list.append("avg")
    distance_df.columns = column_list
    distance_df.to_csv("distance.csv")

    average_df = distance_df["avg"].T
    # # len(average_df)
    # return average_df
    average_df = pd.DataFrame(average_df) 
    average_df.index = coinlist[:-1]
    # average_df.index.name = "coins"
    average_df.columns = ["avg"]
    # print(average_df)
    average_df = average_df.sort_values(by=["avg"], ascending=False)
    # print(average_df)
    clean_df = average_df[(average_df.T != 0.000000).any()]
    print(clean_df)
    clean_df.to_csv("uniqueness.csv")
    average_df.to_csv("average_distance.csv")
    return distance_df, average_df, clean_df
    
def soups():
    url_list = cryptomiso()
    list_of_stats = []
    contributor_errors_list = []
    DNE_errors_list = []
    name_list = []
    for url in url_list:
        print(url)
        name_split = url.split("/")[3:]
        name = ""
        for each in name_split:
            if name != "":
                name += "/"
            name += each 
        name_list.append(name)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        commits_info= soup.find("ul", class_="numbers-summary")
        if commits_info is not None:
            stats = commits_info.find_all("span", class_="num text-emphasized")
            stats_list = []
            for each in stats:
                match = re.search(r'\d+', each.text.replace(",", ""))
                if match is not None:
                    stats_list.append(match.group(0))
                else:
                    contributor_errors_list.append(url)
            list_of_stats.append(stats_list)        
        else:
            DNE_errors_list.append(name)
            list_of_stats.append([None,None,None,None])
    df = pd.DataFrame(list_of_stats)
    df.index.name = "Coins"
    index_list = []
    df.index = coin_list()
    df.columns = ["commits", "branches", "releases", "contributors"]
    df.to_csv("github.csv")
    # df.rows(name_list)
    # df.columns(["commits", "branches", "releases", "contributors"])
    return df


def name_list_df(name_list, length=None):
    #resets name based on the name_list of coins
    pass
# def 

def old_funct():
    coin_list = []
    contributor_dict = {}
    coin_overview = soup.find_all("h4")
    for coin_info in coin_overview:
        texts = coin_info.text
        ticker = coin_info.find("a").contents[0]
        coinname = re.search("\.(.*?)\·", coin_info.text)[1][1:-1].lower()
        coin_list.append(coinname)
        texts = texts.replace(coinname, "")
        texts = texts.replace(ticker, "")
        texts = texts.replace(",", "")
        if len(tuple(re.findall(r'\d+', texts))) == 3:
            [github_rank, commits, contributors] = re.findall(r'\d+', texts)
            stat_dict = {}
            stat_dict["github_rank"] = github_rank
            stat_dict["commits"] = commits
            stat_dict["contributors"] = contributors
            coin_dict[coinname] = stat_dict

    info_list = soup.find_all("span", class_="smaller text-muted")
    another_dict = {}
    for i in range(len(info_list)):
        coinname = coin_list[i]
        word_list = info_list[i].text.split()
        info_dict = {}
        for j in range(len(word_list)):
            if word_list[j] == "Created:":
                info_dict["created_date"] = word_list[j+1]
            elif word_list[j] == "Updated:":
                info_dict["last_updated_date"] = word_list[j+1]
            elif word_list[j] == "Language:":
                info_dict["language"] = word_list[j+1]
            elif word_list[j] == "Watchers:":
                info_dict["watchers"] = int(word_list[j+1])
            elif word_list[j] == "contributor:":
                info_dict["top_contrib"] = word_list[j+1]
                # if int(word_list[j+1]) == 100:
                    # Then we want to beautifulsoup this page and learn more
                if word_list[j+1] not in contributor_dict:
                    contributor_dict[word_list[j+1]] = []
                contributor_dict[word_list[j+1]].append(coinname)
        if coinname in coin_dict:
            another_dict[coinname] = info_dict
    multi_contribute = {}
    for contributors in contributor_dict:
        if len(contributor_dict[contributors]) > 1:
            multi_contribute[contributors] = contributor_dict[contributors]
    return coin_dict, another_dict, multi_contribute, github_list

def df_create():
    result = cryptomiso()
    df1 = pd.DataFrame.from_dict(result[0])
    df2 = pd.DataFrame.from_dict(result[1])
    final_df = pd.concat([df1, df2]).T
    final_df.to_csv("github.csv")
    return final_df
# info contains at most these things:
# created date, most recent update
# github language mentioned, how many watchers

def reddit_search(coinname):
    search_string.replace(' ','%20')
    search_string.replace(':', '%3A')
    bing_search = "https://www.bing.com/search?q=" + search_string
    r = requests.get(bing_search)
    if r is not None:
        soup = BeautifulSoup(r.text, "html.parser")
        a = soup.find_all("h1")
        if "There are no results for" in str(a[-1]):
            print("skipped" + search_string)
            return None
        else:
            print(soup.find("h2"))
            link = soup.find("h2").find("a")['href']
            return link

def many_reddit(coinlist):
    link_list = []
    for coin in coinlist:
        link = reddit_search(coin)
        link_list.append(link)
    return link_list
