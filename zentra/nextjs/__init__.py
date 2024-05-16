from typing import Optional

from zentra.core import LOWER_CAMELCASE_SINGLE_WORD, Component, has_valid_pattern
from zentra.core.enums.ui import LibraryType

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

from zentra.custom import CustomUrl


class NextJs:
    """A Zentra model for all [NextJS](https://nextjs.org/docs/app/api-reference/components) components."""

    @property
    def library(self) -> str:
        return LibraryType.NEXTJS.value


class UrlQuery(BaseModel, NextJs):
    """
    A model for the [NextJS URL object](https://nextjs.org/docs/app/api-reference/components/link#with-url-object) used within the [NextJS Link](https://nextjs.org/docs/app/api-reference/components/link) component.

    Parameter:
    - `pathname` (`string`) - the name of the route to link to. Can be predefined (e.g., `/about`) or dynamic (e.g., `/blog/[slug]`). Must start with a `/`
    - `query` (`dict[string, string]`) - a dictionary object containing the query parameters and values assigned to them. Start values with a `$` to indicate they are a function parameter. Otherwise, they are treated as a static value

    Example usage:
    1. A predefined route (`/about?name=test`).
    ```python
    from zentra.nextjs import Url

    Url(pathname="/about", query={'name': 'test'})
    ```
    JSX equivalent ->
    ```jsx
    {{
        pathname: '/about',
        query: { name: 'test' },
    }}
    ```

    2. A dynamic route (`/blog/my-post`)
    ```python
    Url(pathname="/blog/[slug]", query={'slug': 'my-post'})
    ```
    JSX equivalent ->
    ```jsx
    {{
        pathname: '/blog/[slug]',
        query: { slig: 'my-post' },
    }}
    ```

    3. A predefined route with a function parameter (`/about?name={name}`)
    ```python
    from zentra.nextjs import Url

    Url(pathname="/about", query={'name': '$name'})
    ```
    JSX equivalent ->
    ```jsx
    {{
        pathname: '/about',
        query: { name: name },
    }}
    ```
    """

    pathname: str
    query: dict[str, str]

    @field_validator("pathname")
    def validate_pathname(cls, pathname: str) -> str:
        if not pathname.startswith("/"):
            raise PydanticCustomError(
                "invalid_string",
                "must start with a '/'",
                dict(wrong_value=pathname),
            )
        return pathname


class StaticImage(BaseModel, NextJs):
    """
    A model for [NextJS local images](https://nextjs.org/docs/app/building-your-application/optimizing/images#local-images) used within the [NextJS Image](https://nextjs.org/docs/app/api-reference/components/image) component.

    Parameter:
    - `name` (`string`) - the import variable name for the image. Must be `lowercase` or `camelCase`, a `single world` and up to a maximum of `30` characters
    - `path` (`string`) - the import path to the image. E.g., `'./me.png'`

    Example usage:
    1. A profile picture.
    ```python
    from zentra.nextjs import StaticImage

    StaticImage(name='profilePic', path='./me.png')
    ```
    JSX equivalent ->
    ```jsx
    import Image from 'next/image'
    import profilePic from './me.png'

    <Image src={profilePic} />
    ```
    """

    name: str = Field(min_length=1, max_length=30)
    path: str = Field(min_length=1)

    @field_validator("name")
    def validate_import_name(cls, name: str) -> str:
        if not has_valid_pattern(pattern=LOWER_CAMELCASE_SINGLE_WORD, value=name):
            raise PydanticCustomError(
                "string_pattern_mismatch",
                "must be 'lowercase' or 'camelCase', a 'single word' and a maximum of '30' characters",
                dict(wrong_value=name, pattern=LOWER_CAMELCASE_SINGLE_WORD),
            )

        return name


class Image(Component, NextJs):
    """
    A Zentra model for the [NextJS Image](https://nextjs.org/docs/app/api-reference/components/image) component.

    Parameter:
    - `src` (`string | zentra.nextjs.StaticImage`) - can be either:
        1. A local path string starting with `/`, `./`, or `../`
        2. A statically imported image file represented by a `StaticImage` model
        3. An absolute external URL starting with `http://`, `https://`, `ftp://`, or `file://`
        4. An informative path string starting with `mailto:`, or `tel:`
        5. Or a parameter, signified by a `$` at the start of the parameter name. Parameters are useful when using the `Image` inside an `iterable` function like `zentra.js.Map`
    - `width` (`integer`) - a static width for the image
    - `height` (`integer`) - a static height for the image
    - `alt` (`string`) - an `alt` tag used to describe the image for screen readers and search engines. Also, acts as fallback text if the image is disabled, errors, or fails to load. Can also include parameters, signified by a `$` at the start of the parameter name. This is useful when using the `Image` inside an `iterable` function like `zentra.js.Map`
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the image. Automatically adds them to `className`. `None` by default

    Example Usage:
    1. A statically imported local image.
    ```python
    from zentra.nextjs import Image, StaticImage

    Image(src=StaticImage(name='profilePic', path='./me.png'), width=500, height=500, alt='Picture of the author', styles="aspect-[3/4] h-fit w-fit object-cover")
    ```
    JSX equivalent ->
    ```jsx
    import Image from 'next/image'
    import profilePic from './me.png'

    <Image
        src={profilePic}
        width={500}
        height={500}
        alt="Picture of the author"
        className="aspect-[3/4] h-fit w-fit object-cover"
    />
    ```

    2. Using an external URL.
    ```python
    from zentra.nextjs import Image

    Image(src='https://s3.amazonaws.com/my-bucket/profile.png', width=500, height=500, alt='Picture of the author')
    ```
    JSX equivalent ->
    ```jsx
    import Image from 'next/image'

    <Image
        src="https://s3.amazonaws.com/my-bucket/profile.png"
        width={500}
        height={500}
        alt="Picture of the author"
    />
    ```

    3. Using parameters inside src and alt.
    ```python
    from zentra.nextjs import Image

    Image(src='$artwork.art', width=500, height=500, alt='Picture of the $author $name')
    ```
    JSX equivalent ->
    ```jsx
    import Image from 'next/image'

    <Image
        src={artwork.art}
        width={500}
        height={500}
        alt={`Picture of the ${author} ${name}`}
    />
    ```

    4. Using a path string.
    ```python
    from zentra.nextjs import Image

    Image(src='/profile.png', width=500, height=500, alt='Picture of the author')
    ```
    JSX equivalent ->
    ```jsx
    import Image from 'next/image'

    <Image
        src="/profile.png"
        width={500}
        height={500}
        alt="Picture of the author"
    />
    ```
    """

    src: str | StaticImage
    width: int
    height: int
    alt: str
    styles: Optional[str] = None

    # TODO: add optional attributes such as loader
    @field_validator("src")
    def validate_src(cls, src: str | StaticImage) -> str | StaticImage:
        if isinstance(src, str):
            CustomUrl(url=src, plus_param=True).validate_url()

        return src


