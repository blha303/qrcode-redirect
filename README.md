qrcode-redirect
===============

I have a Huawei G6608, which uses Opera Mini for its main web browser. I didn't want to use an external app for QR code reading, as 1. I doubt Java can use the camera properly, and 2. I'd want it to open in Opera Mini. So I made this.

Usage
-----

* Go to [qr.blha303.biz](http://qr.blha303.biz), upload a QR code, you'll get redirected.

or

* Clone the repository
* Get virtualenv and create a new virtualenv in the current directory: http://s3.pixane.com/pip_distribute.png `virtualenv venv -ppython2.7`
* `venv/bin/pip install -r requirements.txt`
* Edit config.json to point to 1. the web-accessible directory you'll be saving uploaded files, 2. this directory's web access path. Don't worry about changing extensions, unless you need to.
* `venv/bin/python qrcodes.py`. If it tells you to create the upload directory, make sure you do that (and check that it's web accessible)
* Open a browser, go to [http://\<ip of server\>:7578](http://qr.blha303.biz)

This should work with any browser; if you find one where it doesn't work, [create an issue and I'll have a look](https://github.com/blha303/qrcode-redirect/issues).

Before making this public, make sure you secure it. Anyone could upload a malicious script recognized by your web server, and if they know where the web accessible directory is they could execute this file and do damage to your machine. If you're using Apache, add this .htaccess file to the directory:

    <IfModule mod_php5.c>
        php_flag engine off
    </IfModule>
    Options -Indexes -FollowSymLinks