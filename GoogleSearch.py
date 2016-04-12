'''
DISCLAIMER: This code document is for personal use only. Any violation of the Google Terms of Service is not the responsibility of the authors of the document and is performed at your own risk. 
	...Just so you know, this sort of thing does violate the Google ToS. We (the authors) personally did not use it in production code, only as an experiment in twill commands. We hope that you do the same.
'''
from __future__ import print_function	## Source: http://stackoverflow.com/questions/19185338/cython-error-compiling-with-print-function-parameters
import datetime
import traceback
import random 
import time

import sys
pythonVersionNumber = sys.version_info.major 	##tells us if it is Python 2 or 3.

_GoogleSearchImportedBasicModules = True
_GoogleSearchImportedDBHandler = True
_GoogleSearchImportErrors = ""

try:
	import GoogleSearchQuery
except Exception, e:
	_GoogleSearchImportErrors+="\n\n\n\tFatal ERROR while importing GoogleSearchQuery.py: . The module may have syntax errors or may be missing entirely."
	_GoogleSearchImportErrors+="\n\t\tError description: %s"%(e)
	_GoogleSearchImportedBasicModules = False

try:
	import GoogleWebsiteParser
except Exception, e:
	_GoogleSearchImportErrors+="\n\n\n\tFatal ERROR while importing GoogleWebsiteParser.py: . The module may have syntax errors or may be missing entirely."
	_GoogleSearchImportErrors+="\n\t\tError description: %s"%(e)
	_GoogleSearchImportedBasicModules = False

try:
	import BrowserHandler 
	
except Exception, e:
	_GoogleSearchImportErrors+="\n\n\n\tFatal ERROR while importing BrowserHandler.py: . The module may have syntax errors or may be missing entirely."
	_GoogleSearchImportErrors+="\n\t\tError description: %s"%(e)
	_GoogleSearchImportedBasicModules = False

try: 
	import SearchDBHandler
except Exception, e:
	_GoogleSearchImportErrors+="\n\n\n\tERROR while importing SearchDBHandler.py: . The module may have syntax errors or may be missing entirely."
	_GoogleSearchImportErrors+="\n\t\tError description: %s"%(e)
	_GoogleSearchImportedDBHandler = False

## Note: these were move to the start of the file because it's faster. Source: http://stackoverflow.com/questions/128478/should-python-import-statements-always-be-at-the-top-of-a-module 



keepWaiting = True 		## Used for signal handling.





