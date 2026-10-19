# Cudy TR3000 V1 256MB · No-HNAT 定制版

基于 **ImmortalWrt 24.10-SNAPSHOT / Linux 6.6.133** 的第三方定制固件，版本日期为 **2026-10-11**。本版修复 256MB 型号升级镜像中的板型名称，并提供 No-HNAT 配置及 Aurora、Bandix、Nikki/Mihomo 等定制软件组合。

**[下载固件与校验文件](https://github.com/casiuna/immortalwrt-mt7981-cudy-tr3000/releases/tag/tr3000-v1-256mb-20261011)**

当前为 Pre-release，长期运行稳定性仍待实机反馈。

## 固件信息

| 项目 | 内容 |
| --- | --- |
| 支持型号 | Cudy TR3000 V1 256MB |
| 镜像类型 | squashfs sysupgrade |
| 系统 / 内核 | ImmortalWrt 24.10-SNAPSHOT / Linux 6.6.133 |
| 版本日期 | 2026-10-11 |
| 文件大小 | 43,326,286 字节，约 41.32 MiB |
| 源码分支 | `openwrt-24.10-6.6` |
| 源码提交 | `ec9ef10efc65da1e6d1de4e2c043c0e13d08eed8` |

固件文件名：

```text
immortalwrt-mediatek-filogic-20261011-cudy_tr3000-v1-256mb-squashfs-sysupgrade.bin
```

SHA256：

```text
8b79a12afa81fc82bbd4752710a52c5bca3ff4a401e584ca7e9f1a67a373f3f8
```

源码来自 [padavanonly/immortalwrt-mt798x-6.6](https://github.com/padavanonly/immortalwrt-mt798x-6.6)，另含本项目保存的配置、覆盖文件和补丁。Release 附件为本地原始成品；后续重新构建不保证得到相同的二进制摘要。

## 板型识别修复

设备树使用 `cudy,tr3000-v1-256mb`，升级镜像内部采用：

```text
BOARD=cudy_tr3000-v1-256mb
sysupgrade-cudy_tr3000-v1-256mb/CONTROL
```

修复在 `target/linux/mediatek/image/filogic.mk` 的设备定义中增加 `BOARD_NAME := cudy_tr3000-v1-256mb`，解决内部名称顺序错误。构建脚本自动应用补丁，并检查生成镜像的 CONTROL 和 rootfs，防止相同问题再次进入发布产物。

元数据保留旧名称 `cudy,tr3000-256mb-v1` 作为历史兼容别名。离线核验还包括实际 FIT 设备树、fwtool 元数据、SHA256 与 squashfs；详见 [验证记录](firmware-validation.json)。这些检查不替代设备适配确认和长期实机验证。

## No-HNAT 配置

本版采用以下设置：

- 关闭无线 `MTK_WHNAT_SUPPORT` 和 `MTK_WARP_V2`。
- 根据 WARP 开关决定是否打包及自动加载 `mtk_warp_proxy.ko`。
- 通过零字节 `20-mediatek_hnat`、`60-warp` 文件覆盖默认模块自动加载项；两项覆盖已从发布镜像中确认。

`kmod-mediatek_hnat`、`kmod-warp` 等依赖包仍在镜像中，因此 No-HNAT 指上述构建与默认加载设置，而非移除所有硬件加速代码。保留升级配置时，应检查原有的加速设置；长期稳定性与性能表现仍需实机验证。

## 软件与构建资料

软件组合包括 Aurora 主题与配置面板、Bandix、Nikki/Mihomo、WireGuard 和 ZeroTier 等。具体包名与版本以 [成品 manifest](packages.manifest) 为准。

- [定制软件包提交](custom-packages.lock)：记录四个独立软件包仓库的提交。
- [feeds 提交](feeds.conf)：记录本次构建使用的 feeds。
- [配置与补丁 PR #1](https://github.com/casiuna/immortalwrt-mt7981-cudy-tr3000/pull/1)：提供独立配置、源码修复及 Actions 调整。

## 后续构建

PR #1 在原有工作流中新增 **256M-No-HNAT** 设备选项，对应 `config/256m-20261011-no-hnat.config`。原有 128M、128M-Ubootmod、256M 配置和 `all` 列表保持不变；合并前，`main` 尚不包含这些调整。

新选项默认采用本页记录的源码提交，并固定 feeds 与定制软件包提交；手动指定源码 commit 时可覆盖默认值。No-HNAT 驱动补丁和模块覆盖只用于新选项，其后续 Release 标记为 Pre-release。

BOARD_NAME 补丁只修改 256MB 设备定义，现有工作流调用 DIY 脚本时会自动应用。重复执行不会叠加修改；若源码变化导致补丁无法匹配，构建会停止，供维护者检查。

在已准备好的对应源码目录中，手动构建顺序如下：

```sh
export GITHUB_WORKSPACE=/path/to/this-automation-repo
export DEVICE_INPUT=256M-No-HNAT
bash "$GITHUB_WORKSPACE/diy-part1.sh"
./scripts/feeds update -a
./scripts/feeds install -a
bash "$GITHUB_WORKSPACE/diy-part2.sh"
cp "$GITHUB_WORKSPACE/config/256m-20261011-no-hnat.config" .config
python3 "$GITHUB_WORKSPACE/scripts/apply-tr3000-fixes.py" . --no-hnat
make defconfig
make download
make
```

## 设备范围

本固件仅适用于 **Cudy TR3000 V1 256MB 且当前分区布局匹配的设备**，不适用于 128MB、ubootmod 或其他型号。sysupgrade 镜像不用于首次安装或写入 bootloader。

刷写前请核对设备与布局、备份配置并准备恢复方式。刷写存在断网、配置丢失及无法启动的风险，不要绕过设备检查强制刷入。

本项目为第三方定制版本，非 Cudy 或 ImmortalWrt 官方发行。
