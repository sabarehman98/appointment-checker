import datetime
import os
import time
import checker
import mailer

LAST_EMAIL = datetime.datetime.now()

data = []

def init_request():
    timestamp = datetime.datetime.now()
    error, result = checker.check()
    status = ''
    if error:
        status = 'error'
    elif result:
        status = 'active'
    else:
        status = 'inactive'
    data.append({'status': status, 'timestamp': timestamp})

def take_action():
    global EMAIL_AFTER
    global LAST_EMAIL
    global data
    status = data[-1]['status']
    
    if status != 'inactive':
        if status == 'active':
            mailer.send_mail('URGENT: Appointment Open!', 'New Appointment: https://service2.diplo.de/rktermin/extern/choose_realmList.do?locationCode=isla&request_locale=en \n Cancel Old Appointment: https://mail.google.com/mail/u/0/#search/diplo.de/FMfcgzGqRZXPdJGVVpMQhfsGWkVbcWxC')
        elif status == 'error':
            # mailer.send_mail('ERROR: Something went wrong!', 'Something went wrong on the server. Kindly check!')
    elif datetime.datetime.now() > LAST_EMAIL + datetime.timedelta(minutes=int(os.environ.get('EMAIL_AFTER_MIN'))):
        content_list = []
        for d in data:
            content_list.append(str(d['timestamp']) + ' -> ' + d['status'])
        mailer.send_mail('Summary', '\n'.join(content_list))
        data = []
        LAST_EMAIL = datetime.datetime.now()

def main():
    i = 1
    while True:
        print('Cycle ' + str(i) + ':', datetime.datetime.now())
        init_request()
        take_action()
        time.sleep(int(os.environ.get('CHECK_AFTER_SEC')))
        i += 1

if __name__ == '__main__':
    main()
