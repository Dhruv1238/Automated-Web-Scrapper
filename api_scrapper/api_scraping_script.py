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
    wb.save('RemoteOKJobs.xls')

def send_email(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(send_from, 'your_PassWord Here')
        smtp.sendmail(send_from, send_to, msg.as_string())
        smtp.close()


if __name__=='__main__':
    json= get_job_postings()
    output_to_xlsx(json[1:])
    send_email('dhruv.sharma@somaiya.edu', ['dhruv4075@gmail.com'], 'RemoteOK Jobs', 'Please find the attached file', files=['RemoteOKJobs.xls'])
    # print(json[1])