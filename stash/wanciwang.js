[rewrite_local]
# 万词王签到
^https:\/\/recite\.perfectlingo\.com\/api\/dictionary\/dic\/v1\/get-dic-patch url script-response-body wanciwang-signin.js

[mitm]
hostname = recite.perfectlingo.com

// 万词王签到脚本
var options = {
    url: 'https://recite.perfectlingo.com/api/dictionary/dic/v1/get-dic-patch?baseVersion=18',
    method: 'GET',
    headers: {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'recite.perfectlingo.com',
        'Connection': 'keep-alive'
    }
};

$task.fetch(options).then(response => {
    // 请求成功时的处理
    console.log('Response:', response.body);
    if (response.statusCode == 200) {
        // 假设状态码 200 表示签到成功
        $notify('万词王签到成功', '', response.body);
    } else {
        // 状态码不是 200 表示签到可能失败
        $notify('万词王签到失败', '', '状态码: ' + response.statusCode);
    }
}, error => {
    // 请求失败时的处理
    console.log('Error:', error);
    $notify('万词王签到出错', '', error);
});