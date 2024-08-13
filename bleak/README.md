### MacでBleakを使う方法

ペアリングが必要な場合

1. [BLE Scanner 4.0](https://apps.apple.com/jp/app/ble-scanner-4-0/id1221763603)などで事前にペアリングをする。
2. MacのBluetoothで接続解除していることを確認（Macで接続しているとプログラムから接続ができなかった.要調査）
3. read.pyで接続


LinuxだとMACアドレスが使われてMacだとUUIDが使われる。UUIDはセントラルごとに違うので注意。
