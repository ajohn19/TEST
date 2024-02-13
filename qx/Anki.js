// Quantumult X引用地址： https://raw.githubusercontent.com/ajohn19/TEST/main/qx/Anki.js
// Surge/Shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/main/surge/Anki.sgmodule
// Loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/main/loon/Anki.plugin
// Stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/main/stash/Anki.stoverride





 */
var body = JSON.parse($response.body);

body.data.is_vip = true;
body.data.vip_expire_at = 4102403992;
body.data.vip_end_at = 4102403992;
body.data.vip_day = 999; 

$done({ body: JSON.stringify(body) });
