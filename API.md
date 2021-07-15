# API Documentation

## `/api/login`

Method: `POST`

Request Body: json

```json
{
    "username": String,
    "password": String
}
```

Response Body: json

```json
{
    "success": Boolean,
    "token": String,
    "user": {
        "username": String,
        "name": String,
        "type": String,
        "created_on": String
    },
    "message": String
}
```

Notes:
- `message` will be present any time `success` is false.
- `type` will be either `client`, `realtor`, or `admin`


## `/api/register`

Method: `POST`

Request Body: json

```json
{
    "username": String,
    "password": String,
    "name": String
}
```

Response Body: json

```json
{
    "success": Boolean,
    "token": String,
    "user": {
        "username": String,
        "name": String,
        "type": String,
        "created_on": String
    },
    "message": String
}
```

Notes:
- `message` will be present any time `success` is false.
- `type` will be `client`


## `/api/create_listing`

Method: `POST`

Request Body: json

```json
{
    "token": String,
    "name": String,
    "description": String,
    "floor_area": Number,
    "price": Number,
    "rooms": Number,
    "bathrooms": Number,
    "latitude": Number,
    "longitude": Number,
    "is_listed": Boolean,
    "realtor": String
}
```

Response Body: json

```json
{
    "success": Boolean,
    "id": String,
    "message": String
}
```

Notes:
- `message` will be present any time `success` is false.
- `id` is the identifier randomly assigned to the new listing
- `token` must belong to a user with the `admin` or `realtor` type


## `/api/create_user`

Method: `POST`

Request Body: json

```json
{
    "token": String,
    "name": String,
    "username": String,
    "password": String
}
```

Response Body: json

```json
{
    "success": Boolean,
    "message": String
}
```

Notes:
- `message` will be present any time `success` is false.
- `token` must belong to a user with the `admin` type

## `/api/get_listings`

Method: `POST`

Request Body: json

```json
{
    "token": String
}
```

Response Body: json

```json
{
    "success": Boolean,
    "listings": [
        {
            "id": String,
            "name": String,
            "description": String,
            "floor_area": Number,
            "price": Number,
            "rooms": Number,
            "bathrooms": Number,
            "latitude": Number,
            "longitude": Number,
            "is_listed": Boolean,
            "created_on": String,
            "realtor": String
        }
    ],
    "message": String
}
```

Notes:
- `message` will be present any time `success` is false.
- `token` may belong to a user with any type
- `client` users will only see listings that have `is_listed` set to true


## `/api/get_users`

Method: `POST`

Request Body: json

```json
{
    "token": String
}
```

Response Body: json

```json
{
    "success": Boolean,
    "users": [
        {
            "id": String,
            "username": String,
            "name": String,
            "type": String,
            "created_on": String
        }
    ],
    "message": String
}
```

- `message` will be present any time `success` is false.
- `token` must belong to a user with the `admin` type 


## `/api/update_listing`

Method: `POST`

Request Body: json

```json
{
    "token": String,
    "listing": {
        "id": String,
        "name": String,
        "description": String,
        "floor_area": Number,
        "price": Number,
        "rooms": Number,
        "bathrooms": Number,
        "latitude": Number,
        "longitude": Number,
        "is_listed": Boolean,
        "realtor": String
    }
}
```

Response Body: json

```json
{
    "success": Boolean,
    "message": String
}
```

- `message` will be present any time `success` is false.
- `token` must belong to a user with the `admin` or `realtor` type


## `/api/update_user`

Method: `POST`

Request Body: json

```json
{
    "token": String,
    "user": {
        "username": String,
        "name": String,
        "type": String
    }
}
```

Response Body: json

```json
{
    "success": Boolean,
    "message": String
}
```

- `message` will be present any time `success` is false.
- `token` must belong to a user with the `admin` type



## `/api/delete_listing`

Method: `POST`

Request Body: json

```json
{
    "token": String,
    "id": String
}
```

Response Body: json

```json
{
    "success": Boolean,
    "message": String
}
```

- `message` will be present any time `success` is false.
- `token` must belong to a user with the `admin` or `realtor` type
- `id` is the identifier of the listing to be deleted


## `/api/delete_user`

Method: `POST`

Request Body: json

```json
{
    "token": String,
    "username": String
}
```

Response Body: json

```json
{
    "success": Boolean,
    "message": String
}
```

- `message` will be present any time `success` is false.
- `token` must belong to a user with the `admin` type
- `username` is the username of the user to be deleted
