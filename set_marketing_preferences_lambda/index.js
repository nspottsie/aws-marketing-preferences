'use strict';

exports.handler = (event, context, callback) => {
    console.log("Starting up with event data: " + JSON.stringify(event))

    const {Builder, By, Key, until} = require('selenium-webdriver');
    var chrome = require('selenium-webdriver/chrome');
    var builder = new Builder().forBrowser('chrome');
    var chromeOptions = new chrome.Options();
    const defaultChromeFlags = [
        '--headless',
        '--disable-gpu',
        '--window-size=1280x1696', // Letter size
        '--no-sandbox',
        '--user-data-dir=/tmp/user-data',
        '--hide-scrollbars',
        '--enable-logging',
        '--log-level=0',
        '--v=99',
        '--single-process',
        '--data-path=/tmp/data-path',
        '--ignore-certificate-errors',
        '--homedir=/tmp',
        '--disk-cache-dir=/tmp/cache-dir'
    ];

    chromeOptions.setChromeBinaryPath("/var/task/lib/chrome");
    chromeOptions.addArguments(defaultChromeFlags);
    builder.setChromeOptions(chromeOptions);

    // build the driver
    var driver = builder.build();
    console.log("Driver built")

    try {
        const marketing_url = process.env.marketing_preferences_url
        // navitage to the url
        driver.get(marketing_url);
        console.log("Page loaded: " + marketing_url)

        // click the "Unsubscribe From Email" button
        var unsubscribe_button = driver.findElement(By.xpath('//*[@id="Unsubscribe_bttn"]'))
        unsubscribe_button.click()
        console.log("Unsubscribe button clicked")

        // input the email address to unsubscribe
        driver.findElements(By.xpath('//*[@id="Email"]'))
              .then(function(emails){
                emails[0].sendKeys(event.email_address, Key.TAB)
              })
        console.log("Email entered:" + event.email_address)

        // tick the checkbox for unsubscribing from all emails
        var checkbox = driver.findElement(By.xpath('//input[@id="Unsubscribed"]'))
        driver.executeScript("arguments[0].click()", checkbox)
        console.log("Unsubscribe checkbox selected")

        // submit the form
        var submit = driver.findElement(By.xpath('//button[@class="mktoButton submit-unsub"]'))
        driver.executeScript("arguments[0].click()", submit)
        console.log("Form submitted")

        // wait for the page to load
        driver.wait(until.titleIs('AWS Preference Center Unsubscribe Confirmation Page'), 10000);
        console.log("Unsubscribe processed")
    } finally {
        driver.quit();
    }
};
