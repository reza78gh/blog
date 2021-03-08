# blog

blog is a Django project for show posts that write by some wirter and
other people can read , like and send comment for posts.

Usage
-----------

1. Set your DATABASE informations and SECRET_KEY in local_settings.py.sample and rename it to local_settings.py .

2. Install requirements.txt ``pip install -r requirements.txt`` .

3. Run ``python manage.py migrate`` to create models.

4. Run ``python manage.py creategroups`` to create groups
    >groups:
    >writer(نویسنده): can write new post.
    >editor(ویراستار): can write post and accept posts and comments.
    >manager(مدیر): can add, change and delete posts, comments, users, tag, category .
    >normal user is not in any group.
    >attention: each user must be in a group

5. Run ``python manage.py createsuperuser`` to cretae a super user and set users from admin panel.