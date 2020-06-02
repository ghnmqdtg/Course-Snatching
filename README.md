# Course Snatching(Requests Version)
## Introduction
This tool is designed to get enrolled in NTUST courses by using Requests.

Since it's unlucky for some students to fail to get enrolled in courses they want, and I was learning python, so I made it to ameliorate the problem with what I've learned.

But I have to declare that **it's only for research purposes** because using such kinda tool is unfair for other students. The reason why I made it is all for training and improving myself.

**The tool had out of work since NTUST has an upgrade the way to anti-robot with Google's reCAPTCHA in April 2020**, so I think it's time to open source it.

~~The tool has a Selenium version, but the efficiency was terrible.~~

## Basic knowledge
1. Python
2. HTTP methods (GET / POST)
3. [Requests](https://requests.readthedocs.io/en/master/)
4. Understand how NTUST student information system works.


## Preparation
Before running the codes, you will need the following packages:
1. configparser: Parse configuration from config.ini.
2. requests: Send requests to sever and fetch data.
3. BeautifulSoup: Parse HTML elements and information.
4. Image and pytesseract: Deal with captcha.

## How it works?
The following steps tell how my script works:
1. Read configuration file and get user's login info with configparser.
2. Get login page and captcha image in session by using Requests.
3. Convert captcha image into text and delete garbled words.
4. Login (Go back to step.1 if captcha is wrong)
5. Submit course ID (check after submitting 10 times, if credits is still the same, keep doing)
6. Mission Complete.