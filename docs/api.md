# API Documentation

## Authentication

All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication Endpoints

#### Register
- **URL**: `/api/v1/auth/register`
- **Method**: `POST`
- **Body**:
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "full_name": "Full Name"
}
```

#### Login
- **URL**: `/api/v1/auth/login`
- **Method**: `POST`
- **Body** (form data):
```
username: username
password: password123
```
- **Response**:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### User Endpoints

#### Get Current User
- **URL**: `/api/v1/users/me`
- **Method**: `GET`
- **Auth**: Required

#### Get All Users
- **URL**: `/api/v1/users/`
- **Method**: `GET`
- **Auth**: Required (Admin only)
- **Query Parameters**:
  - `skip`: int (default: 0)
  - `limit`: int (default: 100)

#### Get User by ID
- **URL**: `/api/v1/users/{user_id}`
- **Method**: `GET`
- **Auth**: Required (Admin only)

#### Create User
- **URL**: `/api/v1/users/`
- **Method**: `POST`
- **Auth**: Required (Admin only)

#### Update User
- **URL**: `/api/v1/users/{user_id}`
- **Method**: `PUT`
- **Auth**: Required (User can update themselves, Admin can update anyone)

#### Delete User
- **URL**: `/api/v1/users/{user_id}`
- **Method**: `DELETE`
- **Auth**: Required (Admin only)

### Item Endpoints

#### Get All Items
- **URL**: `/api/v1/items/`
- **Method**: `GET`
- **Auth**: Required
- **Query Parameters**:
  - `skip`: int (default: 0)
  - `limit`: int (default: 100)

#### Get Item by ID
- **URL**: `/api/v1/items/{item_id}`
- **Method**: `GET`
- **Auth**: Required

#### Create Item
- **URL**: `/api/v1/items/`
- **Method**: `POST`
- **Auth**: Required
- **Body**:
```json
{
  "title": "Item Title",
  "description": "Item Description"
}
```

#### Update Item
- **URL**: `/api/v1/items/{item_id}`
- **Method**: `PUT`
- **Auth**: Required (Owner only)

#### Delete Item
- **URL**: `/api/v1/items/{item_id}`
- **Method**: `DELETE`
- **Auth**: Required (Owner only)

## Error Responses

All errors follow this format:
```json
{
  "detail": "Error message"
}
```

Common status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `409` - Conflict
- `500` - Internal Server Error

