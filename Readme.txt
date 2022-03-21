此工具為利用adb指令紀錄裝置內CPU,GPU,Memory情況

setting.json內參數說明:

packageName:欲錄製之package名稱
frequency(s):欲錄製之頻率,預設值為1秒一次
enableCPU:是否允許錄製CPU使用量,預設為開啟
enableGPU:是否允許錄製GPU使用量,預設為開啟
enableMem:是否允許錄製記憶體使用量,預設為開啟
showAnimation:是否開啟即時繪製影像(待完成),預設為開啟

使用說明:
1.確定setting.json內參數正確,setting.json需與AppPerformanceMonitor.exe位於同一資料夾內
2.確定裝置有透過usb連上電腦
3.確認adb有安裝在電腦內,可透過命令提示字元輸入: adb version 確認已安裝
4.開啟AppPerformanceMonitor.exe

作業系統:
目前只支援windows,mac待完成

開發:
修改後如欲重新打包成exe,到此資料夾下使用指令: pyinstaller -F AppPerformanceMonitor.py

確認結果:
(範例)
Memory total: 88.245 MB
Now: 2021/11/04/ 15:41:07
CPU : 22%

Memory total: 94.706 MB
Now: 2021/11/04/ 15:41:18
CPU : 22%
可以看到目前時間,CPU,Memory情況,未來會試情況新增輸出csv檔功能