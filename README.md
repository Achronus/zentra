_Last updated 09/07/2024_

# Zentra

![Logo](/docs/assets/imgs/zentra-logo.jpg)

An open-source Python tool that uses [Pydantic](https://docs.pydantic.dev/latest/) models to create [React](https://react.dev/) components. The perfect tool for accelerating [NextJS](https://nextjs.org/) frontends with a Python-based backend, such as [FastAPI](https://fastapi.tiangolo.com/).

It comes packed with API documentation for building your Python models, and a CLI interface that dynamically creates the frontend files based on the models you've created.

_Note: Zentra is still in development. We plan to release a simple version soon with minimal components._

## How It Works

Zentra aims to be a flexible tool that covers a variety of component libraries, while centering around the [NextJS App Router](https://nextjs.org/docs) framework.

### Structural Elements

It focuses on three structural components: `ReactFiles`, `Blocks`, and `Components`. A file can have multiple blocks, and each block can have multiple components.

When using Zentra, you'll use all three to create the frontend. We'll discuss these in more detail in our documentation.

### Component Roadmap

Core component libraries and custom models in development:

- [X] Zentra Structural Models (3/3)
- [X] Custom Data Models (1/1)
- [X] Custom HTML Models (4/4)
- [ ] Custom JavaScript Models (1/4)
- [ ] [Shadcn/ui Form](https://ui.shadcn.com/docs/components/form) Models (0/13)
- [ ] [Shadcn/ui](https://ui.shadcn.com/) (32/48)
- [ ] [NextJS](https://nextjs.org/docs/app/api-reference/components) (2/4)
- [X] [Uploadthing](https://docs.uploadthing.com/getting-started/appdir) (1/1)
- [X] [Lucide React Icons](https://lucide.dev/guide/packages/lucide-react) (1/1 - 1 component for all icons)

Future component libraries:

- [Clerk](https://clerk.com/)
- [Tremor](https://www.tremor.so/)
- [Stripe](https://docs.stripe.com/stripe-js/react?locale=en-GB)
- [LiveBlock](https://liveblocks.io/)
- And more...

## Example Usage

To get a feel for how Zentra works, let's consider the [Shadcn/ui Scroll Area Component](https://ui.shadcn.com/docs/components/scroll-area) as an example. Specifically, the horizontal scrolling example. Here's its JSX:

```jsx
import Image from "next/image"

import { ScrollArea, ScrollBar } from "@/components/ui/scroll-area"

export type Artwork {
  artist: string;
  art: string;
}

export const works: Artwork[] = [
  {
    artist: "Ornella Binni",
    art: "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
  },
  {
    artist: "Tom Byrom",
    art: "https://images.unsplash.com/photo-1548516173-3cabfa4607e9?auto=format&fit=crop&w=300&q=80",
  },
  {
    artist: "Vladimir Malyavko",
    art: "https://images.unsplash.com/photo-1494337480532-3725c85fd2ab?auto=format&fit=crop&w=300&q=80",
  },
]

export function ScrollAreaHorizontalDemo() {
  return (
    <ScrollArea className="w-96 whitespace-nowrap rounded-md border">
      <div className="flex w-max space-x-4 p-4">
        {works.map((artwork) => (
          <figure key={artwork.artist} className="shrink-0">
            <div className="overflow-hidden rounded-md">
              <Image
                src={artwork.art}
                alt={`Photo by ${artwork.artist}`}
                className="aspect-[3/4] h-fit w-fit object-cover"
                width={300}
                height={400}
              />
            </div>
            <figcaption className="pt-2 text-xs text-muted-foreground">
              Photo by{" "}
              <span className="font-semibold text-foreground">
                {artwork.artist}
              </span>
            </figcaption>
          </figure>
        ))}
      </div>
      <ScrollBar orientation="horizontal" />
    </ScrollArea>
  )
}
```

Using Zentra, we can create this component with the following `Python` code:

```python
from zentra_models.core import Block, DataArray, ReactFile
from zentra_models.core.html import Figure, FigCaption, Div, HTMLContent
from zentra_models.core.js import Map
from zentra_models.nextjs import Image
from zentra_models.ui.control import ScrollArea


# Types inferred automatically
artwork = DataArray(
  name="works",
  type_name="Artwork",
  data=[
    {
      "artist": "Ornella Binni",
      "art": "https://images.unsplash.com/photo-1465869185982-5a1a7522cbcb?auto=format&fit=crop&w=300&q=80",
    },
    {
      "artist": "Tom Byrom",
      "art": "https://images.unsplash.com/photo-1548516173-3cabfa4607e9?auto=format&fit=crop&w=300&q=80",
    },
    {
      "artist": "Vladimir Malyavko",
      "art": "https://images.unsplash.com/photo-1494337480532-3725c85fd2ab?auto=format&fit=crop&w=300&q=80",
    },
  ],
)

artwork_map = Div(
  styles="flex w-max space-x-4 p-4",
  items=Map(
    obj_name="works",
    param_name="artwork",
    content=Figure(
      key="$.artwork.artist",
      styles="shrink-0",
      img_container_styles="overflow-hidden rounded-md",
      img=Image(
        src="$.artwork.art",
        alt="Photo by $.artwork.artist",
        styles="aspect-[3/4] h-fit w-fit object-cover",
        width=300,
        height=400,
      ),
      caption=FigCaption(
        styles="pt-2 text-xs text-muted-foreground",
        text=[
          'Photo by{" "}',
          HTMLContent(
            tag="span",
            styles="font-semibold text-foreground",
            text="$.artwork.artist",
          ),
        ],
      ),
    ),
  ),
)

sa = ScrollArea(
  styles="w-96 whitespace-nowrap rounded-md border",
  content=artwork_map,
  orientation="horizontal",
)

scroll_area_demo = ReactFile(
  name="ScrollAreaDemo",  # Name of file with '.tsx' appended
  file_type="component",  # Stores in 'src/components' directory
  blocks=Block(
    name="ScrollAreaHorizontalDemo",
    components=sa,
  ),
)
```

## Active Development

Zentra is a tool that is continously being developed with components being added to it regularly. There's a lot still to do to make it a fully functioning tool, such as a working CLI, detailed API documentation, and components for various libraries.

Our goal is to provide a quality open-source product that works 'out-of-the-box' that everyone can experiment with, and then gradually fix unexpected bugs and introduce more component libraries on the road to a `v1.0.0` release.

## Support

We'll need help from developers like you to make this tool a delight to use, and a product worthy of the `Python`, `NextJS`, `React` and `Software/Web Development` community.

Feedback and criticism will always be welcomed, and is encouraged to help make this tool worthwhile.
