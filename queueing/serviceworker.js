importScripts('https://storage.googleapis.com/workbox-cdn/releases/6.2.0/workbox-sw.js');

workbox.routing.registerRoute(
    ({request}) => request.destination === 'image',
    new workbox.strategies.CacheFirst() // serves from cache if at all available
    // new workbox.strategies.NetworkFirst() // this defaults to using network, unless app is online
);