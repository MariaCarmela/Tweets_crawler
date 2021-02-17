#API GOOGLE
GMAPS_API_KEY= "Your_gmaps_api_key"
# API TWITTER
APP_KEY="Your_twitter_api_key"
APP_SECRET="Your_twitter_secret_key"
OAUTH_TOKEN="Your_twitter_authentication_token"
OAUTH_TOKEN_SECRET="Your_twitter_authentication_secret_token"

#This case is for the city of Rome
# Rome's latitude and longitude (bounding box) 
LAT_MIN = 41.8080113
LONG_MIN = 12.3836430
LAT_MAX = 41.9817915
LONG_MAX = 12.6074895

# Coordinates of Rome [needed for Google maps]
MAP_LAT = (LAT_MAX + LAT_MIN)/2
MAP_LONG =  (LONG_MAX + LONG_MIN)/2
MAP_RADIUS = max(abs(LAT_MAX-LAT_MIN), abs(LONG_MAX-LONG_MIN))
