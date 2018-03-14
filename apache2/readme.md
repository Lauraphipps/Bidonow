# install

```
sudo a2enmod headers
sudo a2enmod proxy proxy_uwsgi
ln -s /app/apache2/webapp.conf /etc/apache2/sites-enabled/bitonow-webapp.conf
sudo service apache2 restart
```
