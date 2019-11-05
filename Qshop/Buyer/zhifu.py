from alipay import AliPay
def Pay(order_id,money):
    alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjpjxQzW2Sgf8k+E0d0HlCFndVlJ5qxSYV+FOgp8HkeIex5AykWa+fKLUcTw89bUUSwVhtgslVIg+TiTWwwU1fbWJbXoHkTzpMxAOtT6hwynskGvxcYUXkwlljUp98HycujUVES1Kbt7Yrf/Y3bLC2Cw+Hd3Ne5IWcfD3EO7ipKjd3f/D3Djnd7geMg1yTkyvM+30tdY5mGF1qz1Gw6M26SBkw/cpqwsbxg9vq+hWSHzuTBZQ77RmhR6sNNUCB4qTyH3EvxyqELIsm+bTANdJt7HFeTaABTTvRAHsp4ImQyDMHA7pW3FDHMyvLpDipvOhDE9LjtWbFtYezBXVVSTPjwIDAQAB
    -----END PUBLIC KEY-----"""

    alipay_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
        MIIEogIBAAKCAQEAjpjxQzW2Sgf8k+E0d0HlCFndVlJ5qxSYV+FOgp8HkeIex5AykWa+fKLUcTw89bUUSwVhtgslVIg+TiTWwwU1fbWJbXoHkTzpMxAOtT6hwynskGvxcYUXkwlljUp98HycujUVES1Kbt7Yrf/Y3bLC2Cw+Hd3Ne5IWcfD3EO7ipKjd3f/D3Djnd7geMg1yTkyvM+30tdY5mGF1qz1Gw6M26SBkw/cpqwsbxg9vq+hWSHzuTBZQ77RmhR6sNNUCB4qTyH3EvxyqELIsm+bTANdJt7HFeTaABTTvRAHsp4ImQyDMHA7pW3FDHMyvLpDipvOhDE9LjtWbFtYezBXVVSTPjwIDAQABAoIBADaOiW//ctjsKVSiyyH9khUZ3LcUIvyzin3E8/bBxXGpI8GSh+Zdeu/QlJsmQuR2/Waejn3J0eR/o+bd7VT7/zUzaXr7Pz3wIgCpWhc5+UXkGmA/DEc0doqJA9OE9p417vjHKmJCA8JbfGdGBcD8jdOLSdC/dcibYf8CBGT0IL6CToSu/5daykAqGpaxc071Dc5I3Mnwx53eYQnJfvxHIzmzfHtVmT0uZGpFJPzO2cRKjv+qhUPR6Xy8XOy/dxgz/vKEi+pnKOwA1tqbAZti3J7fc/YaAXcAzBNG8sunt2tz0Ym0y8KQHHqY/cLAVF/NvzIei88WxG0r6QH7rQbaWOECgYEA9IPABJcE+mBYauaUB5S+p25OGLr8K1bQOO9D4LGe1/bPKRJSeu9gWhn3/ZQa0xCQMlE/QQ1fCpuOBnX7QiTG/ueieDKx8MoFaVUZiGySeRuNVFDYVs4j+7dlnGPBawXAibaSYS1Hfj5x7FEzHxZEO36V4OUBT63Z+WKlP9J6gWkCgYEAlUunahjEF52RSrKc8mibpHU/CgnIau8Shk3jDUSdkEBQEUDyafjzKxywhKzeAXX/M2lbC2ikKklF5RiXLvN/NINhjZ2uTIexc1b0iRmQGgqXSyQZuBSYZ1kKb3rhZEgFuracJZnrIbBLHbv/8eqM5dnfF2qlMQyQBdLrlMUYsjcCgYB7fYreBpO6DCy7mMaMaaA8mWYR8WXoUYkKKDUk5zAtLHaF7L4BXqJP/yuTQ1ik3omlEAmdRi6JAfUh6DZEuqRSGxSgFiJuVOmUwCkMEKGNTs/7FHWeqa/cskw8Rtlpvtb19mJJd//Sj6Ej1AK4oZtGXPE/Swl1f31GCX8iE6BReQKBgB4Xw8UU/OGttw2RdyU9hLHfmDdTxXwYeGlt5ahU/lWHQRxZNQO7VHiKLeJwXcd5m1knkVx5WS3U2yvUixTBrBBPsygycmGmsFQJYP0JlAxLujdBLZX3QMkEH6Bc6nWmNtFt4YeKwORnfpydunduybvC8L7tliKO37Ds1OOF3vZ9AoGAZcFYFLJME7udrKrPjDxCgH+SpGjR60Delytr5uQkhUQ1mKHnfXq6+rGDu8w7AvqxTcS8xNbNmvJoeeoBJ4k2dNs0DcumGm5ULy7+vii1svlxE5xLRyq710WwD7HFlitvyBXJeUY3WPFxf7BT4phDBbKSCJRkYleebcWJpkWmqik=
    -----END RSA PRIVATE KEY-----"""

    alipay = AliPay(
        appid="2016101500695944",  # 支付宝app的id
        app_notify_url="",  # 回调视图
        app_private_key_string=alipay_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(money),  # 将Decimal类型转换为字符串交给支付宝
        subject="商贸商城",
        return_url="http://127.0.0.1:8000/Buyer/pay_result/", #完成之后返回
        notify_url="http://127.0.0.1:8000/Buyer/pay_result/"  # 可选, 不填则使用默认notify url
    )

    # 让用户进行支付的支付宝页面网址
    return "https://openapi.alipaydev.com/gateway.do?" + order_string

if __name__ == '__main__':
    print(Pay("100000002","1000"))