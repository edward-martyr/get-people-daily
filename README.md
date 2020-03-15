# get-people-daily
获取人民日报电子版

# 使用方法

```sh
python3 get-people-daily.py -d yyyy.mm.dd
```

1. yyyy: 年份，四位；
2. mm: 月份，一位或两位；
3. dd: 天，一位或两位；

这个 Fork 修复了本来无法使用 `PyPDF2` 库合并 PDF 页面的问题，并可以显示文件大小。最后可以输出完整的 `yyyy-mm-dd.pdf`，而不是未合并的单独 PDF 页面。

