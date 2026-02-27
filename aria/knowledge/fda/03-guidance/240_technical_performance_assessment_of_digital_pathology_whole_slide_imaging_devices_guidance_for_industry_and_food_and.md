---
source:
  family: "GUIDANCE"
  instrument: "FDA Guidance"
  title: "Technical Performance Assessment of Digital Pathology Whole Slide Imaging Devices :  Guidance for Industry and Food and Drug Administration Staff"
  docket: "FDA-2015-D-0230"
  path: "240_Technical_Performance_Assessment_of_Digital_Pathology_Whole_Slide_Imaging_Devices_Guidance_for_Industry_and_Food_and_Drug_Administration_Staff.pdf"
  pages: 27
  converted: 2026-02-27
  method: pdftotext
---

Contains Nonbinding Recommendations

Technical Performance Assessment
of Digital Pathology Whole Slide
Imaging Devices
Guidance for Industry and Food
and Drug Administration Staff
Document issued on: April 20, 2016
The draft of this document was issued on February 25, 2015
For questions about this document, contact the Division of Molecular Genetics and
Pathology at 301-796-6179 and Nicholas Anderson at 301-796-4310 or
nicholas.anderson@fda.hhs.gov or Aldo Badano at 301-796-2534 or
aldo.badano@fda.hhs.gov.
U.S. Department of Health and Human Services
Food and Drug Administration
Center for Devices and Radiological Health
Office of In Vitro Diagnostics and Radiological Health
Division of Molecular Genetics and Pathology
Molecular Pathology and Cytology Branch

Contains Nonbinding Recommendations

Preface
Public Comment
You may submit electronic comments and suggestions at any time for Agency
consideration to http://www.regulations.gov . Submit written comments to the Division of
Dockets Management, Food and Drug Administration, 5630 Fishers Lane, Room 1061,
(HFA-305), Rockville, MD 20852. Identify all comments with the docket number [FDA2015-D-0230]. Comments may not be acted upon by the Agency until the document is next
revised or updated.

Additional Copies
Additional copies are available from the Internet. You may also send an e-mail request to
CDRH-Guidance@fda.hhs.gov to receive a copy of the guidance. Please use the document
number 1400053 to identify the guidance you are requesting.

Contains Nonbinding Recommendations

Table of Contents
I.

Introduction ............................................................................................................... 1

II.

Background ............................................................................................................... 2

III.

Scope ......................................................................................................................... 2

IV.

Policy ......................................................................................................................... 3

IV(A).

Description and Test Methods for Each Component .................................... 3

IV(A)(1).

Slide Feeder ........................................................................................... 5

IV(A)(1)(a). Description .................................................................................... 5
IV(A)(2).

Light Source .......................................................................................... 5

IV(A)(2)(a). Description .................................................................................... 5
IV(A)(2)(b). Test Method .................................................................................. 6
IV(A)(3).

Imaging Optics ...................................................................................... 6

IV(A)(3)(a). Description .................................................................................... 6
IV(A)(3)(b). Test Methods ................................................................................ 7
IV(A)(4).

Mechanical Scanner Movement ............................................................ 7

IV(A)(4)(a). Description .................................................................................... 7
IV(A)(4)(b). Test Method .................................................................................. 8
IV(A)(5).

Digital Imaging Sensor .......................................................................... 8

IV(A)(5)(a). Description .................................................................................... 8
IV(A)(5)(b). Test Methods ................................................................................ 8
IV(A)(6).

Image Processing Software ................................................................... 9

IV(A)(6)(a). Description .................................................................................... 9
IV(A)(6)(b). Resources ...................................................................................... 9
IV(A)(7).

Image Composition ............................................................................... 9

IV(A)(7)(a). Description .................................................................................... 9
IV(A)(7)(b). Test Methods .............................................................................. 10
IV(A)(8).

Image Files Formats ............................................................................ 10

IV(A)(8)(a). Description .................................................................................. 10
IV(A)(9).

Image Review Manipulation Software ................................................ 11

IV(A)(9)(a). Description .................................................................................. 11
IV(A)(9)(b). Resources .................................................................................... 11

Contains Nonbinding Recommendations
IV(A)(10). Computer Environment ...................................................................... 11
IV(A)(10)(a). Description ................................................................................ 11
IV(A)(11). Display ............................................................................................... 12
IV(A)(11)(a). Description ................................................................................ 12
IV(A)(11)(b). Test Methods ............................................................................ 12
IV(A)(11)(c). Resources .................................................................................. 13
IV(B).

System-level Assessment ............................................................................ 14

IV(B)(1).

Color Reproducibility .......................................................................... 15

IV(B)(1)(a). Description .................................................................................. 15
IV(B)(1)(b). Test Methods ............................................................................... 15
IV(B)(1)(c). Resources .................................................................................... 16
IV(B)(2).

Spatial Resolution ................................................................................ 16

IV(B)(2)(a). Description .................................................................................. 16
IV(B)(2)(b). Test Methods ............................................................................... 16
IV(B)(3).

Focusing Test ....................................................................................... 16

IV(B)(4).

Whole Slide Tissue Coverage.............................................................. 17

IV(B)(4)(a). Description .................................................................................. 17
IV(B)(4)(b). Test Method ................................................................................ 17
IV(B)(5).

Stitching Error ..................................................................................... 18

IV(B)(5)(a). Description .................................................................................. 18
IV(B)(5)(b). Test Methods ............................................................................... 18
IV(B)(6).

Turnaround Time ................................................................................. 19

IV(B)(6)(a). Description .................................................................................. 19
IV(C).

User Interface .............................................................................................. 19

IV(C)(1).

Description........................................................................................... 19

IV(C)(2).

Test Methods ....................................................................................... 19

IV(C)(3).

Resources ............................................................................................. 22

IV(D).

Labeling ...................................................................................................... 22

IV(D)(1).

Test Methods ....................................................................................... 23

IV(D)(2).

Resources ............................................................................................. 23

IV(E).

Quality Control ........................................................................................... 23

1
2
3

Technical Performance Assessment
of Digital Pathology Whole Slide
Imaging Devices

4

Guidance for Industry and Food
and Drug Administration Staff

5
6
7
8
9
10
11
12
13

