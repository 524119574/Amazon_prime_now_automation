# Amazon Prime Now Automation script
This is a script that uses the selenium framework that help you to get a slot for prime now delivery.

## Get Started
First you will need to download the Google Chrome Driver from [here](https://chromedriver.chromium.org/downloads) and add it to path.

Once you download and extract it you will  need to
```bash
mv <path-to-your-driver> /usr/local/bin
```

You then need to set your email, password and 2FA token to the `amazon_email`, `amazon_password` and `otp_key`.
```bash
export amazon_email=<your-email>
export amazon_password=<your-password>
export otp_key=<your-otp-key-for-2fa>
```

## What it does
It will open the prime now and then try to login and go to the page where the website release the slot, it will minimize the browser window and then refresh every 1 minutes in the background. Once it finds a slot it will shows up the browser window and then try to book you into the slot.

## Running it on AWS.
First you will need to get an AWS EC2 instance.
And then you will need to `ssh` into the instance by running:
```bash
ssh -i <path-to-key> ec2-user@<public-dns>
```

Install Chrome driver:

```bash
cd /tmp
wget https://chromedriver.storage.googleapis.com/2.37/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
chromedriver --version 
```

Install Google Chrome:
```bash
curl https://intoli.com/install-google-chrome.sh | bash
sudo mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
google-chrome --version && which google-chrome
```

Install Python3 if necessary:
```bash
sudo yum list all | grep python
```
Install the version that you want to since the naming might not simply
be `python3` or `python3.7`.

And then install `pip`
```bash
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
```

Now if you want to running the script even if you exit the session you can use
`tmux` which you need to install by running `sudo yum install tmux`

And then you run
```bash
tmux              // enter into a new session
python3 main.py   // run the script
ctrl + B D        // detach the session, press these keys in order
exit              // quit the ssh session
```
And then after you `ssh` back in you can run: `tmux list` to make sure that
the session is running in the background

You can then attach to the session by running
```bash
tmux a 0
```



