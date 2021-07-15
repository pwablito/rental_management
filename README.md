# Rental Management

An application to manage apartment rentals

## API KEY

To setup the Google Maps API, you must obtain an API key. For information on how to get the key, visit the [Google Maps API Console](https://developers.google.com/maps/documentation/javascript/get-api-key).

Once you have the key, place it in `client/src/main.js` where it says `<INSERT_API_KEY_HERE>`

Now, the production and development servers should work.

## Production

The production server can be deployed with Docker Compose. To setup and run the server, use `docker-compose up`.

## Development server

To setup database:

```bash
./setup_db.sh
```


To run development server:

```bash
./run.sh
```
Then navigate to `http://127.0.0.1/` in your browser


## Documentation

For documentation on the API, see [API.md](API.md)

## Author: Paul Spencer
