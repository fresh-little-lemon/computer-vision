# CV 实证审计与未运行预实验协议（2026-10-19）

状态：AUDIT_ONLY / PILOT_NOT_RUN / NO_TOPIC_QUALIFIED

九个旧选题目前均不满足“新方法在公平独立测试上实测优于原baseline且有消融支持”的正式推荐标准。四项只有小样本baseline、五项没有本次推理。此前材料应作为未验证研究设想读取。

本checkpoint新增的是只读证据审计、资源核查和按场景划分的实验协议；没有运行新方法，没有新增模型推理，没有下载新模型或数据，没有声称创新或提高。

- EVIDENCE_AUDIT.md：九项已知证据与缺口、本地资源和代码核验
- PILOT_PROTOCOL_NOT_RUN.md：原baseline不改、先做16场景dev机制否证、32场景heldout暂锁定、负面指标/消融/失败退出
- input_audit.json：实际数据数量、跨split来源URL/图像hash检查、权重hash、源码状态
- proposed_split.json：只按元数据确定的16 dev / 32 pilot-heldout场景组，尚未运行
- scripts/：只读审计/划分脚本；不包含模型实验入口
- manifest.json：文件完整性及状态声明

唯一候选为LoMa的内部低成本机制诊断，不是正式选题推荐。LoMa现有3对验证图来自2个场景，已知失败不能证明重复数量归一化的因果解释。先审核dev诊断，若机制不成立就退出；不靠测试调参、换样本或删失败样本得到提升。

官方源：LoMa https://github.com/davnords/LoMa ；HardMatch https://github.com/davnords/HardMatch 。数据、权重均不在本包中，原作者许可证与来源继续适用。
