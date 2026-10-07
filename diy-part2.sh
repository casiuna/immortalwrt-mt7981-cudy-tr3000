#!/bin/bash
#
# https://github.com/P3TERX/Actions-OpenWrt
# File name: diy-part2.sh
# Description: OpenWrt DIY script part 2 (After Update feeds)
#
# Copyright (c) 2019-2024 P3TERX <https://p3terx.com>
#
# This is free software, licensed under the MIT License.
# See /LICENSE for more information.
#

# Modify default IP
#sed -i 's/192.168.1.1/192.168.50.5/g' package/base-files/files/bin/config_generate

# Modify default theme
#sed -i 's/luci-theme-bootstrap/luci-theme-argon/g' feeds/luci/collections/luci/Makefile

# Modify hostname
#sed -i 's/OpenWrt/P3TERX-Router/g' package/base-files/files/bin/config_generate

# 临时解决Rust问题
sed -i 's/ci-llvm=true/ci-llvm=false/g' feeds/packages/lang/rust/Makefile

# add date in output file name
sed -i -e '/^IMG_PREFIX:=/i BUILD_DATE := $(shell date +%Y%m%d)' \
       -e '/^IMG_PREFIX:=/ s/\($(SUBTARGET)\)/\1-$(BUILD_DATE)/' include/image.mk

# set ubi to 122M
# sed -i 's/reg = <0x5c0000 0x7000000>;/reg = <0x5c0000 0x7a40000>;/' target/linux/mediatek/dts/mt7981b-cudy-tr3000-v1-ubootmod.dts

# Keep stable Mihomo variant for Nikki
rm -rf package/feeds/nikki/mihomo-alpha

# Custom Nikki dashboard
mkdir -p files/etc/uci-defaults

cat > files/etc/uci-defaults/99_nikki_custom <<'EOF'
#!/bin/sh

uci -q set nikki.mixin.ui_path='ui'
uci -q set nikki.mixin.ui_name='zashboard-nikki'
uci -q set nikki.mixin.ui_url='https://github.com/casiuna/zashboard/archive/refs/heads/gh-pages-nikki.zip'
uci -q commit nikki

exit 0
EOF

chmod 0755 files/etc/uci-defaults/99_nikki_custom
