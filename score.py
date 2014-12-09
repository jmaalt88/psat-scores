#!/usr/bin/env python

import cookielib
import mechanize
import re

br = mechanize.Browser()
cookiejar = cookielib.LWPCookieJar()
br.set_cookiejar(cookiejar)
br.set_handle_equiv(True)
br.set_handle_gzip(False)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time = 1)
useragent = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) '\
            'Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
br.addheaders = [('User-agent', useragent)]

br.open('https://quickstart.collegeboard.org/posweb/login.jsp')
br.select_form(nr=3)
print 'Enter the credentials for your Collegeboard account:\n'
br['username'] = raw_input('Username: ')
br['password'] = raw_input('Password: ')
br.submit() 
def num_wrong(url):
    try: t = br.open(url).read()
    except: return 0
    matches = re.findall('of\s*\d+', t)
    try: m = matches[0]
    except Exception as e:
        print e
        print t
    try: ans = int(m.split()[1])
    except Exception as e:
        print e
        print m
    return ans

template = 'https://quickstart.collegeboard.org/posweb/questionInfoNewAction.do'\
           '?testYear=2014&questions=incorrect&skillCd=%s&questionInd=1'
crit  = [template % ('CR%d' % x) for x in range(1, 6)]
math  = [template % ('M%d'  % x) for x in range(1, 5)]
writ  = [template % ('W%d'  % x) for x in range(1, 6)]
wrongcrit = sum(num_wrong(url) for url in crit)
wrongmath = sum(num_wrong(url) for url in math)
wrongwrit = sum(num_wrong(url) for url in writ)
critcomp = int((48 - wrongcrit) - 0.25*wrongcrit + 0.5)
mathcomp = int((38 - wrongmath) - 0.25*wrongmath + 0.5)
writcomp = int((39 - wrongwrit) - 0.25*wrongwrit + 0.5)
critcurve = {
48 : 80, 47 : 80, 46 : 78, 45 : 75, 44 : 73, 43 : 71, 42 : 70, 41 : 67,
40 : 66, 39 : 65, 38 : 64, 37 : 62, 36 : 61, 35 : 60, 34 : 59, 33 : 58,
32 : 57, 31 : 56, 30 : 55, 29 : 54, 28 : 53, 27 : 52, 26 : 51, 25 : 51,
24 : 50, 23 : 49, 22 : 48, 21 : 47, 20 : 46, 19 : 46, 18 : 45, 17 : 44,
16 : 43, 15 : 42, 14 : 41, 13 : 40, 12 : 39, 11 : 38, 10 : 37, 9 : 36,
8 : 35, 7 : 33, 6 : 32, 5 : 31, 4 : 30, 3 : 28, 2 : 26, 1 : 24, 0 : 22,
-1 : 21, -2 : 20, -3 : 20, -4 : 20, -5 : 20, -6 : 20, -7 : 20, -8 : 20,
-9 : 20, -10 : 20, -11 : 20, -12 : 20
}
mathcurve = {
38 : 80, 37 : 77, 36 : 75, 35 : 73, 34 : 71, 33 : 70, 32 : 68, 31 : 67,
30 : 65, 29 : 64, 28 : 62, 27 : 60, 26 : 59, 25 : 57, 24 : 56, 23 : 54,
22 : 53, 21 : 51, 20 : 50, 19 : 49, 18 : 48, 17 : 47, 16 : 46, 15 : 45,
14 : 43, 13 : 42, 12 : 42, 11 : 40, 10 : 39, 9 : 38, 8 : 37, 7 : 36,
6 : 35, 5 : 33, 4 : 32, 3 : 30, 2 : 28, 1 : 26, 0 : 25, -1 : 23, -2 : 20,
-3 : 20, -4 : 20, -5 : 20, -6 : 20, -7 : 20
}
writcurve = {
39 : 80, 38 : 76, 37 : 71, 36 : 70, 35 : 69, 34 : 67, 33 : 65, 32 : 63,
31 : 62, 30 : 61, 29 : 59, 28 : 57, 27 : 56, 26 : 55, 25 : 54, 24 : 53,
23 : 51, 22 : 49, 21 : 48, 20 : 48, 19 : 47, 18 : 45, 17 : 44, 16 : 43,
15 : 42, 14 : 41, 13 : 40, 12 : 39, 11 : 38, 10 : 37, 9 : 36, 8 : 35, 7 : 34,
6 : 33, 5 : 32, 4 : 30, 3 : 28, 2 : 26, 1 : 24, 0 : 22, -1 : 20, -2 : 20,
-3 : 20, -4 : 20, -5 : 20, -6 : 20, -7 : 20, -8 : 20, -9 : 20, -10 : 20
} 

critscore = critcurve[critcomp]
mathscore = mathcurve[mathcomp]
writscore = writcurve[writcomp]
total = critscore + mathscore + writscore
ans = '\n'.join([
'Critical Reading : %d (missed %d)' % (critscore, wrongcrit),
'Mathematics      : %d (missed %d)' % (mathscore, wrongmath),
'Writing          : %d (missed %d)' % (writscore, wrongwrit),
'',
'Total            : %d' % total,
''])
with open('out.txt', 'w') as f:
    f.write(ans)
print ans

