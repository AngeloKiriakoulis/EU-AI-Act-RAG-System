/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://172.19.205.48:31262/api/:path*', // My MicroK8s API internalIP, change when deployed.
      },
    ]
  },
}

module.exports = nextConfig 