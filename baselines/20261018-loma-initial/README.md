# CV baseline 实跑 checkpoint（2026-10-18）

## 已完成
- 官方 LoMaB128（DeDoDe-B，非 LoMaB/DeDoDe-G）CPU 前向，官方源码未改
- Toronto 功能示例：224×224、256关键点，38对匹配，冷首对0.709秒，进程峰值983MiB
- HardMatch真实val前3个合格静态pair：53/105/62对匹配，官方F+mAA@10px样本均值0.457731，0.65–0.73秒/对，峰值986MiB
- 首对误差明显较高，全部如实保存；没有选择性删失败样本
- 当前官方归档实际99 val +900 test，README仍写100 val，详见manifest

## 结论边界
这是降采样小样本可运行性与测量结果，不是完整benchmark或论文复现，不能与论文整集分数直接比较。模型使用官方B128结构和权重，改变的是明确披露的输入尺寸、关键点数量和CPU执行配置。标准路径预处理+2048关键点对照正在单独运行；TAPNext++尚未产生结果。

## 内容
- scripts：可复跑入口，仅调用官方模型，不替换网络或推理算法
- logs：实际命令、原始stdout、环境锁定、运行资源测量
- results：原始匹配/GT/F/逐点误差NPZ及等价JSON、评分汇总
- figures：真实推理可视化PNG，非生成图片。HardMatch图含三对完整样本，缩放仅用于阅读
- licenses：代码许可证和模型/数据源说明
- manifest.json：源码commit、下载URL与SHA256

## 图片许可
HardMatch照片来自Wikimedia，保留每张照片完整A/B_metadata.json与attribution.json。第1对照片CC BY-SA 4.0，合成匹配图适用CC BY-SA 4.0；其余照片分别公有领域、CC BY 4.0。修改仅为缩放、排版、标注匹配线。请保留元数据署名。Toronto图来自官方LoMa示例assets，链接与源码commit见manifest。

## 复跑
克隆manifest所列官方仓库到sources并检出精确commit，安装Python3.12、CPU PyTorch/torchvision与logs/pip_freeze.txt所列依赖（不要直接安装含本机editable路径的freeze）。pip install --no-deps -e sources/LoMa -e sources/HardMatch -e sources/tapnet。按manifest下载checkpoint到cache/torch/hub/checkpoints，解压HardMatch到data/hardmatch。然后在仓库根运行logs/*.command中的命令。正式环境可使用不同线程数，但需单独披露。

大型模型、数据整包、任何私人课堂材料均不包含在本checkpoint内。
