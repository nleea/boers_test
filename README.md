This repository contains the solution for a software development project, divided into two main areas:

Database: Design and development of an entity-relationship model, along with advanced SQL queries.
Backend Development: Implementation of a data-driven application using Django.

# Estructura del proyecto

```boers
|
├── config
|    ├── app -> Configuration files (base, dev, prod)
|    ├── core -> Constants, middleware, settings, JSON seed files
|    ├── db -> Database configuration file
|    ├── server -> ASGI, WSGI, and URL configuration files
├── docker
|    ├── Dockerfile
|    ├── docker-compose
|    ├── .dockerignore
└── src
|    ├── application -> Business logic of the application
|    ├── domain -> External entities (e.g., error handling)
|    ├── infrastructure -> Core services
|    ├── interfaces -> Helpers and utilities```


## Application 

```├── auth_module
|    ├── api -> Views, validators, serializers, services, and URLs
|    ├── migrations -> Database migration files
|    ├── models -> Database models
|    ├── repositories -> Service implementations for communication between the user and the application```


## **UserViewSet API**

## Description

`UserViewSet` is a Django ViewSet that manages user-related operations, including listing, retrieving, creating, updating, and deleting users. It interacts with a service layer (`get_service`) that handles business logic and repository operations.

## **Methods**  

### `get_serializer_class(self)`
Determines the serializer class to use based on the action being performed.

- **Returns**:
  - `UserCreateSerializer` for `create` actions.
  - `UserUpdateSerializer` for `update` actions.
  - `UserSerializer` as the default.

### `get_service(self)` (Property)
Returns the appropriate user service instance from `AuthModuleRepositoryFactory`, passing the selected serializer class.

- **Returns**: `UserService` instance.

### `list(self, request)`
Retrieves a list of all users.

- **Request Method**: `GET`
- **Returns**: JSON response containing all users.

### `retrieve(self, request, pk=None)`
Retrieves a specific user by ID.

- **Request Method**: `GET`
- **Parameters**:
  - `pk` (str): The ID of the user to retrieve.
- **Returns**: JSON response containing user details or `404 NOT FOUND` if the user does not exist.

### `create(self, request)`
Creates a new user.

- **Request Method**: `POST`
- **Request Body**: JSON containing user data.
- **Returns**: JSON response containing the created user data or `400 BAD REQUEST` if validation fails.

### `update(self, request, pk=None)`
Updates an existing user by ID.

- **Request Method**: `PUT`
- **Parameters**:
  - `pk` (str): The ID of the user to update.
- **Request Body**: JSON containing updated user data.
- **Returns**: JSON response with updated user data or `400 BAD REQUEST` if validation fails.

### `destroy(self, request, pk=None)`
Deletes a user by ID.

- **Request Method**: `DELETE`
- **Parameters**:
  - `pk` (str): The ID of the user to delete.
- **Returns**: Success response or `404 NOT FOUND` if the user does not exist.

## Usage
This ViewSet is designed to be used with Django REST Framework and can be included in `urls.py` using a `router`:

```python
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = router.urls
```

This will generate the following API endpoints:
- `GET /user/` → List all users
- `GET /user/{pk}/` → Retrieve a specific user
- `POST /user/` → Create a new user
- `PUT /user/{pk}/` → Update an existing user
- `DELETE /user/{pk}/` → Delete a user


## **Authentication API (AuthView)**  

The `AuthView` class handles authentication-related actions, including login, password recovery, and password updates.  

## **Methods**  

### **`login(request)`**  
Handles user authentication and returns an access token.  

- **Method:** `POST`  
- **Request Body:**  
  ```json
  {
    "email": "user@example.com",
    "password": "yourpassword"
  }
  ```
- **Response:**  
  - **200 OK**: Returns a token upon successful authentication.  
  - **401 Unauthorized**: If credentials are invalid.  

**Example Response:**  
```json
{
  "token": {
    "access": "your_access_token",
    "refresh": "your_refresh_token"
  }
}
```

### **`forget_password(request)`**  
Generates a password reset token and sends it via email.  

- **Method:** `POST`  
- **Request Body:**  
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:**  
  - **200 OK**: If the email was found, the reset link is sent.  
  - **400 Bad Request**: If the email field is missing.  
  - **404 Not Found**: If the email does not match any user.  

**Example Response:**  
```json
{
  "message": "Email sent"
}
```

### **`change_password(request)`**  
Updates the user’s password using a valid reset token.  

- **Method:** `POST`  
- **Request Body:**  
  ```json
  {
    "token": "reset_token",
    "new_password": "newSecurePassword"
  }
  ```
- **Response:**  
  - **200 OK**: If the password was successfully updated.  
  - **400 Bad Request**: If the token or new password is missing or invalid.  

**Example Response:**  
```json
{
  "message": "Password updated"
}
```

---

### **Notes:**  
- The `AuthView` service interacts with the authentication module repository to validate users and update credentials.  
- The `forget_password` method sends an email containing a password reset link and token.  
- The `change_password` method validates the token before updating the password.


## **Instrucciones de uso**

Crear el **.env**, hay un ejemplo de las variables de entornos necesitadas en el archvo **.env.example**

Se instalan las dependencias 

### **Using Poetry**

Poetry is a dependency management tool that simplifies package installation and environment management.

