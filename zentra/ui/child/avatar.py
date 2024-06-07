from zentra.base.library import ShadcnUi
from zentra.core import Component
from zentra.nextjs import StaticImage


class AvatarImage(Component, ShadcnUi):
    """
    A helper model that handles the content creation for the `AvatarImage` in the [Shadcn/ui Avatar](https://ui.shadcn.com/docs/components/avatar) component.

     Parameters:
     - `src` (`string | zentra.nextjs.StaticImage`) - can be either:
         1. A local path string starting with `/`, `./`, or `../`
         2. A statically imported image file represented by a `StaticImage` model
         3. An absolute external URL starting with `http://`, `https://`, `ftp://`, or `file://`
         4. An informative path string starting with `mailto:`, or `tel:`
         5. Or a parameter, signified by a `$.` at the start of the parameter name. Parameters are useful when using the `Image` inside an `iterable` function like `zentra.js.Map`
     - `alt` (`string`) - an `alt` tag used to describe the image for screen readers and search engines. Also, acts as fallback text if the image is disabled, errors, or fails to load. Can also include parameters, signified by a `$.` at the start of the parameter name
    """

    src: str | StaticImage
    alt: str


class AvatarFallback(Component, ShadcnUi):
    """
    A helper model that handles the content creation for the `AvatarFallback` in the [Shadcn/ui Avatar](https://ui.shadcn.com/docs/components/avatar) component.

    Parameters:
    - `content` (`string`) - the fallback text if the avatar image doesn't load. Up to a maximum of `2` characters
    """

    content: str
