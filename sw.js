// Code geschrieben von Claude (KI-Modell von Anthropic), siehe README.md.
// Service Worker: speichert die App-Dateien, damit der Umrechner auch ohne Internet startet.
// Die Kurse selbst verwaltet die App (localStorage); Anfragen an die Kurs-API laufen hier nicht durch.
// Bei jeder Änderung an den App-Dateien VERSION erhöhen, damit installierte Apps das Update laden.
const VERSION = "umrechner-v2";
const FILES = [
  "./",
  "./index.html",
  "./data.js",
  "./manifest.webmanifest",
  "./icons/icon-32.png",
  "./icons/icon-180.png",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(VERSION).then((cache) => cache.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((key) => key !== VERSION).map((key) => caches.delete(key))))
      .then(() => self.clients.claim()),
  );
});

self.addEventListener("fetch", (event) => {
  const request = event.request;
  if (request.method !== "GET" || new URL(request.url).origin !== self.location.origin) return;

  // Seitenaufrufe: zuerst online versuchen (für Updates), sonst gespeicherte Fassung.
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then((response) => {
          const copy = response.clone();
          caches.open(VERSION).then((cache) => cache.put("./index.html", copy));
          return response;
        })
        .catch(() => caches.match("./index.html")),
    );
    return;
  }

  // Übrige App-Dateien: aus dem Speicher, sonst aus dem Netz.
  event.respondWith(caches.match(request).then((cached) => cached || fetch(request)));
});
