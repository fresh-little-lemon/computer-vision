# Clean real-result figures for editable slide captions

Supplementary renders only; no model inference, evaluation or sample selection changed. Prior dense figures and metrics remain untouched.

LoMa: each clean horizontal pair contains ALL sparse GT correspondences, green when its official symmetric epipolar residual to the predicted F is <=10 original-image pixels, red otherwise. This is not prediction-match correctness. Fixed val000 contains13 GT pairs, only1within10px; mAA10=0.062937 is a real failure, retained. Preserve per-photo credits and ShareAlike where applicable in loma/attribution.json.

TAPNext++: four real frames0/5/10/15, row-major2x2, greencross=GT/redcircle=prediction, query0/bike-packing. All sampled/evaluated frames continuously visible; no occlusion test. AnnotationsCCBY4.0; sourcevideo creator-specific license, exact variant not independently reverified. Official original-video link and source archive in tapnextpp/clean_figures_manifest.json. frame0_source_clean is the same real input without marks.

PNG files are in the ZIP/binary manifest. No generated/synthetic image content, weights, complete datasets or private recordings.
