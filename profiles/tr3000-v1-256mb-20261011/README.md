# TR3000 V1 256MB：2026-10-11 本地成品

这是第三方定制的 ImmortalWrt 24.10-SNAPSHOT / Linux 6.6.133 固件，长期稳定性尚未确认，以 **Pre-release** 发布。

- 源码：[padavanonly/immortalwrt-mt798x-6.6](https://github.com/padavanonly/immortalwrt-mt798x-6.6)，分支 `openwrt-24.10-6.6`
- 本地源码提交：`ec9ef10efc65da1e6d1de4e2c043c0e13d08eed8`，另有本目录记录的配置、覆盖文件与两个补丁。
- 版本日期：**2026-10-11**；原产物文件的本地 mtime 是 2026-10-12 04:03:34 +08，不能用版本日期伪称具体编译完成时间。
- [下载本次本地原始成品](https://github.com/casiuna/immortalwrt-mt7981-cudy-tr3000/releases/tag/tr3000-v1-256mb-20261011)
- 文件：`immortalwrt-mediatek-filogic-20261011-cudy_tr3000-v1-256mb-squashfs-sysupgrade.bin`
- 大小：**43,326,286 字节**
- SHA256：`8b79a12afa81fc82bbd4752710a52c5bca3ff4a401e584ca7e9f1a67a373f3f8`

## 板型修复与离线验证

设备定义 `Device/cudy_tr3000-v1-256mb` 增加 `BOARD_NAME := cudy_tr3000-v1-256mb`，不是只重命名镜像。
实际 FIT 内设备树 compatible 为 `cudy,tr3000-v1-256mb`，rootfs 魔数为 squashfs；
tar 内存在 `sysupgrade-cudy_tr3000-v1-256mb/CONTROL`，内容为 `BOARD=cudy_tr3000-v1-256mb`。
fwtool 提取的元数据 board 同样正确。详见 [离线验证记录](firmware-validation.json)。

元数据保留 `cudy,tr3000-256mb-v1` 作为历史兼容别名；它不是本镜像内部 BOARD 或 CONTROL 目录名称。
用户报告该成品曾通过设备端 `sysupgrade -T`；本次仅做离线检查，**没有连接设备，也没有重新执行设备端测试**。

## No-HNAT 的准确含义

本地真实实现为：关闭无线 `MTK_WHNAT_SUPPORT`、`MTK_WARP_V2` 选择；按 WARP 开关条件打包和自动加载
`mtk_warp_proxy.ko`；用零字节 `files/etc/modules.d/20-mediatek_hnat` 和 `60-warp` 覆盖自动加载项。
两份零字节覆盖文件已从本次镜像内读取确认。

`kmod-mediatek_hnat`、`kmod-warp` 仍因依赖被选入，并不宣称所有 HNAT/WED 代码或软件流卸载均已移除。
保留已安装配置可能影响实际运行状态；本次没有做设备端模块、吞吐量或长期稳定性测试。

定制包包含 Aurora 主题及配置、Bandix、Nikki/Mihomo、LuCI WireGuard/ZeroTier 等。
准确版本以 [成品 manifest](packages.manifest) 为准，不在此编造默认密码或性能数据。
四个独立包仓库提交见 [custom-packages.lock](custom-packages.lock)，feeds 提交见 [feeds.conf](feeds.conf)。

## 后续 Actions 兼容性

现有 128M、128M-Ubootmod、256M 及 `all` 的配置文件保持不变。
新增手动设备选项 **256M-No-HNAT**，使用 `config/256m-20261011-no-hnat.config`，不会自动加入 `all`。
新配置来自本地真实完整 .config；只把本机 ccache 绝对路径改为可移植设置，并明确写出两个禁用项。
此选项默认使用上述源码提交（手动指定 commit 时可覆盖）、固定 feeds/定制包提交，应用两份补丁和本目录 files。
后续构建会产生新的固件，不保证字节级重现本次历史 SHA256。

所有设备构建都会经过仅作用于 256MB 设备定义的 BOARD_NAME 补丁；
补丁可重复应用，若上游改动导致不匹配则失败，避免静默生成错误板型。
No-HNAT 驱动修复和模块覆盖仅作用于新选项。它的后续 Release 强制为 Pre-release。
本次没有启动 Actions、下载 ImmortalWrt 源码或执行任何 make 编译。

手动复现的对应顺序（只供后续构建使用；本次未执行）：

```sh
# 在已按上述分支/提交准备好的 ImmortalWrt 源码目录中：
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

## 设备范围与刷写风险

仅用于 **Cudy TR3000 V1 256MB、匹配当前分区布局的 squashfs sysupgrade**。
不是 128MB、ubootmod、其他 Cudy 型号或用于首次安装/写入 bootloader 的镜像。
刷写可能中断网络、丢失配置或导致设备无法启动；使用者需自行核实板型、布局、备份及恢复方式。
不要绕过设备检查或强制刷入。本任务未刷写、重启或修改运行中的路由器。

本目录与本次 Release 均为第三方定制，非 ImmortalWrt 或 Cudy 官方稳定发行。
