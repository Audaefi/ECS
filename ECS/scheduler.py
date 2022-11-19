from scrapy import cmdline
import schedule
import time

schedule_set = str(input("Set Schedule CMD Line >> "))
print(schedule_set)
cmdline.execute(schedule_set.split())

'''
def schedule_job():
    cmdline.execute("scrapy crawl myspider -a arg1=" + numbers + " -a arg2=" + colors + "".split())


schedule.every().day.at("10:30:42").do(schedule_job)
while True:
    schedule.run_pending()
    time.sleep(1)
'''
