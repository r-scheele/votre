# heroku login - login into your heroku account
# heroku create [app_name] - create a unique app name
# git remote - check if heroku added the needed remote
# heroku addons:create [name_of_add - could be a postgres database - heroku-postgresql:hobby-dev]
# heroku logs -t - check the logs for errors
# heroku apps:info [app_name] - checks information about the app
# heroku run ["command"] - runs a normal terminal command on heroku example - heroku run "alembic upgrade head"
# heroku ps:restart restart the application on heroku

"""
to push changes to git and heroku
# git status
# git add .
# git commit -m [message]
# git push -u origin [branch] e.g main
# git push heroku [branch] e.g main
#
"""