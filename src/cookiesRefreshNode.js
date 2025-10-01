const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');
const os = require('os');

async function getAppleAuthCookies() {
    // Use existing Chrome installation
    const userDataDir = path.join(os.homedir(), 'AppData', 'Local', 'Google', 'Chrome', 'User Data');
    const browser = await chromium.launchPersistentContext(userDataDir, {
        channel: 'chrome',
        headless: false,
        args: ['--profile-directory=Default']
    });

    try {
        // Get the first page or create one
        const page = browser.pages().length > 0 ? browser.pages()[0] : await browser.newPage();

        // Navigate to Apple Store page directly
        console.log("Accessing Apple Store website...");
        await page.goto('https://www.apple.com/shop/buy-iphone/iphone-17-pro');

        // Wait for navigation and dynamic content to load
        await page.waitForLoadState('networkidle');
        
        // Wait for page to stabilize
        await page.waitForTimeout(2000);
        
        // Wait for element and ensure it's in view
        const sizeSelector = page.locator("input[data-autom='dimensionScreensize6_9inch']");
        await sizeSelector.waitFor({ state: 'attached' });
        
        // Disable smooth scrolling and sticky header
        await page.evaluate(() => {
            document.querySelector('.rf-bfe-stickybar').style.position = 'static';
            window.scrollTo = (x, y) => { window.scroll(x, y) };
        });
        
        // Scroll and wait
        await page.evaluate(() => {
            const element = document.querySelector("input[data-autom='dimensionScreensize6_9inch']");
            if (element) {
                element.scrollIntoView();
                window.scrollBy(0, -100); // Adjust to avoid floating headers
            }
        });
        
        // Wait for scroll to complete
        await page.waitForTimeout(1000);
        
        // Click via JavaScript
        await page.evaluate(() => {
            const element = document.querySelector("input[data-autom='dimensionScreensize6_9inch']");
            if (element) {
                element.click();
                element.checked = true;
            }
        });
        
        // Wait for click to take effect
        await page.waitForTimeout(1000);
        
        // Continue with other selections using JavaScript
        const selectors = [
            "input[data-autom='dimensionColordeepblue']",
            "input[value='2tb'][name='dimensionCapacity']",
            "#noTradeIn",
            "input[value='fullprice']",
            "input[name='carrierModel'][value='UNLOCKED/US']",
            "input[name='applecare-options'][data-autom='noapplecare']"
        ];
        
        for (const selector of selectors) {
            await page.evaluate((sel) => {
                const element = document.querySelector(sel);
                if (element) {
                    element.click();
                    if (element.type === 'radio' || element.type === 'checkbox') {
                        element.checked = true;
                    }
                }
            }, selector);
            await page.waitForTimeout(500);
        }
        
        // Click Check availability
        await page.evaluate(() => {
            const element = document.evaluate(
                "//span[text()='Check availability']",
                document,
                null,
                XPathResult.FIRST_ORDERED_NODE_TYPE,
                null
            ).singleNodeValue;
            if (element) {
                element.click();
            }
        });
        
        // Wait for click to process
        await page.waitForTimeout(2000);

        // Get all cookies from the browser context
        const cookies = await browser.cookies();

        // Filter required cookies
        const requiredCookies = {};
        for (const cookie of cookies) {
            if (['dssid2', 'shld_bt_ck'].includes(cookie.name)) {
                requiredCookies[cookie.name] = cookie.value;
                console.log(`Found ${cookie.name}: ${cookie.value}`);
            }
        }

        // Create the cookies directory if it doesn't exist
        await fs.mkdir(path.join(__dirname, 'src', 'appleEndpoints'), { recursive: true });

        // Format all cookies for requests
        const formattedCookies = {};
        for (const cookie of cookies) {
            formattedCookies[cookie.name] = cookie.value;
        }

        // Save all formatted cookies
        await fs.writeFile(
            path.join(__dirname, 'src', 'appleEndpoints', 'cookiesHome.json'),
            JSON.stringify(formattedCookies, null, 4)
        );

        console.log(`\nSaved ${Object.keys(formattedCookies).length} cookies to cookiesHome.json`);

    } catch (error) {
        console.error(`An error occurred: ${error.message}`);
    } finally {
        // Close the browser context
        await browser.close();
    }
}

// Helper function to format cookies for requests
function formatCookiesForRequests(cookies) {
    return cookies.reduce((acc, cookie) => {
        acc[cookie.name] = cookie.value;
        return acc;
    }, {});
}

// Run the script
getAppleAuthCookies().catch(console.error);