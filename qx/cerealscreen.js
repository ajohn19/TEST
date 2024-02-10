









// Quantumult X引用地址： https://raw.githubusercontent.com/ajohn19/TEST/main/qx/cerealscreen.js
// Surge/Shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/main/surge/cerealscreen.sgmodule
// Loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/main/loon/cerealscreen.plugin
// Stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/main/stash/cerealscreen.stoverride

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

// Adding a dummy change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy change to trigger git commit