This guidance represents the current thinking of the Food and Drug Administration
(FDA or Agency) on this topic. It does not establish any rights for any person and is
not binding on FDA or the public. You can use an alternative approach if it satisfies
the requirements of the applicable statutes and regulations. To discuss an alternative
approach, contact the FDA staff or Office responsible for this guidance as listed on the
title page.

14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36

I.

Introduction

FDA is issuing this guidance to provide industry and agency staff with recommendations
regarding the technical performance assessment data that should be provided for
regulatory evaluation of a digital whole slide imaging (WSI) system. This document
does not cover the clinical submission data that may be necessary to support approval or
clearance. This document provides our suggestions on how to best characterize the
technical aspects that are relevant to WSI performance for their intended use and
determine any possible limitations that might affect their safety and effectiveness.
Recent technological advances in digital microscopy, in particular the development of
whole slide scanning systems, have accelerated the adoption of digital imaging in
pathology, similar to the digital transformation that radiology departments have
experienced over the last decade. FDA regulates WSI system manufacturers to help
ensure that the images intended for clinical uses are reasonably safe and effective for
such purposes. Essential to the regulation of these systems is the understanding of the
technical performance of the WSI system and the components in the imaging chain, from
image acquisition to image display and their effect on pathologist’s diagnostic
performance and workflow. Prior to performing non-technical analytical studies (i.e.,
those using clinical samples) and clinical studies to evaluate a digital imaging system’s
performance, the manufacturer should first determine the technical characteristics that are
relevant to such performance for its intended use and determine any possible limitations

1

Contains Nonbinding Recommendations
37
38
39
40
41
42
43
44
45

that might affect its safety and effectiveness. This guidance provides recommendations
for the assessment of technical characteristics of a WSI device.

46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
66
67
68

II. Background

69
70
71
72
73
74
75
76
77
78
79
80
81

III. Scope

FDA's guidance documents, including this guidance, do not establish legally enforceable
responsibilities. Instead, guidances describe the Agency's current thinking on a topic and
should be viewed only as recommendations, unless specific regulatory or statutory
requirements are cited. The use of the word should in Agency guidance means that
something is suggested or recommended, but not required.

For over a hundred years, the reference method for the diagnosis of cancer and many
other critical clinical conditions has been histopathological examination of tissues using
conventional light microscopy. This process is known as surgical pathology in the
United States.
In surgical pathology, patient tissue from surgery, biopsy or autopsy goes through a
process that includes dissection, fixation, embedding, and cutting of tissue into very thin
slices which are then stained, for example by the hematoxylin and eosin (H&E) protocol,
and permanently mounted onto glass slides. The slides are examined by a pathologist
under a light microscope by dynamically adjusting the focus and using different
magnifications. By integrating their interpretations obtained by microscopic examination
of the tissue from all slides pertaining to a case, pathologists arrive at a diagnosis of the
case.
WSI refers to the digitization of the stained entire tissue specimen on a glass slide. The
glass slide is still prepared and stained just as for conventional light microscopy.
Depending on the system used, various magnifications, scanning methodologies,
hardware, and software are employed to convert the optical image of the slide into a
digital whole slide image. With WSI, the pathologist views the image on a computer
monitor rather than through the microscope oculars.

This document provides guidance regarding only the technical performance assessment
of WSI systems for regulatory evaluation. WSI systems are defined here as those
consisting of (a) an image acquisition subsystem that converts the content of a glass slide
into a digital image file, and (b) a workstation environment for viewing the digital
images. If not otherwise specified, the term “image” in the context of whole slide
imaging refers to a pyramid structure consisting of multiple images at different
resolutions. The baseline image has the highest resolution. This guidance is applicable
for surgical pathology tasks performed in the anatomic pathology laboratory. It is
intended to provide recommendations to industry and FDA staff regarding only the
technical performance assessment data needed for the regulatory evaluation of a WSI
device. This document is not meant to provide guidance for special stain techniques or
2

Contains Nonbinding Recommendations
82
83
84
85
86

fluorescence imaging or for the non-technical analytical studies (utilizing clinical
samples) or pivotal clinical studies necessary to support safety and effectiveness, nor
does this guidance alone suffice to demonstrate safety and effectiveness of WSI systems.
Interpretation of WSI images on mobile platforms is beyond the scope of this guidance.

87
88
89
90
91
92
93
94
95
96
97
98
99
100
101
102
103
104
105
106
107
108
109
110
111
112
113
114
115
116
117
118
119
120
121
122
123
124
125
126

IV. Policy
The following subsections of this section describe the technical performance assessment
data FDA believes will facilitate the regulatory evaluation of a WSI device.

IV(A). Description and Test Methods for Each Component
This subsection details the descriptions and the test methods at the component level that
should be included in the technical performance assessment of a WSI device. For
purposes of this guidance only, a component is a piece of hardware, software, or a
combination of hardware and software that processes the image signals flowing through
the imaging chain. The concept of a component is based on the transformation of the
image signals. For example, the digital imaging sensor is a hardware device that converts
optical signals into digital signals. The image composition component is a software
program that stitches sub-images together to form a whole slide image. A component
and a physical device need not be in close physical proximity. For example, the light
source component and the image optics component are usually tightly coupled within the
same device, while the display calibration data is often distributed in both the color
profile in the computer environment component and the on-screen display settings in the
display component.
The components in a WSI device can be grouped in two subsystems: image acquisition
and image display. The image acquisition subsystem digitizes the tissue slide as a digital
image file. The image display subsystem converts the digital image file into optical
signals for the human reader. In the paradigm of telemedicine, the digital image file can
be electronically sent to a remote site for reading, so the image acquisition subsystem and
the image display subsystem do not need to be physically coupled. Methods for
independently testing the image acquisition and display subsystems are described in
Section IV(B).
Sponsors should provide a block diagram of the components found in the WSI system in
the premarket submission. A chart indicating the relationship among the components and
the test methods utilized for the specific system characterization should also be provided.
Diagram 1 on the following page is offered as an example block diagram of typical
components found in current WSI systems. The components of a particular WSI system
might not include all of those listed in the diagram or may include additional
components. Sponsors are encouraged to provide additional diagrams, illustrations, and
photographs of their devices as part of their submissions.

3

Contains Nonbinding Recommendations
127
128
129
130
131
132
133
134
135
136
137
138
139
140
141
142
143
144
145
146
147
148
149
150
151
152
153
154
155
156
157
158
159
160
161
162
163
164
165
166
167