class GoogleSearch:
	
	possibleBrowserHandlers = None
	browserHandler = None
	dbHandler = None


	def __init__(self, browserHandlerChoice=None, printing=True):
		if _GoogleSearchImportedBasicModules:

			## Assign possibleBrowserHandlers:
			try:
				self.possibleBrowserHandlers = BrowserHandler.POossibleBrowserHandlers
			except Exception:
				self.possibleBrowserHandlers = None


			## Assign browserHandler:
			if self.possibleBrowserHandlers != None:
				defaultSequence = [self.possibleBrowserHandlers.SPLINTER, self.possibleBrowserHandlers.TWILL0_9, self.possibleBrowserHandlers.SPLINTER_HEADLESS]
				
				self._setBrowserHandlerFromChoice(
					defaultSequence=defaultSequence, 
					browserHandlerChoice=browserHandlerChoice, 
					printing=printing
				)
			
			## Assign dbHandler:
			if _GoogleSearchImportedDBHandler:
				try:
					self.dbHandler = SearchDBHandler.SearchDBHandler()
				except Exception:
					self.dbHandler = None

		else:
			self.browserHandler = None
			self.dbHandler = None



	def _setBrowserHandlerFromChoice(self, defaultSequence, browserHandlerChoice, printing):
		if self.canRunBasic(printing=printing):
			if browserHandlerChoice == None:	## Use the default sequence...
				if self._tryAssignBrowserHandler(browserHandlerPriorityList=defaultSequence, errorPrinting=False)==False:
					if printing:
						print("\n\tFATAL ERROR in GoogleSearch.__init__(): no browserHandler is available, please follow their instructions for installation.")


			elif browserHandlerChoice not in self.possibleBrowserHandlers:
				if printing:
					print("\n\tERROR in GoogleSearch.__init__(): invalid browserHandlerChoice input.")

			else:
				sequence = []
				if browserHandlerChoice==self.possibleBrowserHandlers.SPLINTER:
					sequence = [self.possibleBrowserHandlers.SPLINTER, self.possibleBrowserHandlers.SPLINTER_HEADLESS, self.possibleBrowserHandlers.TWILL0_9]
					
				elif browserHandlerChoice==self.possibleBrowserHandlers.SPLINTER_HEADLESS:
					sequence = [self.possibleBrowserHandlers.SPLINTER_HEADLESS, self.possibleBrowserHandlers.SPLINTER, self.possibleBrowserHandlers.TWILL0_9]

				elif browserHandlerChoice==self.possibleBrowserHandlers.TWILL0_9:
					sequence = [self.possibleBrowserHandlers.TWILL0_9, self.possibleBrowserHandlers.SPLINTER, self.possibleBrowserHandlers.SPLINTER_HEADLESS]


				if self._tryAssignBrowserHandler(browserHandlerPriorityList=sequence, errorPrinting=False) == False:
					if printing:
						print("\n\tERROR in GoogleSearch.__init__(): cannot instantise any self.browserHandler variable. Browser Handlers tried so far: %s"%sequence)

		else:
			if printing:
				print("\n\tFATAL ERROR in GoogleSearch.__init__(): Cannot run because required modules cannot be imported.")

	

	def _tryAssignBrowserHandler(self, browserHandlerPriorityList, errorPrinting=True):
		for bh in browserHandlerPriorityList:
			if bh == self.possibleBrowserHandlers.SPLINTER:
				self.browserHandler = self.BrowserHandler.splinterBrowserHandler(headless=True, errorPrinting=errorPrinting)
				if self.browserHandler.checkBrowserAvailability():
					return True

			elif bh == self.possibleBrowserHandlers.SPLINTER_HEADLESS:
				self.browserHandler = self.BrowserHandler.splinterBrowserHandler(headless=False, errorPrinting=errorPrinting)
				if self.browserHandler.checkBrowserAvailability():
					return True

			elif bh == self.possibleBrowserHandlers.TWILL0_9:
				self.browserHandler = self.BrowserHandler.twillBrowserHandler(errorPrinting=errorPrinting)
				if self.browserHandler.checkBrowserAvailability():
					return True

		self.browserHandler=None
		return False




	





	def canRunBasic(self, printing=True):
		if _GoogleSearchImportedBasicModules and self.possibleBrowserHandlers != None and self.browserHandler != None:
			return True

		if printing:
			print(_GoogleSearchImportErrors)
			if self.possibleBrowserHandlers == None:
				print("\n\tFatal Error in class GoogleSearch : cannot instantise self.possibleBrowserHandlers")
			if self.browserHandler == None:
				print("\n\tFatal Error in class GoogleSearch : cannot instantise self.browserHandler")
		return False


	def canRunDB(self, printing=True):
		if _GoogleSearchImportedDBHandler and self.dbHandler != None:
			return True

		if printing:
			print(_GoogleSearchImportErrors)
			if self.dbHandler == None:
				print("\n\tError in class GoogleSearch : cannot instantise self.dbHandler")
		return False



	def hasDBHandler(self):
		if self.dbHandler == None:
			return False
		return True



	def hasBrowserHandler(self):
		if self.browserHandler == None:
			return False
		return True


	def browserHandlerTest(self, printing=False):
		if self.hasBrowserHandler():
			try:
				self.browserHandler.go("http://www.google.com")
				if self.browserHandler.getCurrentPageHtml() != None:
					return True

			except Exception, e:
				if printing:
					print("\n\tFatal ERROR in class GoogleSearch : Browser Handler cannot access websites.")
					print("\n\t\tError description: %s"%(e))
			
		return False



	def listpossibleBrowserHandlers(self, printing=True):
		if printing:
			print("\nAvailable browser handlers:")
			for bH in self.possibleBrowserHandlers:
				print("\t%s"%bH)
			print("\n") 
		return self.possibleBrowserHandlers







	def setDatabase(self, dbFilePath="GoogleSearchResults.db", dbTableName="SearchResultUrls", printing=True):
		return self.dbHandler.setDatabase(dbFilePath=dbFilePath, dbTableName=dbTableName, printing=printing)


	
		




	def getTopSearchResults(self,
		numResults,
		searchQueryString=None,

		siteList=[],
		fuzzyTopicsList=[],
		necessaryTopicsList=[],
		inurl=None,
		daterangeFrom=None, 
		daterangeTo=None,


		googleDomain="http://www.google.com",
		resultsPerPage  = 10,
		waitBetweenPages= 150,
		
		printing = True,
		printingDebug = False
		):
		"""
		Extracts and returns a tuple of ordered search results.
		We can pass the exact query itself as a string into 'searchQueryString'. 
		Alternatively, we can pass the items siteList, fuzzyTopicsList, necessaryTopicsList, inurl, daterangeFrom, daterangeTo=None to the function, and it generates the query for us.

		The returned argument is a tuple of two parts: 
			part 1 is the searchQueryString used to generate the results
			part 2 is the tuple of ordered results.

		"""
		if self.canRunBasic(printing=printing) == False:
			return ()		## return an empty tuple


		if searchQueryString==None:
			## check for errors:
			errors = self._checkInputsForErrors(
				necessaryTopicsList=necessaryTopicsList, 
				fuzzyTopicsList=fuzzyTopicsList, 
				siteList=siteList, 
				inurl=inurl, 
				resultsPerPage=resultsPerPage,  
				waitBetweenPages=waitBetweenPages)
		
			if errors!="": 
				if printing:
					print("###-------------------------ERRORS-------------------------###\n%s"%errors)
				return None


			googleSearchQueryObj = self._initializeGoogleSearchQueryObj(
				siteList=siteList, 
				fuzzyTopicsList=fuzzyTopicsList, 
				necessaryTopicsList=necessaryTopicsList, 
				inurl=inurl, 
				daterangeFrom = daterangeFrom, 
				daterangeTo = daterangeTo, 
				printing=printing)

			searchQueryString = googleSearchQueryObj.toString()



		## check for warnings in the data:
		warnings = self._checkInputsForWarnings(resultsPerPage=resultsPerPage, waitBetweenPages=waitBetweenPages)
		if warnings!="":
			if printing:
				print("\n\n\n###-------------------------WARNINGs-------------------------###\n%s"%warnings)


		if printing:
			print("\n\n\nBrowser Handler in use:\n\t%s"%(self.browserHandler.getName()))


		## Actually extract search results.
		resultsLinkDict = self._getSearchResults(
			searchQueryString = searchQueryString,
			googleDomain = googleDomain,
			numResultsRequested = numResults,
			resultsPerPage = resultsPerPage,
			waitBetweenPages = waitBetweenPages,
			printing = printing,
			printingDebug = printingDebug
		)

		## Convert resultsLinkDict into an ordered tuple
		searchResultsList = []
		for pageNo in sorted(resultsLinkDict.keys()):
			for resultUrl in resultsLinkDict[pageNo]:
				searchResultsList.append(resultUrl)

		return (searchQueryString, tuple(searchResultsList)[0:numResults])






	def saveToSQLiteDatabase(self, 
		googleDomain="http://www.google.com",
		necessaryTopicsList=[], fuzzyTopicsList=[], 
		siteList=[], 
		inurl=None, 
		timePeriod=None, numTimePeriodsRemaining=1, 
		resultsPerPage=10, resultsPerTimePeriod=30, 
		resumeFrom=None, 
		waitBetweenPages=150, waitBetweenSearches=180, 
		printing=True, printingDebug=False,
		insertBetweenPages = True, insertBetweenSearches = True, 
		insertOnError = True, 
		skipErroneousSearches = False
		):

		"""This function saves the GoogleSearchResults to a database of your choosing. It is assumed that you may run this function several times with different parameters; the database will remain for all those times. The module sqliteDefaults is used to perform the actual SQLite handling.
		Return values:
			> If None is returned, that means the operation has failed and no results were extracted. 
			> We otherwise return allResults, which is a dictionary indexed by a (startDate, EndDate) pair [it becomes (-1,-1) if no daterange is specified]. Each element in allResults is a dictionary of similar structure to resultsLinkDict, i.e. a dictionary indexed by result page numbers [1 onwards] whose elements are a tuple of search result urls for that page.
		"""
		

		## check for errors:
		errors = self._checkInputsForErrors(dbFilePath=dbFilePath, dbTableName=dbTableName, 
			necessaryTopicsList=necessaryTopicsList, fuzzyTopicsList=fuzzyTopicsList, 
			siteList=siteList, 
			inurl=inurl, 
			timePeriod=timePeriod, numTimePeriodsRemaining=numTimePeriodsRemaining, 
			resultsPerPage=resultsPerPage, resultsPerTimePeriod=resultsPerTimePeriod, 
			resumeFrom=resumeFrom, waitBetweenPages=waitBetweenPages, waitBetweenSearches=waitBetweenSearches)
	
		if errors!="": 
			if printing:
				print("###-------------------------ERRORS-------------------------###\n%s"%errors)
			return None


		# ## Initialize the database.
		# conn = self._SQLiteDBSetup(dbFilePath, dbTableName, printing)
		# if conn == None:
		# 	return None


		## check for warnings in the data:
		warnings = self._checkInputsForWarnings(resultsPerPage=resultsPerPage, waitBetweenPages=waitBetweenPages)
		if warnings!="":
			if printing:
				print("\n\n\n###-------------------------WARNINGs-------------------------###\n%s"%warnings)


		if printing:
			print("\n\n\nBrowser Handler in use:\n%s"%(self.browserHandler.getName()))

		## Actually extract data.

		if timePeriod==None:	## We only get for one time period, thus no dateranges have to be given.
			googleSearchQueryObj = self._initializeGoogleSearchQueryObj(
				siteList=siteList, 
				fuzzyTopicsList=fuzzyTopicsList, 
				necessaryTopicsList=necessaryTopicsList, 
				inurl=inurl,  
				printing=printing)

			resultsLinkDict = self._getSearchResults(
				searchQueryString=googleSearchQueryObj.toString(),
				googleDomain=googleDomain,
				numResultsRequested=resultsPerTimePeriod,
				resultsPerPage  = resultsPerPage,
				waitBetweenPages= waitBetweenPages,
				printing = printing,
				insertBetweenPages=insertBetweenPages,
				printingDebug = printingDebug)

			if self._isEmpty(resultsLinkDict):
				print("GoogleSearch.saveToSQLiteDatabase(): no results obtained.\n")
				return None

			self.dbHandler.insertResultsLinkDictIntoDB(resultsLinkDict=resultsLinkDict, googleSearchQueryObj=googleSearchQueryObj, printing=printing, printingDebug=printingDebug)

			allResults = {}
			allResults[(-1,-1)]=resultsLinkDict


			if printing:
				print("\n\n\n\tDONE GETTING RESULTS FOR TOPIC '%s'\n\n"%(googleSearchQueryObj.getTopicStringForDB()))

			return allResults

		else:
			allResults = self._getStaggeredSearchResults(
				googleDomain=googleDomain,
				necessaryTopicsList=necessaryTopicsList, 
				fuzzyTopicsList=fuzzyTopicsList, 
				siteList=siteList, 
				inurl=inurl, 
				timePeriod=timePeriod, 
				numTimePeriodsRemaining=numTimePeriodsRemaining, 
				resultsPerPage=resultsPerPage, 
				resultsPerTimePeriod=resultsPerTimePeriod, 
				resumeFrom=resumeFrom,

				waitBetweenPages=waitBetweenPages, 
				waitBetweenSearches=waitBetweenSearches, 

				printing=printing, 
				printingDebug=printingDebug, 

				skipErroneousSearches = skipErroneousSearches,
				insertBetweenPages = insertBetweenPages,
				insertBetweenSearches = insertBetweenSearches,
				insertOnError = insertOnError,

				conn=conn, 
				dbTableName=dbTableName,
				dbFilePath=dbFilePath
			)

			if self._isEmpty(allResults):
				if printing:
					print("GoogleSearch.saveToSQLiteDatabase(): no results obtained.\n")
				return None
			return allResults










	##-----------------------------------PRIVATE METHODS-----------------------------------##


	def _doSomeWaiting(self, avgWaitTime, printing=True, waitingBetweenMessage="", countDown=True):
		## Note: this uses global variable stopWaiting, which is modified by ctrl_c_signal_handler()
		
		global keepWaiting

		waitTime=random.uniform(0.3*avgWaitTime, 1.5*avgWaitTime)
		if printing:
			if waitingBetweenMessage=="":
				if printing:
					print("\n\n\t\tWaiting %s seconds."%(waitTime))
			else:
				if printing:
					print("\n\n\t\tWaiting %s seconds between %s."%(waitTime, waitingBetweenMessage))
		startTime = time.time()
		if countDown and printing:
			currentTime = time.time()
			while time.time() - startTime < waitTime and keepWaiting:
				nextTime = time.time()
				if nextTime-currentTime >= 1:
					timeString = "\t\t\tTime remaining: %s seconds.         "%(int(waitTime - (time.time()-startTime)))
					print("\r"+timeString, end="")
					sys.stdout.flush()
					currentTime = time.time()
				# time.sleep(max(0,time.time()-currentTime-0.1))	## <-does not allow Ctrl+C behaviour.

			print("\r\t\tDone waiting.                                           ")
			print("\n")

			if keepWaiting==False:		## used for signal handling.
				keepWaiting = True
				self.browserHandler.resetBrowser()

		else:
			time.sleep(waitTime)





	def _getSearchResults(self, 
		searchQueryString,
		numResultsRequested,
		googleDomain="http://www.google.com",
		resultsPerPage  = 10,
		waitBetweenPages= 150,
		printing = True,
		printingDebug = False,
		conn = None, dbTableName=None, insertBetweenPages = False, googleSearchQueryObj=None
		):
		

		"""
		Returns the dictionary 'resultsLinkDict', which contains all the links in an organized manner:
			resultsLinkDict[i] is a ordered tuple of results of the i'th page (i starts from 1).
			resultsLinkDict[i][j] is an item containing the j'th URL on the i'th page.
			
			The last page may not have all the links, so the correct way to index this dict is:
		## for resultPage in resultsLinkDict:
		##     for resultUrl in resultPage:
		##         <code/>

		
		"""
		if self.hasImportedNecessaryModules()==False:
			if printing:
				print("\n\tGoogleSearch._getSearchResults(): cannot proceed because the necessary modules are not present.")
			return {}



		warnings = self._checkInputsForWarnings(resultsPerPage=resultsPerPage, waitBetweenPages=waitBetweenPages)
		if warnings!="":
			if printing:
				print("\n\n\n###-------------------------WARNINGs-------------------------###\n%s"%warnings)


		if printing:
			print("\n\tTrying to execute query:\n\t\t%s"%searchQueryString)

		resultsLinkDict={}	
		searchResultsObtained=0;	## keeps track of the TOTAL number of search results obtained. 

		## Ideally, 'searchResultsObtained' should be exactly 'numResultsRequested' after this function completes. 
		## However, if the query itself has only 'X' results, where X < numResultsRequested (we requested 'numResultsRequested' results), then 'searchResultsObtained' should be X by the end of this function, i.e. we get all the possible results; we should also print a message warning the caller that it was not possible to get numResultsRequested.

		pageCount=0;

		# numResultsRequested=int(math.ceil(numResultsRequested/10))


		firstResultsPageHTML = self.browserHandler.getInitialGoogleSearchResultsPageHtml(searchQueryString=searchQueryString, googleDomain=googleDomain, errorPrinting=printingDebug)
		## We have now clicked the button on the www.google.com page. Now it is time to extract the links.


		googleParser = self.GoogleWebsiteParser.GoogleWebsiteParser()
		totalNumResultsFromSearch = googleParser.extractTotalNumberOfResultsFromQuery(
			htmlString=firstResultsPageHTML, 
			printing=printing,
			printingDebug=printingDebug
			)

		if totalNumResultsFromSearch!=None:
			if printing:
				print("\n\tYour query has about %s results in total. We will try to get the top %s results\n"%(totalNumResultsFromSearch, numResultsRequested))

		firstPageResultUrls = googleParser.extractResultUrlsFromGoogleSearchResultsPageHtml(htmlString=firstResultsPageHTML, printing=printing, printingDebug=printingDebug)

		
		if firstPageResultUrls == None or firstPageResultUrls==[]:
			if printing:
				print("\n\n\t\tGoogleSearch._getSearchResults(): your query,\n\t\t\t%s\n\t\t...returned no results. This might be due to your IP getting blocked, or there may be no results for your query."%(searchQueryString))
			return None


		## Now, we know we have returned SOME results for the first page:
		pageCount=1;
		searchResultsObtained = searchResultsObtained+len(firstPageResultUrls);
		resultsLinkDict[1] = firstPageResultUrls	## is a tuple

		if printing:
			# print("fizbo")
			print("\n\t\t\tCurrent page number:%s\n\t\t\tResults obtained so far: (%s/%s)."%(pageCount, searchResultsObtained, numResultsRequested))
			for printingResUrl in resultsLinkDict[1]:
				print("\t\t\t\t%s"%printingResUrl)

		if numResultsRequested <= searchResultsObtained:	## We WANTED < 10 results, i.e. the first 'X' results, where X <= 10
			resultsLinkDict[1] = resultsLinkDict[1][0:numResultsRequested]
			return resultsLinkDict


		if insertBetweenPages and conn!=None and dbTableName!= None:
			self._insertGetSearchResults(
				conn=conn, 
				dbTableName=dbTableName,
				numResultsRequested=numResultsRequested,
				pageCount=pageCount, 
				pageResultUrls=firstPageResultUrls,
				googleSearchQueryObj=googleSearchQueryObj,
				printing=printing,
				printingDebug = printingDebug)
		
		

		## Get the other pages of results:

		currentPageHTML = firstResultsPageHTML
		
		while searchResultsObtained < numResultsRequested:

			if searchResultsObtained >= totalNumResultsFromSearch:
				if printing:
					print("\n\n\t\tGoogleSearch._getSearchResults(): your query,\n\t\t\t%s\n\t\t..only had %s results, not %s as you requested. All were extracted."%(searchQueryString, searchResultsObtained, numResultsRequested))
				return resultsLinkDict



			## We first see if the next page exists, then we _doSomeWaiting()
			nextPageUrl = googleParser.extractNextGoogleSearchResultsPageLink(
							htmlString=currentPageHTML, 
							googleDomain=googleDomain, 
							printing=printing,
							printingDebug=printingDebug
			)


			if nextPageUrl==None:
				if printing:
					print("\n\n\t\tGoogleSearch._getSearchResults(): your query,\n\t\t\t%s\n\t\t...has only obtained %s results, not %s as you requested."%(searchQueryString, searchResultsObtained, numResultsRequested))
				return resultsLinkDict


			if resultsPerPage != 10:
				resultsPerPage = min(max(resultsPerPage,10), 100)	## You cannot get more than 100 results per page.
				nextPageUrl+="&num=%s"%resultsPerPage


			## Wait period between searches
			if waitBetweenPages!=None:
					self._doSomeWaiting(waitBetweenPages, printing=printing, waitingBetweenMessage="pages")
			else:	
				self._doSomeWaiting(120, printing=printing, waitingBetweenMessage="pages")




			## go to next page
			currentPageHTML = self._tryGetCurrentPageHTML(nextPageUrl=nextPageUrl, printing=printing, printingDebug=printingDebug)

			if currentPageHTML==None:
				if printing:
					print("\n\n\t\tGoogleSearch._getSearchResults(): unable to visit next results page. This might be due to network issues and browser issues, or your IP may be getting blocked.")
				return resultsLinkDict



			## get next page results.
			currentPageResultUrls = googleParser.extractResultUrlsFromGoogleSearchResultsPageHtml(htmlString=currentPageHTML, printing=printing, printingDebug=printingDebug)


			if currentPageResultUrls==None:
				if printing:
					print("\n\n\t\tGoogleSearch._getSearchResults(): unable to extract results from the HTML (usually, this is caused by CAPTCHA being triggered). This may be due to your IP getting blocked.")
				return resultsLinkDict
			
			pageCount += 1


			searchResultsObtained = searchResultsObtained + len(currentPageResultUrls)
			
			resultsLinkDict[pageCount] = currentPageResultUrls

			if printing:
				print("\n\n\t\t\tCurrent page number:%s\n\t\t\tResults obtained so far: (%s/%s)."%(pageCount,searchResultsObtained, numResultsRequested))
				for printingResUrl in resultsLinkDict[pageCount]:
					print("\t\t\t\t%s"%printingResUrl)

			if insertBetweenPages and conn!=None and dbTableName!= None:
				self._insertGetSearchResults(
					conn=conn, 
					dbTableName=dbTableName,
					numResultsRequested=numResultsRequested,
					pageCount=pageCount, 
					pageResultUrls=currentPageResultUrls,
					googleSearchQueryObj=googleSearchQueryObj,
					printing=printing,
					printingDebug = printingDebug)


			# if insertBetweenPages and conn!=None and dbTableName!= None:
			# 	self._insertGetSearchResults(
			# 		conn=conn, 
			# 		dbTableName=dbTableName,
			# 		numResultsRequested=numResultsRequested,
			# 		pageCount=pageCount, 
			# 		pageResultUrls=currentPageResultUrls,
			# 		googleSearchQueryObj=googleSearchQueryObj,
			# 		printing=printing,
			# 		printingDebug = printingDebug)


			# ## if we have got as many as we need
			# if searchResultsObtained + len(currentPageResultUrls) >= numResultsRequested:	
			# 	resultsLinkDict[pageCount] = currentPageResultUrls[0:numResultsRequested-searchResultsObtained]
			# 	if printing:
			# 		# print("dumbo")
			# 		print("\n\t\t\tCurrent page number:%s\n\t\t\tResults obtained so far: (%s/%s)."%(pageCount, searchResultsObtained, numResultsRequested))
			# 	return resultsLinkDict

			# ## We have not got enough results, so keep going:
			# else:	
			# 	searchResultsObtained = searchResultsObtained + len(currentPageResultUrls);
			# 	resultsLinkDict[pageCount] = currentPageResultUrls
			# 	if printing:
			# 		# print("lolbo")
			# 		print("\n\t\t\tCurrent page number:%s\n\t\t\tResults obtained so far: (%s/%s)."%(pageCount, searchResultsObtained, numResultsRequested))

			self.browserHandler.clearBrowserData()

		if printingDebug:
			print("\n\n\n\n\nGoogleSearch._getSearchResults(): resultsLinkDict = ")
			for printingPageNum in sorted(resultsLinkDict.keys()):
				print("\tPage #%s"%printingPageNum)
				for printingResUrl in resultsLinkDict[printingPageNum]:
					print("\t\t%s"%printingResUrl)




		return resultsLinkDict







	def _insertGetSearchResults(self, 
		conn, 
		dbTableName,
		numResultsRequested, 
		googleSearchQueryObj,
		pageCount, 
		pageResultUrls,
		printing, 
		printingDebug
		):

		tempDict = {}
		try:
			if printingDebug:
				print("pageCount:%s\n%s\n\n"%(pageCount,pageResultUrls))
			tempDict[pageCount] = pageResultUrls
			self._insertResultsLinkDictIntoDB(conn=conn, 
				dbTableName=dbTableName, 
				resultsLinkDict=tempDict, 
				googleSearchQueryObj=googleSearchQueryObj, 
				printing=printing,
				printingDebug = printingDebug
			)
		except Exception, e:
			if printing:
				print("\n\t\tGoogleSearch._insertGetSearchResults(): cannot insert page results into database.")
				print("\t\tError description: %s\n"%e)







	def _getStaggeredSearchResults(self, 
		googleDomain,
		necessaryTopicsList, 
		fuzzyTopicsList, 
		siteList, 
		inurl, 
		timePeriod, 
		numTimePeriodsRemaining, 
		resultsPerPage, 
		resultsPerTimePeriod, 
		resumeFrom, 

		waitBetweenPages, 
		waitBetweenSearches, 
		
		printing, 
		printingDebug,
		
		insertBetweenPages, 
		insertBetweenSearches, 
		insertOnError, 
		skipErroneousSearches,

		conn=None, 
		dbFilePath=None,
		dbTableName=None
		
		):
		
		"""
		This is a helper function to others, it actually extracts the data over multiple time periods.
		If conn and dbTableName are passed non-Nonetype values, it is assumed we want to insert into DB. 

		Even if not, the function returns allResults, which is a dictionary of dictionaries. It holds all the staggered results over several time periods. It is indexed by a tuple of the daterange. 
		e.g. 
		allResults[(2449588,2449618)] = ('"Infosys" site:financialtimes.com daterange:2449588-2449618', resultsLinkDict)
		
		allResults is returned regardless of wether we insert into the database or not. 
		Along with it is returned a status message: if we are successful, we return True. If we are not successful, we return False.


		"""


		## Find if we have run this query before and there is any date to resume from.
		startDate, endDate, actualNumTimePeriodsRemaining = self._determineWhenToResumeFromDB(
			conn=conn, 
			dbTableName=dbTableName, 
			fuzzyTopicsList=fuzzyTopicsList, 
			necessaryTopicsList=necessaryTopicsList, 
			resumeFrom=resumeFrom, 
			timePeriod=timePeriod, 
			numTimePeriodsRemaining=numTimePeriodsRemaining, 
			printing=printing)

		if printingDebug:
			print("As returned from _determineWhenToResumeFromDB():\nstartDate = %s, endDate=%s, actualNumTimePeriodsRemaining=%s"%(startDate, endDate, actualNumTimePeriodsRemaining))



		googleSearchQueryObj = self._initializeGoogleSearchQueryObj(siteList=siteList, fuzzyTopicsList=fuzzyTopicsList, necessaryTopicsList=necessaryTopicsList, inurl=inurl, 
			daterangeFrom = startDate, daterangeTo = endDate, 
			printing=printing)

		topic = googleSearchQueryObj.getTopicStringForDB()

		if printing:
			self._printExtractionStats(dbFilePath=dbFilePath, dbTableName=dbTableName, googleDomain=googleDomain, topic=topic, inurl=inurl, timePeriod=timePeriod, numTimePeriodsRemaining=actualNumTimePeriodsRemaining, resultsPerTimePeriod=resultsPerTimePeriod, resultsPerPage=resultsPerPage, waitBetweenPages=waitBetweenPages, waitBetweenSearches=waitBetweenSearches
			)

		if actualNumTimePeriodsRemaining == 0:
			if printing:
				print("\n\n\n\tDONE GETTING RESULTS FOR TOPIC '%s'\n\n"%(topic))
			return {}


		else:
			if printing:
				if actualNumTimePeriodsRemaining < numTimePeriodsRemaining:
					print("\n\n\tTopic\n\t\t%s\nwas found in database.\n\tResuming from Julian date: %s. \n\tRemaining: %s time periods of %s days each.\n"%(topic, endDate, actualNumTimePeriodsRemaining, timePeriod))
				else:
					print("\n\n\tNo topic in database matches:\n\t\t%s\n\tStarting new topic entry, from Julian date: %s.\n\tRemaining: %s time periods of %s days each.\n"%(topic, endDate, actualNumTimePeriodsRemaining, timePeriod))

		

		## Actually start extracting:
		allResults = {}

		for i in range(0, actualNumTimePeriodsRemaining):
			resultsLinkDict = None

			try:	## perform one entire search.

				if insertBetweenPages:
					resultsLinkDict = self._extractAndInsertByPage(conn=conn, dbTableName=dbTableName, googleSearchQueryObj=googleSearchQueryObj,  googleDomain=googleDomain, numResultsRequested=resultsPerTimePeriod, resultsPerPage=resultsPerPage, waitBetweenPages=waitBetweenPages, printing=printing, printingDebug=printingDebug)
					
				elif insertBetweenSearches:
					resultsLinkDict = self._extractAndInsertBySearch(conn=conn, dbTableName=dbTableName, googleSearchQueryObj=googleSearchQueryObj,  googleDomain=googleDomain, numResultsRequested=resultsPerTimePeriod, resultsPerPage=resultsPerPage, waitBetweenPages=waitBetweenPages, printing=printing, printingDebug=printingDebug)
				


			except Exception, e:
				if printing:
					print("\n\n\n\tGoogleSearch._getStaggeredSearchResults(): An error occured while extracting urls.")
					print("\t\tError description: %s\n"%e)
				if printingDebug:
					print("\nPrinting stack traceback:\n")
					traceback.print_stack()
					print("\n\n\n")

				if insertOnError:
					if self._isEmpty(resultsLinkDict) == False:
						self._insertResultsLinkDictIntoDB(conn=conn, dbTableName=dbTableName, 
							resultsLinkDict=resultsLinkDict,
							googleSearchQueryObj=googleSearchQueryObj, printing=printing
						)




			if self._isEmpty(resultsLinkDict) and skipErroneousSearches==False:
				return allResults
						

			if self._isEmpty(resultsLinkDict)==False:
				allResults[googleSearchQueryObj.getDateRangeTuple()] = (googleSearchQueryObj.toString(), resultsLinkDict)

			if printing:
				print("\n\tREMAINING: %s time_period of results."%(actualNumTimePeriodsRemaining-i-1))
			
			if actualNumTimePeriodsRemaining-i-1 == 0:
				if printing:
					print("\n\n\n\tDONE GETTING RESULTS FOR TOPIC '%s'\n\n"%(topic))
				return allResults


			googleSearchQueryObj.goToPreviousDateRange()

			if printing:
				print("\n\n\n\n\n\n\tWAITING BEFORE NEXT SEARCH QUERY IS FIRED...")
			self._doSomeWaiting(avgWaitTime=waitBetweenSearches, printing=printing, waitingBetweenMessage="searches")

		return allResults





	def _extractAndInsertBySearch(self, 
		conn, dbTableName,
		googleSearchQueryObj, 
		googleDomain,
		numResultsRequested,
		resultsPerPage,
		waitBetweenPages,
		printing,
		printingDebug
		):

		resultsLinkDict = self._getSearchResults(
			searchQueryString = googleSearchQueryObj.toString(),
			googleDomain = googleDomain,
			numResultsRequested = numResultsRequested,
			resultsPerPage = resultsPerPage,
			waitBetweenPages = waitBetweenPages,
			printing = printing,
			printingDebug = printingDebug
		)


		self._insertResultsLinkDictIntoDB(conn=conn, 
			dbTableName=dbTableName, 
			resultsLinkDict=resultsLinkDict, 
			googleSearchQueryObj=googleSearchQueryObj, 
			printing=printing,
			printingDebug = printingDebug
		)

		return resultsLinkDict




	def _extractAndInsertByPage(self, 
		conn, dbTableName,							
		googleDomain,		
		numResultsRequested,	
		resultsPerPage,		
		waitBetweenPages,
		googleSearchQueryObj,	
		printing,			
		printingDebug			
		):
		resultsLinkDict={}
		try: 
			resultsLinkDict = self._getSearchResults(
				searchQueryString = googleSearchQueryObj.toString(),
				googleDomain = googleDomain,
				numResultsRequested = numResultsRequested,
				resultsPerPage = resultsPerPage,
				waitBetweenPages = waitBetweenPages,
				printing = printing,
				printingDebug = printingDebug,
				conn = conn, dbTableName=dbTableName, insertBetweenPages = True, googleSearchQueryObj=googleSearchQueryObj
			)
		except Exception:
			if printing:
				print("\n\t\tGoogleSearch._extractAndInsertByPage(): there was an error running function _getSearchResults(), and as a result the search was not completed fully.")

		if self._isEmpty(resultsLinkDict) == False:
			self._insertResultsLinkDictIntoDB(conn=conn, 
				dbTableName=dbTableName, 
				resultsLinkDict=resultsLinkDict, 
				googleSearchQueryObj=googleSearchQueryObj, 
				printing=False,
				printingDebug = printingDebug
			)
		else:
			if printing:
				print("\n\t\tGoogleSearch._extractAndInsertByPage(): cannot insert into database as the resultant urls dictionary i.e. resultsLinkDict, is empty.")


		return resultsLinkDict

















	def _isEmpty(self, thing, exceptThisThing="\!@#$%^&*()[]:;?<>,.1234567890/"):		
		"""Checks if 'thing' is empty; returns True for a bunch of empty things; only exceptThisThing is permitted.
		"""
		if thing!=exceptThisThing and (thing==None or thing=="" or thing==[] or thing=={} or thing==()):
			return True
		return False


	def _isIntegerInRange(self, n, lowerBound=None, upperBound=None):
		if type(n)!=type(0):
			return False
		elif lowerBound!=None and upperBound!=None and (n<lowerBound or n>upperBound):
			return  False
		elif upperBound!=None and n>upperBound:
			return False
		elif lowerBound!=None and n<lowerBound:
			return False

		return True



	def _checkInputsForErrors(self, 
		necessaryTopicsList, 
		fuzzyTopicsList, 
		siteList, 
		inurl, 

		resultsPerPage=None, 
		resultsPerTimePeriod=None, 

		timePeriod=None, 
		numTimePeriodsRemaining=None, 


		resumeFrom=None, 
		waitBetweenPages=None, 
		waitBetweenSearches=None,

		dbFilePath=None, 
		dbTableName=None
		):

		errorFunctionBase = "\n\tERROR in GoogleSearch._checkInputsForErrors(): "
		errors = ""


		## check dbFilePath and dbTableName:
		if self._isEmpty(dbFilePath, None):
			errors+=errorFunctionBase+"The SQLite file name (i.e. dbFilePath variable) cannot be None or an empty string."

		elif dbFilePath!=None and dbFilePath.endswith(".db") == False:
			errors+=errorFunctionBase+"The SQLite file must be a .db file."


		if self._isEmpty(dbTableName, None):
			errors+=errorFunctionBase+"The SQLite table name (i.e. dbTableName variable) cannot be None or an empty string."



		## check fuzzyTopicsList and necessaryTopicsList:
		if self._isEmpty(fuzzyTopicsList) and self._isEmpty(necessaryTopicsList):
			errors+=errorFunctionBase+"both fuzzyTopicsList and necessaryTopicsList cannot be empty or None."
			

		if self._isEmpty(fuzzyTopicsList)==False and type(fuzzyTopicsList)!=type([]):
			errors+=errorFunctionBase+"if fuzzyTopicsList is not empty, it must be a list of strings."
			
		if self._isEmpty(necessaryTopicsList)==False and type(necessaryTopicsList)!=type([]):
			errors+=errorFunctionBase+"if necessaryTopicsList is not empty, it must be a list of strings."


		## check siteList:
		if self._isEmpty(siteList)==False and type(siteList)!=type([]):
			errors+=errorFunctionBase+"if siteList is not empty, it must be a list of strings."

		## check inurl:
		if self._isEmpty(inurl, ""):
			errors+=errorFunctionBase+'if inurl is to be empty, set it to "".'
		elif inurl!=None and type(inurl)!=type(""):
			errors+=errorFunctionBase+'inurl, if not None, must be a string with no spaces.'
		elif inurl!=None and inurl.find(" ") != -1:
			errors+=errorFunctionBase+'inurl must be a string with no spaces.'


		## check 'timePeriod', 'numTimePeriodsRemaining', 'resultsPerPage', 'resultsPerTimePeriod', 'resumeFrom', 'waitBetweenPages', 'waitBetweenSearches' :
		
		if timePeriod!=None and self._isIntegerInRange(timePeriod, lowerBound=1) == False:
			errors+=errorFunctionBase+"timePeriod must be an integer greater than 0, or None."

		if numTimePeriodsRemaining!=None and self._isIntegerInRange(numTimePeriodsRemaining, lowerBound=1) == False:
			errors+=errorFunctionBase+"numTimePeriodsRemaining must be an integer, greater than 0."
		
		if resultsPerPage!=None and self._isIntegerInRange(resultsPerPage, lowerBound=10, upperBound=100) == False:
			errors+=errorFunctionBase+"resultsPerPage must be an integer between 10 and 100, or None."
		
		if resultsPerTimePeriod!=None and self._isIntegerInRange(resultsPerTimePeriod, lowerBound=1) == False:
			errors+=errorFunctionBase+"resultsPerTimePeriod must be an integer greater than 0, or None."
		
		if resumeFrom!=None and self._isIntegerInRange(resumeFrom, lowerBound=2440588) == False:	## start of UNIX time, i.e. 1 Jan 1970
			errors+=errorFunctionBase+"resumeFrom must be an integer greater than 2440587, or None."
		
		if waitBetweenPages!=None and self._isIntegerInRange(waitBetweenPages, lowerBound=0) == False:
			errors+=errorFunctionBase+"waitBetweenPages must be an integer greater than -1, or None."
		
		if waitBetweenSearches!=None and self._isIntegerInRange(waitBetweenSearches, lowerBound=0) == False:
			errors+=errorFunctionBase+"waitBetweenSearches must be an integer greater than -1, or None."

		return errors





	def _checkInputsForWarnings(self, resultsPerPage, waitBetweenPages):
		warningFunctionBase = "\n\n\tWARNING in GoogleSearch._checkInputsForWarnings(): "
		warnings = ""
		
		## check ratio of resultsPerPage to waitBetweenPages:
		resultsPerPagetowaitBetweenPagesRatioWarning = warningFunctionBase+"the wait time between pages may not be large enough to prevent IP blocking."+"\n\tRecommend wait time between pages: %s seconds or more."

		if resultsPerPage <= 20 and waitBetweenPages/float(resultsPerPage) < 150/float(10):
			warnings+=resultsPerPagetowaitBetweenPagesRatioWarning%(10*( int(resultsPerPage*( 150/float(10) )/10) ))

		elif resultsPerPage > 20 and resultsPerPage <= 50 and waitBetweenPages/float(resultsPerPage) < 240/float(20):
			warnings+=resultsPerPagetowaitBetweenPagesRatioWarning%(10*( int(resultsPerPage*( 240/float(20) )/10) ))
			
		elif resultsPerPage > 50 and resultsPerPage <= 80 and waitBetweenPages/float(resultsPerPage) < 450/float(50):
			warnings+=resultsPerPagetowaitBetweenPagesRatioWarning%(10*( int(resultsPerPage*( 450/float(50) )/10) ))
			
		elif resultsPerPage >80 and resultsPerPage < 100 and waitBetweenPages/float(resultsPerPage) < 540/float(80):
			warnings+=resultsPerPagetowaitBetweenPagesRatioWarning%(10*( int(resultsPerPage*( 540/float(80) )/10) ))

		elif resultsPerPage == 100 and waitBetweenPages/float(resultsPerPage) < 600/float(100):
			warnings+=resultsPerPagetowaitBetweenPagesRatioWarning%(10*( int(resultsPerPage*( 600/float(100) )/10) ))

		return warnings





	def _printExtractionStats(self, dbFilePath, dbTableName, googleDomain, topic, inurl, timePeriod, numTimePeriodsRemaining, resultsPerTimePeriod, resultsPerPage, waitBetweenPages, waitBetweenSearches):

		print("\n\n\n###-------------------------EXTRACION STATS-------------------------###\n")
		print("dbFilePath = %s"%(dbFilePath))
		print("dbTableName = %s"%(dbTableName))
		print("googleDomain = %s"%(googleDomain))
		print("topic = %s"%(topic))
		if inurl!="":
			print("inurl = %s"%inurl)
		print("timePeriod = %s days"%(timePeriod))
		print("numTimePeriodsRemaining = %s"%(numTimePeriodsRemaining))
		print("resultsPerTimePeriod = %s"%(resultsPerTimePeriod))
		print("resultsPerPage = %s"%(resultsPerPage))
		print("waitBetweenPages = %s seconds"%(waitBetweenPages))
		print("waitBetweenSearches = %s seconds"%(waitBetweenSearches))






	def _initializeGoogleSearchQueryObj(self, 
		siteList=[],
		fuzzyTopicsList=[],
		necessaryTopicsList=[],
		inurl=None,
		daterangeFrom=None,
		daterangeTo=None,
		printing=False
		):

		gs = self.GoogleSearchQuery.GoogleSearchQuery()
		if siteList != []:
			gs.setSiteList(siteList=siteList, printing=printing)
		if fuzzyTopicsList != []:
			gs.setFuzzyTopicsList(fuzzyTopicsList=fuzzyTopicsList, printing=printing)
		if necessaryTopicsList != []:
			gs.setNecessaryTopicsList(necessaryTopicsList=necessaryTopicsList, printing=printing)
		if inurl!=None:
			gs.setInUrl(inurl=inurl, printing=printing)
		if daterangeFrom!=None and daterangeTo!=None:
			gs.setDateRange(daterangeFrom=daterangeFrom, daterangeTo=daterangeTo, printing=printing)
		return gs













	def _tryGetCurrentPageHTML(self, nextPageUrl, printing=True, printingDebug=False):
		## We attempt to get the HTML of a page.3 times before giving up.
		try:
			self.browserHandler.go(nextPageUrl)
			currentPageHTML = self.browserHandler.getCurrentPageHtml()
			if currentPageHTML==None: 
				x=1/0
		except Exception:
			try:
				self._doSomeWaiting(avgWaitTime=15, printing=False)
				currentPageHTML = self.browserHandler.getHtml(url=nextPageUrl)
				if currentPageHTML==None: 
					x=1/0
			except Exception:
				try:
					if self.browserHandler.clearBrowserData() == False:
						if printing:
							print("\n\tGoogleSearch._tryGetCurrentPageHTML(): Cannot clear browser data.")
					self.browserHandler.go(nextPageUrl)
					currentPageHTML = self.browserHandler.getCurrentPageHtml()
					if currentPageHTML==None:	
						x=1/0
				except Exception:
					if self.browserHandler.resetBrowser() == False:
						if printing:
							print("\n\tGoogleSearch._tryGetCurrentPageHTML(): Cannot reset browser.")
					self.browserHandler.go(nextPageUrl)
					currentPageHTML = self.browserHandler.getCurrentPageHtml()
		if printingDebug:
			print("GoogleSearch._tryGetCurrentPageHTML(): Length of HTML obtained: %s"%(len(currentPageHTML)))
		return currentPageHTML




	def _determineWhenToResumeFromDB(self, 
		conn, 
		dbTableName, 
		fuzzyTopicsList, 
		necessaryTopicsList, 
		resumeFrom, 
		timePeriod, 
		numTimePeriodsRemaining, 
		printing
		):

		tempGoogleSearchQueryObj = self.GoogleSearchQuery.GoogleSearchQuery()
		tempGoogleSearchQueryObj.setFuzzyTopicsList(fuzzyTopicsList)
		tempGoogleSearchQueryObj.setNecessaryTopicsList(necessaryTopicsList)
		topic = tempGoogleSearchQueryObj.getTopicStringForDB()

		startDate = endDate = 0
		initialStartDate = tempGoogleSearchQueryObj._convertToValidJulianDate(datetime.datetime.now().date())
		
		resultsSortedByDateQuery = "SELECT StartDate, EndDate FROM %s WHERE Topic='%s' ORDER BY StartDate ASC"%(dbTableName, topic)
		urlsSortedByDate = self.sqliteDefaults.verified_select_sqlite(conn, resultsSortedByDateQuery, printing=False)

		if len(urlsSortedByDate) == 0:
			endDate = initialStartDate
			

		else: 	
			lastExtractedDate = urlsSortedByDate[0][0]	## Gets the StartDate of the last extracted URL
			endDate = lastExtractedDate		## We must resume googlesearching from this date

			if resumeFrom != None and resumeFrom!=-1:
				endDate = resumeFrom		## resume_from should be set to the start date of the latest period in which no urls were extracted. NOTE: once you find a time period in which you DO get some UNIQUE urls, you should not use resume_from in subsequent runs.


			numTimePeriodsPassed = int(round((initialStartDate - endDate)/timePeriod))	## WHATEVER YOU DO, THE PRODUCT OF timePeriod*numTimePeriodsRemaining should remain constant,
			numTimePeriodsRemaining = numTimePeriodsRemaining - numTimePeriodsPassed

		startDate = endDate - timePeriod
		return startDate, endDate, numTimePeriodsRemaining















