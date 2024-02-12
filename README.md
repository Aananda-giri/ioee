# ioee
* Django-powered application for Engineering Students.

# Features
## 1. Code Share
* **store and share** your lab work (**file/code**)
* **no login** required

* [deployed here in heroku](https://ioee.herokuapp.com/)

## 2. Pdf Search Engine
* **Searches pdfs** shared by other ioe students
* currently crawled (from google drive) and indexed over **`50,000 pdfs`**
* redis to cache the results.
* Deep search: split query text into individual words and search parallely (using thread pooling) for individual words.
* [deployed here in heroku](https://ioee.herokuapp.com/pdf)

# references:
* [django-heroku-deployment](https://devcenter.heroku.com/articles/deploying-python)
* [Repli's blog on their experience with code editors](https://blog.replit.com/code-editors)
* [code-mirror docs](https://codemirror.net/6/docs/)
* [setting up code-mirror](https://dyclassroom.com/codemirror/how-to-setup-codemirror)