Diagram 1: Example block diagram of typical components found in current WSI
systems

4

Contains Nonbinding Recommendations
168
169
170
171
172
173
174
175
176
177
178
179
180
181
182
183
184
185
186
187
188
189
190
191
192
193
194
195
196
197
198
199
200
201
202
203
204
205
206
207
208
209
210
211
212
213

IV(A)(1).

Slide Feeder

IV(A)(1)(a).

Description

The slide feeder is the mechanism(s) used to introduce the slide(s) to the scanner. For the
slide feeder, sponsors should provide the following information, if applicable:
· Configuration of the slide feed mechanism (a physical description of the
equipment)
o Slide configuration (physical description of the slide (i.e., custom or
commercial off-the-shelf))
o Number of slides in queue (carrier)
o Class of automation (e.g., robotics, pneumatics, etc.)
· User interaction
o Hardware (e.g., loading of slides into carrier)
o Software (e.g., does the system recognize the number of slides or is this
specified by the user)
o Feedback (e.g., alarms, notifications, etc.)
o Failure Mode and Effects Analysis (FMEA) (including severity,
likelihood, mitigations, etc.)

IV(A)(2).

Light Source

IV(A)(2)(a).

Description

The light source, including the light guide, generates and delivers light to the slide being
imaged. The two major components are the lamp and condenser. For the light source,
sponsors should provide the following information and specifications, if applicable:
· Lamp
o Bulb type (e.g., halogen, xenon arc, LED)
o Manufacturer and model
o Wattage
o Spectral power distribution
o Expected lifetime
o Output adjustment control (electrical/electronic/mechanical)
o Optical filter(s)
§ Type (e.g., heat blocking, polarization, neutral density, diffusing)
o Manufacturer and model
o Expected intensity variation (coefficient of variation )
§ Over the duration of scanning a single slide
§ Over the course of a single workday
§ Over the lifetime of the device
o Expected spectral variation
§ Over the duration of scanning a single slide
§ Over the course of a single workday
§ Over the lifetime of the device
o Capability of tracking intensity and spectral degradation with lifetime
5

Contains Nonbinding Recommendations
214
215
216
217
218
219
220
221
222
223
224
225
226
227
228
229
230
231
232
233
234
235
236
237
238
239
240
241
242
243
244
245
246
247
248
249
250
251
252
253
254
255
256
257
258
259

·

Condenser
o Illumination format (e.g., Kohler, critical)
o Manufacturer and model
o Numerical aperture
o Focal length
o Working distance
IV(A)(2)(b).

Test Method

The following steps should be used to measure the spectral distribution of light incident
on the slide. Position the input of a calibrated spectrometer or monochromator at the
plane where the slide would be placed, centered on the illumination spot from the
condenser. If desired, the light can be coupled into the spectrometer via light guide (e.g.,
fiber optic cable) or an integrating sphere. The measurement aperture should be at least
as large as the anticipated field of view on the slide at the lowest magnification of the
imaging optics. The wavelength accuracy and relative spectral efficiency of the
spectrometer or monochromator in the wavelength range of 360-830 nm should be
calibrated prior to measurements and reported. Plots of the measured spectrum with at
least 10 nm spectral resolution should be provided, using radiometric units (e.g., spectral
irradiance in W/cm2/nm, spectral radiance in W/sr/cm2/nm).

IV(A)(3).

Imaging Optics

IV(A)(3)(a).

Description

The imaging optics comprises the microscope objective and auxiliary lens(es) (e.g., tube
lens), which optically transmit an image of the tissue from the slide to the digital image
sensor. Sponsors should provide the following information and specifications, if
applicable:
· Optical schematic with all optical elements identified from slide (object plane) to
digital image sensor (image plane)
· Microscope objective
o Manufacturer
o Type
o Magnification
o Numerical aperture (NA)
o Focal length
o Working distance
· Auxiliary lens(es)
o Manufacturer
o Lens type
o Focal length
· Magnification of imaging optics: ISO 8039:2014 Optics and optical instruments
— Microscopes — Magnification

6

Contains Nonbinding Recommendations
260
261
262
263
264
265
266
267
268
269
270
271
272
273
274
275
276
277
278
279
280
281
282
283
284
285
286
287
288
289
290
291
292
293
294
295
296
297
298
299
300
301
302
303
304
305

IV(A)(3)(b).

Test Methods

Sponsors should conduct the following tests in conformance with the International
Standards, if applicable:
· Relative irradiance of imaging optics at image plane per ISO 13653:1996 Optics
and optical instruments – General optical test methods - Measurement of relative
irradiance in the image field
· Distortion per ISO 9039:2008 Optics and photonics — Quality evaluation of
optical systems —Determination of distortion
· Chromatic aberrations per ISO 15795:2002 Optics and optical instruments —
Quality evaluation of optical systems — Assessing the image quality degradation
due to chromatic aberrations

IV(A)(4).

Mechanical Scanner Movement

IV(A)(4)(a).

Description

The mechanical scanner addresses the physical characteristics of the stage upon which
the glass slide is affixed. The key components include stage configuration, movement,
and control. This information is relevant whether it is only the stage that is moving and
the optics are stationary, or if there is movement on all axes. For the mechanical scanner,
sponsors should provide the following information and specifications, if applicable:
· Configuration of the stage (a physical description of the stage)
o Stage size
o Stage manufacturer and model number
o Stage material (e.g., anodized aluminum)
o Single multi-axis or multiple stacked linear stages (manufacturer and
model number)
o Type of guides or ways (e.g., bearings)
o Sample retention mechanism (slide holder)
· Method of movement of the stage (e.g., stepper motor, servomotor, piezomotor,
etc., coupled with belt, ball-screw, lead-screw, etc.)
o Movement resolution for XY-axes
o Movement in Z-axis
o Speed range
o Travel distance
o Maximum scanning area
o Localization and reading of bar code labels
· Control of movement of the stage
o Open or closed loop operation
o Positional accuracy (calibration) and repeatability
§ Lost motion compensation (e.g., backlash)
o Physical control (e.g., joystick) for single-slide, non-batch mode
o Selection of area to be scanned (in accordance to image composition
software)
§ whole slide
7

Contains Nonbinding Recommendations
306
307
308
309
310
311
312
313
314
315
316
317
318
319
320
321
322
323
324
325
326
327
328
329
330
331
332
333
334
335
336
337
338
339
340
341
342
343
344
345
346
347
348
349
350
351

