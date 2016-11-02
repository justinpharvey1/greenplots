import sys
import logging
import requests
from requests.auth import HTTPDigestAuth



event = {"body": {"params": {"zipcode": "03755", "acreage": "1", "beds": "1", "baths": "1", "price": "100000", "solar": "true", "electricheater": "true", "wellwater": "true", "insulation": "true"}}}


#parse payload
payload = event['body']
params = payload['params']


zipCode = params['zipcode']
acreage = params['acreage']
beds = params['beds']
baths = params['baths']
price = params['price']
hasSolar = params['solar']
hasElectricHeater = params['electricheater']
hasWellWater = params['wellwater']
hasInsulation = params['insulation']


#Authentication 
RETS_USERNAME = "99262idx"
RETS_PASSWORD = "DVFGD7PSYh6yCt6RGzvf"
RETS_LOGIN_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/login?rets-version=rets/1.8"
loginParams = {'username': RETS_USERNAME, 'password': RETS_PASSWORD}

session = requests.session()

loginResponse = session.get(RETS_LOGIN_URL, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
print "\n\n", loginResponse.text

#Search for Properties
RETS_SEARCH_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/search"
searchQuery = "(ListPrice=" + str(price) + "+),(" + "Beds=" + beds + "+)"
searchParams = {'SearchType': 'Property', 'Class': 'ResidentialProperty', 'QueryType': 'DMQL2', 'Format': 'COMPACT', 'StandardNames': '1', 'Select': 'ListingID,ListPrice', 'Query': searchQuery, 'Count': '1', 'Limit': '15', 'rets-version': 'rets/1.8'}
searchResponse = session.get(RETS_SEARCH_URL, params=searchParams, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
print "Results: \n", searchResponse.text


#Logout the session 
RETS_LOGOUT_URL = "http://neren.rets.paragonrels.com/rets/fnisrets.aspx/NEREN/Logout"
logoutParams = {'rets-version': 'rets/1.8.2'}
logoutResponse = session.get(RETS_LOGOUT_URL, params=logoutParams, auth=HTTPDigestAuth(RETS_USERNAME, RETS_PASSWORD))
print "Logout: \n", logoutResponse, "\n\n\n"

