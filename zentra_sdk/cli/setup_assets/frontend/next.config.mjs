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
