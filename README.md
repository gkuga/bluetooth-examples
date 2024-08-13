ネットを探すと同時接続数に関して様々な制限にかんする問題について言及されている。

- [Part F. Controller Error Codes](https://www.bluetooth.com/wp-content/uploads/Files/Specification/HTML/Core-54/out/en/architecture,-mixing,-and-conventions/controller-error-codes.html)
- [Is there a maximum of parallel BLE Connections? Only 5 are working! #214](https://github.com/noble/noble/issues/214)
- [HFP: Error 0x0d (connection rejected due to limited resources) when HF initiates a synchronous connection](https://github.com/bluekitchen/btstack/issues/175)
- [BLE-Stack APIs](https://software-dl.ti.com/lprf/simplelink_cc2640r2_sdk/1.35.00.33/exports/docs/ble5stack/ble_user_guide/html/doxygen/group___h_c_i___error___codes.html)
- [bluez/bluez/doc/errors.txt](https://github.com/bluez/bluez/blob/master/doc/errors.txt)
- [Raspberry Pi 3B+ が保持できる BLE コネクション数の限界を調べてみた #RaspberryPi](https://dev.classmethod.jp/articles/raspberry-pi-3b-plus-max-ble-connection/)

### 同時接続数に関する仮説

Bluetoothドングルの同時接続数がまず存在する。その制限に関してはHCIでエラーが定義されている。その次にUSBハブの帯域が問題になる。最後にBluetoothスタックで接続を維持するときのリソース制限が問題になる。リソースにはメモリやCPU,g_io_add_watch_fullなどでファイルやソケットを監視したときの上限など。

### 制限に係る事項(要調査)

- Bluetoothアダプタのハードウェア制限
  - 多くの市販のBluetoothアダプタは、同時に5～10台程度のデバイスに接続できるように設計されているが、特定の高性能アダプタではそれ以上の接続が可能。
- Bluetoothスタックの制限
  - LinuxのBluetoothスタック（たとえば、BlueZ）の実装にも制限がある。BlueZは通常、20～30台程度のデバイスと同時に接続することができるが、これもシステムの設定やアダプタの能力に依存する。スタック自体に特別な設定を施すことで、さらに多くのデバイスをサポートすることも可能。
- システムリソース
  - CPU、メモリ、ネットワーク帯域などのシステムリソースも制限要因となる。接続するデバイスが増えると、これらのリソースが消費され、限界に達するとそれ以上の接続が困難になる。
- 接続の種類（CentralとPeripheralの役割）
  - LinuxがCentral（ホスト）として動作する場合、接続できるPeripheral（周辺機器）の数には制限がある。Peripheralとしての接続は通常、1つのデバイスのみが接続先として機能しますが、Centralとして動作する場合には複数のデバイスと同時に接続可能。
- プロファイルごとの制限
  - 接続に使用するBLEプロファイルにも制限がある場合がある。たとえば、特定のプロファイルが同時に扱える接続数に制約がある場合、その制約が全体の接続数に影響を与えることがある。

実際の制限は、使用するBluetoothアダプタやカーネルバージョン、BlueZのバージョンに依存する。具体的な制限を確認するためには、hciconfig, btmon, btinfo などのツールでアダプタの状態を調べたり、BlueZの設定ファイルを確認したりすることが有効。

`hciconfig -a` によりLMPバージョン,Bluetoothのバージョンが表示される。BLEをサポートしているか確認できる。アダプタの型番や製造元, これに基づいて、製造元のドキュメントを参照し、同時接続数の制限を確認することができる。

#### USBハブによる制限

- 帯域幅の制約
  - BluetoothアダプタはUSBポートを介して接続されているため、USBポートの帯域幅が制約になる。複数のBluetoothアダプタをUSBハブに接続すると、USBバス全体の帯域幅が分割され、帯域幅が不足する可能性がある。この帯域幅の制約により、データ転送速度が低下し、接続の安定性やパフォーマンスが影響を受けることがある。一部のUSBポートやチップセットには、接続できるデバイスの数に制限がある。USB 2.0では、ポートの帯域幅が制限されており、複数のBluetoothアダプタを接続すると、パフォーマンスの低下が発生する可能性がある。USB 3.0やUSB 3.1のポートは、より多くの帯域幅を提供しますが、それでも帯域幅の制約がある。複数のBluetoothアダプタが同じUSBバスに接続されると、アダプタ間でリソースが競合し、パフォーマンスや接続の安定性に影響を与える可能性がある。
- 電力供給の問題
  - USBハブは、接続されたデバイスに対して電力を供給する。バスパワーのハブを使用する場合、電力供給が不足することがある。特に、Bluetoothアダプタが多く接続されている場合、十分な電力を供給できず、接続が不安定になることがある。
- ハブの品質と設計
  - 高品質なUSBハブは、電力供給や帯域幅の管理が適切に行われるため、Bluetoothアダプタの接続数に対する影響が少なくなる。しかし、低品質なハブや電力供給が不十分なハブでは、接続数が増えると問題が発生することがある。

`lsusb -t` で接続するUSBのバージョンはわかる。

#### その他

ドライバを変えることも何かに寄与するかもしれない

- [Realtek RTL8761B の Bluetooth 5 USB ドングルを Linux で動かす](https://qiita.com/aryta/items/86b3b1287629611efce1)