import signal


def ctrl_c_signal_handler(signal_number, frame):
    global keepWaiting
    print("\n\n")
    option=""
    while option!=1 and option!=2 and option!=3:	## While it is not an integer
		option=raw_input("Program is paused. Enter an option:\n1.Exit\n2.Continue\n3.Continue, skip waiting.\n>")
		try:
 	 		option=int(option)
 	 	except Exception:
 	 		print("\n\tERROR: Please enter an integer value.\n")
 	 		if type(option)!=type("str"):
 	 			exit()

 	 	if type(option)==type(0):	## if 'option' is an integer
	  		if option==1:	## Exit
	  			exit()
	  		# if option==2:	## paused
	  		# 	yorn=""
	  		# 	while yorn !='n' and yorn !='N' and yorn!='y' and yorn!='Y':
	 	 	# 		yorn=raw_input("\nResume execution? (Y/n):\n>")
	  		# 		if yorn=='y' or yorn=='Y':
	  		# 			break
	  		# 		if yorn=='n' or yorn=='N':
	  		# 			exit()
	  		if option==2:	## Continue
	  			break
	  		if option==3:
	  			keepWaiting = False
	  			break
	  		

signal.signal(signal.SIGINT, ctrl_c_signal_handler)		## assign ctrl_c_signal_handler to Ctrl+C, i.e. SIGINT