·

§ automatically determined area with tissue content
Failure Mode and Effects Analysis (FMEA) (including severity, likelihood,
mitigations, etc.)
IV(A)(4)(b).

Test Method

Sponsors should demonstrate the mechanical performance of the stage with respect to
positional repeatability and accuracy on all relevant axes, in accordance with ISO 2302:2014 Test code for machine tools—Part 2: Determination of accuracy and
repeatability of positioning numerically controlled axes.

IV(A)(5).

Digital Imaging Sensor

IV(A)(5)(a).

Description

The digital image sensor is an array of photosensitive elements (pixels) that convert the
optical signals of the slide to digital signals, which consist of a set of values
corresponding to the brightness and color at each point in the optical image. Please
provide the following information and specifications:
· Sensor type (e.g., CMOS, CCD) and manufacturer
· Pixel information/specifications
o Number and dimensions of pixels
o Design of color filter array
§ Configuration of color filter array
§ Spectral transmittance of color filter mask
· Responsivity specifications
o Relative response versus wavelength
o Linearity
o Spatial uniformity
· Noise specifications
o Dark current level (electrons per second)
o Read noise (electrons)
· Readout rate (e.g., pixels per second, frames per second)
· Digital output format (e.g., bits per pixel, bits per color channel)
IV(A)(5)(b).

Test Methods

Sponsors should conduct the following tests in conformance with the corresponding
International Standards, if applicable:
·

·

Opto-electronic conversion function per ISO 14524:2009 Photography —
Electronic still-picture cameras — Methods for measuring optoelectronic
conversion functions (OECFs)
Noise measurements per ISO 15739:2013 Photography — Electronic still-picture
imaging — Noise measurements
8

Contains Nonbinding Recommendations
352
353
354
355
356
357
358
359
360
361
362
363
364
365
366
367
368
369
370
371
372
373
374
375
376
377
378
379
380
381
382
383
384
385
386
387
388
389
390
391
392
393
394
395

IV(A)(6).

Image Processing Software

IV(A)(6)(a).

Description

Image processing software refers to the embedded software components of the image
acquisition device. It typically includes control algorithms for image capture and
processing algorithms for raw data conversion into the digital image file. Sponsors
should provide the following information and specifications, if applicable:
· Exposure control
· White balance
· Color correction
· Sub-sampling
· Pixel-offset correction
· Pixel-gain or flat-field correction
· Pixel-defect correction
IV(A)(6)(b).

Resources

See the guidance entitled “Guidance for the Content of Premarket Submissions for
Software Contained in Medical Devices”
(http://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocument
s/ucm089543.htm) for the information that should be provided.

IV(A)(7).

Image Composition

IV(A)(7)(a).

Description

Image composition is a step present in systems that produce whole slide images as
opposed to individual fields of view. Whole slide scanning is typically performed in
accordance with the positioning of a stage that moves in submicron steps. At each
location of the stage movement, an image of the field of view is acquired. Images can be
acquired with a degree of overlapping (redundancy) between them to avoid gaps in data
collection. Images can also be acquired at different depths of focus followed by the
application of focusing algorithms. At the end of this process, all acquired images are
combined (stitched) together to create a composite high resolution image. There are a
number of features that can affect this process, and they are listed below. Sponsors
should provide a description of these features, if applicable:
· Scanning method
o Single objective or multiple miniature objectives in an array pattern
o Scanning pattern: square matrix acquisition (tiling), line scanning, etc.
o Overlap between scanned regions
o Merging algorithms that stitch the aligned images together into a
composite image file. Such algorithms may employ functions to align
adjacent fields of view in accordance to the scanning pattern, overlap, etc.

9

Contains Nonbinding Recommendations
396
397
398
399
400
401
402
403
404
405
406
407
408
409
410
411
412
413
414
415
416
417
418
419
420
421
422
423
424
425
426
427
428
429
430
431
432
433
434
435
436
437
438
439

·
·

o Automatic background correction functions to eliminate the effect of nonuniformities in the microscope’s illumination and image merging
procedure. These non-uniformities if not corrected might create visible
borders (seams and stitch lines) between the adjacent fields of view.
Scanning speed: time to scan the whole slide. This time is dependent on selected
magnification, and the amount of tissue on the glass slide.
Number of planes at the Z-axis to be digitized (stack depth)
IV(A)(7)(b).

Test Methods

Testing for image composition can be performed on a system level using special
calibration slides (such as grid patterns) that can test for line uniformity and focus
quality. Sponsors should provide the following outputs for these tests, if applicable:
· Images of digitized calibration slides
· Analysis of focus quality metrics
· Analysis of coverage of the image acquisition for the entire tissue slide

IV(A)(8).

Image Files Formats

IV(A)(8)(a).

Description

The final result from image acquisition can be a whole slide image consisting of a stack
of all acquired fields of view and magnifications during WSI. The complete digitized
image file usually occupies between 1-20 gigabytes of storage space depending on the
sample and the magnification of the objective lens used. Images can then be stored in a
number of ways and formats. Sponsors should provide the following information:
· Compression method (e.g., the wavelet-based JPEG2000 compression standard or
TIFF)
· Compression ratio: ratio of uncompressed to compressed file size. This metric
should be provided along with descriptive information on the data it was
measured from, since compression ratio is dependent on the content of the data
applied to.
· Compression type: lossless or lossy compression
· File format: can be formats easily accessible with public domain software such as
JPEG or TIFF, or can be proprietary formats only accessible with specific vendor
viewers. The file format depends on the file organization and related use.
· For systems that interact with DICOM-compliant software and hardware,
sponsors should provide a DICOM compatibility report.
· File organization:
o Single file with multi-resolution information (pyramidal organization)
o Stack of files at different magnifications

10

Contains Nonbinding Recommendations
440
441
442
443
444
445
446
447
448
449
450
451
452
453
454
455
456
457
458
459
460
461
462
463
464
465
466
467
468
469
470
471
472
473
474
475
476
477
478
479
480
481
482
483

IV(A)(9).

Image Review Manipulation Software

IV(A)(9)(a).

Description

