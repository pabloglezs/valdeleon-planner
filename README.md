# Valdeleón Planner

Plano interactivo para decorar el chalet nº 98 de Residencial Valdeleón (Valdefresno, León): muebles a escala sobre los muros del plano de venta, vista 3D con modo "caminar", opción de casa en espejo y catálogo de más de 130 muebles.

Es una página estática (`index.html`) servida por nginx. Los muros van incrustados en el propio HTML; el navegador del visitante necesita internet para cargar three.js (cdnjs y jsDelivr) y la tipografía (Google Fonts). Los muebles que mueve cada persona se guardan en su navegador, no en el servidor.

## Estructura

| Ruta | Para qué sirve |
|---|---|
| `index.html` | La aplicación completa (generada desde `src/`) |
| `Dockerfile` | Imagen basada en `nginx-unprivileged` (puerto 8080, sin root) |
| `nginx.conf` | Servidor, cabeceras de seguridad y `/healthz` |
| `docker-compose.yml` | Stack que construye la imagen desde este repositorio |
| `docker-compose.portainer.yml` | Stack que usa una imagen ya construida (sin Git) |
| `src/` | Plantilla, máscaras de muros y script para regenerar `index.html` |

## Despliegue continuo con Portainer

1. En Portainer: **Stacks > Add stack > Repository**.
2. *Repository URL*: `https://github.com/pabloglezs/valdeleon-planner`, *Reference*: `refs/heads/main`, *Compose path*: `docker-compose.yml`.
3. En *Environment variables* añade `PORT` con el puerto del servidor que quieras exponer (por ejemplo `8123`). Es obligatorio.
4. Activa **GitOps updates** (*Automatic updates*) y elige una de estas dos formas:
   - **Polling**: Portainer revisa el repositorio cada X minutos (por ejemplo 5).
   - **Webhook**: copia la URL que te da Portainer y en GitHub ve a **Settings > Webhooks > Add webhook**, pégala en *Payload URL*, con *Content type* `application/json` y el evento *push*. Así se redespliega al instante en cada `git push`.
5. Marca **Re-pull image and redeploy** para que reconstruya la imagen en cada actualización y pulsa **Deploy the stack**.

Cada `git push` a `main` reconstruye la imagen y recrea el contenedor.

El repositorio es público, así que Portainer no necesita credenciales. Si lo haces privado, activa *Authentication* en el stack y usa un token personal de GitHub con permiso de lectura.

## Nginx Proxy Manager

El contenedor escucha siempre en el 8080 por dentro; el puerto de fuera es el valor de `PORT`.

**Por el puerto publicado**

1. **Hosts > Proxy Hosts > Add Proxy Host**.
2. *Domain Names*: tu dirección, por ejemplo `casa.tudominio.es`.
3. *Scheme* `http`, *Forward Hostname / IP*: la IP del servidor Docker, *Forward Port*: el valor de `PORT`.
4. Pestaña **SSL**: solicita certificado y activa *Force SSL* y *HTTP/2 Support*.

**Sin publicar puerto (misma red de Docker)**: borra el bloque `ports` del compose, descomenta las líneas de `networks` con el nombre real de la red de NPM y en NPM usa el host `chalet98` y el puerto `8080`.

Usa siempre HTTPS: así los datos guardados en el navegador quedan asociados a tu dominio.

## Modificar la aplicación

La página se genera a partir de `src/tpl.html`:

```bash
python src/build.py
git add -A && git commit -m "Describe el cambio" && git push
```

`build.py` solo usa la biblioteca estándar de Python y escribe `index.html` en la raíz.

## Probar en local

```bash
docker build -t chalet98:latest .
docker run --rm -p 8123:8080 chalet98:latest
```

Abre `http://localhost:8123`. La comprobación de salud está en `/healthz`.

## Para que funcione sin internet en el navegador

Hay que alojar en local `three.min.js` y `OrbitControls.js` (versión 0.128.0) y la fuente IBM Plex, cambiar sus rutas en `src/tpl.html` y ajustar la política `Content-Security-Policy` de `nginx.conf`.
