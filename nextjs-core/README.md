#  NextJS Core

A docker container for quickly bootstrapping [Next.js](https://nextjs.org/) applications using Bun.

## Package Stack

- [Next.js](https://nextjs.org/)
- [Shadcn/ui](https://ui.shadcn.com/)
- [Next Themes](https://ui.shadcn.com/docs/dark-mode/next)
- [Lucide React Icons](https://lucide.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Axios](https://axios-http.com/)

## How To Use it

1. Pull the container

```cmd
docker pull achronus/nextjs-core:latest
```

2. Run it

```cmd
docker run -d --name nextjs-container achronus/nextjs-core
```

3. Copy the frontend files to your current directory

```cmd
docker cp nextjs-container:frontend .
```

4. Cleanup

```cmd
docker stop nextjs-container && docker rm nextjs-container && docker rmi achronus/nextjs-core
```

Done! Access the frontend directory, install the packages (e.g., `npm install`) and start programming!
