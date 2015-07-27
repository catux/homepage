Com escriure un post
====================

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

* Commit a la branca `master`
* Esperar uns 5 minuts fins que CodeShip agafi l'actualització i la puji


Com pujar imatges
=================

* Posa el fitxer a `app/src/images/`
* Referencia-la utilitzant `<img src={{ homepage }}images/elnom.jpg>`


Instal·lació per desenvolupament
================================

```
npm install
bower install
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
grunt
```

* Recordeu modificar la variable homepage que forma tots els enllaços

Al fitxer `app/src/templates/context/_all.json` 

```
 {
-  "homepage": "http://catux.org/"
+  "homepage": "http://localhost:9000/"
 }
```


Empaquetat
=========

* Executa `grunt prod`
* Resultat a `/app/public/`

