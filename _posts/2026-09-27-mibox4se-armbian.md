---
layout: post
title: "小米盒子 4SE 安装 Armbian：系统引导、eMMC 安装与 SSH 配置"
description: "记录小米盒子 4SE 安装 Armbian 的步骤，包括 FEL 引导、复用原厂 U-Boot、设备树适配、eMMC 写入、Wi-Fi 配置及 SSH 登录验证。"
category: "Linux"
tags: ["Linux", "Armbian", "小米盒子", "Allwinner H3", "U-Boot"]
---

* 目录
{:toc}

---

本文记录在小米盒子 4SE 上安装 Armbian 的过程。安装完成后，系统从 eMMC 加载根文件系统，支持正常软件重启、Wi-Fi 自动连接和 SSH 登录。

安装采用保留原厂 U-Boot 的方案，以 Beelink X2 社区镜像为基础，完成设备树、存储控制器和无线模块的适配。以下步骤对应本次设备及适配后的启动文件，不是将通用镜像直接写入盒子的安装方式。

## 一、确认硬件与系统版本

本次安装使用的硬件如下：

| 项目 | 型号或容量 |
| --- | --- |
| 设备 | 小米盒子 4SE，外部型号 MDZ-23-AA |
| 主板 | M20_V50，PCB 日期 2018-08-23 |
| SoC | Allwinner H3 |
| 内存 | 正常启动后 Linux 识别约 991 MiB |
| eMMC | Kingston EMMC04G-M627 |
| eMMC 用户区 | 3,791,650,816 字节 |

安装后的系统版本为：

| 项目 | 版本 |
| --- | --- |
| 镜像基础 | Beelink X2 社区镜像 |
| Armbian | community 26.11.0-trunk.59 |
| 发行版 | Debian 13 |
| 内核 | 6.18.54-current-sunxi |

## 二、准备安装文件并备份原系统

安装前需要准备：

- 可通过 USB 与盒子通信的电脑，以及 `sunxi-fel` 工具；
- 原厂 `fes1`，用于初始化 DRAM；
- 从原机备份中提取的 U-Boot；
- 适配后的 Linux 内核、设备树、initramfs 和辅助启动 ELF；
- Armbian 根文件系统。

先保存 eMMC 原始备份、分区布局和原厂引导环境，再执行持久写入。本次安装会改写原安卓数据分区、boot 分区中的启动负载，以及环境分区前 128 KiB；原厂 U-Boot 保留。

辅助 ELF 和设备树需要针对该主板适配。分区偏移、镜像长度及启动环境应以本机备份为准，不能直接套用其他 H3 设备的写入参数。

## 三、进入 FEL 并确认 USB 通信

使设备进入 H3 ROM 提供的 FEL 模式后，在电脑上执行：

```bash
sunxi-fel version
```

本次设备返回：

```text
AWUSBFEX soc=00001680(H3) 00000001 ver=0001 44 08
scratchpad=00007e00 00000000 00000000
```

其中 `AWUSBFEX` 表示 FEL 通信已建立，`soc=00001680(H3)` 确认芯片型号。后续通过 FEL 加载内存初始化程序及引导文件。

ADB 与 FEL 属于不同的通信路径，Android 下可使用 ADB，并不代表已经进入 FEL。应以 `sunxi-fel version` 的协议响应确认状态。

## 四、复用原厂 U-Boot 启动 Linux

本次安装使用以下引导链路：

```text
H3 ROM FEL
    ↓
厂商 fes1：初始化 DRAM
    ↓
原机备份中的 U-Boot
    ↓
bootelf：执行辅助启动 ELF
    ↓
原厂 bootm：启动 Linux
    ↓
initramfs → Armbian 根文件系统
```

先通过厂商 `fes1` 初始化内存，再加载原厂 U-Boot。辅助 ELF 调用原厂已有的启动能力，并处理 Linux 启动所需的设备树参数。

### 配置定时器频率

在 Linux 设备树的 `/timer` 节点中，将 `clock-frequency` 明确设置为 24 MHz：

```dts
clock-frequency = <24000000>;
```

该设置用于保证 ARM timer 正确初始化，是本次内核启动所需的适配项。

### 设置实际使用的设备树

