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
