=====
django-imagemanagement
=====
RESTful Image Management API 

Quick start
-----------


1. Add "imagemanagement" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'imagemanagement',
    ]

2. Include the imagemanagement URLconf in your project urls.py like this::

		url(r'^image/',include('imagemanagement.urls')),

3. Run `python manage.py migrate` to create all the models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create an access key (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/image/ to use the API.

6. Supported HTTP Methods : GET, POST, PATCH, DELETE
