# User Authentication

Now let's discuss something integral to almost every project: **user authentication**. 

I can't tell you how many hours we've spent thinking about this topic, mulling over what frameworks to use, how to integrate it with our databases, etc. Talk about boring! 😴

Thankfully, [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/tutorial/security/) makes it extremely easy, and with Zentra it's straight out of the box! 😍

We abstract a lot of the details away using the [`zentra_api`](../lib/index.md) package to keep things simple for you, but still give you the freedom to configure authentication how you want!

Our authentication files live in the `app/auth` directory, shown below. 

```cmd title="Authentication Directory"
<project_name>/
├── app/
│   ├── ...
│   ├── auth/
│   │   └── __init__.py
│   │   └── responses.py
│   │   └── schema.py
│   ├── ...
...
```

You may have noticed that the folder follows the exact same file structure as the routes we created in the [Creating Routes](../../api/tutorial/create-routes.md) tutorial. We've done this deliberately!

The `auth` directory is just another set of API routes but separated for convenience. 

!!! danger "Auth Reset"

    Don't like how we've done things? Just delete the folder and start fresh! Don't worry, we won't be offended! 😉

!!! warning

    Technically, there is a little more you should remove when getting rid of the `auth` routes, such as the configuration settings and the database models 😅, but simply removing the folder is good enough to disable the routes. 

    We plan to add a `--no-auth` flag in a future version that will do all of this for you, but 9 times out of 10 you'll need authentication anyway! 😁


The main thing you need to know here is how the routes work, rather than the underlying functionality. Feel free to explore the code yourself! It's an extension of the [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) security tutorial with refresh tokens and a bit of Zentra flair 😉.

Okay, now let's check out our routes!

## Routes