原厂 `bootm` 未按预期使用传入的 Linux DTB，因此需要由辅助程序修正内存中的设备树指针，再执行后续启动阶段，确保内核获得适配后的硬件描述。

### 加载并校验启动包

启动包包含内核、设备树和 initramfs。安排加载地址时，需要避开后续搬移可能覆盖的内存区域。本次将 ELF 加载到 `0x48000000`。

上传完成后，分块回读数据并比较 SHA-256，确认内存中的内容与本地文件一致。分块读取可以避免单次较长的 USB 请求超时。

### 建立 USB 控制台

在临时 Linux 环境中，将 `setsid sh -i` 的输入输出直接绑定到 `ttyGS0`，通过 USB 控制台执行命令、检查内核日志，并继续完成存储和网络配置。

## 五、适配 eMMC 并写入根文件系统

原厂引导遗留的 MMC2 时钟配置需要在 Linux 下修正。本次采用以下顺序：

1. 解绑对应的 MMC 驱动。
2. 清除寄存器 `0x01c20090` 的 bit 30，保留其他位。
3. 重新绑定 MMC 驱动。
4. 将 eMMC 工作频率限制为 **6 MHz**。
5. 读取数据片段，与原始备份比较，确认读取正确。
6. 写入 Armbian 根文件系统，并执行完整回读校验。

本次安装使用较低的 eMMC 频率，是为了避免较高频率下出现的数据错误。该寄存器处理对应本机原厂引导后的状态，不应作为其他设备的通用配置。

安装完成后，根文件系统位于：

```text
/dev/mmcblk0p1  ext4
```

本次根分区约 1.9 GB，安装后剩余约 576 MB。安装软件前，可通过 `df -h /` 检查剩余空间。

## 六、配置 XR819 Wi-Fi

XR819 无线模块需要正确的供电与复位顺序。本次适配顺序为：

1. 将 **PL7 拉高**。
2. 等待 **30 ms**。
3. 释放 **PL0 复位**。

在设备树 overlay 及电源时序中完成上述调整后，驱动加载固件并创建 `wlan0` 接口。

随后配置无线网络凭据和自动连接，使设备通过 DHCP 获取局域网地址。完成配置后，可检查接口与路由：

```bash
ip addr show wlan0
ip route
```

确认 `wlan0` 已获得地址，并存在可用的默认路由，再配置 SSH 访问。

## 七、设置 eMMC 启动与 SSH 登录

临时引导验证完成后，将启动负载写入 boot 分区，并修改原厂 U-Boot 环境中的 `boot_normal`，使其读取 Linux ELF 后执行 `bootelf`。

持久安装包括三部分：

| 内容 | 处理方式 |
| --- | --- |
| 根文件系统 | 写入原安卓数据分区对应的目标区域 |
| 启动负载 | 写入 boot 分区 |
| 启动环境 | 更新环境分区前 128 KiB，使 `boot_normal` 加载 Linux ELF |

根分区、启动包和环境变量写入后均进行回读校验，确认持久存储中的内容正确，再重启设备。

系统启动后，配置 SSH 公钥登录，并从同一局域网的电脑连接：

```bash
ssh <用户名>@<盒子的局域网地址>
```

上述用户名和地址需替换为实际配置。安装后的系统已具备 SSH、systemd、Python、curl 和 cron 等基础工具。

## 八、验证安装结果

登录系统后，可执行以下命令检查内核、初始化进程、根文件系统与网络状态：

```bash
uname -a
ps -p 1 -o comm=
findmnt -n -o SOURCE,FSTYPE /
ip addr show wlan0
systemctl is-active ssh
```

本次安装的验证结果如下：

| 项目 | 结果 |
| --- | --- |
| 根文件系统 | `/dev/mmcblk0p1`，ext4 |
| PID 1 | systemd |
| 正常软件重启 | 重启后启动 ID 改变，无需再次从电脑上传启动包 |
| 网络 | Wi-Fi 自动连接并取得地址 |
| 远程管理 | SSH 密钥登录成功 |
| 服务运行 | systemd 临时服务执行并返回预期输出 |

至此，小米盒子 4SE 已完成 Armbian 安装，可从 eMMC 启动系统，并通过 Wi-Fi 和 SSH 进行远程管理。
