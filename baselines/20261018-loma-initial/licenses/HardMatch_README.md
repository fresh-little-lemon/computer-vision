<div align="center">
<h1>HardMatch: Difficult Image Matching</h1>


<a href="https://arxiv.org/abs/2604.04931"><img src="https://img.shields.io/badge/arXiv-2604.04931-b31b1b" alt="arXiv"></a>
<a href="https://www.davnords.com/loma"><img src="https://img.shields.io/badge/Project_Page-green" alt="Project Page"></a>

**Chalmers University of Technology**; **Linköping University**; **University of Amsterdam**; **Lund University**

[David Nordström*](https://scholar.google.com/citations?user=-vJPE04AAAAJ), [Johan Edstedt*](https://scholar.google.com/citations?user=Ul-vMR0AAAAJ&hl), [Georg Bökman](https://scholar.google.com/citations?user=FUE3Wd0AAAAJ), [Jonathan Astermark](https://scholar.google.com/citations?user=dsEPAvUAAAAJ), [Anders Heyden](https://scholar.google.com/citations?user=9j-6i_oAAAAJ), [Viktor Larsson](https://scholar.google.com/citations?user=vHeD0TYAAAAJ), [Mårten Wadenbäck](https://scholar.google.com/citations?user=6WRQpCQAAAAJ), [Michael Felsberg](https://scholar.google.com/citations?user=lkWfR08AAAAJ), [Fredrik Kahl](https://scholar.google.com/citations?user=P_w6UgMAAAAJ)
</div>

<p align="center">
    <img src="assets/teaser.png" alt="example" width=800%>
    <br>
    <em>Categorization of the 1,000 HardMatch pairs. </em>
</p>

## Overview
HardMatch is an extremely difficult image matching benchmark featuring 1,000 hand annotated image pairs. The benchmark is released as part of the [LoMa](https://arxiv.org/abs/2604.04931) paper (ECCV 2026, Oral). 

## Updates
- [August 5, 2026] PyPi package released and code made more accesible.
- [June 27, 2026] Initial dataset release following ECCV 2026 acceptance.

## Setup/Install
In your python environment (tested on Linux python 3.12):
```bash
uv add hardmatch
```
or 
```bash
pip install hardmatch
```

## How to Use
```python
from hardmatch import HardMatchBenchmark
matcher = YourFancyMatcher()
result = HardMatchBenchmark().benchmark(matcher)
```
`matcher` needs to satisfy the `BenchmarkMatcher` protocol ([`hardmatch.types.BenchmarkMatcher`](src/hardmatch/types.py)):

```python
class YourFancyMatcher:
    offset = 0.0  # pixel offset subtracted from returned keypoints before scoring

    def match(self, img_A_path: str, img_B_path: str) -> tuple[np.ndarray, np.ndarray]:
        """Return (kpts_A, kpts_B): corresponding (N, 2) keypoints in pixel
        coordinates of the original image files, one row per match."""
        ...
        return kpts_A, kpts_B
```
We additionally provide two example matchers through `demo.py`: [SuperPoint](https://github.com/rpautrat/SuperPoint) + [LightGlue](https://github.com/cvg/LightGlue) (`SPLG`), and [LoMa](https://github.com/davnords/loma) (`LoMa`). This defaults to evaluating on the 900 test pairs. There are also 100 validation pairs. To try the demo, first clone the repo, and then run:
```bash
uv sync --extra baselines
uv run demo.py --matcher loma
# Expected result: mAA_10px: 0.5061
```
Note, the results differs a tiny bit from the results in the [paper](https://arxiv.org/abs/2604.04931). This is because after submission we had to change the dataset a tiny bit (around 10 pairs) for licensing issues.

## Visualizing the Data
In our online [viewer](https://www.davnords.com/loma/hardmatch) you can see all of the 1,000 pairs and filter by categories / groups. Highly recommended to get a sense for what type of pairs we have collected and annotated.


## Download
Running the benchmark will automatically download the data (660MB). You can also manually download it [here](https://github.com/davnords/storage/releases/download/hardmatch/hardmatch.zip).

## License
All our code is MIT license. The pairs are scraped from [WikiMedia Commons](https://commons.wikimedia.org/wiki/Main_Page). As such, each pair has its own license that you can find in the data. They are generally permissive. 

## Acknowledgement
Our evaluation technique builds on [WxBS](https://arxiv.org/abs/1504.06603).

## BibTeX
If you find our dataset useful, please consider citing our paper!
```
@inproceedings{nordstrom2026loma,
      title={LoMa: Local Feature Matching Revisited}, 
      author={David Nordström and Johan Edstedt and Georg Bökman and Jonathan Astermark and Anders Heyden and Viktor Larsson and Mårten Wadenbäck and Michael Felsberg and Fredrik Kahl},
      booktitle={Proceedings of the European Conference on Computer Vision (ECCV)},
      year={2026}
}
```