For the image review manipulation software, sponsors should provide the following
information, describing software features, if applicable.
· Continuous panning (moving in x-y space) and pre-fetching (buffering adjacent
images to speed up panning time)
· Continuous zooming (magnification)
· Discrete Z-axis displacement
· Ability to compare multiple slides simultaneously on multiple windows
· Ability to perform annotations
· Image enhancement such as sharpening functions
· Color manipulation, including color profile, white balance, color histogram
manipulation, and color filters
· Annotation tools
· Tracking of visited areas and annotations
· Digital bookmarks (revisit selected regions of interest)
· Virtual “multihead microscope” (this is when multiple pathologists
simultaneously review the same areas remotely)
IV(A)(9)(b).

Resources

See the guidance entitled “Guidance for the Content of Premarket Submissions for
Software Contained in Medical Devices”
(http://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocument
s/ucm089543.htm) for additional information on this subject.

IV(A)(10). Computer Environment
IV(A)(10)(a).

Description

Computer environment refers to the workstation, including both hardware and software
components, that retrieves the digital image file and drives the display for the user to
review the images. Sponsors should provide the following information and
specifications, if applicable:
· Computer hardware
· Operating system
· Graphics card
· Graphics card driver
· Color management settings
· Color profile
· Display interface (e.g., DVI or DisplayPort)

11

Contains Nonbinding Recommendations
484
485
486
487
488
489
490
491
492
493
494
495
496
497
498
499
500
501
502
503
504
505
506
507
508
509
510
511
512
513
514
515
516
517
518
519
520
521
522
523
524
525
526

IV(A)(11). Display
IV(A)(11)(a).

Description

The final stage of a WSI system is the display component that presents the scanned image
to the pathologists for reading. Technically, display refers to the optoelectronic device
that converts the digital image signals in the RGB space into optical image signals. For
the display, sponsors should provide the following information and specifications, if
applicable:
· Technological characteristics of the display device (e.g., in-plane switching LCD
panel with TFT active-matrix array with fluorescent backlight)
· Physical size of the viewable area and aspect ratio
· For transmissive displays, backlight type and properties including temporal,
spatial, and spectral characteristics
· Frame rate and refresh rate
· Pixel array, pitch, pixel aperture ratio and subpixel matrix scheme (e.g., chevron,
RGBW)
· Subpixel driving to improve grayscale resolution (e.g., spatial and temporal
dithering)
· Supported color spaces
· Display Interface
· User controls of brightness, contrast, gamma, color space, power-saving options,
etc. via the on-screen display (OSD) menu
· Ambient light adaptation including the ambient light sensing method,
instrumentation, and software tool description
· Touch screen technology including method, functionality, and any calibration or
periodical re-tuning requirements
· Color calibration tools (sensor hardware and associated software), color profile,
and method for color management
· Frequency and nature of quality-control tests to be performed by the user and/or
the physicist with associated action limits.

IV(A)(11)(b).
·

·

Test Methods

User controls: Modes and settings of the display undergoing testing should be
specified, including brightness, contrast, gamma, white point, color space, etc.
See 2.1 Modified-Performance Modes, IDMS 1.03.
Spatial resolution: Measurements of the transfer of information from the image
data to the luminance fields at different spatial frequencies of interest typically
done by reporting the modulation transfer function. Non-isotropic resolution
properties should be characterized properly by providing two-dimensional
measurements or measurements along at least two representative axes. See 7.7
Effective Resolution, IDMS 1.03.

12

Contains Nonbinding Recommendations
527
528
529
530
531
532
533
534
535
536
537
538
539
540
541
542
543
544
545
546
547
548
549
550
551
552
553
554
555
556
557
558
559
560
561
562
563
564
565
566
567
568
569
570
571
572

·

·

·

·

·
·

·
·

·

·

·

Pixel defects (count and map): Measurements (counts) and location of pixel
defects. This is typically provided as a tolerance limit. Pixel defects can interfere
with the visibility of small details in medical images. See 7.6 Defective Pixels,
IDMS 1.03.
Artifacts: Evaluate for image artifacts such as ghosting and/or image sticking
from displaying a fixed test pattern for a period of time. See 4.6 Artifacts and
Irregularities, IDMS 1.03.
Temporal response: Measurements of the temporal behavior of the display in
responding to changes in image values from frame to frame. Since these
transitions are typically not symmetric, rise and fall time constants are needed to
characterize the system. See 10.2.3 Gray-to-Gray Response Time, IDMS 1.03.
Maximum and minimum luminance (achievable and recommended):
Measurements of the maximum and minimum luminance that the device outputs
as used in the application under recommended conditions and the achievable
values if the device is set to expand the range to the limit. See 2.4 Vantage-Point
Suite of Measurement, IDMS 1.03.
Grayscale: Measurements of the mapping between image values and the
luminance. See 6.1 Grayscale, IDMS 1.03.
Luminance uniformity and Mura test: Measurements of the uniformity of the
luminance across the display screen. See 8.1.2 Sampled Vantage-Point Uniformity
and 8.2.3 Mura Analysis, IDMS 1.03.
Stability of luminance and chromaticity response with temperature and lifetime
Bidirectional reflection distribution function: Measurements of the reflection
coefficients of the display device. Specular and diffuse reflection coefficients can
be used as surrogates for the full bidirectional reflection distribution function. See
11.12 Diagnostic: Characterizing Hemisphere Uniformity, IDMS 1.03.
Gray Tracking: Chromaticity at different luminance levels as indicated by the
color coordinates in an appropriate units system (e.g., CIE u’v’). See AAPM Task
Group 196 Report.
Color scale: Color coordinates of primary and secondary colors as a function of
the digital driving level and their additivity. See 6. Gray- and Color-Scale
Measurement and 5.4 Color-Signal White, IDMS 1.03.
Color gamut volume: See 5.31 Volume-Color-Reproduction Capability, IDMS
1.03.
IV(A)(11)(c).

Resources

Those interested in learning more about these types of display considerations should
consider reading:
·

IDMS 1.03 - Information Display Measurements Standard Version 1.03,
International Committee for Display Metrology, Society for Information Display,
www.icdm-sid.org

·

E. Samei, A. Badano, D. Chakraborty, K. Compton, C. Cornelius, K. Corrigan,
M. J. Flynn, B. Hemminger, N. Hangiandreou, J. Johnson, M. Moxley, W.
13

Contains Nonbinding Recommendations
573
574
575
576
577
578
579
580
581
582
583
584
585
586
587
588
589
590
591
592
593
594
595
596
597
598
599
600
601
602
603
604
605
606
607
608
609
610
611
612
613
614
615
616
617
618