###-----------------------------TESTS-----------------------------###
# g = GoogleSearch()

# g._doSomeWaiting(avgWaitTime=30, printing=True, countDown=True, waitingBetweenMessage="things")


# tempDict = g.saveToSQLiteDatabase( 
# 	googleDomain="http://www.google.com",
# 	necessaryTopicsList=['Microsoft'], fuzzyTopicsList=['innovations'], 
# 	siteList=[], 
# 	inurl='micro', 
# 	timePeriod=100, numTimePeriodsRemaining=3, 
# 	resultsPerPage=10, resultsPerTimePeriod=25, 
# 	waitBetweenPages=150, waitBetweenSearches=210, 
# 	printing=True
# )


# tempDict = g.saveToSQLiteDatabase( 
# 	googleDomain="http://www.google.com",
# 	necessaryTopicsList=['Microsoft'], fuzzyTopicsList=['innovations'], 
# 	siteList=[], 
# 	inurl='micro', 
# 	resumeFrom = 2457347,
# 	timePeriod=100, numTimePeriodsRemaining=3, 
# 	resultsPerPage=10, resultsPerTimePeriod=25, 
# 	waitBetweenPages=150, waitBetweenSearches=210, 
# 	printing=True
# )



# tempDict = g.saveToSQLiteDatabase( 
# 	googleDomain="http://www.google.com",
# 	necessaryTopicsList=[], fuzzyTopicsList=['AI learning'], 
# 	siteList=[], 
# 	inurl="", 
# 	timePeriod=100, numTimePeriodsRemaining=3, 
# 	resultsPerPage=10, resultsPerTimePeriod=15, 
# 	waitBetweenPages=150, waitBetweenSearches=210, 
# 	printing=True,
# 	insertBetweenPages=True
# )


