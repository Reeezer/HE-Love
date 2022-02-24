# HE-Love
A Tinder web app alternative to find and meet people at school


## Clone to develop

### Step 1
Clone the project

```
git clone https://github.com/HE-Arc/HE-Love.git
```

### Step 2

Create a virtual env for the project

```
cd HE-Love
py -m venv .venv
```

### Step 3

Activate the venv

```
source .venv/Scripts/activate
```

### Step 4

Install dependecies

```
pip install -r requirements.txt
```

### Step 5

Start server

```
py manage.py runserver
```

The server will start on port 8000 by default

## Migrations

If it is the first install, you also need to run migrations and seeding

```
py manage.py migrate
py manage.py loaddata users genders
```

The loaddata command might be outdated. You need to add all models in the fixtures folder if that is the case

## Installing vue CLI

go to https://nodejs.org/en/ to download and install node.js current (17.6.0)
After that open a cmd and install vue-cli
```
npm install -g @vue/cli
```

Then run this command to compile vue on the fly

```
npm run serve
```
