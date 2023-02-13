# Init

The purpose of this blog site is to provide technical information, demonstrations, and tutorials relating to software projects I've completed. For my first post, I'm going to discuss the current architecture of this blog.

## Overall Architecture

I've been developing Python based web applications for almost 4 years. So, the architecture of this application is similar to most of my other projects. In a sentence, I'm running a Django based web application in a Docker container.

The rest of this post will cover each major component from the bottom up.

## Docker

Docker is my favorite technology. It allows the creation of portable, reproducible environments isolated from their host system. It's also a key component in my [megalith hosting strategy](https://blog.thatcherthornberry.com/posts/my-megalith). This project consists of 4 containers: a Postgres database, a Django application, an Nginx reverse proxy, and a Redis database.

All of the containers run on the same network and when this project is deployed to the megalith VM, this project will share the Postgres and Redis servers with other projects.

## Nginx

This project is deployed within my megalith VM. The megalith VM is a single server that hosts multiple projects. Nginx isn't a direct part of this project but, in operation, it plays a key role. In one sentence, I'm running Nginx as a reverse proxy. When you visit any subdomain of `thatcherthornberry.com`, Nginx routes the request to the correct application.

## Django

Django is a python web framework which abstracts many standard web development tasks. Namely, it provides a database abstraction layer, a templating engine, and a URL routing system. It also provides a development server for testing and debugging.

Django follows the software architectural pattern known as Model-View-Controller (MVC). The model is the database, the view is the HTML template, and the controller is the Python code that handles the request. In operation, when a user requests the url `https://blog.thatcherthornberry.com`, Django routes that request to a specific view. The view then queries the database for the data it needs to render the page. The view then renders the HTML template with the data and returns the result to the user.

### Gunicorn

Django provides a development server out of the box but leaves it to the developer to implement their own production web server; I'm using Gunicorn: a Python WSGI HTTP Server for UNIX. It's based on the pre-fork worker model. The pre-fork worker model The Gunicorn server is lightweight and fast.

It's also easy to configure.

Development server:

    ```python manage.py runserver 0.0.0.0:8000```

Gunicorn:

    ```gunicorn blog.wsgi:application --bind 0.0.0.0:8000```

## Redis

Redis is an in-memory key-value store. I'm using it as a cache for this application which means I'm storing the rendered HTML of each page in Redis. When a user requests a page, Django first checks Redis to see if the page is cached. If it is, Django returns the cached page. If it isn't, Django renders the page, stores it in Redis, and returns it to the user. This gives a small performance boost relative to Django's built in caching system.

## Postgres

Postgres is a relational database. Django provides a database abstraction layer as well as an ORM (Object Relational Mapper). The ORM allows you to interact with the database using Python objects. For example, if you have a table called `blog_post` with a column called `title`, you can query the database for all posts with the title `Hello World` using the following code:

    ```python
    from blog.models import Post
    posts = Post.objects.filter(title="Init")
    ```

## Markdown

All of my posts are written in Markdown, a lightweight markup language. I have a simple script which converts them to HTML using the python library [Markdown](https://pypi.org/project/Markdown/). This script also handles creating database artificats for each post. When a page is rendered, Django queries the database for the post and renders the HTML template with the post data.

## Bootstrap

Bootstrap is my favorite CSS framework. It is super lightweight and abstracts one of the most important functionalities of a website: responsiveness. There are two dominant mediums for viewing a webpage: desktop and mobile. There are stark differences between these mediums; most importantly screen size and screen orientation. Bootstrap provides a grid based layout system which allows you to create a single layout that works on both mediums.

## DALL-E 2

Each post has a unique image associated with it. I'm using [DALL-E 2](https://openai.com/blog/dall-e/) to generate these images. DALL-E 2 is a neural network which takes a text prompt and generates an image.

## TODO

To be honest, I'm deploying this project against my will. There are so many things I want to add. But, I need to work on getting projects out the door before I've implemented all of the fun things I want to. For now, I'll list the things I want to add in the future.

- An Elasticsearch database that synchronizes with the data in Postgres for full text search
- User visits tracking
- A TODO post page
  - While I'm writing, I often think I should write a post about X thing. I want to create the link within the post I'm writing tot he future post. If the post doesn't exist, a TODO page explaining the post hasn't been written yet.
  - When users visit the page, I'll increment a counter which will motivate me to write the post
  - Also, an email sign up to notify users when the post is published
- A comment system
- An RSS feed
- Blog email subscription, read posts directly in email
- An ML powered grammar/spelling checker
- Estimated reading time
- Post change history
- Better formatting for code blocks (line numbers, syntax highlighting, copy command, etc.)
