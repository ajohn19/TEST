




// Quantumult X引用地址： https://raw.githubusercontent.com/ajohn19/TEST/main/qx/zxhdmx.js
// Surge/Shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/main/surge/zxhdmx.sgmodule
// Loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/main/loon/zxhdmx.plugin
// Stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/main/stash/zxhdmx.stoverride


// qx引用地址： https://raw.githubusercontent.com/ajohn19/TEST/main/qx/zxhdmx.js
// surge/shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/main/surge/zxhdmx.sgmodule
// loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/main/loon/zxhdmx.plugin
// stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/main/stash/zxhdmx.stoverride


// qx引用地址： https://raw.githubusercontent.com/ajohn19/TEST/qx/zxhdmx.js
// surge/shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/surge/zxhdmx.sgmodule
// loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/loon/zxhdmx.plugin
// stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/stash/zxhdmx.stoverride


// qx引用地址： https://raw.githubusercontent.com/ajohn19/TEST/main/qx/zxhdmx.js
// surge/shadowrocket 模块地址： https://raw.githubusercontent.com/ajohn19/TEST/main/surge/zxhdmx.sgmodule
// loon 插件地址： https://raw.githubusercontent.com/ajohn19/TEST/main/loon/zxhdmx.plugin
// stash 覆写地址： https://raw.githubusercontent.com/ajohn19/TEST/main/stash/zxhdmx.stoverride

/*
 * 项目名称: zxhdmx
 * Quantumult X 链接: https://raw.githubusercontent.com/ajohn19/TEST/main/qx/zxhdmx.js
 * Surge 模块链接: https://raw.githubusercontent.com/ajohn19/TEST/main/surge/zxhdmx.sgmodule
 * Loon 插件链接: https://raw.githubusercontent.com/ajohn19/TEST/main/loon/zxhdmx.plugin
 * Stash 覆写链接: https://raw.githubusercontent.com/ajohn19/TEST/main/stash/zxhdmx.stoverride
 * 
 * 
 * 
 * 
 * 
 */
const anni = {};
const anni1 = JSON.parse(typeof $response != "undefined" && $response.body || null);

if (typeof $response == "undefined") {
  delete $request.headers["x-revenuecat-etag"];
  delete $request.headers["X-RevenueCat-ETag"];
  anni.headers = $request.headers;
} else if (anni1 && anni1.subscriber) {
  anni1.subscriber.subscriptions = anni1.subscriber.subscriptions || {};
  anni1.subscriber.entitlements = anni1.subscriber.entitlements || {};

  const data = {
    "expires_date": "2099-12-31T12:00:00Z",
    "original_purchase_date": "2022-11-18T03:57:16Z",
    "purchase_date": "2022-06-15T12:00:00Z",
    "ownership_type": "PURCHASED",
    "store": "app_store"
  };

  anni1.subscriber.subscriptions["truth_or_dare_premium_monthly"] = data;
  anni1.subscriber.entitlements["premium"] = JSON.parse(JSON.stringify(data));
  anni1.subscriber.entitlements["premium"].product_identifier = "truth_or_dare_premium_monthly";

  anni.body = JSON.stringify(anni1);
}

$done(anni);

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
igger git commit

// Adding a dummy stoverride change to trigger git commit

// Adding a dummy plugin change to trigger git commit

// Adding a dummy plugin change to trigger git commit
