// Quantumult X引用地址： https://raw.githubusercontent.com/ajohn19/TEST/main/qx/hesheng.js
// Surge/Shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/main/surge/hesheng.sgmodule
// Loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/main/loon/hesheng.plugin
// Stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/main/stash/hesheng.stoverride























// qx引用地址： https://raw.githubusercontent.com/ajohn19/TEST/main/qx/hesheng.js
// surge/shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/main/surge/hesheng.sgmodule
// loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/main/loon/hesheng.plugin
// stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/main/stash/hesheng.stoverride


// qx引用地址： https://raw.githubusercontent.com/ajohn19/TEST/qx/hesheng.js
// surge/shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/surge/hesheng.sgmodule
// loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/loon/hesheng.plugin
// stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/stash/hesheng.stoverride


// qx引用地址： https://raw.githubusercontent.com/ajohn19/TEST/main/qx/hesheng.js
// surge/shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/main/surge/hesheng.sgmodule
// loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/main/loon/hesheng.plugin
// stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/main/stash/hesheng.stoverride

/*
 * 项目名称: hesheng
 * Quantumult X 链接: https://raw.githubusercontent.com/ajohn19/TEST/main/qx/hesheng.js
 * Surge 模块链接: https://raw.githubusercontent.com/ajohn19/TEST/main/surge/hesheng.sgmodule
 * Loon 插件链接: https://raw.githubusercontent.com/ajohn19/TEST/main/loon/hesheng.plugin
 * Stash 覆写链接: https://raw.githubusercontent.com/ajohn19/TEST/main/stash/hesheng.stoverride
 * 
 * 
 * 
 * 
 * 
 */
var anni = {};
var anni01 = JSON.parse(typeof $response != "undefined" && $response.body || null);
var headers = {};
for (var key in $request.headers) {
  const reg = /^[a-z]+$/;
  if (key === "User-Agent" && !reg.test(key)) {
    var lowerkey = key.toLowerCase();
    $request.headers[lowerkey] = $request.headers[key];
    delete $request.headers[key];
  }
}
var UA = $request.headers['user-agent'];
var uaProductMapping = {
  'SoundLab': {product_id: '8800'},
};
var receipt = {
  "quantity": "1",
  "purchase_date_ms": "1686776705000",
  "expires_date": "2099-12-31 05:05:05 Etc\/GMT",
  "expires_date_pst": "2099-12-31 05:05:05 America\/Los_Angeles",
  "is_in_intro_offer_period": "false",
  "transaction_id": "999999999999999",
  "is_trial_period": "false",
  "original_transaction_id": "999999999999999",
  "purchase_date": "2023-06-15 05:05:05 Etc\/GMT",
  "product_id": "888888888888888",
  "original_purchase_date_pst": "2023-06-15 05:05:05 America\/Los_Angeles",
  "in_app_ownership_type": "PURCHASED",
  "subscription_group_identifier": "20877951",
  "original_purchase_date_ms": "1686776705000",
  "web_order_line_item_id": "999999999999999",
  "expires_date_ms": "4102347905000",
  "purchase_date_pst": "2023-06-15 05:05:05 America\/Los_Angeles",
  "original_purchase_date": "2023-06-15 05:05:05 Etc\/GMT"
}
var renewal = {
  "expiration_intent": "1",
  "product_id": "888888888888888",
  "is_in_billing_retry_period": "0",
  "auto_renew_product_id": "888888888888888",
  "original_transaction_id": "999999999999999",
  "auto_renew_status": "0"
}
for (var uaKey in uaProductMapping) {
  if (UA && UA.includes(uaKey)) {
    var productInfo = uaProductMapping[uaKey];
    var product_id = productInfo.product_id;
    receipt.product_id = product_id;
    renewal.product_id = product_id;
    renewal.auto_renew_product_id = product_id;
    anni01.receipt.in_app = [receipt];
    anni01.latest_receipt_info = [receipt];
    anni.pending_renewal_info = [renewal];
    break;
  }
}
anni = anni01;
$done({ body: JSON.stringify(anni) });

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit

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
ummy stoverride change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit
