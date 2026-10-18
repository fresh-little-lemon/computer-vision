# Run from /workspace/shared/cv-baseline-runs (ROOT). No official algorithm edits.
# Actual first successful run used cached or downloaded official HF repo ID.
HF_HOME="$PWD/cache/huggingface" HF_HUB_DISABLE_XET=1 PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 subspace-env/bin/python scripts/measure_command.py logs/subspacead_visa3_resource.json subspace-env/bin/python scripts/subspacead_official_capture.py --dataset_name visa --dataset_path "$PWD/data/visa_micro/1cls" --categories pcb1 --model_ckpt facebook/dinov2-with-registers-small --image_res 224 --layers=-4,-5,-6,-7 --k_shot 1 --aug_count 0 --batch_size 1 --pca_ev 0.99 --seed 42 --agg_method mean --outdir "$PWD/outputs/subspacead_visa3/official"
# Reproduce immutable weights: prepopulate the recorded HF revision (provenance.json)
# and set HF_HUB_OFFLINE=1; or pass its local snapshot directory as --model_ckpt.