!!! note

    All authentication routes start with [`api/auth/`](#routes). This simple naming convention keeps our API consistent and easy to use.

    We follow the same pattern with our token routes - [`api/auth/token`](#routes).

Zentra API has five starting authentication routes:

1. [`/api/auth/users/me`](#get-user) - retrieves the user's own details, if they are authenticated.
2. [`/api/auth/register`](#register-user) - creates a user in the database given a `username` and `password`.
3. [`/api/auth/token`](#login-for-access-token) - provides an access token for the user, if their login details are correct
4. [`/api/auth/token/verify/{token}`](#verify-user-token) - verifies that an access token is valid (e.g., hasn't expired yet)
5. [`/api/auth/token/refresh`](#refresh-access-token) - creates a new access token from the refresh token 

### Get User

??? api "Route"

    [`/api/auth/users/me`](#get-user)

So we know this route get's the user's details, but what details? Well, this depends on two factors:

1. What user information you are storing in the database
2. What information the `GetUser` response model has access to

By default, we use two separate database tables for our users: 

1. `DBUserDetails` for personal information, and
2. `DBUser` for login credentials 

We've found this to be effective for both performance and security, especially when storing a lot of personal information. 

Here's our tables:

```python title="db_models/user.py"
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from app.core.db import Base


class DBUser(Base):
    """A model of the `User` table."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)


class DBUserDetails(Base):
    """A model of the `UserDetails` table."""

    __tablename__ = "user_details"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email = Column(String, unique=True, default=None)
    phone = Column(String, unique=True, default=None)
    full_name = Column(String, default=None)
```

Notice how we only capture three main details here: the user's `full_name`, `email`, and `phone` number. Feel free to update this as needed! 😁

So, what about our `GetUser` response model? Using a bit of [Pydantic [:material-arrow-right-bottom:]](https://docs.pydantic.dev/latest/) ✨ (courtesy of FastAPI) and Python class inheritance, we combine the `UserBase` with the `UserDetails` model.

```python title="auth/schema.py" hl_lines="22-23"
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., description="A unique username to identify the user")


class CreateUser(UserBase):
    password: str = Field(
        ..., description="The users password to login to the platform"
    )
    is_active: bool = Field(default=True, description="The users account status")


class UserDetails(BaseModel):
    email: str | None = Field(default=None, description="The users email address")
    phone: str | None = Field(default=None, description="The users contact number")
    full_name: str | None = Field(default=None, description="The users full name")
    is_active: bool = Field(..., description="The users account status")


class GetUser(UserBase, UserDetails):
    pass
```

So our data could look like this:

```json title="Example Data JSON"
{
    "email": "johndoe@email.com",
    "phone": "+44123456789",
    "full_name": "Agent 47",
    "is_active": true,
    "username": "agent47",
}
```

Great! That's simple enough, but should we really only be sending this information through our route? It's not very informative. Surely, there's a better way?

This is where one of Zentra's unique features come in! When passing our response model through a `zentra_api.responses.SuccessResponse` we get a way more detailed and informative JSON response. 

For this specific route, here's our responses:

=== "200 Ok"

    ```json title=""
    {
        "status": "success",
        "code": 201,
        "response": "200_OK",
        "data": {
            "email": "johndoe@email.com",
            "phone": "+44123456789",
            "full_name": "Agent 47",
            "is_active": true,
            "username": "agent47",
        },
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    }
    ```

=== "400 Bad Request"

    ```json title=""
    {
        "status": "error",
        "code": 400,
        "response": "400_BAD_REQUEST",
        "message": "User already registered.",
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    }
    ```

=== "401 Unauthorized"

    ```json title=""
    {
        "status": "error",
        "code": 401,
        "response": "401_UNAUTHORIZED",
        "message": "Not authenticated.",
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    }
    ```

Like ✨, we now immediately see if the response is successful, what type of response code is passed, we get the same data we needed, and get to see any HTTP headers that were passed with the request. 

Your API's just got a whole lot funner to work with! 😁

!!! tip

    You can learn more about how these responses work in our [Route Responses](../../api/route-responses.md) page. 

Onto the next one!

### Register User

??? api "Route"

    [`/api/auth/register`](#register-user)

Unlike our previous route, that reads information from the database, this one adds a new user to the `DBUser` table. 

Instead of using the `GetUser` response model, it uses the `CreateUser` response model.

```python title="auth/schema.py" hl_lines="8-12"
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(..., description="A unique username to identify the user")


class CreateUser(UserBase):
    password: str = Field(
        ..., description="The users password to login to the platform"
    )
    is_active: bool = Field(default=True, description="The users account status")


class UserDetails(BaseModel):
    email: str | None = Field(default=None, description="The users email address")
    phone: str | None = Field(default=None, description="The users contact number")
    full_name: str | None = Field(default=None, description="The users full name")
    is_active: bool = Field(..., description="The users account status")


class GetUser(UserBase, UserDetails):
    pass
```

This is pretty self-explanatory. Given three values: `username`, `password`, and `is_active`; we create a new user in the database.

Here's an example of the routes responses:

=== "201 Created"

    ```json title=""
    {
        "status": "success",
        "code": 201,
        "response": "201_CREATED",
        "data": {
            "username": "agent47"
        },
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    }
    ```

=== "400 Bad Request"

    ```json title=""
    {
        "status": "error",
        "code": 400,
        "response": "400_BAD_REQUEST",
        "message": "User already registered.",
        "headers": null
    }
    ```

### Login For Access Token

??? api "Route"

    [`/api/auth/token`](#login-for-access-token)

Next, we have our login route for retrieving an access and refresh token. Access and refresh tokens are JSON Web Tokens (JWTs) that act as a form of authentication to the API. They both have a slightly different purpose. Here's a brief overview:

- **Access token** - allows the user to use the API
- **Refresh token** - acts as a user session for a period of time 

In our case, we use the `HS256` algorithm for encryption with a `15` minute expiry for access tokens and a `7` day expiry for refresh tokens. They use the `AUTH__SECRET_ACCESS_KEY` and `AUTH__SECRET_REFRESH_KEY`, respectively, found in your `.env` file. 

??? info "Updating Auth Settings"

    We want to provide a solution that works out of the box without overwhelming you with configuration settings, so we deliberately fixed the algorithm and expiry times - it's less things to worry about!

    However, if you need more flexibility you can tweak these settings using the `.env` file. Here's an example:

    ```toml title=".env" hl_lines="5-7"
    ...
    # Authentication configuration details
    AUTH__SECRET_ACCESS_KEY=c_KnbHr01TI5qjsAZoGLpeZrpdK4u5AOy7RXHFpsMeE # (1)!
    AUTH__SECRET_REFRESH_KEY=M2Myg1Z2vfUNHzIBVcsKhZCcFi6n4knNLv57Gip6a3M
    AUTH__ALGORITHM="HS256" # (2)!
    AUTH__ACCESS_TOKEN_EXPIRE_MINS=15  # (3)!
    AUTH__REFRESH_TOKEN_EXPIRE_MINS=10080  # (4)!
    ...
    ```

    1. The JWT encryption keys. Keep them secret, keep them safe! 🤫 
    2. The encryption algorithm. Currently, this is limited to three options: `['HS256', 'HS384', 'HS512']`
    3. The access token expiration time in minutes
    4. The refresh token expiration time in minutes. `10080 = 7 days`. This always lasts longer than your access token

JWTs are out of the scope of this tutorial, but if you want to learn more, we highly recommend you check out these links from [JWT.io [:material-arrow-right-bottom:]](https://jwt.io/introduction) and [Auth0 [:material-arrow-right-bottom:]](https://auth0.com/learn/json-web-tokens).

Here's an example of the routes responses:

=== "202 Accepted"

    ```json title=""
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI1ODg2MjkwfQ.9nkNDi-_6uel6nUIiAHELrB8j1CqK1h-N7hx2QwRYxw",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI2NDkwMTkwfQ.pw5wtaLPq14h0nzbbhSmq-C1qfwYsLsxvNTozzfG4HM",
        "token_type": "bearer"
    }
    ```

=== "401 Unauthorized"

    ```json title=""
    {
        "status": "error",
        "code": 401,
        "response": "401_UNAUTHORIZED",
        "message": "Incorrect username or password.",
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    }
    ```

### Verify User Token

??? api "Route"

    [`/api/auth/token/verify/{token}`](#verify-user-token)

This route compliments the previous one and simply verifies that an access token is valid using your `AUTH__SECRET_ACCESS_KEY` in your `.env` file. 

Here's an example of the routes responses:

=== "200 Ok"

    ```json title=""
    {
        "status": "success",
        "code": 200,
        "response": "200_OK",
        "message": "Token is valid.",
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    }
    ```

=== "401 Unauthorized"

    ```json title=""
    {
        "status": "error",
        "code": 401,
        "response": "401_UNAUTHORIZED",
        "message": "Not authenticated.",
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    }
    ```

### Refresh Access Token

??? api "Route"

    [`/api/auth/token/refresh`](#refresh-access-token)

The last route is another simple one! Given a refresh token it creates a new access token for the user.

When working with frontend applications, you'll often find yourself using this route and the token verification one together. After all, when an access token expires, you'll need to refresh it!

Here's an example of the routes responses:

=== "201 Created"

    ```json title=""
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI1ODg2MzQzfQ.rQBlpSx6UQgz8U52mSeVqb6-B7Xe8vKUTVO4ghJyaQU",
        "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI2NDkwMTkwfQ.pw5wtaLPq14h0nzbbhSmq-C1qfwYsLsxvNTozzfG4HM",
        "token_type": "bearer"
    }
    ```

=== "401 Unauthorized"

    ```json title=""
    {
        "status": "error",
        "code": 401,
        "response": "401_UNAUTHORIZED",
        "message": "Invalid refresh token.",
        "headers": {
            "WWW-Authenticate": "Bearer"
        }
    }
    ```

## Future Plans

So far our routes focus on JWT tokens and OAuth2 authentication. This is great for most use cases but sometimes you may need something a little more extensive such as Oauth2 scopes, cookies, or API keys. 

We have plans to integrate these in the future, but ultimately it's up to you to decide what type of authentication you need. Zentra is just an extension on top of FastAPI, so the possibilities are truly endless. ✨

---

Okay, now that we understand more about our authentication, let's move onto our **project settings**. See you there! 😁
