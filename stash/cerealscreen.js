[rewrite_local]
https:\/\/youxifanyizhushou\.com\/ios\/api\/ url script-response-body cerealscreen.js

[Mitm]
hostname = youxifanyizhushou.com

var Levi = JSON.parse($response.body);
Levi= {
  "data" : [
    {
      "productPayType" : 3,
      "times" : 30,
      "level" : 0,
      "desc" : "购买",
      "expireTime" : "2099-02-29 12:48:32"
    }
  ],
  "code" : 0
}


$done({body : JSON.stringify(Levi)});
