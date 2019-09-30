# Matega API Documentation

# NOTE: THIS DOCUMENTATION IS DEPRECATED AND HAS BEEN DISCONTINUED, SINCE NO EXTERNAL API IS NEEDED AT THIS POINT


## Chefs

### Application
To **submit a new application** or update an existing one, send a `POST` request to <br>
```
    /api/application/
```

with the data <br>
```JSON
{
  "user": <Integer>,
  "text": <String>
}
```
To **delete an application**, send a ```DELETE``` request to <br>
```
    /api/application/
```
with the data <br>
```JSON
{
  "user": <Integer>
}
```
This will delete the application connected to the userID.

