
const BrowserHistory = require('node-browser-history');
const prependFile = require('prepend-file');
const path = require('path');
const fs = require('fs')

/**
 * Gets Chrome History
 * @param historyTimeLength 
 * @returns {Promise<array>}
 */
BrowserHistory.getChromeHistory(1).then(function (history) {

    try {

        // get chrome history last minute only extract newest element

        const last_element = history[0].slice(-1)

        // from newest element extract title, url

        let page_title = last_element[0].title

        let page_url = last_element[0].url

        let file = path.join(__dirname, '..','data','history.txt')
        
        fs.readFile(file, 'utf8', function (err, data) {

            if (err) throw err;

            included = data.includes(page_url)

            if (included == false) {

                // create string to be logged in history.txt

                let write_output = [page_title, page_url]

                let url_output = [page_url]

                let write_string = page_title + "\n" + page_url + "\n"

                // prepend the wtite_string to history.txt

                prependFile(file, write_string, function (err) {

                    if (err) return console.log(err);
                               
                });
            }
            else {
                ///console.log('Reacently visited site already included')
            }

        });


    } catch (error) {
        //console.log("No new website visited ")
    }

});