Pavlicek, H. Roehrig, L. Rutz, J. Shepard, R. Uzenoff, J. Wang, and C. Willis,
Assessment of display performance for medical imaging systems, Report of the
American Association of Physicists in Medicine (AAPM) Task Group 18,
Technical Report, AAPM (April 2005).
·

IEC 62563-1:2009, Medical electrical equipment – Medical image display
systems – Part 1: Evaluation methods

·

Amendment 1 to IEC 62563-1: Medical image display systems – Part 1:
Evaluation methods

·

The guidance entitled “Guidance for Industry and FDA Staff: Display Accessories
for Full-Field Digital Mammography Systems-Premarket Notification (510(k))
Submissions”
(http://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceD
ocuments/ucm107549.htm).

IV(B). System-level Assessment
This subsection details the test methods at the system level that should be included in the
technical performance assessment of a WSI device. In this guidance, system refers to a
series of consecutive components in the imaging chain with clearly defined, measureable
input and output. For example, a system-level test can be designed for the image
acquisition subsystem, the image display subsystem, or a combination of both. The goal
of system-level tests is to assess the composite performance of a series of consecutive
components in the imaging chain. System-level tests should be conducted when the
component-level tests are either unfeasible or unable to capture the interplay between
components.
The common framework of the system-level tests described in this section is to compare
the system under test with an ideal system based on the same input, and then report the
difference between their outputs quantitatively. Designing such a system-level test
typically involves the following steps: (1) define the scope of the system and its input and
output, (2) define the input, which in most cases is a test target or phantom, (3) measure
the input to establish the ground truth that would be generated by an ideal system, (4)
measure the output of the system under test, and (5) calculate the errors between the truth
and the output with a quantitative metric. The framework of a typical system-level test is
shown in Diagram 2. Notice that the ideal system is a hypothetical device that generates
the perfect output with respect to the objective of the test such as color or focus. The
purpose of the ideal system is to define the intended behavior of the system under test.
The ideal system does not need to be implemented. Instead, the ideal system should be
simulated by a test method that establishes the truth of the input phantom.

14

Contains Nonbinding Recommendations
619
620

Diagram 2: Framework of a typical system-level test.

621
622

System under test

Output

Input
(Phantom)

f

623

Ideal system

Error

Truth

624
625
626
627
628
629
630
631
632
633
634
635
636
637
638
639
640
641
642
643
644
645
646
647
648
649
650
651
652
653
654
655
656
657
658
659
660
661
662

IV(B)(1).

Color Reproducibility

IV(B)(1)(a).

Description

Color reproducibility is one of the key characteristics of a WSI system. The color
characteristics are determined by every component in the imaging chain. Therefore, the
color characteristics might be best evaluated at the system level. Color reproducibility
indicates the accuracy and precision of the color transformation from the tissue sample on
the slide to the image on the display. The colors of the tissue specimen should be
accurately and precisely reproduced on the display based on the color reproduction intent,
which should be clearly defined and justified by the sponsor.
IV(B)(1)(b).

Test Methods

The WSI system should be tested with a target slide. The target slide should contain a set
of measurable and representative color patches. Ideally the color patches should have
similar spectral characteristics to stained tissue. The color patches should include a
grayscale ramp for evaluating the grayscale response. The truth of the color patches
should be measured with proper apparatuses separately.
For each color patch, the intended color (i.e., the expected output color based on the color
reproduction intent defined by the Sponsor) should be calculated based on the truth of the
color patches.
The target slide should be scanned and displayed by the WSI system. The output color of
each color patch should be measured from the display.
The three datasets – truth, intended color, and output color – should be compared and
analyzed. The sponsor should provide a rationale if the intended color is different from
the truth.

15

Contains Nonbinding Recommendations
663
664
665
666
667
668
669
670
671
672
673
674
675
676
677
678
679
680
681
682
683
684
685
686
687
688
689
690
691
692
693
694
695
696
697
698
699
700
701
702
703
704
705
706
707
708

Diagram 3: Framework of the system-level color reproducibility test.

WSI under test
Target
Slide
Meter

IV(B)(1)(c).

Truth

Color
Reproduction
Intent

Output Color

-

Accuracy
Precision

Intended Color

Resources

Useful references on the subject of color reproducibility can be found at the International
Color Consortium website http://www.color.org.

IV(B)(2).

Spatial Resolution

IV(B)(2)(a).

Description

Spatial resolution is another key characteristic of a WSI system. The goal of this systemlevel test is to evaluate the composite optical performance of all components in the image
acquisition phase (i.e., from slide to digital image file).
IV(B)(2)(b).

Test Methods

The following test is recommended for assessing spatial resolution of the image
acquisition phase:
· Resolution and spatial frequency response: ISO 12233:2014(E) — Photography
— Electronic still picture imaging — Resolution and spatial frequency responses.

IV(B)(3).

Focusing Test

·

The quality of focus in WSI can be affected by a number of inter-related factors,
including the scanning method and approaches for constructing a focus map. Due
to a trade-off between the number of focus points and the overall speed of the
scanning process, focusing is typically based on a sample of focus points,
determined automatically (auto-focus) or manually by the user. Since tissue can
have uneven depth, auto-focus algorithms are needed to detect and adjust for
different depths of focus.

·

Data demonstrating that the focus quality is acceptable, even in the presence of
uneven tissue, should be provided. Such data with proper justification could be
derived from a phantom study, from clinical data, or both in a complementary
fashion. The technology of phantom construction for testing focus is under
development and this guidance will be updated as such technologies become
available. Sponsors could attempt to build their own phantoms for testing depth
16

Contains Nonbinding Recommendations
709
710
711
712
713
714
715
716
717
718
719
720
721
722
723
724
725
726
727
728
729
730
731
732
733
734
735
736
737
738
739
740
741
742
743
744
745
746
747
748
749
750
751
752
753
754

of focus for their device. Alternatively, sponsors could provide experimental data
using clinical tissue slides. Sampling of cases for such an experiment should be
enriched for uneven tissue cases within a range representative of typical
laboratory output. Alternative approaches for assessing the focus quality of a
WSI will be considered along with proper justification. In addition, the following
specifications should be provided, if applicable:
o Focus method: auto-focus for high-throughput or user-operated focus
points
o Instructions for the selection of manual focus points (if applicable),
including number of focus points and location in relation to a tissue
sample
o Metrics used to evaluate focusing and description of methods to extract
them
o Methods for constructing focus map from sample focus points
Diagram 4: Framework of the system-level focusing test.
WSI under test
Phantom
Slide

