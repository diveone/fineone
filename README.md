# Configuration

Set-up environment variables:
* FINONE_CONFIG
* Credentials
* SECRET_KEY
* Add env variable: APP_CONFIG_file=/path/to/config/dev.py


# API Documentation

## Rate Quotes
```
GET `api/v1/rate-quote` 		Rate quote list
GET `api/v1/rate-quote/:id`		Specific product
```

## Requests (Administrative only)
```
GET `api/v1/requests`			List of requests
GET `api/v1/requests/:id`		Request detail w/ quotes link (paginated)
```

## HTTP Responses
```
200		OK				Success
201		Created			Successfully created
204		No content 		Success but no content
400		Bad Request		Client error; bad data
401		Unauthorized	Not authenticated
403		Forbidden		Not authorized
404		Not Found		Resource doesn't exist
405		Not Allowed		Method forbidden
```


