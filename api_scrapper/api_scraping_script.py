import requests
import xlwt
from xlwt import Workbook
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

BASE_URL = "https://remoteok.com/api"
USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"
REQUEST_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.5"
}

def get_job_postings():
    res=requests.get(BASE_URL, headers=REQUEST_HEADERS)
    return res.json()

def output_to_xlsx(data):
    wb = Workbook()
    job_sheet = wb.add_sheet('Jobs_Sheet')
    header = list(data[0].keys())
    for i in range(len(header)):
        job_sheet.write(0, i, header[i])

    for i in range(len(data)):
        job = data[i]
        values = list(job.values())
        for x in range(len(values)):
            job_sheet.write(i+1, x, values[x])
    wb.save('job_postings.xls')


if __name__=='__main__':
    json= get_job_postings()
    output_to_xlsx(json[1:])
    # print(json[1])