IV(B)(4).

Actual
Focus

f
WSI with perfect
focusing capability

Error

Optimal
Focus

Whole Slide Tissue Coverage

IV(B)(4)(a).

Description

During the scan phase, WSI systems usually skip blank areas where tissue is absent in
order to reduce scan time and file size. The purpose of the whole slide tissue coverage
test is to demonstrate that all of the tissue specimen on the glass slide is included in the
digital image file.
IV(B)(4)(b).

Test Method

Sponsors should include a test that demonstrates the completeness of the tissue coverage.
Sponsors should describe the test method and include the following items:
· Selection of the input tissue slide
· How to determine the complete coverage of the input tissue slide
· How to measure the actual coverage of the WSI output
· Calculate the ratio of the actual to complete coverage

17

Contains Nonbinding Recommendations
755
756
757
758
759
760
761
762
763
764
765
766
767
768
769
770
771
772
773
774
775
776
777
778
779
780
781
782
783
784
785
786
787
788
789
790
791
792
793
794
795
796
797
798
799
800

Diagram 5: Framework of the system-level whole slide tissue coverage test
WSI under test
Tissue
Slide

f
WSI with complete
coverage capability

IV(B)(5).

Actual
Coverage
Error

Complete
Coverage

Stitching Error

IV(B)(5)(a).

Description

Stitching is the technique that enables a WSI system to combine thousands of sub-images
into a single whole-slide image. Although during the scanning process a certain amount
of overlapping between adjacent sub-images is maintained for alignment purposes,
successful stitching relies on the texture present in the overlapped area. When the
stitching algorithm fails to align two sub-images seamlessly, the error may or may not be
perceivable by the human reader depending on whether noticeable stitching artifacts are
generated. Therefore, a system-level test should be conducted when assessing the
stitching quality of the WSI system.
IV(B)(5)(b).

Test Methods

Sponsors should include a test that evaluates the stitching errors and include the
following items:
· Selection of the input test slide
· Method for sampling of the stitching boundaries where stitching errors might
occur
· How to determine the ideal stitching as the ground truth
o For example, the region of the stitching boundaries can be re-imaged in
one shot such that there is no stitching artifact.
· How to evaluate quality of the actual stitching based on the perfect stitching
o For example, compare the image of stitching boundaries with the perfect
one that does not have stitching artifact. The difference between these two
images can be used as a figure of merit of the stitching quality.
Diagram 6: Framework of the system-level stitching error test
Actual
Stitching

WSI under test
Tissue
Slide

f
WSI with perfect
stitching capability
18

Perfect
Stitching

Error

Contains Nonbinding Recommendations
801
802
803
804
805
806
807
808
809
810
811
812
813
814
815
816
817
818
819
820
821
822
823
824
825
826
827
828
829
830
831
832
833
834
835
836
837
838
839
840
841
842
843
844
845
846

IV(B)(6).

Turnaround Time

IV(B)(6)(a).

Description

Turnaround time is the time required by the WSI system to execute a particular user
operation such as panning/zooming where the software and I/O (input/output) devices
retrieve image data, execute the computation, and refresh the image on the display. The
turnaround time starts when the user enters a command via a keyboard stroke or a mouse
click/movement and finishes when the image is completely updated on the display.
Turnaround time is important for a WSI system when fast and repetitive panning
operations are performed during a search task, which is delay-free in an optical
microscope. Prolonged, unpredictable turnaround time may impact the user’s diagnostic
performance. The user interface should properly prompt the user when the operation is
incomplete and the requested image is not available . The turnaround time may vary
greatly depending on the user-requested operation, image content, data size/location,
computer workload, display size, etc. The sponsor should report the typical turnaround
time as well as the test method and test conditions.

IV(C). User Interface
IV(C)(1).

Description

The user interface covers all components and accessories of the WSI system with which
users interact while loading the slides and acquiring, manipulating, and reviewing the
images. It also includes preparing the system for use (e.g., unpacking, set up,
calibration), and performing maintenance. Elements of the user interface have been
noted in many of the preceding sections and include two broad categories:
· Options through which the user operates the WSI system, such as:
o Software menu options (e.g., scanning parameters)
o Physical controls (e.g., clips on the slide feeder)
o Connectors and connections (e.g., cables connecting system components)
· Information presented to the user through
o Visual displays (e.g., scanned image, software menus)
o Sounds (e.g., tone played when scanning completed)
o Instructions (e.g., software users’ manual)
o Labels

IV(C)(2).

Test Methods

It is recommended that the analysis to identify the use-related hazards of the WSI system
include the consideration of use errors involving failure to acquire, perceive, read,
interpret, and act on information from the WSI system correctly or at all and the harm
that could be caused by such errors. A human factors/usability validation test should be
performed to demonstrate that representative users of the WSI system can perform
essential tasks and those critical to safety under simulated use conditions.
19

Contains Nonbinding Recommendations
847
848
849
850
851
852
853
854
855
856
857
858
859
860
861
862
863
864
865
866
867
868
869
870
871
872

When selecting participants for validation testing, sponsors should carefully consider user
capabilities and expectations that could potentially impact the safe and effective use of
the WSI system. Examples of items that should be considered, if applicable, include
visual acuity and type of vision correction and the impact of expectations formed from
prior experience with other systems (e.g., optical microscope).
When selecting the critical tasks to be evaluated, sponsors should incorporate all known
use related errors and problems from similar devices (devices having similar
technological characteristics and indications for use) into the validation testing.
Consideration also should be given to whether task performance changes over time, and
if test duration needs to account for user fatigue. Examples might include a user altering
a task sequence in response to fatigue from repetitive image selection and manipulation
with mouse or keyboard.
When creating the simulated use conditions for validation testing, special consideration
should be given to the location of the WSI system primary workstation, its components,
their arrangement and how their locations affect user performance. Examples of location
considerations might include multiple monitors, a monitor with sub-optimal display
settings, or glare on a monitor from indoor lighting.
A human factors/usability validation test report should generally include the information
found in Table 1.
Table 1: Items a Human Factors/Usability Validation Test Report Should Include
Section
1

