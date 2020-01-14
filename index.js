const https = require('https')
const {parse} = require('node-html-parser')
const htmlparser2 = require("htmlparser2");

const parser = new htmlparser2.Parser(
    {
        onopentag(name, attribs) {
            if (name === "script" && attribs.type === "text/javascript") {
                console.log("JS! Hooray!");
            }
        },
        ontext(text) {
            console.log("-->", text);
        },
        onclosetag(tagname) {
            if (tagname === "script") {
                console.log("That's it?!");
            }
        }
    },
    { decodeEntities: true }
);

var options = {
    host: 'matheo.uliege.be',
    port: 80,
    path: '/handle/2268.2/1813'
  };
  

// const pageFetcher = new Promise((num) => {
//     const root = parse()
// })

https.get("https://matheo.uliege.be/handle/2268.2/6800", function(res) {
    console.log("Got response: " + res.statusCode);

    let data = ''
    res.on("data", function(chunk) {
        data += chunk
        // console.log("BODY: " + chunk);
    });

    res.on('end', () => {
        parser.write(data.toString())
        parser.end();
        // console.log(data.toString());
        // const root = parse(data)
        // console.log(root.querySelector('.btn'));
    });


    

  }).on('error', function(e) {
    console.log("Got error: " + e.message);
  });

