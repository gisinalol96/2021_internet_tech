# Домашнее задание по курсу "Технологии Интернет"

КОманды для запуска написаны для PowerShell, в Bash/zsh вместо "$env:" используем "export" или "env" соответственно

### В папке serverus:
Python >= 3.6
~~~
python -m pip install -r requirements.txt

$env:FLASK_APP = "server.py"

python -m flask run
~~~

### в папке clientus:
~~~
npm install
npm run serve
~~~
