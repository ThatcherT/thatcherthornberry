# What is a megalith?

Megalith is a term I made up to describe the single encompassing architecture I use to deploy my personal projects. The architecture is a manifestation of [my deep-seated obsession with efficiency](https://thatcherthornberry.com/posts/efficiency).

## Overview

The purpose of this architecture is optimize the tradeoff between development time, deployment complexity, and cost. All of my projects live under the domain thatcherthornberry.com. The core of each project lives in its own, isolated docker container, but tend to share some resources with other projects such as databases.

## Source Control

Each project lives in its own repository, for example [QSongs](https://github.com/thatchert/spotifly). The [megalith repository](https://gihub.com/thatchert/thatcherthornberry) pulls each project into its repository using a technology called [git subtree](https://www.atlassian.com/git/tutorials/git-subtree). This technique allows me to keep each project separate but also keep the deployment process consolidated to a single repository.

### GitHub Actions

GitHub actions is my tool of choice for CI/CD because of its convenience. If you have a GitHub repository, GitHub actions can be implemented with minimal changes to your codebase.

For each new project, I add a simple script to `.github/workflows` which sends a [repository dispatch](https://docs.github.com/en/actions/reference/events-that-trigger-workflows#repository_dispatch) event to the megalith repository. The megalith repository then pulls the latest changes from the project repository and merges it with its own git history.

In the megalith repository, I have a CI/CD pipeline waiting for changes to be pushed to the master branch. Consequently, when I make a change to the megalith itself, or a sub repository, the CI/CD pipeline is triggered and the changes are deployed to the production server.

## DNS

I registered thatcherthornberry.com with [Google](https://domains.google.com). There are (at least) two parts to every domain name: the second-level domain (thatcherthornberry) and the top-level domain (com). Google is a registrar, which means they manage the second-level domain. All top-level domains are managed by [ICANN](https://www.icann.org/), which is a non-profit organization that manages the internet's domain name system. ICANN delegates management of specific top-level domains to different organizations. For instance, the U.S. based company VeriSign manages the .com and .net top-level domains.

After registering a domain, I pay Google $12 per year to keep it. However, this payment is split among the various organizations. Here is a made up [example of the breakdown](https://webmasters.stackexchange.com/questions/61467/if-icann-only-charges-18%c2%a2-per-domain-name-why-am-i-paying-10?newreg=68106e778e23493a829a5861411ad722):

- $0.18 to ICANN
- $8.85 to Verisign
- $0.30 to a credit card processor
- $2.67 to Google

### SSL

Once you've registered a domain, you have permission to use it. However, steps remain to serve content over your domain securely. Secure Sockets Layer (SSL) is a protocol to secure communications over the internet. I'll add more information to this section in the future. For now, I'll just say that I use [Let's Encrypt](https://letsencrypt.org/) to generate SSL certificates for my domains. A Docker container runs a client to interface with the Let's Encrypt Certificate Authority to generate a wildcard certificate for thatcherthornberry.com. The certificate is valid for all subdomains of thatcherthornberry.com. Thus, allowing me to serve content over https for an domain under my website such as <https://qsongs.thatcherthornberry.com>. and <https://blog.thatcherthornberry.com>.

## Nginx

In the name of cost efficiency, I host all of my projects on a single e2-micro VM from Google for $3 per month. Within Google's domain management service, I created a few rules to route all traffic to thatcherthornberry.com or \*.thatcherthornberry.com to the VM. Nginx receives all requests to port 80 and 443 (http and https, it forwards http request to the SSL port 443). When it receives a request, it checks the host header to determine which project to serve. Thus, a request to <https://qsongs.thatcherthornberry.com> will be routed to the Docker container hosting the QSongs project. Once it hits that container, the request is handled by the container's logic (typically a Gunicorn web server serving a Django project).

Additionally, Nginx is configured to serve static files directly from the file system. This is handy because Gunicorn is not optimized to serve static files.

## Docker

Docker is one of my favorite technologies. It allows isolated environments to coexist on a single host.

As mentioned, the core of each project lives in its own Docker container. Nginx forwards requests to the appropriate container and the project can handle that request however it needs to.

Although the core of each project is isolated, to save resources, projects often share resources with eachother. For instance, many of my projects use PostgreSQL as a database. A single container runs a PostgreSQL server and all projects connect to that server and use their own isolated Database.

### Docker Compose

Docker Compose is a simple tool for container orchestration. All it really does is allow you to define a set of containers and their dependencies in a single file and deploy them with a single command.

To deploy all of my projects and there containers, I need to create a single docker-compose.yaml file which holds the configuration for each project. In the past, I would have to manually create this file. Recently, I created an aggregator which pulls the docker-compose file for each project and merges them into a single file.

## Problems, The Future

This megalith architecture has served me well for almost 2 years. Thus I've had time to identify some insatisfactory aspects of the architecture.

### Git Subtree Issues

The biggest gripe I have with Git Subtree is its instability. While making changes in the megalith repository, I have to be very careful not to make changes to any files that belong to a subtree as this will cause major conflicts.

Additionally, I haven't put the time in to automating the process of creating git subtrees within the megalith. So, each time I'd like to deploy a new project to my site, I have to manually create a git subtree. Although this is a simple process, it is not maximally efficient.

I haven't yet landed on a potential solution.

### Nginx Issues

Unlike Docker Compose, I've failed to create an aggregator for Nginx. Thus, each time I deploy a new project, I have to manually add a new server block to the Nginx configuration. Once I find the motivation, I'll create an aggregator for these .conf files.
