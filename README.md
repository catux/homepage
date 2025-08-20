# Catux Homepage

Web oficial de l'Associació d'usuaris de GNU/Linux de la Catalunya Central.

## Com escriure un post

* Ves al directori `app/src/templates/posts`
* Crea un fitxer amb el següent contingut:

```
    {% extends 'post_template.html' %}

    {% block title %}
        El títol del post
    {% endblock %}

    {% block author %}
        El teu nickname
    {% endblock %}

    {% block post_date %}
        2006-06-20 00:00:00
    {% endblock %}

    {% block categories %}
        Notícies, ...
    {% endblock %}

    {% block post %}
        Text del teu post
    {% endblock %}
```

* Commit a la branca `main`
* El GitHub Action s'encarregarà de fer el build i deploy automàticament

## Com pujar imatges

* Posa el fitxer a `app/src/images/`
* Referencia-la utilitzant `<img src={{ homepage }}images/elnom.jpg>`


## Instal·lació per desenvolupament

```
npm install --dev
```

* Recordeu modificar la variable homepage que forma tots els enllaços

Al fitxer `app/src/templates/context/_all.json`

```
 {
-  "homepage": "http://catux.org/"
+  "homepage": "http://localhost:3000/"
 }
```

## Comandes de desenvolupament

* `npm run dev` - Inicia el servidor de desenvolupament amb hot-reload a http://localhost:3000
* `npm run build` - Genera la versió de producció
* `npm run sass` - Compila els fitxers SCSS a CSS
* `npm run templates` - Processa les plantilles Nunjucks
* `npm run posts` - Genera la llista de posts
* `npm run copy` - Copia imatges i fonts

## Empaquetat i desplegament

* Executa `npm run build` localment per generar els fitxers estàtics
* Resultat a `/app/public/`

## Desplegament automàtic amb GitHub Actions

El projecte utilitza GitHub Actions per desplegar automàticament el lloc web a [catux.github.io](https://catux.github.io) quan es fa push a la branca `master`.

### Com funciona

1. Quan es fa push a la branca `master`, s'activa el workflow definit a `.github/workflows/deploy.yml`
2. El workflow fa el següent:
   - Clona el repositori font (aquest)
   - Clona el repositori destí (catux/catux.github.io)
   - Instal·la les dependències
   - Executa `npm run build`
   - Copia els fitxers generats a `/app/public/` al repositori destí
   - Fa commit i push dels canvis al repositori destí

### Requisits

Per a que el desplegament automàtic funcioni, cal configurar un secret a la configuració del repositori:

- `DEPLOY_PAT`: Un Personal Access Token de GitHub amb permisos `repo` per poder fer push al repositori catux.github.io

Per crear un PAT, segueix aquests passos:
1. Ves a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Genera un nou token amb permisos `repo`
3. Copia el token i afegeix-lo com a secret al repositori amb el nom `DEPLOY_PAT`

També es pot executar el workflow manualment des de la pestanya "Actions" del repositori.