1️⃣ Install Poetry (if not installed)

pip install poetry

2️⃣ Navigate to Your Project Directory
cd /path

3️⃣ Install Dependencies from pyproject.toml
poetry install

### **Using pip with requirements.txt**

1️⃣ Create a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies from requirements.txt

pip install -r requirements.txt

Run migrations:

```sh
poetry: poetry run python manage.py migrate
---
python: python manage.py migrate
```

la semilla corre, ya que se encuentra relacionada con el con la migracion


Inicio del proceso

# **AUTH**

## URL: http://0.0.0.0:8000/auth/login/

- **Method:** `POST`  
- **Request Body:**  
  ```json
  {
    "email":"admin@example.com",
    "password": "123456"
  }
  ```
## O

- **Method:** `POST`  
- **Request Body:**  
  ```json
  {
    "username":"admin",
    "password": "123456"
  }
  ```

- **Return:**
```json 
{
    "status": 200,
    "errors": null,
    "data": {
        "token": {
            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTIwNDE5OSwiaWF0IjoxNzQxMTE3Nzk5LCJqdGkiOiJhYTMzMDgzZTU4NGQ0MzQ4Yjc4ZTU5OTIxZGQyNTllYiIsInVzZXJfaWQiOjF9.2-lRnzodVziMSenPxUnLNokrIX7gyIAG_MkPNYe2MW4",
            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxMTYwOTk5LCJpYXQiOjE3NDExMTc3OTksImp0aSI6IjJhYjkwOWMxYmQ2ZjRhMDQ5NDc1M2Y1YWI1OTE1OTI2IiwidXNlcl9pZCI6MX0.Zv-GbsERGnfTFbY-2Hck8Pwf6M_M1lZ7h-kmPohBOI4"
        }
    },
    "method": "POST",
    "url": "/auth/login/"
}
```

# **Forget Password**

## URL: http://0.0.0.0:8000/auth/forget_password/

- **Method:** `POST`  
- **Request Body:**  
  ```json
  {
      "email": "neldecas12@gmail.com"
  }
  ```
- **Return:**
```json
  {
      "status": 200,
      "errors": null,
      "data": {
          "message": "Email sent"
      },
      "method": "POST",
      "url": "/auth/forget_password/"
  }
 ```

 Luego de esto ir al correo y copiar el token

[IMAGE 1](./img/email_change_password.png)

# **Change Password**

## URL: http://0.0.0.0:8000/auth/change_password/

- **Method:** `POST`  
- **Request Body:**  
  ```json
  {
      "token": "689ef44e-ed38-433e-9ebe-3cc69c5fbdd2",
      "new_password": "qwER12Q@3e"
  }
  ```
Con el token relacionado a un usuario se puede cambiar la contrase~a de este

# **User API**

## URL: http://0.0.0.0:8000/user/
- **Method:** `POST`  
- **Request Body:**  
  ```json
  {
      "username": "TEST769",
      "password": "5588sdjRR@s",
      "person": {
          "fullname": "TEST",
          "email": "user22460864@example.com"
      }
  }
  ```
- **Return:**
```json
  {
      "status": 200,
      "errors": null,
      "data": {
          "id": 11,
          "username": "TEST769",
          "person": {
              "id": 10,
              "fullname": "TEST",
              "email": "user22460864@example.com"
          }
      },
      "method": "POST",
      "url": "/user/"
  }
 ```

## URL: http://0.0.0.0:8000/user/
- **Method:** `GET`  
- **Request Body:**  
  NONE
- **Return:**
```json
  {
      "status": 200,
      "errors": null,
      "data": [
          {
              "id": 1,
              "username": "admin",
              "person": null
          },
      ]
  }
 ```
## URL: http://0.0.0.0:8000/user/:id/
- **Method:** `PUT`  
- **Request Body:**  
  ```json
  {
      "username": "TEST4",
      "active": false,
      "person": {
          "fullname": "TEST4"
      }
  }
  ```
- **Return:**
```json
  {
      "status": 200,
      "errors": null,
      "data": {
          "id": 2,
          "username": "TEST4",
          "person": {
              "id": 1,
              "fullname": "TEST4",
              "email": "jane.smith@example.com"
          },
          "active": false
      },
      "method": "PUT",
      "url": "/user/2/"
  }
 ```
## URL: http://0.0.0.0:8000/user/:id/
- **Method:** `DELETE`  
- **Request Body:**  
  NONE
- **Return:**
```json
  {
      "status": 200,
      "errors": null,
      "data": {
          "message": "Usuario con ID :id eliminado correctamente."
      },
      "method": "DELETE",
      "url": "/user/7/"
  }
 ```

 ## **NOTES**

 Utiliza el sistema smtp por facilidad en el envio de correos
 Se debe colocar un email y una contrase~a de aplicaciones en las variables de entorno
 EMAIL_HOST_USER=''
 EMAIL_HOST_PASSWORD=''

## **Docker**

Se utilizo docker y docker compose para la orquestacion
**USAR**

```sh
docker compose up
```

en la carpeta docker del proyecto


# **IMPORTANTE**
Crear el archivo .env en la raiz del proyecto para que se puedan utilizar las variables de entorno

O si se va utilizar docker tambien se puede definir las variables en el docker-compose.yml, ya estan definidas algunas, estan comentadas