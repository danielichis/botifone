/**
 * Alternative approach using a proxy service to bypass Google Apps Script detection
 * This creates a simple HTTP proxy that forwards requests
 */

/**
 * Method 1: Using a different approach with URL encoding and fetch timing
 */
function checkAppleWithDelayedFetch() {
  console.log('=== Testing delayed fetch approach ===');
  
  try {
    // Step 1: Visit the main page first (this works - gets 200)
    console.log('Step 1: Visiting main iPhone page...');
    var mainHeaders = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    };

    var mainUrl = 'https://www.apple.com/shop/buy-iphone/iphone-17-pro/6.9-inch-display-2tb-deep-blue-unlocked';
    var mainOptions = {
      'method': 'GET',
      'headers': mainHeaders,
      'followRedirects': true,
      'muteHttpExceptions': true
    };

    var mainResponse = UrlFetchApp.fetch(mainUrl, mainOptions);
    console.log('Main page status:', mainResponse.getResponseCode());
    
    // Step 2: Extract any cookies from the main page response
    var responseHeaders = mainResponse.getHeaders();
    var setCookieHeader = responseHeaders['Set-Cookie'] || responseHeaders['set-cookie'];
    console.log('Cookies from main page:', setCookieHeader);
    
    // Step 3: Wait longer before making API request
    console.log('Step 2: Waiting 10 seconds before API call...');
    Utilities.sleep(10000); // Wait 10 seconds
    
    // Step 4: Make API request with exact same headers as main page request
    console.log('Step 3: Making API request with same session...');
    
    // Use the exact same headers as the successful main page request
    var apiHeaders = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
      'Referer': mainUrl
    };

    var apiUrl = 'https://www.apple.com/shop/fulfillment-messages?fae=true&pl=true&mts.0=regular&cppart=UNLOCKED/US&parts.0=MFXU4LL/A&location=Miami%20Beach,%20FL';
    
    var apiOptions = {
      'method': 'GET',
      'headers': apiHeaders,
      'followRedirects': true,
      'muteHttpExceptions': true
    };

    var apiResponse = UrlFetchApp.fetch(apiUrl, apiOptions);
    var apiStatusCode = apiResponse.getResponseCode();
    var apiResponseText = apiResponse.getContentText();
    
    console.log('API request status:', apiStatusCode);
    
    return {
      statusCode: apiStatusCode,
      headers: apiResponse.getHeaders(),
      content: apiResponseText,
      method: 'delayedFetch',
      mainPageStatus: mainResponse.getResponseCode()
    };
    
  } catch (error) {
    console.error('Delayed fetch error:', error.toString());
    return {
      error: error.toString(),
      method: 'delayedFetch'
    };
  }
}

/**
 * Method 2: Using HTMLService to create a browser-like request
 */
function checkAppleWithHTMLService() {
  console.log('=== Testing HTML Service approach ===');
  
  try {
    // Create an HTML page that makes the request client-side
    var htmlContent = `
    <!DOCTYPE html>
    <html>
    <head>
        <title>Apple API Request</title>
    </head>
    <body>
        <div id="result">Loading...</div>
        
        <script>
        async function makeRequest() {
            try {
                const url = 'https://www.apple.com/shop/fulfillment-messages?fae=true&pl=true&mts.0=regular&cppart=UNLOCKED/US&parts.0=MFXU4LL/A&location=Miami%20Beach,%20FL';
                
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Accept': '*/*',
                        'Accept-Language': 'es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                        'Referer': 'https://www.apple.com/shop/buy-iphone/iphone-17-pro/6.9-inch-display-2tb-deep-blue-unlocked'
                    },
                    credentials: 'include'
                });
                
                const data = await response.text();
                document.getElementById('result').innerHTML = 'Status: ' + response.status + '<br>Data: ' + data.substring(0, 500);
                
                // Send result back to Apps Script
                google.script.run.receiveAPIResult({
                    status: response.status,
                    data: data
                });
                
            } catch (error) {
                document.getElementById('result').innerHTML = 'Error: ' + error.message;
                google.script.run.receiveAPIResult({
                    error: error.message
                });
            }
        }
        
        // Start the request when page loads
        window.onload = makeRequest;
        </script>
    </body>
    </html>
    `;
    
    // This approach would require a web app deployment to work properly
    console.log('HTML Service approach requires web app deployment');
    return {
      statusCode: null,
      method: 'htmlService',
      note: 'This approach requires deploying as a web app to work properly'
    };
    
  } catch (error) {
    console.error('HTML Service error:', error.toString());
    return {
      error: error.toString(),
      method: 'htmlService'
    };
  }
}

