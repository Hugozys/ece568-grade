#!/usr/bin/python3
import requests
import json
import re
import datetime
import argparse
import configparser
import csv

homework = "" 
url = ""
my_data= dict() #at least reporter level
tanums = 0
rotation = 0
def is_valid(repo): #filter past gitlab projects
    p = re.compile('2019.*')
    if (p.match(repo['created_at']) != None):
        return True
    return False

def match_netid(repo):
    pattern= "([a-z]{2,3}\d{2,3})/"+ homework + "-(.*).git" 
    m = re.search(pattern,repo["ssh_url_to_repo"])
    if m == None:
        m = re.search("([a-z]{2,3}\d{2,3}).*.git", repo["ssh_url_to_repo"])
    return m

def get_late_days(late_seconds):
    one = 24*3600
    two = one*2
    if (late_seconds <= 0):
        return "0"
    elif (late_seconds <= one):
        return "1"
    elif (late_seconds <= two):
        return "2"
    else:
        return ">=3"

def get_date_object(date_str):
    pattern="(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).*"
    m = re.search(pattern,date_str)
    mt = m.groups()
    return datetime.datetime(int(mt[0]),int(mt[1]),int(mt[2]),int(mt[3]),int(mt[4]),int(mt[5]))
    
def calc_late_date(repo):
    finish_time = get_date_object(repo["last_activity_at"])
    start_time = get_date_object(deadline)
    return get_late_days((finish_time-start_time).total_seconds())
    
def write_repo(repolst,writer):
    global rotation
    global tanums
    for repo in repolst:
        if is_valid(repo):
            last_known_activity = repo["last_activity_at"]
            id_res = match_netid(repo)
            owner = id_res.group(1)
            netid1 = "NA"
            netid2 = "NA"
            netid3 = "NA"
            if (len(id_res.groups()) == 2):
                member = id_res.group(2).split('-')
                netid1 = member[0]
                netid2 = member[1]
                if (len(member) == 3):
                    netid3 = member[2]
                    pass
                
            else: #incorrect naming conventions
                netid2 = owner
                pass      
            late_days = calc_late_date(repo)
            rotation = rotation % tanums + 1
            writer.writerow({'owner':owner, 'netid1':netid1,'netid2':netid2,'netid3':netid3,'repo':repo["ssh_url_to_repo"],'grader':rotation,'last seen':last_known_activity,'late':late_days})
            pass
        pass
    pass

        


def crawl():
    with open(homework+".csv","w",newline='') as csvfile:
        fieldnames=['owner','netid1', 'netid2','netid3','repo','grader','last seen','late']
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        res = requests.get(url, my_data)
        for i in range(0, int(res.headers["X-Total-Pages"])): #figure out total pages
            my_data['page'] = i+1 #access current pages
            res = requests.get(url,my_data)
            repolst = res.json()
            write_repo(repolst,writer)
            pass


def filldata(config):
    global homework
    global url
    global deadline
    global my_data
    global tanums
    homework = "erss-hwk"+config["SUBMISSION"]["homework"]
    url = config["SUBMISSION"]["url"]
    deadline = config["SUBMISSION"]["deadline"]
    my_data = {'private_token':config["SUBMISSION"]["token"],'search':homework,'min_access_level':20}
    tanums = int(config["GRADE"]["tanums"])
    pass

def check(config):
    if "SUBMISSION" in config and "GRADE" in config:
        if "url" in config["SUBMISSION"] and "homework" in config["SUBMISSION"] and "deadline" in config["SUBMISSION"] and "token" in config["SUBMISSION"]:
            return True
        pass
    else:
        return False
    
def read_config(filepath):
    try:
            config = configparser.ConfigParser()
            config.read(filepath)
            if check(config):
                filldata(config)
            else:
                print("invalid config file")
            pass
    except FileNotFoundError:
        print("The filepath you specify doesn't exist.")
        exit()
        pass
    



def process_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config",help="customize configure file path. Default is ./config")
    args = parser.parse_args()
    if (args.config):
        read_config(args.config)
    else:
        read_config("./config")
        pass
    pass


process_config()
crawl()
    

