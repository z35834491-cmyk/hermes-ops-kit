<p align="right">
  <b>简体中文</b> · <a href="precipitation.en.md">English</a>
</p>

# 故障经验怎么沉淀

没有回流，合同包会停在当前这批示例上。本仓库要的是**可重复的沉淀合同**，不是去扫你本机 Hermes 聊天记录。

公开 `precipitate.py` **不读** `~/.hermes`、oplog、原始日志，也不连集群。自动写入 Git、自动改 `check-catalog.yaml` 也不做。那会把秘密带进可开源的树。

活的闭环是：

```text
本机 Hermes 处理完一次故障
        ↓
你（或私有 skill）写出一份已经脱敏的 lesson-candidate.yaml
        ↓
python3 scripts/precipitate.py --from ...   →  *.generated.yaml 草稿
        ↓
人工审阅 → 晋升到 examples/runbooks/<name>.yaml
        ↓
make check / sanitize_check
```

和 `onboard.py` 一样：脚本只产**候选**，晋升必须人点头。

## 一次怎么跑

1. 复制模板，去掉真实 IP、主机名、业务名、密码、原始日志：

```bash
cp templates/lesson-candidate-template.yaml /tmp/lesson-candidate.yaml
```

也可对照 `examples/lesson-candidate.example.yaml`。字段合同见 `config/schema/lesson-candidate.schema.yaml`。

2. 生成 runbook 草稿（文件名必须是 `*.generated.yaml`）：

```bash
python3 scripts/precipitate.py \
  --from /tmp/lesson-candidate.yaml \
  --output /tmp/example-component-health-diagnostic.generated.yaml \
  --force
```

3. 草稿校验通过后，**人工**拷成正式示例（不要提交 `.generated.yaml`）：

```bash
python3 scripts/validate_runbook.py /tmp/example-component-health-diagnostic.generated.yaml
# 审阅后再：
# cp ... examples/runbooks/<name>.yaml
```

自动草稿只接受 **L0 / read-only**。L1+ 变更、回滚、审批字段仍手写 runbook。

## Hermes 侧怎么接（私有）

把下面这段交给本机 Hermes，让它在复盘后**只写候选 YAML**，不要把 oplog 原文丢进 Git：

```text
根据刚处理完的故障，写一份 Hermes Ops Kit lesson-candidate YAML。
必须已经脱敏：禁止 IP、主机名、业务域名、密码、token、kubeconfig 内容、原始日志。
只用 <NAMESPACE>、<COMPONENT> 这类占位符。
risk_level 只能是 L0，mode 只能是 read-only。
字段对齐 hermes-ops-kit/templates/lesson-candidate-template.yaml。
不要读取或修改 ~/.hermes 以外的生产配置；不要直接改 examples/runbooks/。
```

私有 overlay / Hermes skill 可以把这份 YAML 写到仓库外，再调用 `precipitate.py`。那一层不进本仓库。

## 什么算沉淀成功

- 候选过 `precipitate.py`，草稿过 `validate_runbook.py`
- 晋升后的 runbook 能过 `make check`
- `sanitize_check.py` 不再报私网 IP / 明文 secret
- catalog 如需新检查项，另开人工改动，不由本脚本合并

脱敏细则仍见 [local-hermes-to-ops-kit.md](local-hermes-to-ops-kit.md)。