# tempDict = g.saveToSQLiteDatabase( 
# 	googleDomain="http://www.google.com",
# 	necessaryTopicsList=[], fuzzyTopicsList=['poker champion vegas'], 
# 	siteList=["www.reddit.com","www.tumblr.com"], 
# 	inurl="",  
# 	resultsPerPage=10, resultsPerTimePeriod=15, 
# 	timePeriod=100, numTimePeriodsRemaining=3,
# 	waitBetweenPages=150, 
# 	printing=True,
# 	insertBetweenPages=True
# )




# resTup = g.getTopSearchResults(
# 	searchQueryString='iphone 6s california',
# 	numResults=30,
# 	googleDomain="http://www.google.co.in",
# 	resultsPerPage  = 10,
# 	waitBetweenPages= 150,
# 	printing = True,
# 	printingDebug = False)
# print("\n\n\nResults obtained from query:\n\t%s\n\t..."%resTup[0])
# for resUrl in resTup[1]:
# 	print("\t%s"%resUrl)
# print("\n")









# import datetime
# resTup = g.getTopSearchResults(
# 	googleDomain="http://www.google.com",
# 	necessaryTopicsList=['apple'], fuzzyTopicsList=['watch'], 
# 	siteList=["wired.com"], 
# 	inurl=None, 
# 	daterangeFrom = datetime.date(2013,01,01),
# 	daterangeTo = datetime.date(2016,01,01)
	
# 	numResults=25,
# 	resultsPerPage  = 10,
# 	waitBetweenPages= 150,
# 	printing = True,
# 	printingDebug = False)
# print("\n\n\nResults obtained from query:\n\t%s\n\t..."%resTup[0])
# for resUrl in resTup[1]:
# 	print("\t%s"%resUrl)
# print("\n")




		
		







			
