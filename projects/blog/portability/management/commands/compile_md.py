import os

import markdown
from django.core.management.base import BaseCommand

from portability.models import Post


class Command(BaseCommand):
    help = "Compile markdown files in portability/md_posts into html files in portability/templates"

    def handle(self, *args, **options):
        """
        This function handles the main logic of the script, which is to read markdown files,
        convert them to html, and then write the result to an html file.
        """
        files = os.listdir("portability/md_posts")
        for file in files:
            file_name = file.split(".")[0]
            with open(f"portability/md_posts/{file_name}.md", "r") as f:
                md = f.read()
                html = markdown.markdown(md)

                # Extract the subheading from the markdown file
                subheading = md.split("\n")[0].strip("# ")

                # get the image file name from the folder portability/static/portability/post_images
                # the image is the file name but may have any extension
                image_files = os.listdir("portability/static/portability/post_images")
                for image_file in image_files:
                    if image_file.split(".")[0] == file_name:
                        image = image_file
                        break

                # get or create the post in the database
                post, created = Post.objects.get_or_create(title=file_name)

                post.title = file_name
                post.image = image
                post.subheading = subheading
                post.content = html
                post.save()

                with open(f"portability/templates/posts/{file_name}.html", "w") as f:
                    html_content = self.render_template(file_name, html, subheading)
                    f.write(html_content)
                    print(f"Wrote {file_name}.html")

    def render_template(self, title, content, subheading):
        """
        This function reads in the base_md.html file, inserts the title, content, and subheading
        into the appropriate places in the file, and then returns the result as a string.
        """
        with open("portability/templates/base_md.html", "r") as f:
            base = f.read()
            # replace {{title}} with the title of the post
            base = base.replace("{{title}}", title)
            # replace {{content}} with the content of the post
            base = base.replace("{{content}}", content)
        return base
