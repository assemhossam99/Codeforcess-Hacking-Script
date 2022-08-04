from bs4 import BeautifulSoup
import requests
import subprocess
from subprocess import Popen, PIPE, check_output

def runCode(code, timeLimit):
    f = open('code.cpp', 'w')
    f.write(code)
    f.close()
    p = subprocess.Popen(["g++", "-Wall", "-o", "code", 'code.cpp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.communicate()
    try:
        # res = subprocess.call('pro.exe < input.txt > out.txt', shell=True)
        res = check_output('code.exe < input.txt', shell=True, timeout=timeLimit).decode()
    except subprocess.TimeoutExpired:
        p.kill()
        res = 'tle'
    f = open('out.txt', 'w')
    f.write(res)
    f.close()


def compareOutputs():
    fUser = open('out.txt', 'r')
    fCorrct = open('correctOutput.txt', 'r')
    userOut = str(fUser.read()).replace('\n', '')
    correctOut = str(fCorrct.read().strip()).replace('\n', '')
    userOut = userOut.replace(' ', '')
    correctOut = correctOut.replace(' ','')
    return userOut == correctOut


pages = input('Enter the number of pages: ')
contest_id = input('Enter the contest ID: ')
problemLetter = input('Enter the problem: ')
timeLimit = input('Enter the time limit of the problem in seconds: ')

#itreate over all pages of accepted solution of a problem
for page in pages:
    print(page)
    html = requests.get(f'https://codeforces.com/contest/{contest_id}/status/{problemLetter}/page/{page}?order=BY_PROGRAM_LENGTH_ASC')
    soup = BeautifulSoup(html.text, 'lxml')
    cells = soup.find_all('td')
    submissions = soup.find_all('td', class_='id-cell')
    rows = []
    row = []
    for idx, cell in enumerate(cells):
        if idx % 8 == 1:
            ID = cell.text.strip()
            row.append(str(ID))
        elif idx % 8 == 3:
            handle = str(cell.text)
            handle = handle.strip()
            if handle[0] == '*':
                handle = handle[2:]
            row.append(str(handle))
        elif idx % 8 == 5:
            language = cell.text.strip()
            row.append(str(language))
            rows.append(row)
            row = []
    #print(rows)
    for row in rows:
        submissionID = row[0]
        handle = row[1]
        language = row[2]
        if "++" not in language:
            continue
        html = requests.get(f'https://codeforces.com/contest/1714/submission/{submissionID}')
        soup = BeautifulSoup(html.text, 'lxml')
        code = soup.find(id='program-source-text')
        code = str(code.text)
        runCode(code, float(timeLimit))
        if compareOutputs() == False:
            print(f'Error in {handle} code with submission ID {submissionID}')
        else:
            print(f'{handle} code is correct')
