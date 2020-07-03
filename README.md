The goal of this assignment is to learn about this type of database and different ways of working with it. Build a simple Django server that uses MPTT models from django-mptt to create a Dropbox-esque web interface where you can create "folders" and "files" in an arbitrary structure and then display that structure.

- from django-mptt docs \*

install django-mptt:

- pip install django-mptt

Getting started
Add mptt To INSTALLED_APPS
As with most Django applications, you should add mptt to the INSTALLED_APPS in your settings.py file:

INSTALLED_APPS = (
'django.contrib.auth', # ...
'mptt',
)
Set up your model
Start with a basic subclass of MPTTModel, something like this:

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Genre(MPTTModel):
name = models.CharField(max_length=50, unique=True)
parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

You must define a parent field which is a TreeForeignKey to 'self'. A TreeForeignKey is just a regular ForeignKey that renders form fields differently in the admin and a few other places.

Because you’re inheriting from MPTTModel, your model will also have a number of other fields: level, lft, rght, and tree_id. These fields are managed by the MPTT algorithm. Most of the time you won’t need to use these fields directly.

That MPTTMeta class adds some tweaks to django-mptt - in this case, just order_insertion_by. This indicates the natural ordering of the data in the tree.

Now create and apply the migrations to create the table in the database:

python manage.py makemigrations <your_app>
python manage.py migrate
Create some data
Fire up a django shell:

python manage.py shell
Now create some data to test:

from myapp.models import Genre
rock = Genre.objects.create(name="Rock")
blues = Genre.objects.create(name="Blues")
Genre.objects.create(name="Hard Rock", parent=rock)
Genre.objects.create(name="Pop Rock", parent=rock)
Make a view
This one’s pretty simple for now. Add this lightweight view to your views.py:

def show_genres(request):
return render(request, "genres.html", {'genres': Genre.objects.all()})
And add a URL for it in urls.py:

(r'^genres/\$', show_genres),
Template
django-mptt includes some template tags for making this bit easy too. Create a template called genres.html in your template directory and put this in it:

{% load mptt_tags %}

<ul>
    {% recursetree genres %}
        <li>
            {{ node.name }}
            {% if not node.is_leaf_node %}
                <ul class="children">
                    {{ children }}
                </ul>
            {% endif %}
        </li>
    {% endrecursetree %}
</ul>