class Link(Component, NextJs):
    """
    A Zentra model for the [NextJS Link](https://nextjs.org/docs/app/api-reference/components/link) component.

    Parameters:
    - `href` (`string | zentra.nextjs.UrlQuery`) - a path or URL to navigate to starting with any of the following:
      1. Local paths - `/`, `./`, or `../`
      2. File urls - `ftp://` or `file://`
      3. Informative urls - `mailto:` or `tel:`
      4. HTTP urls - `http://` or `https://`
      5. Or, a `zentra.nextjs.UrlQuery` model
    - `text` (`string, optional`) - a string of text to display inside the `Link`. `None` by default
    - `styles` (`string, optional`) - a set of custom CSS classes to apply to the link. Automatically adds them to `className`. `None` by default
    - `new_tab` (`boolean, optional`) - a flag for opening the link in a new tab. `False` by default
    - `replace` (`boolean, optional`) - a boolean flag for enabling replacement of the current history state instead of adding a new URL into the [browser's history](https://developer.mozilla.org/en-US/docs/Web/API/History_API) stack. `False` by default
    - `scroll` (`boolean, optional`) - a boolean flag for setting the scroll behaviour. When `True` links will scroll to the top of a new route or maintain its scroll position for backwards and forwards navigation. When `False` links will `not` scroll to the top of the page. `True` by default
    - `prefetch` (`boolean, optional`) - a boolean flag for prefetching behaviour. Happens when a `Link` component enters the user's viewport (initially or through scroll). Involves loading the linked route (`href`) and its data in the background to improve the performance of the client-side navigations. Only enabled during production. `None` by default. Options:
      1. `None` - prefetching depends on whether the route is `static` or `dynamic`. For `static` routes, the full route is prefetched (including all its data). For `dynamic` routes, we prefetch the partial route down to the nearest [loading.js](https://nextjs.org/docs/app/building-your-application/routing/loading-ui-and-streaming#instant-loading-states) segment boundary
      2. `True` - the full route is prefetched for both static and dynamic routes
      3. `False` - prefetching never happens on hover or when entering the viewport

    Example Usage:
    1. A simple link.
    ```python
    from zentra.nextjs import Link

    Link(href="/dashboard")
    ```
    JSX equivalent ->
    ```jsx
    <Link href="/dashboard" />
    ```

    2. A simple link with text.
    ```python
    from zentra.nextjs import Link

    Link(href="/dashboard", text="Dashboard")
    ```
    JSX equivalent ->
    ```jsx
    <Link href="/dashboard">
        Dashboard
    </Link>
    ```

    3. An advanced link with everything.
    ```python
    from zentra.nextjs import Link, UrlQuery

    Link(
        href=UrlQuery(
            pathname="/dashboard",
            query={"name": "test"},
        ),
        text="Dashboard",
        styles="rounded-md border",
        new_tab=True,
        replace=True,
        scroll=False,
        prefetch=False,
    )
    ```
    JSX equivalent ->
    ```jsx
    <Link
        href={{
            pathname: '/dashboard',
            query: { name: 'test' },
        }}
        target="_blank"
        className="rounded-md border"
        replace
        scroll={false}
        prefetch={false}
    >
        Dashboard
    </Link>
    ```
    """

    href: str | UrlQuery
    text: Optional[str] = None
    styles: Optional[str] = None
    new_tab: bool = False
    replace: bool = False
    scroll: bool = True
    prefetch: Optional[bool] = None

    @property
    def import_str(self) -> str:
        """Returns the core import string for the component."""
        return f'import {self.classname} from "next/{self.classname.lower()}"'

    @field_validator("href")
    def validate_href(cls, href: str | UrlQuery) -> str | UrlQuery:
        if isinstance(href, str):
            CustomUrl(url=href).validate_url()

        return href
