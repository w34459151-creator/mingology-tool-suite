# 地址库更新方案

## 采用的来源

- 中国行政区：现有 `rebuild_cn_address_library.py`，来源为 modood 行政区数据。
- 全球城市和居民点：`update_address_library.py` 使用 GeoNames 下载快照。
- 真太阳时只使用记录中的经度；地址必须先解析出坐标。

没有一个全球地址库同时做到“最全、最新、行政层级统一、免费、可离线”。GeoNames 覆盖广且可下载，适合作为离线主库；OpenStreetMap/Nominatim 适合人工补充，不适合作为每次排盘的唯一在线依赖。

## 每月更新

双击 `install_monthly_address_update.bat` 创建 Windows 任务计划。任务在每月 1 日 03:00 执行 `run_monthly_address_update.bat`。

更新器具有以下保护：

- 先下载并生成临时数据，校验数量、层级字段和经纬度。
- 校验失败或网络失败时，不替换现有地址库。
- 只替换 WORLD 记录，保留现有 CN 记录。
- 使用原子替换，避免程序读到半个 JSON 文件。

默认数据集为 `cities500`，约覆盖全球人口大于 500 的 populated places，适合 Tkinter 地址选择器。若确实需要最大覆盖量，可把任务环境变量 `GEONAMES_DATASET` 设置为 `allCountries`，但数据量会显著增大，地址选择器也会变得不适合直接展示全部记录。

## 运行前提

GeoNames 数据采用 CC BY 4.0，应在软件关于页面或文档中保留来源说明。月度任务需要网络访问 `download.geonames.org`。建议先手动运行 `run_monthly_address_update.bat`，确认下载、磁盘空间和更新时间均正常，再安装任务计划。

## 仍需保留的硬规则

地址解析失败时不得静默按北京时间排盘；应阻止排盘并要求用户选择地址或输入经度。所有排盘入口必须使用同一个已校验的真太阳时上下文。