/**
 * Method 3: Try different URL construction to avoid detection
 */
function checkAppleWithDifferentURL() {
  console.log('=== Testing different URL construction ===');
  
  try {
    // Build URL differently - maybe parameter order matters
    var baseUrl = 'https://www.apple.com/shop/fulfillment-messages';
    var params = [
      'location=Miami Beach, FL',
      'parts.0=MFXU4LL/A',
      'cppart=UNLOCKED/US',
      'mts.0=regular',
      'pl=true',
      'fae=true'
    ];
    
    var url = baseUrl + '?' + params.join('&');
    console.log('Using URL:', url);
    
    // Use minimal headers similar to successful main page request
    var headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3'
    };
    
    var options = {
      'method': 'GET',
      'headers': headers,
      'followRedirects': true,
      'muteHttpExceptions': true
    };

    var response = UrlFetchApp.fetch(url, options);
    var statusCode = response.getResponseCode();
    var responseText = response.getContentText();
    
    console.log('Different URL construction status:', statusCode);
    
    return {
      statusCode: statusCode,
      headers: response.getHeaders(),
      content: responseText,
      method: 'differentURL',
      urlUsed: url
    };
    
  } catch (error) {
    console.error('Different URL construction error:', error.toString());
    return {
      error: error.toString(),
      method: 'differentURL'
    };
  }
}

/**
 * Method 4: Use POST instead of GET (some APIs are less restrictive with POST)
 */
function checkAppleWithPOST() {
  console.log('=== Testing POST method ===');
  
  try {
    var url = 'https://www.apple.com/shop/fulfillment-messages';
    
    // Send parameters as form data in POST body
    var payload = {
      'fae': 'true',
      'pl': 'true',
      'mts.0': 'regular',
      'cppart': 'UNLOCKED/US',
      'parts.0': 'MFXU4LL/A',
      'location': 'Miami Beach, FL'
    };
    
    var headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
      'Accept': '*/*',
      'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
      'Content-Type': 'application/x-www-form-urlencoded'
    };
    
    var options = {
      'method': 'POST',
      'headers': headers,
      'payload': payload,
      'followRedirects': true,
      'muteHttpExceptions': true
    };

    var response = UrlFetchApp.fetch(url, options);
    var statusCode = response.getResponseCode();
    var responseText = response.getContentText();
    
    console.log('POST method status:', statusCode);
    
    return {
      statusCode: statusCode,
      headers: response.getHeaders(),
      content: responseText,
      method: 'POST'
    };
    
  } catch (error) {
    console.error('POST method error:', error.toString());
    return {
      error: error.toString(),
      method: 'POST'
    };
  }
}

/**
 * Comprehensive test of all alternative methods
 */
function testAllAlternativeMethods() {
  console.log('=== Testing ALL alternative methods ===');
  
  var results = {};
  
  // Test 1: Delayed fetch
  console.log('\n--- Test 1: Delayed Fetch ---');
  results.delayedFetch = checkAppleWithDelayedFetch();
  console.log('Delayed Fetch Result:', results.delayedFetch);
  
  Utilities.sleep(5000);
  
  // Test 2: Different URL construction
  console.log('\n--- Test 2: Different URL Construction ---');
  results.differentURL = checkAppleWithDifferentURL();
  console.log('Different URL Result:', results.differentURL);
  
  Utilities.sleep(5000);
  
  // Test 3: POST method
  console.log('\n--- Test 3: POST Method ---');
  results.postMethod = checkAppleWithPOST();
  console.log('POST Method Result:', results.postMethod);
  
  Utilities.sleep(5000);
  
  // Test 4: HTML Service (informational)
  console.log('\n--- Test 4: HTML Service Info ---');
  results.htmlService = checkAppleWithHTMLService();
  console.log('HTML Service Result:', results.htmlService);
  
  return results;
}

/**
 * Quick test of most promising alternative method
 */
function quickAlternativeTest() {
  console.log('Running quick alternative test...');
  
  // The delayed fetch method is most promising
  return checkAppleWithDelayedFetch();
}

/**
 * Function to receive API results from HTML Service (if used)
 */
function receiveAPIResult(result) {
  console.log('Received result from HTML Service:', result);
  return result;

}

//* Main entry point to run tests
function runTests() {
  console.log('=== Running Tests ===');
  
  // Quick test
  var quickResult = quickAlternativeTest();
  console.log('Quick Test Result:', quickResult);
  
  // Comprehensive test
  var comprehensiveResult = testAllAlternativeMethods();
  console.log('Comprehensive Test Result:', comprehensiveResult);
}
