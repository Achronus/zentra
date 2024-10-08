# Frontend Files

The `frontend` directory is home to all the [`Next.js`](#frontend-files) and [`React`](#frontend-files) assets.

??? Note "Frontend Folder Structure"

    ```shell title=""
    frontend/
    ├── public/
    │   ├── next.svg
    │   └── vercel.svg
    ├── src/
    │   ├── app/
    │   │   ├── favicon.ico
    │   │   ├── globals.css
    │   │   ├── layout.tsx
    │   │   └── page.tsx
    │   ├── components/
    │   └── lib/
    │       └── utils.ts
    ├── .env.local
    ├── .eslintrc.json
    ├── components.json
    ├── next-env.d.ts
    ├── next.config.mjs
    ├── package.json
    ├── postcss.config.mjs
    ├── tailwind.config.ts
    └── tsconfig.json
    ```

## Configuration Files

```shell title="Root Frontend Files"
frontend/
...
├── .env.local # (1)!
├── .eslintrc.json # (2)!
├── components.json # (3)!
├── next.config.mjs # (4)!
├── next-env.d.ts # (5)!
├── package.json # (6)!
├── postcss.config.mjs # (7)!
├── tailwind.config.ts # (8)!
└── tsconfig.json # (9)!
```

1. An environment variable file for storing API keys and confidential information unique to the frontend.
2. The config file for [Eslint [:material-arrow-right-bottom:]](https://eslint.org/). This is automatically generated by `Next.js` and should never be manual edited.
3. The config file for [Shadcn/ui  [:material-arrow-right-bottom:]](https://ui.shadcn.com/docs/components-json). We recommend changing the `style` and `baseColor` in this file to your preference.
4. The config file for [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/). We'll discuss this in more detail shortly.
5. A [TypeScript [:material-arrow-right-bottom:]](https://www.typescriptlang.org/) declaration file for [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/). This file is automatically generated and should never be manually modified.
6. The package management file for [Node [:material-arrow-right-bottom:]](https://nodejs.org/). It contains a list of all the projects `dependencies` and commands that can be run. You may occassionally visit this file.
7. The config file for [Postcss [:material-arrow-right-bottom:]](https://postcss.org/). This is installed automatically with [Tailwind CSS [:material-arrow-right-bottom:]](https://tailwindcss.com/).
8. The config file for [Tailwind CSS [:material-arrow-right-bottom:]](https://tailwindcss.com/docs/theme). You'll likely visit this file occassionally for adding custom theme styles.
9. The config file for [TypeScript [:material-arrow-right-bottom:]](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html). It is automatically created with [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/) and does not need to be manually edited.

At the root level, we have numerous `configuration` files, you can read more about each one using the `+` icons above.

### Environment File (.env.local)

The environment file is configured to help connect the backend and frontend together. It only contains a single URL that can be easily changed when moving to production.

Here's what the file looks like:

```python title=".env.local"
# The URL to connect FastAPI and NextJS together - used in `next.config.mjs`
BACKEND_CONNECTION_URL=http://localhost:8080/
```

As long as there is a URL provided to connect the backend, this file can be edited freely. You'll often need to use it when working with API keys from packages like `Clerk` and `Stripe`.

### Next Configuration File (next.config.mjs)

We've preconfigured this config file to directly integrate with the FastAPI backend using the `BACKEND_CONNECTION_URL` in the [`.env.local`](#) environment file.

This allows you to use the same URL path that hosts your frontend with your `api` paths to access your backend routes.

For example, if you have your was frontend hosted on `https://awesomeposts.com/` and your backend on `https://newapi.com/` these access the same API routes:

- `https://awesomeposts.com/api/posts` = `https://newapi.com/api/posts`

This makes frontend development a little bit easier and abstracts your API away from your users.

For reference, here's what the config file looks like:

```js title="frontend/next.config.mjs"
/** @type {import('next').NextConfig} */

const apiUrl = process.env.BACKEND_CONNECTION_URL;

const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: apiUrl,
        pathname: `/api/*`,
      },
    ],
  },
  rewrites: async () => {
    return [
      {
        source: "/api/:path*",
        destination: `${apiUrl}/api/:path*`,
      },
      {
        source: "/docs",
        destination: `${apiUrl}/docs`,
      },
      {
        source: "/openapi.json",
        destination: `${apiUrl}/openapi.json`,
      },
    ];
  },
};

export default nextConfig;
```

Unless you have something specific in mind, you don't need to configure this file any further.

## Public Directory

```shell title="frontend/public/"
frontend/
├── public/
│   ├── next.svg
│   └── vercel.svg
...
```

This directory is a place to store static files, such as images. You can then reference these files from the base URL (`/`). You can read more about it in the [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/docs/app/building-your-application/optimizing/static-assets) documentation.

On project creation, this directory contains the basic files generated by [Next.js [:material-arrow-right-bottom:]](https://nextjs.org/).

## Source Directory

```shell title="frontend/src/"
frontend/
...
├── src/
│   ├── app/
│   │   ├── favicon.ico
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   └── lib/
│       └── utils.ts
...
```

The [`src`](#source-directory) directory is the main directory you will be working with. This is the _application_ code directory for the frontend!

It uses the [Next.js App Router [:material-arrow-right-bottom:]](https://nextjs.org/docs/app) layout, and to keep things simple and fully customisable, the files are identical to a freshly started Next.js project using the `npx create-next-app@latest` command.

In it, you'll find 3 directories: [`app`](#app), [`components`](#components) and [`lib`](#lib). Let's take a closer look at them!

### App

The [`app`](#app) directory handles the functionality for [Next.js Routing [:material-arrow-right-bottom:]](https://nextjs.org/docs/getting-started/project-structure#app-routing-conventions).

It's a fast and simple way to build pages with ease while maintaining a well structured project.

it contains `four` files:

- [`favicon.ico`](#app) - the favicon icon for the website
- [`globals.css`](#app) - the global CSS file applied to the whole project
- [`layout.tsx`](#app) - the global layout of the pages used in the project
- [`page.tsx`](#app) - the root/home page for the project (`/`)

You'll primarily focus on editing the `layout.tsx` and `page.tsx` files in this directory. We also encourage you to replace the `favicon.ico` with your own to help make the project unique to you!

`globals.css` is already configured with `Tailwind CSS`. If you need to use CSS outside of the Tailwind's styles, we recommend using [CSS Modules [:material-arrow-right-bottom:]](https://nextjs.org/docs/app/building-your-application/styling/css-modules).

### Components

The [`components`](#components) directory houses all your global reusable `React` components that are shared across the project.

For example, when you add a [Shadcn/ui [:material-arrow-right-bottom:]](https://ui.shadcn.com/docs/cli#add) component using their CLI, they can be found here inside a `ui` directory.

### Lib

The [`lib`](#lib) directory contains global application-specific files. These could include `utility` functions, `constants`, facades and more.

This comes preconfigured with a [`utils.ts`](#lib) file with a single function. Here's what it looks like:

```ts title="lib/utils.ts"
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

The `cn` function is an extremely useful utility method for handling [Tailwind CSS [:material-arrow-right-bottom:]](https://tailwindcss.com/) classing and compressing them into a single string.

We use this function regularly and it's been an absolute lifesafer when styling our components. [ByteGrad [:material-arrow-right-bottom:]](https://www.youtube.com/watch?v=re2JFITR7TI) has an excellent video about this on YouTube.

We plan to make some additional changes to this layout in the future, such as adding `types`, `layouts` and `constants` directories to help organise your frontend files.
