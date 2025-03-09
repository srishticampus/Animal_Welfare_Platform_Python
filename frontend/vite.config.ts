import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import virtualHtml from 'vite-plugin-virtual-html'

const pages = {
  index: '/index.html',
  about: '/about.html',
  adoption: '/adoption.html',
  cart: '/cart.html',
  checkout: '/checkout.html',
  contact: '/contact.html',
  details: '/details.html',
  "forgot-password": '/forgot-password.html',
  login: '/login.html',
  order: '/order.html',
  "pet-details": '/pet-details.html',
  pets: '/pets.html',
  rescue: '/rescue.html',
  "reset-password": '/reset-password.html',
  shop: '/shop.html',
  signup: '/signup.html',
}

export default defineConfig({

  plugins: [
    tailwindcss(),
    virtualHtml({
      pages,
    }),
  ]
})