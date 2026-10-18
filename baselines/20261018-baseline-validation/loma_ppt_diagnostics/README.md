# Readable LoMa diagnosis figures

Three unchanged, deterministically selected validation pairs; these are supplemental display figures. The original 200-line images and all raw predictions remain untouched.

Top: at most 30 evenly spaced predicted correspondences, drawn in neutral blue. No prediction is chosen based on quality. Bottom: all sparse ground-truth correspondences, colored by their official symmetric epipolar residual to the model-estimated F, green <=10 original-image pixels, red >10 pixels. These colors diagnose estimated geometry against real annotations; they are not ground-truth correctness labels for each predicted match. The display selection never changes evaluation.

Pair 0 is a real baseline failure (mAA10=0.062937, GT median residual44.27px), while pairs1/2 are better. No claimed new method or improvement is involved. The 3-pair sample is not a full benchmark.

Per-photo Wikimedia licenses and attribution remain in the LoMa official-preprocess checkpoint results. The pair0-derived image is CC BY-SA4.0; preserve credits, source links and license. See source checkpoint attribution.json.
