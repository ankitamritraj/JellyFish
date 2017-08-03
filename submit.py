import mechanize
from bs4 import BeautifulSoup
import time

br = mechanize.Browser()
br.set_handle_robots(False)

BASE_URL 	 = "http://codeforces.com/"
FILE_NAME	 = "test.c"
relative_url = "enter?back=%2F" 

#-------------------------------Login---------------------------------#
print "Loggin into account..."
response = br.open(BASE_URL + relative_url)
br.select_form(nr = 1)
br.form['handle'] = 'cf username'
br.form['password'] = 'password'
br.submit()

# Handling invalid login 
if br.geturl() == (BASE_URL + relative_url):
	print "Invalid Credentials :/"
	print "Exiting..."
	exit()
print "Done Login :)"
#-----------------------------Done Login------------------------------#

#------------------------------User Input-----------------------------#
roundNumber = " "
problemCode = " "
# roundNumber = raw_input('Enter round number : ')
# problemCode = raw_input('Enter problem code : ').upper()
#---------------------------------------------------------------------#


# -----------------------Retrieving Contest Page----------------------#
relative_url = "contest/" + roundNumber + "/problem/" + problemCode
br.open(BASE_URL + relative_url)

# Handling invalid Round Number/Problem Code
if br.geturl() == BASE_URL:
	print "Invalid Round Number/Problem Code"
	print "Exiting..."
	exit()
#---------------------------------------------------------------------#

# ---------------------------Submitting Code--------------------------#
print "Submitting code..."
br.select_form(nr = 2)
br.form.add_file(open(FILE_NAME), 'text/plain', FILE_NAME, name='sourceFile')
br.submit()
submittedURL = br.geturl()
print "Code submitted sucessfully :)"
#---------------------------------------------------------------------#


#-----------------------Fetching Dyanamic Status----------------------#
print "Fetching Status!"
response 	= br.open(submittedURL)
data 		= response.read()
soup 		= BeautifulSoup(data,'html.parser')
getAll 		= soup.find_all(attrs = {"waiting":"true"})
getAllFalse = soup.find_all(attrs = {"waiting":"false"})
isPresent 	= False
for tr in getAll:
	isPresent = True

while (isPresent == True):
	partA = getAll[0].contents[1].contents[0]
	partB = partA.contents[1].contents[0]
	print partA.contents[0] + partB
	time.sleep(1)
	response = br.open(submittedURL)
	data = response.read()
	soup = BeautifulSoup(data,'html.parser')
	getAll = soup.find_all(attrs = {"waiting":"true"})	 
	isPresent = False
	for child in getAll:
		isPresent = True

#------------------------------Final Verdict--------------------------#

if isPresent == False:
	print "Finsh Judging"
	partA = getAllFalse[0].contents[1].contents[0]
	if partA == "Compilation error":
		print partA
	elif partA.contents[0] == "Accepted" :
		print partA.contents[0]
	else:
		partB = partA.contents[1].contents[0]
		print partA.contents[0] + partB
exit()
#----------------------------------------------------------------------#