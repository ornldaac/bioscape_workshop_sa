# Part 3 - Foliar Trait Mapping

by: Kyle Kovach, Zhiwei Ye, Henry Frye, Phil Townsend

<div style="display: flex; justify-content: center; align-items: center;">
  <img src="https://brand.wisc.edu/content/uploads/2023/09/vert-w-crest-logo-web-digital-color.png" alt="Logo 1" width="260" height="160">
  <img src="https://avatars.githubusercontent.com/u/25855722?s=200&v=4" alt="Logo 2" width="160" height="120">
  <img src="https://upload.wikimedia.org/wikipedia/commons/b/b6/NASA_Jet_Propulsion_Laboratory_%28JPL%29_Logo.webp" alt="Logo 2" width="400" height="120">
</div>

## About This Tutorial

We're happy you're here!  This tutorial is for the application of the foliar functional trait model coefficients to hyperspectral imagery.

## What Will You Do Here:
1. Import this Github repository into your local working environment.
2. Startup an instance of Jupyter Notebook.
3. Review links for workshop files.
</br>3a. _(Optional)_ Edit the code line for the specific hyperspectral image file name for the shared folder on SMCE.
</br>3b. _(Optional)_ Edit the code line for the specific coefficient model file name.
4. Execute the code line-by-line in Jupyter Notebook to produce the foliar trait map.
5. Visualize the results

## What the Code is Actually Doing:
1. Loads the hyperspectral image you specify
2. Brightness normalizes the spectral bands by vector normalizing (we'll explain)
3. Applies the trait coefficients per band
4. Renders the image

```mermaid
flowchart LR
    A[Import Hyperspectral Image]-->B[Vector Normalize Image]
    B[Vector Normalize Image]-->C[Apply Coefficients]
    C[Apply Coefficients]-->D[Render Trait Map]
```

## Why This is Important:
Foliar traits are interesting when predicted with spectroscopy to derive specific numeric values, but often, visualizing the trait maps can offer insights into spatial patterns.

## Credits
Thank you to the NASA JPL and GSFC teams, as well as the ORNL DAAC and the University of Cape Town!

[![Python][python-shield]][python-url]

<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
[python-url]: https://www.python.org
