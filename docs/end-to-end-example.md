<p align="right">
  <b>简体中文</b> · <a href="end-to-end-example.en.md">English</a>
</p>

# 端到端示例

不连真实基础设施，只演示 env-map → 巡检 JSON → runbook → 审批合同如何串起来。

```text
env-map.example.yaml
  ↓
scripts/inspect.py --json --save
  ↓
reports/<env>/inspection-*.json
  ↓
对照 runbook 元数据
  ↓
风险 >= L1 时走审批请求
  ↓
未来 BestNative 只读展示 / 审批中心
```

## 1. 环境地图

```bash
cp config/env-map.example.yaml config/env-map.local.yaml
```

`env-map.local.yaml` 只描述本机路径和凭据来源，不写凭据值。

## 2. 巡检

```bash
python3 scripts/inspect.py test --config config/env-map.local.yaml --json --save
```

公开模板只生成合同形状的输出。真实只读检查放在私有 overlay。

## 3. 巡检结果

形状见 [../examples/inspection-result.example.json](../examples/inspection-result.example.json)。异常项的 `suggestion` 会指向 runbook 名，例如 `Run k8s-pod-abnormal-diagnostic`。

## 4. Runbook 元数据

对应文件：`examples/runbooks/k8s-pod-abnormal-diagnostic.yaml`。元数据声明风险级、是否要审批、输入、预检查、执行模式、验证。

## 5. 审批

L0 只读不需要审批。L1/L2/L3 使用 `templates/approval-request-template.json` 的形状。BestNative 以后存审批状态；本仓库只提供合同。

## 6. 安全边界

- 发现输出只是候选，不是事实
- 公开巡检保持只读，直到私有 overlay 接上安全 checker
- 平台接入前，执行必须有审批/审计
- 公开示例保持脱敏
