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


The main thing you need to know here is how the routes works, rather than the underlying functionality. Feel free to explore the code yourself! It's almost identical to this [FastAPI [:material-arrow-right-bottom:]](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) security tutorial just with a bit of Zentra flair.

Okay, now let's check out our routes!

## Routes

!!! note

    All authentication routes start with [`api/auth/`](#routes)! 

Zentra API has four starting authentication routes:

1. [`/api/auth/users/me`](#get-user) - retrieves the user's own details, if they are authenticated.
2. [`/api/auth/register`](#register-user) - creates a user in the database given a `username` and `password`.
3. [`/api/auth/token`](#login-for-access-token) - provides an access token for the user, if their login details are correct
4. [`/api/auth/verify-token/{token}`](#verify-user-token) - verifies that an access token is valid (e.g., hasn't expired yet)

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

Next, we have the login for access token route. This generates a new access token when a user provides valid login credentials. 

It's specific to JSON Web Tokens (JWTs) and is a common way to securely login your users. 

JWTs are out of the scope of this tutorial, but we highly recommend you check out these links from [JWT.io [:material-arrow-right-bottom:]](https://jwt.io/introduction) and [Auth0 [:material-arrow-right-bottom:]](https://auth0.com/learn/json-web-tokens) for more information.

Here's an example of the routes responses:

=== "202 Accepted"

    ```json title=""
    {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzI2NDMwMTc5fQ.hvEZ8j-IclgSufY58I_5hB0L4mEtkhkjHORygohMs50",
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

    [`/api/auth/verify-token/{token}`](#verify-user-token)

The final route compliments the previous one and simplify verifies that an access token is valid using your `AUTH__SECRET_KEY` in your `.env` file. 

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

## Future Plans

So far our routes focus on JWT tokens and OAuth2 authentication. This is great for most use cases but sometimes you may need something a little more extensive such as Oauth2 scopes, cookies, or API keys. 

We have plans to integrate these in the future, but ultimately it's up to you to decide what type of authentication you need. Zentra is just an extension on top of FastAPI, so the possibilities are truly endless. ✨

---

Okay, now that we understand more about our authentication, let's move onto our **project settings**. See you there! 😁
