<div align="center">
  <img src="https://github.com/langheran/APKLOT/blob/master/images/logo.png"><br><br>
</div>
<!-- omit in toc -->
-----------------

[![Join the chat at https://gitter.im/apklot/users](https://badges.gitter.im/apklot/users.svg)](https://gitter.im/apklot/users) [![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://raw.githubusercontent.com/langheran/APKLOT/master/LICENSE.md) [![Dataset Size](https://img.shields.io/github/repo-size/langheran/apklot.svg)](https://github.com/langheran/APKLOT/tree/master/1.%20Satellite/Dataset)

**APKLOT** is a dataset for aerial parking block segmentation. It is suitable for deep learning on GPU enabled devices.

## Table of contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Objectives](#objectives)
- [Related work](#related-work)
- [Ground truth description](#ground-truth-description)
- [Included scripts guide](#included-scripts-guide)
- [Format conversion](#format-conversion)
  - [Subset selection - ``1. build_training_test_folders``](#subset-selection---1-buildtrainingtestfolders)
  - [Pascal format conversion - ``2. pascal``](#pascal-format-conversion---2-pascal)
- [Statistical features - ``4. features``](#statistical-features---4-features)
- [Mask evaluation](#mask-evaluation)
- [Dataset expansion](#dataset-expansion)
  - [Download more images](#download-more-images)
  - [Jittering - ``3. jittering``](#jittering---3-jittering)
- [Useful Software](#useful-software)
  - [Google Maps Api](#google-maps-api)
  - [labelme](#labelme)
  - [dlib](#dlib)
- [History and Background](#history-and-background)
- [Organizers](#organizers)
- [Support](#support)
- [Legal Notice](#legal-notice)
- [How to Cite](#how-to-cite)

## Introduction

The main goal of this dataset is to segment parking block spaces from several parking lots of the world in realistic satellite photos. Satellite photos were generated using the free Google Maps API service. Given a training set, this is fundamentally a supervised-learning learning problem.

For the purpose of this dataset, a parking block is a painted area specially designed inside the parking lot for parking. we are not considering the following:

- Parking spot(s)/block(s) outside the parking lot.
- Badly parked vehicles, including those parked on the traffic lane and non-parking spot (benches, gardens, etc).
- Debris or machinery in the parking block when it is used as manner of storage facility.
- Trees in the way of the parking block.

These are the countries and cities included in *APKLOT*:

|    Country    |    City     | \# Instances |
| ------------- | ----------- | ------------ |
| México        | México      | 90           |
| México        | Monterrey   | 6            |
| México        | Guadalajara | 7            |
| United States | New York    | 119          |
| United States | Los Ángeles | 78           |
| United States | Chicago     | 25           |
| United States | Houston     | 53           |
| Chile         | Santiago    | 62           |
| Spain         | Madrid      | 23           |
| Japan         | Tokyo       | 40           |

: Countries and cities included in _APKLOT_

## Objectives

- Provides aerial view image dataset for parking block segmentation, i.e. generate pixel-wise  areas given the class visible at each pixel through a mask.
- Provides benchmark code for evaluating the quality of the masks.
- Enables evaluation and comparison of different methods vs the results of obtained in the companion paper.

## Related work

The authors on [[1]](#user-content-ref-dblp-journals/corr/hsiehlh17) present the CARPK dataset.  It is the first large-scale dataset for counting cars from flying drones. CARPK provides 89,777 instances bounding boxes from moving video in 4 distinct parking lots.

## Ground truth description

The ground truth is available in two formats:

1. **Pascal VOC 2010.** The PASCAL Visual Object Classes format [[2]](#user-content-ref-everingham10) is one of the most used for segmentation. Here is a brief description of the each folder, however if you wish to dive deeper you can refer to [the Pascal VOC page](http://host.robots.ox.ac.uk/pascal/VOC/):
    1.  **JPEGImages.** The binary image files on JPEG compression format are stored here.
    2.  **Annotations.** Contains xml Pascal VOC annotation files. The most prominent feature of these files is that they do not contain the real shape polygon, just a bounding rectangle without orientation.
    3.  **ImageSets\\Segmentation.** 3 text files are included here: (1) train.txt, (2) trainval.txt and (3) val.txt. Each is a list of files without extension for the train, validation and test set respectively.
    4.  **SegmentationClass.** Contains the masks for training by class i.e. a class-wise color is assigned.
    5.  **SegmentationObject.**  Contains the masks i.e. a object-wise color is assigned. Due we are using just one class, it is worthwhile to point out that this folder contains exactly the same images as the **SegmentationClass** folder and is included for compatibility issues.

![Example segmentation images on the Pascal VOC: (A) **JPEGImages** folder, (B) **SegmentationClass** folder, (C) **SegmentationObject** folder. ](1.%20Satellite/Description/images/apklot_examples/seg.png)

2. **LabelMe masks.** LabelMe mask format was introduced as part of a [web site](http://labelme.csail.mit.edu/Release3.0/) for image segmentation on [[3]](#user-content-ref-dblp-journals/corr/abs-1210-3448). Here are the most  important elements of the ensued json file:
    1. **shapes.** An array containing each of the shape polygons that were labeled as a parking block.
    2. **imageData.** This element was deleted on behalf of reducing redundancy and making the dataset smaller. There is one Jupyter Notebook on the **labelme** folder - *imagedata.ipynb* - which can restore or delete this dictionary element if one would like to modify some area mapping with the [labelme  python](https://github.com/wkentaro/labelme) tool. You <u>should</u> restore the imageData dictionary element in order to run once again the labelme tool on the provided json file.
    3. **Other features.** lineColor, fillColor and image path is also provided for the *labelme* tool to render the polygons on edit mode.

## Included scripts guide

All the scripts were written in Jupyter Notebooks with a python 3.6 kernel for readers' ease. The scripts and the folder that contains them are numbered for you to execute in order on behalf of achieving the following objectives:

1. Select the train, validation and tests sets for building the PASCAL dataset from the labelme annotations.
1. Generate each of the required folders for the PASCAL VOC 2010 format.
1. Expand the image set with jittering and corresponding annotations.
1. Extract statistical features to evaluate the datasets

```

                         +---1. build_training_test_folders
                         |   |   build.ipynb
                         |   \---builds
                         |       \---\<date\>
                         +---2. pascal
                         |   |   1. JPEGImages.ipynb
                         |   |   2. Annotations.ipynb
                         |   |   3. ImageSets.Segmentation.ipynb
                         |   |   4. SegmentationClass.ipynb
                         |   \---5. SegmentationObject.ipynb
                         +---3. jittering
                         |   |   1. Jittering.ipynb
                         |   |   2. Annotations.ipynb
                         |   |   3. ImageSets.Segmentation.ipynb
                         |   \---4. MoveEmpty.ipynb
                         \---4. features
                             |   1. marked_area.ipynb
                             |   2. stats features.ipynb
                             \---3. evaluation.ipynb
```
\normalsize
\begin{figure}
\captionof{lstlisting}{Included scripts tree file structure}
\end{figure}

## Format conversion

### Subset selection - ``1. build_training_test_folders``

Sometimes it is convenient to just reduce the training data for selecting the sample size or filter out some countries we want to ignore. In those cases having a script to rebuild the dataset is convenient.

That said, the purpose of this task is to allow change the training and test sets from all the images folder and two txt files that specify both training and testing filenames without extension. Thus, the input is the images folder containing both png images and json labelme annotations and two txt files list. The output is two folders  containing those images. Subset selection is done in this folder, *1. build_training_test_folders*. Inside you will find *build.ipynb* notebook. You have to setup the following:

1. **training.txt** and **testing.txt** files.
2. Inside the script:
    1. **IMAGES_PATH.** Where are all the png images and labelme annotations located.
    2. **BUILD_DAY.** The name of the folder where the **training.txt** and **testing.txt** files are.
    3. **BUILD_OUTPUT.** Where the **training** and **testing** folders will be created for the new dataset.

Then, you can just run the script and the folders will be generated at the desired location.

### Pascal format conversion - ``2. pascal``

## Statistical features - ``4. features``

Finally, we want to assess how well suited is the data by itself to an specific algorithm we are developing. E.g., in some environments we would like to filter out parking spaces with very little annotated spaces to train more effectively,  in others we would like to bound the algorithm in terms of computational power.

![Stats features from the APKLOT dataset: (A) size in KB, (B) width and height of the image, (C) total area vs annotated area, (D) area count per image.](1.%20Satellite/Description/images/features.png)

Figure \@ref(fig:fig2) show some of the  statistical features that were extracted by using the *features.ipynb* script:

- **(A) Size.** We can see that the interquatile range lies beneath 200KB. However, there maybe outliers reaching at most 3.4 MB. You should be careful in identifying these outliers in case your algorithm fall short of GPU memory [^1].

[^1]: By ignoring this warning and if you are using CUDA, a cudaMalloc error could be thrown.

- **(B) Width and Height.** We can see from theses section that most images have a quadratic proportion with more or less the same width than height. Just as the previous case, a researcher could filter out images out of proportion to cope with the required input dimensions, e.g. the input layer of a neural network.

- **(C) Total area vs Annotated area.** This plot evince that sparse annotations dominate the dataset. Subset of a larger proportion could be assembled. However, we should take into account that the total area will ever be greater than the annotated area, and that due to the image borders will be approximately $\frac{1}{4}$ of the [total](http://www.eveandersson.com/pi/monte-carlo-circle).

- **(D) Area count per image.** We can see that each image has marked about $15$  disconnected parking block regions. There are images in which this number is really small, meaning a big fully connected clustered region. Depending on the problem, these regions might be desirable or just as well should be avoided. E.g. If we want to boost our segmentation algorithm with the prior probability from near regions, then big clusters should be used for training. On the contrary, if we want our algorithm to be robust enough to be able to detect parking spots solely on the appearance of just one of them, then images with a large area count (disconnected spots) should be selected.

## Mask evaluation 

_3. evaluation.ipynb_ 

Intersection over union is an evaluation metric that is used extensively on the object detection task, specifically in the PASCAL VOC dataset. It is also known as the Jaccard index and measures the similarity pixel sets between bounding boxes. The formula for calculating the intersection over union o a bounding box is given by the following formula:
$$
\frac{iTP}{(iTP+FP+iFN)}
$$


![Example segmentation images on our dataset _APKLOT_. ](1.%20Satellite/Description/images/segmentation_examples/seg.png)

Clear metrics [[4]](#user-content-ref-stiefelhagen2006clear).

## Dataset expansion

### Download more images

### Jittering - ``3. jittering``

Jittering was done by using the [imgaug](https://github.com/aleju/imgaug) python library. The following listing shows the code that was used for jittering:

```{#lst3 .py .numberlines startfrom="1"}
seq = iaa.Sequential([
        iaa.Crop(px=(0, 50)), # crop images from each side by 0 to 16px (randomly chosen)
        iaa.Fliplr(0.5), # horizontally flip 50% of the images
        iaa.Flipud(0.5),
        iaa.Affine(rotate=(-45, 45))
    ])
```

\normalsize
\begin{figure}
\captionof{lstlisting}{Jittering transformations}
\end{figure}

Lets give it a closer look and explain it line by line:

> (2) Randomly crop by a value between 0 and 50 pixels
> 
> (3) Horizontally flip 50\% of the images
> 
> (4) Vertically flip 50\% of the images
> 
> (5) Rotate images by a value between -45 and 45 degrees

## Useful Software

### Google Maps Api

### labelme

We already digressed around labelme but here we indulge in a more formal introduction. Labelme is a polygon manual annotation tool for segmentation that was published on [[3]](#user-content-ref-dblp-journals/corr/abs-1210-3448). It was first exposed to the public through a [webpage](http://labelme.csail.mit.edu/Release3.0/) and then through a python pip [package](https://github.com/wkentaro/labelme).

### dlib

Dlib is an open source library that was published on [[5]](#user-content-ref-king-2009-dml-1577069-1755843). It has extensive documentation through its [webpage](http://dlib.net/).

## History and Background

| Year | Statistics| New developments| Notes|
| ---- | :------------------------------------------------------------------ | :-------------------------------------- | :------------------------------- |
| 2018 | Only 1 class discriminating between parking blocks and other spaces. <br /> Train: <br /> &nbsp;&nbsp;  _300_ images <br /> &nbsp;&nbsp;  _4034_ labelme polygons  <br /> Validation: <br /> &nbsp;&nbsp;  _100_ images <br /> &nbsp;&nbsp;  _1513_ labelme polygons <br /> Test: <br /> &nbsp;&nbsp;  _101_ images <br /> &nbsp;&nbsp;  _1459_ labelme polygons | One segmentation task: <br /> Parking Block detection | Images were taken from <br /> Google Maps API. |



## Organizers

- Nisim Hurst -Tarrab<sup><a href="https://orcid.org/0000-0002-6125-9978" target="orcid.widget" rel="noopener noreferrer" style="vertical-align:top;"  target='_blank'><img src="/images/orcid_16x16.png" style="width:1em;margin-right:.2em;" alt="ORCID iD icon"></a></sup> (MSc. in Computer Science from Tecnologico de Monterrey).
- Leonardo Chang<sup><a href="https://orcid.org/0000-0002-0703-2131" target="orcid.widget" rel="noopener noreferrer" style="vertical-align:top;"  target='_blank'><img src="/images/orcid_16x16.png" style="width:1em;margin-right:.2em;" alt="ORCID iD icon"></a></sup> (researcher at Tecnologico de Monterrey).

with major contributions from

- Miguel González-Mendoza<sup><a href="https://orcid.org/0000-0001-6451-9109" target="orcid.widget" rel="noopener noreferrer" style="vertical-align:top;"  target='_blank'><img src="/images/orcid_16x16.png" style="width:1em;margin-right:.2em;" alt="ORCID iD icon"></a></sup> (distinguished professor and researcher in the _School of Science and Engineering_, Tecnologico de Monterrey)

## Support
The preparation and running of this dataset is supported by the *Instituto Tecnologico y de Estudios Superiores de Monterrey*, and was funded up to some point by the *Consejo Nacional de Ciencia y Tecnología* CONACyT. If you wish to contribute to this dataset or have any doubt, please contact us at langheran@gmail.com.

## Legal Notice

The Aerial Parking Lot dataset (APKLOT), is made available under the MIT license found in the ``LICENSE.md`` file. A MIT license is one of several public copyright licenses that enable free distribution of otherwise copyrighted work.

APKLOT consist of 500 still images with more than 7000 marked polygons of parking blocks. The images were extracted from Google Maps API. Users are entitled to use this image under this conditions:

1. Comply with the _fair-use_ google maps terms of service given at their [page](https://www.google.com/permissions/geoguidelines/).
2. Comply with the license file on the ``LICENSE.md`` file.
3. Comply with best practices for attribution found here: https://wiki.creativecommons.org/wiki/best_practices_for_attribution
4. Understand that the authors make no guarantee or warranty of non-infringement with respect to the dataset.
   
## How to Cite

At the time of this writing (``2019-05-08``), the corresponding article is under editorial revision. Please be patient until we post the proper ``bibtex`` reference:

```
@article{hurst2019, 
title={Robust Parking Block Segmentation from a Surveillance Camera Perspective},
	volume={1},
	number={1},
	journal={Expert Systems with Applications},
	publisher={Pergamon Press, Inc.},
	author={Hurst-Tarrab, Nisim and Chang, Leonardo and Gonzalez-Mendoza, Miguel},
	year={2019},
	month={Jun},
	pages={1--11}
}
```

Version: 1.0
Date: 2019-05-08

<div id="references" class="section level2 unnumbered">
<h2>References</h2>
<div id="refs" class="references">
<div id="ref-dblp-journals/corr/HsiehLH17">
<p>[1] M. Hsieh, Y. Lin, and W. H. Hsu, “Drone-based object counting by spatially regularized regional proposal network,” <em>Computing Research Repository (CoRR)</em>, vol. abs/1707.05972, 2017.</p>
</div>
<div id="ref-Everingham10">
<p>[2] M. Everingham, L. Van Gool, C. K. I. Williams, J. Winn, and A. Zisserman, “The pascal visual object classes (voc) challenge,” <em>International Journal of Computer Vision</em>, vol. 88, no. 2, pp. 303–338, Jun. 2010.</p>
</div>
<div id="ref-dblp-journals/corr/abs-1210-3448">
<p>[3] A. Barriuso and A. Torralba, “Notes on image annotation,” <em>Computing Research Repository (CoRR)</em>, vol. abs/1210.3448, 2012.</p>
</div>
<div id="ref-stiefelhagen2006clear">
<p>[4] R. Stiefelhagen, K. Bernardin, R. Bowers, J. Garofolo, D. Mostefa, and P. Soundararajan, “The clear 2006 evaluation,” in <em>International evaluation workshop on classification of events, activities and relationships</em>, 2006, pp. 1–44.</p>
</div>
<div id="ref-king-2009-dml-1577069-1755843">
<p>[5] D. E. King, “Dlib-ml: A machine learning toolkit,” <em>J. Mach. Learn. Res.</em>, vol. 10, pp. 1755–1758, Dec. 2009.</p>
</div>
</div>
</div>