Contents
Intended device users, uses, use environments, and training
·
·
·
·

2

Device user interface
·
·

3

Intended user population(s) and critical differences in
capabilities between multiple user populations
Intended uses and operational contexts of use
Use environments and key considerations
Training intended for users and provided to test participants

Graphical depiction (drawing or photograph) of device user
interface
Verbal description of device user interface

Summary of known use problems
·
·

Known problems with previous models
Known problems with similar devices
20

Contains Nonbinding Recommendations
·

4

User task selection, characterization and prioritization
·
·
·

5

Evaluation methods
Key results and design modifications implemented
Key findings that informed the HFE/UE validation testing
protocol

Validation testing
·
·
·
·
·
·
·
·

7

Risk analysis methods
Use-related hazardous situation and risk summary
Critical tasks identified and included in HFE/UE validation tests

Summary of formative evaluations
·
·
·

6

Design modifications implemented in response to user
difficulties

Rationale for test type selected (i.e., simulated use or clinical
evaluation)
Number and type of test participants and rationale for how they
represent the intended user populations
Test goals, critical tasks and use scenarios studied
Technique for capturing unanticipated use errors
Definition of performance failures
Test results: Number of device uses, success and failure
occurrences
Subjective assessment by test participants of any critical task
failures and difficulties
Description and analysis of all task failures, implications for
additional risk mitigation

Conclusion
A statement to the effect that “The <device name/model> has been
found to be reasonably safe and effective for the intended users, uses
and use environments” should be included under the following
conditions:
·
·

The methods and results described in the preceding sections
support this conclusion.
Any residual risk that remains after the validation testing would
not be further reduced by modifications of design of the user
interface (including any accessories and the Instructions for Use
(IFU)), is not needed, and is outweighed by the benefits that
21

Contains Nonbinding Recommendations
may be derived from the device’s use.
873
874
875
876
877
878
879
880
881
882
883
884
885
886
887
888
889
890
891
892
893
894
895
896
897
898
899
900
901
902
903
904
905
906
907
908
909
910
911
912
913

Recommended methods for performing a human factors/usability validation test are
described in the resources listed in section IV(C)(3) entitled “Resources” directly below.
The goal of testing is to assure that users can operate the WSI system successfully for the
intended uses without negative clinical consequences to the patient and that potential use
errors or failures have been eliminated or reduced.

IV(C)(3).

Resources

FDA recognizes standards published by national and international organizations that
apply human factors engineering/usability engineering (HFE/UE) principles to device
design and testing. The recognized standards listed below provide suggestions on
conducting an analysis of use-related hazards and a human factors/usability validation
test to assess the safety and effectiveness of the final device design.
·

ISO 14971:2007, Medical Devices – Application of Risk Management to Medical
Devices: Provides systematic process to manage the risks associated with the use
of medical devices.
· AAMI/ANSI HE75:2009, Human Factors Engineering – Design of Medical
Devices: Comprehensive reference of recommended practices related to human
factors design principles for medical devices.
· IEC 62366-1:2015, Medical devices – Application of usability engineering to
medical devices: Describes the process to conduct medical device usability testing
and incorporate results into a risk management plan.
In addition, FDA has published guidance with human factors related recommendations to
assist manufacturers and facilitate premarket review. The guidance entitled “Guidance
for the Content of Premarket Submissions for Software Contained in Medical Devices”
(http://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceDocument
s/ucm089543.htm). This guidance document provides recommendations to industry
regarding premarket submissions for software devices, including stand-alone software
applications and hardware-based devices that incorporate software. It includes test
methods to assure that the software conforms to the needs of the user and to check for
proper operation of the software in its actual or simulated use environment.

IV(D). Labeling
The premarket application must include labeling in sufficient detail to satisfy the
requirements of 21 CFR Part 801 and 21 CFR 809.10. The labeling includes
supplementary information necessary to use and care for the WSI system such as
instruction books or direction sheets and software user manuals.

22

Contains Nonbinding Recommendations
914
915
916
917
918
919
920
921
922
923
924
925
926
927
928
929
930
931
932
933
934
935
936
937
938
939
940
941
942
943
944
945
946
947
948
949
950
951
952
953
954
955
956
957
958
959

Although instructions, labeling, and training can influence users to use devices safely and
effectively, they should not be the primary strategy used to control risk. Modification of
the user interface design is a more effective approach to mitigate use-related hazards.

IV(D)(1).

Test Methods

It is recommended that studies on labeling and training be conducted separately from
other human factors/usability validation testing. Human factors/usability validation
testing should be conducted with the final version of the labeling and related materials.
Timing and content of training should be consistent with that expected of actual users.

IV(D)(2).

Resources

FDA has published several guidance documents on labeling to facilitate premarket
review and assist manufacturers.
· The guidance entitled “Labeling - Regulatory Requirements for Medical Devices”
(http://www.fda.gov/downloads/MedicalDevices/DeviceRegulationandGuidance/
GuidanceDocuments/UCM095308.pdf).
o This publication covers labeling issues that device manufacturers,
reconditioners, repackers, and relabelers should consider when a product
requires labeling. Labeling includes adequate instructions for use,
servicing instructions, adequate warnings against uses that may be
dangerous to health, or information that may be necessary for the
protection of users.
· The guidance entitled “Device Labeling Guidance #G91-1 (blue book memo)”
(http://www.fda.gov/MedicalDevices/DeviceRegulationandGuidance/GuidanceD
ocuments/ucm081368.htm).
o This guidance is intended to ensure the adequacy of, and consistency in
device labeling information. It is intended for use by industry in preparing
device labeling.
· The guidance entitled “Human Factors Principles for Medical Device Labeling”
(http://www.fda.gov/downloads/MedicalDevices/DeviceRegulationandGuidance/
GuidanceDocuments/UCM095300.pdf).
o This report presents the principles of instruction, human factors, and
cognitive psychology that are involved in designing effective labeling for
medical devices.

IV(E). Quality Control
Sponsors should provide information on the quality control procedures, including
frequency and testing methods to be performed by the laboratory technologists and/or
field engineers with associated quantitative action limits. Discussions of tests for
constancy should include discussions of the slide feeder and scanning mechanisms,
coverage of the entire tissue slide, the bar code reader, the light source, the imaging
sensor device, and the calibrations at the component and system level. A detailed quality
control manual should be provided.
23


