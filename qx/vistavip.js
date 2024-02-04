/*
 * 项目名称: vistavip.js
 * Quantumult X 链接: https://raw.githubusercontent.com/ajohn19/TEST/main/qx/vistavip.js
 * Surge 模块链接: https://raw.githubusercontent.com/ajohn19/TEST/main/surge/vistavip.sgmodule
 * Loon 插件链接: https://raw.githubusercontent.com/ajohn19/TEST/main/loon/vistavip.plugin
 * Stash 覆写链接: https://raw.githubusercontent.com/ajohn19/TEST/main/stash/vistavip.stoverride
 */
var body = $response.body;

// 将 "isVip":\d 替换为 "isVip": 1
body = body.replace(/"isVip":\d/g, '"isVip":1');

// 将 "isMiniVip":\d 替换为 "isMiniVip": null
body = body.replace(/"isMiniVip":\d/g, '"isMiniVip":null');

// 将 "endTime":\d+ 替换为 "endTime": 169522559900099
body = body.replace(/"endTime":\d+/g, '"endTime":169522559900099');

// 将 "isActive":\d 替换为 "isActive": 1
body = body.replace(/"isActive":\d/g, '"isActive":1');

// 将 "isUpgradeVip":0 替换为 "isUpgradeVip":1
body = body.replace(/"isUpgradeVip":0/g, '"isUpgradeVip":1');

// 将 "expireVip":\d 替换为 "expireVip": 0
body = body.replace(/"expireVip":\d/g, '"expireVip":0');

// 将 "subscription":null 替换为 "subscription": ""
body = body.replace(/"subscription":null/g, '"subscription":""');

// 将 "checkInStatus":0 替换为 "checkInStatus": 1
body = body.replace(/"checkInStatus":0/g, '"checkInStatus":1');

// 将 "expireVip":1 替换为 "expireVip": 0
body = body.replace(/"expireVip":1/g, '"expireVip":0');

// 将 "isfree":0 替换为 "isfree": 1
body = body.replace(/"isfree":0/g, '"isfree":1');

// 将 "isFree":0 替换为 "isFree": 1
body = body.replace(/"isFree":0/g, '"isFree":1');

// 将 "isPreview":0 替换为 "isPreview": 1
body = body.replace(/"isPreview":0/g, '"isPreview":1');

// 将 "isBuyArticle":0 替换为 "isBuyArticle": 1
body = body.replace(/"isBuyArticle":0/g, '"isBuyArticle":1');

// 将 "isFreeMag":0 替换为 "isFreeMag": 1
body = body.replace(/"isFreeMag":0/g, '"isFreeMag":1');

$done({ body });

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy stoverride change to trigger git commit
