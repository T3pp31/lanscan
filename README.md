# Lan Scan
LAN内に存在するデバイスを探索し，IPアドレス，MACアドレス，ベンダ，ホスト名を表示します．
Searches for devices in the LAN and displays their IP address, MAC address, vendor, and host name.

# 注意事項
このリポジトリのプログラムを第三者のサーバ，サービス，コンピュータ等に用いないでください．
許可された範囲内で利用してください．
このリポジトリの作成者はいかなる責任も負いません．


# 動作確認環境
Python3.9.7

# How to use
使うNICによって'en0'の部分を書き換えてください．

# 並列化
192.168.1.1のポートスキャンをしているのと同時に
192.1681.2~4程度まで同時にポートスキャンできるようにしたい
'