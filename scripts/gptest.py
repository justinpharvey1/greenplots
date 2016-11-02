import requests



#Utility score
UTILITY_SCORE_KEY = '8wfxqbwq'
HAS_HOME_DATA = True
UTILITY_SCORE_URL = 'http://api.myutilityscore.com/getutilityscore'
requestHeaders = {'Api-Key':UTILITY_SCORE_KEY}
utilityData = requests.post(UTILITY_SCORE_URL, headers = requestHeaders, data = {"has_property_data":HAS_HOME_DATA,"home_type":"SF","city":"San Francisco, CA","post_code":"91342","area_unit":"foot","year_built":"1948","home_area":"1600","lot_area":"3200"})



#Rainfall data
RAINFALL_URL = 'https://www.melissadata.com/lookups/ZipWeather.asp?ZipCode=03755&submit1=Submit'
rainfallData = requests.get(RAINFALL_URL)
rainfallHTML = rainfallData.text
rainfallParts = rainfallHTML.split("Yearly Total")
rainfallParts = rainfallParts[1].split(">")
rainfallParts = rainfallParts[9].split("<")
annualRainfall = rainfallParts[0]



#Air quality data 
AIR_SCORE_KEY = 'ADED5391-1CE4-418E-83B2-4677E364793C'
AIR_SCORE_URL = 'http://www.airnowapi.org/aq/observation/latLong/current'
airDataParams = {'format': 'application/json', 'latitude': '38.3651', 'longitude': '-114.4141', 'distance': '100', 'API_KEY': AIR_SCORE_KEY}
airData = requests.get(AIR_SCORE_URL, params=airDataParams)




print airData.json()




