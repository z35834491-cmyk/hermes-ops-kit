<p align="right">
  <b>简体中文</b> · <a href="private-checker-guide.en.md">English</a>
</p>

# 私有 Checker 指南

如何在不把真实环境细节泄漏进公开模板的前提下，接上真实只读检查。

## 目标

```text
公开仓库     = 合同、骨架、脱敏示例
私有 overlay = 真实 env-map.local.yaml、真实 checker、凭据来源
```

## 推荐布局

不要为了私有拓扑去改公开 checker。overlay 放在仓库外：

```text
~/hermes-ops-private/
  env-map.local.yaml
  checkers/
    k8s_private.py
    mysql_private.py
  creds/
    <credential files>
```

用你自己的包装或未来适配器接到 `inspect.py`。

## Checker 合同

```python
def run(check_id, env, env_config, catalog_entry, execute=False, runner=None):
    ...
    return CheckResult(...)
```

必填：`id`、`component`、`status`（`ok|warning|critical|unreachable|failed|skipped`）、`severity`、`title`、`evidence`、`suggestion`。

## 安全规则

- 只读
- 禁止 delete / restart / scale / patch / apply / edit
- 禁止外写
- 命令 runner 不要 `shell=True`
- 不要打印凭据值
- 不要把真实 IP、主机名写进公开示例
- 需要凭据时只从来源读取，并只报告「是否存在」

示例见 `examples/private-checker-template.py`。

## 晋升回公开仓

如果私有 checker 变得通用：去掉真实 IP/主机名/凭据路径 → 变成通用 checker 或脱敏示例 → 用模拟输出补测试 → `make check` → 更新 CHANGELOG。
