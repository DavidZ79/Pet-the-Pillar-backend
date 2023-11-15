# python should already be installed: https://piazza.com/class/llh11qsijxu6gc/post/806

# download pip
sudo apt-get update
sudo apt-get install python3-pip

# install virtualenv: https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
pip install virtualenv

# activate venv
source venv/bin/activate

# install required packages
pip install Django
pip install djangorestframework
pip install djangorestframework-simplejwt

# install pillow prerequisites: https://pillow.readthedocs.io/en/latest/installation.html
sudo apt-get install libtiff5-dev libjpeg8-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev

# install pillow: https://pillow.readthedocs.io/en/latest/installation.html
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow --no-binary :all:

# migrations
python manage.py makemigrations
python manage.py migrate

echo "Startup completed successfully"