[![Build Status](https://travis-ci.org/Acme-Board/board.svg?branch=develop)](https://travis-ci.org/Acme-Board/board) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/b879faad743f449a8af839ebb3c91b78)](https://www.codacy.com/gh/Acme-Board/board?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Acme-Board/board&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/b879faad743f449a8af839ebb3c91b78)](https://www.codacy.com/gh/Acme-Board/board?utm_source=github.com&utm_medium=referral&utm_content=Acme-Board/board&utm_campaign=Badge_Coverage)

Plataforma sobre alquiler de juegos de mesa
===========================================

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/f517890a06a54295a77f9ea5b5e31a74)](https://app.codacy.com/gh/Acme-Board/board?utm_source=github.com&utm_medium=referral&utm_content=Acme-Board/board&utm_campaign=Badge_Grade_Settings)

El objetivo de este proyecto es implementar una plataforma para el alquiler
de juegos de mesa, de manera que se facilite este alquiler ya que se realiza
entre los mismo usuarios. La ventaja de esta web es que los juegos te aparecen
por distancia, o sea, los primeros serán los más cercanos así no dependes de 
un local o almacen en el cual hay que  ir a recogerlo.

Se trata de un proyecto para la asignatura ISPP, pensado para acercarse a un
proyecto realista que se puede encontrar en cualquier empresa. Hay que buscar 
la innovación y el beneficio y buscar clientes pilotos que al final compren 
la aplicación por su utilidad (la compra no se realiza, es una forma de reflejar
que sería algo por lo que pagarían).

Módulos
-------

Este proyecto Django se divide en 3 módulos principales, los cuales estarán desacoplados
entre ellos. Donde cualquier de ellos sw podrá reemplazar individualmente.

* **rent:** Este es el módulo principal de la aplicación, se encargar del alquiler de los juegos y mostrar los mismos.
* **user:** Este se encarga de la organización de los usuarios y del registro de los mismos.
* **stripe:** Se encarga del tema de los pagos, como su mismo nombre indica, usaremos stripe para esta tarea.
* **review:** El subsistema de chat está destinado para poder valorar los productos que suben los usuarios como a los propios usuarios.

Configurar Postgres (Windows)
-----------------------------

Para instalar Postgres en Windows, lo primero es descargar e instalar es necesario seguir los pasos de esta pequeña guía: http://www.postgresqltutorial.com/install-postgresql/ (Consejo: toma nota del directorio donde lo instalaste), y el ejecutable lo puedes encontra aquí: http://www.enterprisedb.com/products-services-training/pgdownload#windows.

Abre la línea de comandos (Inicio → Todos los programas → Accesorios → Linea de comandos o Inicio → Ejecutar → cmd)
Ejecuta el siguiente comando para añadir la ruta al PATH de Windows o añádela manualmente (asegúrate de que el la carpeta sea la misma que anotaste cuando estabas instalando con un \bin al final)

    setx PATH "%PATH%;C:\Program Files\PostgreSQL\9.3\bin"

Cierra y vuelve a abrir la línea de comandos.
    
* **Crear la base de datos**

Primero, vamos a iniciar la consola de Postgres ejecutando el siguiente comando:

    psql -U <username> -W
    
donde username es el nombre de usuario que se usó en la instalación. Después pedirá introducir la contraseña que se puso para ese usuario.

Ahora vamos a crear un usuario para nuestra bbdd con la siguiente linea

    # CREATE USER board WITH PASSWORD 'board';
    
Y para la bbdd escribimos lo siguiente 

    # CREATE DATABASE boardDB OWNER board;

Configurar el proyecto
----------------------

Para configurar el proyecto, será necesario instalar las dependencias del proyecto, las cuales están en el
fichero requirements.txt:

    pip install -r requirements.txt

Entramos en la carpeta del proyecto (cd board) y realizamos la primera migración para preparar la
base de datos que utilizaremos:
    
    python manage.py makemigrations

    python manage.py migrate

Y para finalizar, vamos a crear un super usuario

    python manage.py createsuperuser
    
Por último, ya podremos ejecutar el módulos o módulos seleccionados en la configuración de la
siguiente manera:

    python manage.py runserver

Ejecutar test en local
----------------------

Los tests se hacen en las clases tests.py de cada módulo, si se desea crear otra clase a parte, 
el nombre del archivo debe de empezar por test_nombreTest.py, para qu Django sepa que ahí se 
encuentran test.

A continuación, se abre la consola SQL Shell y se loguea como admin (normalmente user=postgres 
y pass=postgres) e introducimos el siguiente comando para dar privilegios a nuestro usuario para
que pueda crear una bbdd para los test case:
    
    ALTER USER board CREATEDB;
    
Y para poder ejecutar los test en local, desde una consola nos situamos en el directorio del proyecto
e introducimos uno de los siguientes comandos:

    python manage.py test
    
para ejecutar todos los tests de todos los módulos del proyecto, o

    python manage.py test rent
    
para ejecutar los tests del módulo en cuestión, en este caso del módulo rent.
