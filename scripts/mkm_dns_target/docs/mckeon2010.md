# A critical-layer framework for turbulent pipe flow

B. J. M<sup>c</sup>KEON<sup>1</sup>† AND A. S. SHARMA<sup>2</sup> 

<sup>1</sup>Graduate Aerospace Laboratories, California Institute of Technology, Pasadena, CA 91125, USA <sup>2</sup>Department of Aeronautics, Imperial College, London SW7 2AZ, UK 

(Received 13 December 2009; revised 8 April 2010; accepted 8 April 2010; first published online 1 July 2010) 

A model-based description of the scaling and radial location of turbulent fluctuations in turbulent pipe flow is presented and used to illuminate the scaling behaviour of the very large scale motions. The model is derived by treating the nonlinearity in the perturbation equation (involving the Reynolds stress) as an unknown forcing, yielding a linear relationship between the velocity field response and this nonlinearity. We do not assume small perturbations. We examine propagating helical velocity response modes that are harmonic in the wall-parallel directions and in time, permitting comparison of our results to experimental data. The steady component of the velocity field that varies only in the wall-normal direction is identified as the turbulent mean profile. A singular value decomposition of the resolvent identifies the forcing shape that will lead to the largest velocity response at a given wavenumber–frequency combination. The hypothesis that these forcing shapes lead to response modes that will be dominant in turbulent pipe flow is tested by using physical arguments to constrain the range of wavenumbers and frequencies to those actually observed in experiments. An investigation of the most amplified velocity response at a given wavenumber–frequency combination reveals critical-layer-like behaviour reminiscent of the neutrally stable solutions of the Orr–Sommerfeld equation in linearly unstable flow. Two distinct regions in the flow where the influence of viscosity becomes important can be identified, namely wall layers that scale with $R ^ { + 1 / 2 }$ and critical layers where the propagation velocity is equal to the local mean velocity, one of which scales with $\mathbf { \hat { \Pi } } _ { R ^ { + \hat { 2 } / 3 } }$ in pipe flow. This framework appears to be consistent with several scaling results in wall turbulence and reveals a mechanism by which the efects of viscosity can extend well beyond the immediate vicinity of the wall. The model reproduces inner scaling of the small scales near the wall and an approach to outer scaling in the flow interior. We use our analysis to make a first prediction that the appropriate scaling velocity for the very large scale motions is the centreline velocity, and show that this is in agreement with experimental results. Lastly, we interpret the wall modes as the motion required to meet the wall boundary condition, identifying the interaction between the critical and wall modes as a potential origin for an interaction between the large and small scales that has been observed in recent literature as an amplitude modulation of the near-wall turbulence by the very large scales. 

Key words: boundary layer receptivity, boundary layer structure, critical layers, pipe flow boundary layer, turbulence theory, turbulent boundary layers 

## 1. Introduction

The accurate descriptions of statistical scaling and instantaneous structural coherence of turbulent fluctuations, and their relationship to the mean flow, are amongst the important unsolved problems in physics. Even at the simplest level, we still lack a complete explanation of the development of the mean velocity profile in canonical flows as the Reynolds number increases. Such an understanding would be an important step towards accurate prediction of skin friction in complex aeronautical and industrial flows, and would underpin any efort at a turbulence control scheme. A brief summary of three distinct approaches to these problems is given here. 

The research literature is replete with statistical descriptions of the wall-normal distributions of the components of the Reynolds stress tensor, with an obvious bias to the streamwise normal stress, which is most easily measured. New understanding of turbulence has emerged in the past decade. This has included diferences in some characteristics between the canonical cases of pipe, channel and zero-pressure gradient boundary-layer flow (Monty et al. 2009), in contrast to the long-standing hypothesis of universality of near-wall scaling. Relevant to the present work, several studies have revealed highly energetic structures with streamwise wavelength of order 10 times the outer length scale, deemed variously ‘very large scale motions’ (VLSMs) or ‘superstructures’. The VLSM phenomenon, discussed at length later in this work, suggests a more complicated nature of the scaling of the turbulence than an inner/outer/overlap structure proposed for the mean velocity and confirmed to the resolution of experimental measurements. Specifically, it suggests the influence on the inner near-wall flow of turbulent activity that scales on outer variables. 

The advent of particle image velocimetry (PIV) techniques and advances in simulation, alongside more traditional visualization techniques, have illuminated the development and grouping of organized coherent structures. These include the autonomous near-wall cycle and an eddy type that is statistically well described by the hairpin vortex paradigm. 

In parallel to these experimental and computational approaches, considerable progress has been made in understanding the amplification properties of the Navier– Stokes operator, and in particular the linearized operator, in laminar flows. More recent work has extended some of these techniques to the turbulent case, with limited success. 

In what follows, we summarize some key concepts and questions arising from these three distinct approaches which are pertinent to the current work. 

## 1.1. The challenge to classical scaling: the influence of very large scale motions on the near-wall region

Classical scaling ideas involve inner and outer layers, where the appropriate spatial scales are respectively the viscous unit and the outer length scale, and the appropriate velocity scale is the friction velocity. In the case of the outer layer this velocity is impressed by the boundary condition at the wall. For suficiently high Reynolds number, there may also be an overlap layer in which both scalings hold and therefore the important length scale must be the local distance from the wall. This scaling appears to work well for the mean velocity despite recent challenges (Marusic et al. 2010). However it is unable to collapse the turbulent fluctuations in the inner and overlap regions, an apparent reflection of the influence of outer scales on the inner region, termed ‘inner–outer interaction’ as explored by Bandyopadhyay & Hussain (1984), that is reflected in the spectral energy distribution. 

The recent focus on VLSMs in canonical turbulent wall flows has given some insight into the source of this interaction. Coherence across the wall layer at long streamwise length scales has been known since the observations of Kovasznay, Kibens & Blackwelder (1970). The work of Kim & Adrian (1999) and Morrison et al. (2004) identified the energetic importance of VLSMs in the streamwise spectra in turbulent pipe flow and the subsequent work by Adrian and co-workers (Guala, Hommema & Adrian 2006; Balakumar & Adrian 2007) has indicated that large and very large scale features must be considered to be ‘active’ in the sense that they carry significant shear stress. This contrasts with Townsend’s geometrical arguments that only the small scales display suficient coherence in the wall-normal and streamwise fluctuations to extract significant energy from the mean flow, via the product of the Reynolds shear stress and the mean velocity gradient. 

Simulating and observing these high aspect ratio VLSMs places heavy demands on existing computational and experimental techniques, a constraint that has obstructed progress in our understanding of their origin and development in turbulent flows. The statistical imprint in the streamwise and wall-normal directions is clear from hot-wire measurements. Hutchins & Marusic (2007b) showed for suficiently high Reynolds numbers that this imprint reaches from a peak energy located somewhere in the overlap region down to the wall, even having a footprint on the wall shear stress (Marusic & Heuer 2007): Hutchins & Marusic (2007a) and Monty et al. (2007) used Taylor’s hypothesis to reconstruct the long streamwise–spanwise coherence in the streamwise velocity from arrays of hot-wires in turbulent boundary layers and pipe flow, respectively. Their use of Taylor’s hypothesis highlights a major observational dificulty: at these large scales, Taylor’s hypothesis may not apply, since the necessary arguments based on the ratio of eddy turnover time scale to convective time scale no longer hold. In addition, the wall-normal extent of the VLSMs means that if the VLSM convects with the local mean velocity somewhere in the overlap layer, Taylor’s hypothesis with a scale-independent convective velocity must be in error closer to the wall, and likely also further from the wall to a much lesser degree. 

Having listed some of the outstanding questions concerning the VLSMs, we now provide a brief summary of what is known about their extent and influence on the near-wall region. The first study by Hutchins and Marusic (2007a) suggested that the peak streamwise VLSM energy occurred at a constant fraction of the boundary-layer thickness, $y / \delta \sim 0 . 0 5$ . Further studies by McKeon (2008) and Mathis, Hutchins & Marusic (2009) over a wider range of Reynolds numbers showed that in fact there is a weak-Reynolds-number-dependence of the location of the peak. This can be masked by the error associated with identifying the peak from experimental data when only a small-Reynolds-number range is considered. The latter authors compared the peak’s location with the centre of a mean velocity overlap region that has an inner limit that is either fixed in inner units or Reynolds-number-dependent, giving rise to $\delta ^ { + 1 / 2 }$ and $\delta ^ { + 3 / 4 }$ dependence of the peak location, respectively, where $\delta ^ { + } = \delta u _ { \tau } / \nu ,$ , ν is the kinematic viscosity and the friction velocity $u _ { \tau } = \sqrt { \tau _ { w } / \rho }$ The wall shear stress is denoted $\tau _ { w }$ and $\rho$ represents the density. However the agreement depends crucially on single data points obtained at very high Reynolds number in the near-neutral atmospheric surface layer, and these vary between studies (Metzger, McKeon & Holmes 2007; Mathis et al. 2009; Guala, Metzger & McKeon 2010b). 

Recent studies show that the streamwise extent of the dominant large-scale motion is proportional to the outer flow length scale and is closely given by $\lambda _ { x , V L S M } \sim 1 0 R$ in internal flows (Kim & Adrian 1999; Monty et al. 2009) and $\lambda _ { x , s u p e r s t r u c t u r e } \sim 6 \delta$ in boundary layers (Hutchins & Marusic 2007b), while the direct numerical simulation (DNS) of channel flow of Jimenez, del´ Alamo & Flores (2004) and the study of Monty<sup>´</sup> et al. (2009) indicate the additional importance of a slightly smaller wavelength, $\lambda _ { x , L S M } \sim 3 h$ . Here R, δ and h are the pipe radius, boundary-layer thickness and channel half-height, respectively. Monty et al. (2009) recently performed a rigorous comparison of the streamwise velocity spectra in the diferent flows at the same Reynolds number and elucidated the respective importance of these three wavelengths in diferent regions of the flow. The spanwise extent in each case appears to be of the order of one outer length scale (Monty et al. 2007; Hutchins & Marusic 2007a), giving the largest scale structure an approximate axially elongated aspect ratio of 10:1:1. 

Subsequently, Mathis et al. (2009) expounded on earlier observations that the very large scales apply an amplitude modulation to the small-scale turbulence near the wall. Using a Hilbert transform technique, they were able to quantify the interaction and its Reynolds-number-dependence, as well as demonstrate a change in the sign of the modulation that corresponded with the location of the VLSM energy peak. Guala, Metzger & McKeon (2009a, b) and Chung & McKeon (2010) have also proposed methodologies to describe this efect, with the latter identifying that the modulation can also be described in terms of the spatial phase relationship between large- and small-scale turbulent activity. 

It is clear, then, that the very large scale structure reflects an aspect of boundarylayer dynamics that has hitherto been poorly understood, but has importance for scaling of local and global turbulence properties, as well as for future flow control schemes. 

## 1.2. Alternative scaling approaches from theory and observation: critical layers

Several theories have been proposed to account for the missing physics in the classical scaling, including the mesolayer of Long & Chen (1981), the focus on the location of the Reynolds stress peak by Sreenivasan and co-workers (Sreenivasan & Sahay 1997) and the hierarchical structure associated with the mean momentum balance of Klewicki and co-workers, e.g. Klewicki et al. (2007). 

Sreenivasan (1988) formulated an inviscid structural model of the turbulent boundary layer consisting of two vortex sheets of opposite sign symmetrically located about the hypothetical wall location. By analogy with the critical layer in transitional boundary layers, he showed that the wall-normal location of the peak in Reynolds shear stress should have a Reynolds-number-dependence given by $\hat { y } _ { p k } ^ { + } \sim R ^ { + 1 / 2 }$ with a proportionality constant of two determined from experimental data. Here $y ^ { + } = y u _ { \tau } / \nu$ is the wall-normal distance y non-dimensionalized with the viscous scaling length, defined as the kinematic viscosity ν divided by the friction velocity. Experimental evidence from boundary layers, pipe and channel flows supported this critical-layer interpretation, the resulting streamwise and spanwise wavelengths for maximum amplification, the $y _ { p k } ^ { + } \sim R ^ { + \bar { 1 / 2 } }$ scaling (Sreenivasan & Sahay 1997) and the hypothesis that the mean velocity at the peak in the Reynolds shear stress corresponds to a constant fraction of the free-stream velocity. In addition, Sreenivasan & Bershadski (2006) were able to extend the study of the region in the vicinity of the Reynolds stress peak by performing a logarithmic expansion and predicting the resultant form for the mean velocity profile. 

The reader should note that an analogy with critical-layer theory in laminar flow was also made by Sirovich, Ball & Keefe (1990), who found that the most energetic propagating eigenfunctions in a proper orthogonal decomposition (POD, also known as Karhunen–Loeve analysis) of turbulent channel flow had their principal support in the region of the peak in Reynolds shear stress. Duggleby et al. (2007) have also given some insight into the most energetic POD modes in low-Reynolds-number turbulent pipe flow, illuminating a distinction between propagating and non-propagating, wall, lift, asymmetry and ring modes defined by the relative magnitude of the streamwise and azimuthal wavenumbers. A truncated POD representation of turbulent pipe flow was also used by Aubry et al. (1988) to develop a model for the dynamical behaviour of the streamwise roll modes and establish a connection between near-wall turbulent flow and the dynamics of a chaotic system. 

## 1.3. Linear and nonlinear tools for analysis of the Navier–Stokes equations

Other researchers, essentially forming a diferent community, have exploited tools from linear systems and dynamical systems theory, with a notable focus on the large algebraic energy growth that is possible due to the non-normality of a stable Navier–Stokes operator that has been linearized about a base flow. In this picture of transition, for suficiently large perturbations, such growth is understood to then bring the locally stable system out of its basin of attraction, inducing nonlinear behaviour that is associated with turbulence. An operator A is non-normal if $A A ^ { * } \neq A ^ { * } A$ where $A ^ { * }$ denotes the adjoint of A. The adjoint is defined with respect to an inner product, so we see that non-normality is only defined with respect to a particular inner product. Typically, for this type of study, the $\mathcal { L } _ { 2 }$ or perturbation energy norm is of interest. Flows that are linearized about a steady flow solution with shearing can yield highly non-normal operators. In the past 15 years, significant progress has been made in understanding system non-normality as a mechanism for energy amplification in shear flows (Butler & Farrell 1992b; Farrell & Ioannou 1993; Trefethen et al. 1993) leading to nonlinear breakdown in both linearly stable and unstable flows (Jovanovic & Bamieh 2004). 

There has been less investigation of the non-normal growth mechanisms in turbulent flow, with the notable exceptions of the early attempt by Butler & Farrell (1992b) to predict the spacing of near-wall streaks in turbulent flow and the more recent studies of del Alamo & Jim<sup>´</sup> enez (2006), Cossu, Pujals & Depardon (2009) and Willis, Hwang´ & Cossu (2009). These approaches exploit the properties of the linear operator to ‘select’ by preferential amplification the ‘optimal’ disturbance that leads to the largest amplification in some norm across all disturbances. A notable and somewhat limiting issue in the treatment of turbulent flow is the modelling of the interaction of the amplified disturbances with the ‘background’ turbulence. A solution introduced by Reynolds & Hussain (1972) has been to use the eddy viscosity formulation of Cess (1958); this relies on an a priori knowledge of the spatially averaged wall-normal variation of the mean Reynolds stress integrated across contributions from various wavenumbers. Other attempts have been made to use linear analysis to explain the dominant features of turbulent flow in terms of optimal transient modes in the initial value problem (Butler & Farrell 1992b; del Alamo & Jim<sup>´</sup> enez 2006; Cossu´ et al. 2009), response to stochastic forcing (Farrell & Ioannou 1998; Bamieh & Dahleh 2001) and system norm analysis (Meseguer & Trefethen 2003; Jovanovic & Bamieh 2005). In a recent work, Willis et al. (2009) have investigated the maximal response to harmonic forcing in pipe flow. Perhaps most importantly, it has been shown that both linear nonnormality (Henningson & Reddy 1994) and the terms that are linear in the turbulent fluctuation (Kim & Lim 1993) are required to sustain turbulence in infinite or periodic wall-bounded flows. del Alamo & Jim<sup>´</sup> enez (2006) made a direct comparison between´ a transient growth analysis of channel flow and earlier DNS results, and showed that while the analysis could predict two spanwise wavelengths that would experience large transient energy growth that were in good agreement with the computational and experimental observations, the corresponding predicted streamwise wavelengths were significantly too high. Cossu et al. (2009) performed a similar analysis in a turbulent boundary layer, modelling it as a parallel flow. The realization that turbulent wall flows can be linearly stable followed the work of Reynolds & Tiederman (1967), who demonstrated this for turbulent channel flow. In terms of the physical mechanisms and structure behind the energetic near-wall cycle, Schoppa & Hussain (2002) used linear perturbation methods to propose a streak transient growth mechanism capable of reproducing with good fidelity structures observed in a low-Reynolds-number DNS of a channel. Walefe (1997, 2001, 2003) followed a diferent approach, developing exact solutions of the Navier–Stokes equations that give rise to unstable coherent structures which they propose form the foundations of transitional flow and nearwall turbulence. Subsequently, there has been much interest in the importance and observability of travelling wave solutions of the Navier–Stokes equations, e.g. Wedin & Kerswell (2004) and Viswanath (2009) in pipe flow (which, of course, is also linearly stable). The ongoing work of Gayme et al. (2010) with a forced two-dimensional three velocity component model provides another attempt to predict the form of the turbulent mean flow. 

## 1.4. Selection of pipe flow for further study

Of the canonical turbulent flows, pipe flow has received considerable attention since Osborne Reynolds’ seminal work identifying the role of the Reynolds number in the flow behaviour. Pipe flow is also important to many obvious industrial applications. From an experimental point of view, providing that the development length is suficiently long for the flow to be considered to be fully developed, a pipe constitutes a well-defined, simple-to-generate geometry. As such, there is a wealth of experimental pipe flow data available for comparison, with the results from the Princeton/ONR Superpipe providing detailed information on the mean velocity (Zagarola & Smits 1998; McKeon et al. 2004), streamwise (Morrison et al. 2004) and wall-normal (Zhao & Smits 2007) fluctuations, and azimuthal correlations (Bailey et al. 2008; Bailey & Smits 2009) across three decades in Reynolds number. The results of Monty et al. (2007) at an intermediate Reynolds number have already been described in the context of the VLSMs. In addition, a recent DNS study by Wu & Moin (2008) explored the properties of the spatial velocity field at relatively low turbulent Reynolds number, while the POD analysis of Duggleby et al. (2007) categorized energetic propagating and non-propagating modes a posteriori, from full field information from a DNS at $R ^ { + } = 1 8 0$ . Lastly, the geometry of the pipe has the useful property of imposing a restriction on the azimuthal wavenumber to integer values only, which simplifies our analysis in the subsequent sections. 

## 1.5. Contribution

In this work we propose a simple analysis of the Navier–Stokes equations for incompressible, fully developed turbulent pipe flow. Subsequent steps permit the identification of the dominant forcing directions for given streamwise and spanwise wavenumbers and frequency, rather than the globally dominant directions. The resulting model describes the spatial distribution of turbulent energy in the threedimensional propagating velocity response modes that are most responsive to harmonic forcing. We ofer the model as a first step towards bridging the gap between statistical and structural interpretations of wall turbulence, since it provides qualitative information on both the temporal and spatial distributions of velocity associated with each response mode. We suggest that such a reconciliation of the difering observations of the same system would provide an important advance in the field. In what follows, we use the model to investigate an issue of intense current interest in the boundary-layer community: the radial extent, characteristics and scaling of VLSMs. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/72bcde8bec0c1622d1ea79919a104d59dc61acd8a21198d7fe38d7a428b53a5f.jpg)



<sup>Figure</sup> <sup>1.</sup> Schematic of pipe geometry and nomenclature.


## 2. A simple model for the spatio-temporal distribution of turbulent energy in pipe flow

In following analysis, we develop a formulation of the Navier–Stokes equations designed to examine the receptivity of turbulent pipe flow to forcing. In this way, we develop a framework that permits investigation of the form and likely magnitude of spatially and temporally harmonic propagating finite-amplitude fluctuations about the turbulent mean profile in pipe flow. 

## 2.1. Pipe flow equations and non-dimensionalization

The non-dimensional Navier–Stokes equations for fully developed incompressible pipe flow with constant viscosity are given by 

$$
\partial_ {t} \boldsymbol {u} = - \nabla p - \boldsymbol {u} \cdot \nabla \boldsymbol {u} + \frac {1}{R e} \nabla^ {2} \boldsymbol {u},\tag{2.1}
$$

$$
\nabla \cdot \boldsymbol {u} = 0.\tag{2.2}
$$

We follow the convention of Meseguer & Trefethen (2003), where the equations of motion are non-dimensionalized with respect to the pipe diameter and twice the bulk, volume-averaged velocity, $U _ { b u l k }$ (which in their study is equal to the laminar flow centreline velocity). Thus the Reynolds number in (2.2) can be defined as 

$$
R e = \frac {U _ {b u l k} D}{\nu}.
$$

Here D is the pipe diameter. We retain the boundary-layer terminology in fixing $y = 1 - r$ , and u, $\boldsymbol { v } ( = - \boldsymbol { v } ^ { \prime } )$ and w as corresponding to the streamwise, wall-normal and azimuthal velocities such that $\pmb { u } = ( v ^ { \prime } , w , u )$ , as shown in figure 1. 

## 2.2. Model development

We introduce a projection onto a divergence free basis: $\{ \xi _ { m } ( r ) \}$ in the radial direction, Fourier transformation in the homogeneous spatial directions and the Laplace transform in time. Implicitly, we are considering a pipe that is infinitely long or periodic in the axial direction. Assuming fully developed flow allows us to express the velocity field as the sum of harmonic modes. Then, 

$$
\begin{array}{c} \boldsymbol {u} (r, x, \theta , t) = \frac {1}{2 \pi \mathrm{i}} \sum_ {m, n} \int_ {- \mathrm{i} \infty} ^ {\mathrm{i} \infty} \int_ {- \infty} ^ {\infty} c _ {m k n \omega} \boldsymbol {\xi} _ {m} (r) \mathrm{e} ^ {s t - \mathrm{i} k x - \mathrm{i} n \theta}   \mathrm{d} k   \mathrm{d} s, \\ = \frac {1}{2 \pi \mathrm{i}} \sum_ {m, n} \int_ {- \mathrm{i} \infty} ^ {\mathrm{i} \infty} \int_ {- \infty} ^ {\infty} c _ {m k n \omega} \boldsymbol {\xi} _ {m k n \omega} (r)   \mathrm{d} k   \mathrm{d} s, \end{array}\tag{2.3}
$$

(2.4) 

with $s = \mathrm { i } \omega ,$ , so that only harmonic forcing and response is considered. Note that these harmonic modes constitute helical wave-like disturbances that propagate obliquely relative to the mean (axial) velocity, in the direction of the wavenumber vector. 

The wavenumbers $( k , n , \omega )$ are non-dimensional such that $k = k ^ { \prime } R$ , etc. The integration path for the Laplace transform is over the closed right half-plane, which is analytic in the case of pipe flow. In the inviscid limit special treatment for singularities on the imaginary axis would be required, but we do not consider this limit. 

We work with the spatial $\mathcal { L } _ { 2 }$ inner product throughout, 

$$
(a, b) = \int_ {x \in \Omega} a (x) b ^ {*} (x) d x.\tag{2.5}
$$

The basis functions are required to have the special properties 

$$
\left(\pmb {\xi} _ {a}, \pmb {\xi} _ {b}\right) = \delta_ {a b},\tag{2.6}
$$

$$
\nabla \cdot \pmb {\xi} (r) _ {m k n \omega} = 0.\tag{2.7}
$$

This is done to eliminate the pressure term. For notational convenience we make the definitions 

$$
\boldsymbol {u} _ {k n \omega} = \left(\boldsymbol {u}, \mathrm{e} ^ {- \mathrm{i} (\omega t - k x - n \theta)}\right),\tag{2.8}
$$

$$
\tilde {\pmb {u}} = \pmb {u} - \pmb {u} _ {0 0 0},\tag{2.9}
$$

$$
\boldsymbol {f} _ {k n \omega} = \left(- \tilde {\boldsymbol {u}} \cdot \nabla \tilde {\boldsymbol {u}}, \mathrm{e} ^ {- \mathrm{i} (\omega t - k x - n \theta)}\right).\tag{2.10}
$$

This finally yields equations for the fluctuations that are linear in ${ \pmb u } _ { k n \omega } .$ , and a base flow equation, 

$$
\mathrm{i} \omega \pmb {u} _ {k n \omega} = \mathcal {L} _ {k n \omega} \pmb {u} _ {k n \omega} + \pmb {f} _ {k n \omega}, \quad \forall (k, n, \omega) \neq (0, 0, 0),\tag{2.11}
$$

$$
0 = \boldsymbol {f} _ {0 0 0} - \boldsymbol {u} _ {0 0 0} \cdot \nabla \boldsymbol {u} _ {0 0 0} + \frac {1}{R e} \nabla^ {2} \boldsymbol {u} _ {0 0 0}.\tag{2.12}
$$

The unknown constant forcing $f _ { 0 0 0 }$ describes the maintenance of ${ \pmb u } _ { 0 0 0 }$ via the radial derivative of the Reynolds stresses, generated from interaction with the other velocity modes. We identify ${ \pmb u } _ { 0 0 0 }$ with the turbulent mean velocity profile, by definition. Similarly, $\scriptstyle f _ { k n \omega }$ describes the excitation of ${ \pmb u } _ { k n \omega }$ by the triadic interaction with other wavenumbers. We cannot solve these equations on a mode-by-mode basis without additional information because $\mathcal { L } _ { k n \omega }$ incorporates ${ \pmb u } _ { 0 0 0 }$ and $f _ { 0 0 0 }$ incorporates u˜. This is essentially an appearance of the closure problem. However, the reader will notice that the perturbation equation (2.11) is a linear system with an unknown forcing $\scriptstyle f _ { k n \omega }$ . This fact is central to our treatment. 

We avoid the closure problem for the base flow equation simply by knowing a priori the mean profile from experimental data. This allows calculation of $\mathcal { L } _ { k n \omega }$ and precludes the need for an eddy viscosity formulation normally required, e.g. by Reynolds & Hussain (1972), del Alamo & Jim<sup>´</sup> enez (2006), etc.´ 

While $f _ { 0 0 0 }$ can be simply calculated from the mean profile, we do not know the Reynolds stress at any other wavenumber combination, $f _ { k n \omega } .$ Our approach is not to make assumptions about this forcing, but to simply examine the response of (2.11) at individual $( k , n , \omega )$ triplets over the set of all possible harmonic forcings. 

The linear operator has the explicit form for pipe flow 

$$
\mathcal {L} _ {k n \omega} = \\ \left( \begin{array}{c c c} R e ^ {- 1} (\partial_ {r} ^ {2} + r ^ {- 1} \partial_ {r} - n ^ {2} r ^ {- 2} & 2 \mathrm{i} n r ^ {- 2} & 0 \\ - k ^ {2} - r ^ {- 2}) + \mathrm{i} k u _ {0 0 0} & & \\ - 2 \mathrm{i} n r ^ {- 2} & R e ^ {- 1} (\partial_ {r} ^ {2} + r ^ {- 1} \partial_ {r} - n ^ {2} r ^ {- 2} & 0 \\ & - k ^ {2} - r ^ {- 2}) + \mathrm{i} k u _ {0 0 0} & \\ - \partial_ {r} u _ {0 0 0} & 0 & R e ^ {- 1} (\partial_ {r} ^ {2} + r ^ {- 1} \partial_ {r} - n ^ {2} r ^ {- 2} \\ & & - k ^ {2}) + \mathrm{i} k u _ {0 0 0} \end{array} \right),\tag{2.13}
$$

where, as before, the states in u are the radial, azimuthal and axial velocities, respectively. 

We make the following observations: 

(a) Only integer n are permissible. 

(b) We expect downstream travelling waves such that k and ω are of the same sign: henceforth k, $\omega > 0$ 

While equation (2.11) is linear in ${ \pmb u } _ { k n \omega } ,$ and $\mathcal { L } _ { k n \omega }$ is identical to the operator obtained by linearizing around the turbulent mean velocity profile, no linearization has been performed. Nonlinear efects at other wavenumber–frequency combinations are retained through the action of the forcing $\scriptstyle f _ { k n \omega }$ 

The forcing $f$ acts perpendicular to $\mathbf { \delta } _ { \mathbf { u } , \mathrm { ~ \tiny ~ } }$ that is, $( f , \pmb { u } ) = 0$ . This can be interpreted as $f$ being conservative with respect to fluctuation energy, and so responsible for the transfer of energy in spectral space but not directly responsible for the extraction of energy from the base flow. A similar formulation to the current one, using this fact to derive a globally laminarizing control law, was described in Sharma et al. (2006). 

The decomposition fully describes the energetic interaction between the base flow and fluctuations ${ \pmb u } _ { k n \omega } ,$ for all $( k , n , \omega )$ , given a mean profile. That is, (2.11) and (2.12) are simply a harmonic decomposition of the full Navier–Stokes equations and, importantly, no other assumptions have been made at this point. 

Next, we proceed to analyse the response of $\mathcal { L } _ { k n \omega }$ at a particular wavenumber combination, subjected to the harmonic forcing $\scriptstyle f _ { k n \omega }$ 

## 2.3. Resolvent norms and model formulation

Equation (2.11) can be rearranged as 

$$
\pmb {u} _ {k n \omega} = (\mathrm{i} \omega I - \mathcal {L} _ {k n \omega}) ^ {- 1} \pmb {f} _ {k n \omega}.\tag{2.14}
$$

The operator $( \mathrm { i } \omega I - \mathcal { L } _ { k n \omega } ) ^ { - 1 }$ is called the resolvent and is the focus of our analysis. It provides a measure of the turbulent energy response that is possible for a given forcing. Some interpretation of the resolvent is given in Appendix A. 

For pipe flow, using (2.13) and for $( k , n , \omega ) \neq ( 0 , 0 , 0 )$ , the resolvent can be written as 

$$
\begin{array}{l} (\mathrm{i} \omega I - \mathcal {L} _ {k n \omega}) ^ {- 1} \\ = \left( \begin{array}{c c c} - A R e ^ {- 1} - \mathrm{i} k U + \mathrm{i} \omega & - B & 0 \\ B & - A R e ^ {- 1} - \mathrm{i} k U + \mathrm{i} \omega & 0 \\ \partial_ {r} U & 0 & - A R e ^ {- 1} - \mathrm{i} k U + \mathrm{i} \omega \end{array} \right) ^ {- 1}, \end{array}\tag{2.15}
$$

with $A = ( \partial _ { r } ^ { 2 } + \partial _ { r } / r - n ^ { 2 } r ^ { - 2 } - k ^ { 2 } - r ^ { - 2 } ) , B = 2 \mathrm { i } n r ^ { - 2 }$ and $U = u _ { 0 0 0 }$ . Equation (2.15) clearly highlights that the operator is not self-adjoint in the presence of $\partial _ { r } U$ . The shear is a source of non-normality under the energy norm, coupling the radial and axial velocity components. The $A / R e$ term will always be small for Reynolds number large enough for turbulent flow. One might expect large values of the resolvent norm under any of the following conditions: 

(a) in regions of high shear, where the $\partial _ { r } U$ is large; 

(b) at critical layers where $\omega / k = U ( y )$ , so the component of the normal speed of propagation of the wave in the streamwise direction is equal to the local mean velocity; 

(c) for stationary disturbances with $k = \omega = 0$ 

We note that this last condition of streamwise constant disturbances is the one that is returned as the global ‘optimal’ in the $H _ { \infty }$ norm. 

## 2.4. Most amplified forcing and response modes

We seek a decomposition of the resolvent at a particular wavenumber pair and frequency which ranks the response to forcing in some sense. We take the Schmidt decomposition (called the singular value decomposition in the discrete case) of the resolvent, namely 

$$
(\mathrm{i} \omega I - \mathcal {L} _ {k n \omega}) ^ {- 1} = \sum_ {j = 1} ^ {\infty} \boldsymbol {\psi} _ {j} (k, n, y, \omega) \sigma_ {j} (k, n, \omega) \boldsymbol {\phi} _ {j} ^ {*} (k, n, y, \omega),\tag{2.16}
$$

with an orthogonality condition 

$$
\int_ {y} \boldsymbol {\phi} _ {l} (k, n, y, \omega) \boldsymbol {\phi} _ {m} ^ {*} (k, n, y, \omega) d y = \delta_ {l m},\tag{2.17}
$$

$$
\int_ {y} \boldsymbol {\psi} _ {l} (k, n, y, \omega) \boldsymbol {\psi} _ {m} ^ {*} (k, n, y, \omega) d y = \delta_ {l m},\tag{2.18}
$$

and 

$$
\sigma_ {j} \geqslant \sigma_ {j + 1} \geqslant 0.
$$

The $\phi _ { j }$ and $\psi _ { j }$ form the right and left Schmidt bases for the forcing and velocity fields and the real $\sigma _ { j }$ are the singular values. This decomposition exists if there are no eigenvalues of $\mathcal { L }$ with zero real part and is unique up to a pre-multiplying unitary complex factor on both bases corresponding to a phase shift and up to the ordering of the $\sigma _ { j }$ values (Young 1988). 

This basis pair can then be used to decompose arbitrary forcing and the resulting velocity at a particular Fourier component 

$$
\boldsymbol {f} _ {k n \omega} = \sum_ {l = 1} ^ {\infty} \boldsymbol {\phi} _ {l k n \omega} a _ {l k n \omega},\tag{2.19}
$$

$$
\boldsymbol {u} _ {k n \omega} = \sum_ {l = 1} ^ {\infty} \sigma_ {l k n \omega} \boldsymbol {\psi} _ {l k n \omega} a _ {l k n \omega}.\tag{2.20}
$$

The energy of the same Fourier component of the resulting disturbance velocity is 

$$
E _ {k n \omega} = (\boldsymbol {u} _ {k n \omega}, \boldsymbol {u} _ {k n \omega}) = \sum_ {l = 1} ^ {\infty} \sigma_ {l k n \omega} ^ {2} a _ {l k n \omega} ^ {2}.\tag{2.21}
$$

Clearly the forcing shape that gives the largest energy at a particular frequency and wavenumber combination is given with $a _ { l k n \omega } = 0 , \ l \ne 1$ . This approach permits the investigation of the dependence of maximum energy amplification on the form of the forcing in the wavenumber and frequency domain. The singular value decomposition for a given wavenumber pair and frequency corresponds to full volume, three component forcing and response modes ranked by the receptivity of the linear Navier–Stokes operator. The velocity response must have the same k and n but not necessarily the same y distribution (spatial phase variation in y) as the forcing. 

By Parseval’s theorem, the energy integrated over frequency and wavenumber is equal to that integrated over the temporal and spatial domains (the spectral and physical spaces are isomorphic). As such, the $\mathcal { L } _ { 2 }$ norm of the resolvent is its leading singular value, $\sigma _ { 1 }$ . This means that the normalized harmonic forcing that gives the largest disturbance energy in the $\mathcal { L } _ { 2 } ( \varOmega \times [ 0 , \infty ) )$ sense is $f = \phi _ { 1 }$ , with a ‘gain’ of $\sigma _ { 1 }$ . The next largest arises from $f = \phi _ { 2 }$ and so on, at a particular wavenumber pair and frequency. The corresponding flow response modes are given by the related $\pmb { v } = \pmb { \psi } _ { 1 } , \pmb { \psi } _ { 2 } ,$ etc. For $\sigma _ { j }$ near zero, the forcing modes are not easily computed because they are efectively degenerate. However, for the leading singular values the mode shapes are extremely robust to numerical error. 

This decomposition permits analysis of what we call the ‘forcing and response modes’ associated with large responses of the flow. (Note that these modes are not eigenmodes.) In this sense, this decomposition analyses the receptivity of the flow to forcing. 

We introduce our first modelling assumption here, namely that because of the ranking of the response modes by their amplitude per unit forcing and the rapid decay of the magnitude of the singular values $\sigma _ { j }$ with increasing j (to be shown in § 3.1), a selection process occurs at each wavenumber–frequency combination, such that for a broadband forcing the forcing component in the direction corresponding to the first singular value is preferentially amplified. Therefore the first response mode with an amplitude proportional to the product of $\sigma _ { 1 }$ and $| \boldsymbol { f } _ { k n \omega } |$ should dominate (but not necessarily fully describe) the velocity field observed in the full flow at this $( k , n , \omega )$ 

In what follows, we focus our attention on the response modes associated with the first singular value for a range of wavenumber–frequency combinations $( k , n , \omega )$ and show that they agree very well with experimental observations and classical scaling concepts. We stress that our decomposition leads to a preferential selection of particular harmonic forcing perturbations at a given $( k , n , \omega )$ rather than the more usual selection of forcing perturbations over all possible disturbances associated with the identification of global optimal perturbations. We use this local selection in wavenumber/frequency space and physical arguments about the range of scales that are present in real flows to test the hypothesis that the first singular response modes are observed in experimental data and can help to explain several scaling concepts in wall turbulence. 

## 2.5. Computational approach

The computational analysis of the linear operator, ${ \mathcal { L } } ,$ , was performed using a modified version of the spectral code of Meseguer & Trefethen (2003). The code essentially provides the operator $\mathcal { L } _ { k n \omega }$ described above, evaluated at a number N of wallnormal grid points. For the particular problem under consideration here, the only modification to the linear operator used by Meseguer & Trefethen (2003) is the use of the turbulent mean velocity profile instead of the steady parabolic laminar base flow, as discussed above. We retain the same non-dimensionalization, namely using the centreline velocity for a laminar flow with an equivalent mass flux, the steady laminar flow pressure gradient and the pipe radius, a. This formulation is equivalent to using the bulk-averaged velocity, $U _ { b u l k } .$ , and pipe diameter, D, as velocity and length scales, which is more natural to the turbulent problem. Of course, because the turbulent velocity profile is blunter than a laminar one, the constant mass-flux constraint means that the non-dimensional turbulent centreline velocity will always be less than one. 

The form of the turbulent mean profiles was determined directly from experimental data obtained using Pitot probes in the Princeton/ONR Superpipe and reported by McKeon et al. (2004). This experimental data spans the Reynolds number range $3 1 \times 1 0 ^ { 3 } \leqslant R e \leqslant 3 5 \times 1 0 ^ { 6 }$ or $8 6 \bar { 0 } \leqslant R ^ { + } \lesssim 5 3 5 \times 1 \bar { 0 } ^ { 3 }$ . Interpolation between Reynolds numbers was performed in a process equivalent to assuming a Reynolds-numberindependent form of the velocity profile. Issues of numerical stability limit our study to Reynolds numbers $R e \leqslant 1 0 \times 1 0 ^ { 6 }$ , well below the estimate of the Reynolds number at which the Superpipe results may show some efect of wall roughness, $R e \sim 2 4 \times 1 0 ^ { 6 }$ (Shockling, Allen & Smits 2006). Note that this Reynolds number range also spans conditions that have been described as representative of high-Reynolds number turbulence in pipe flow by McKeon & Morrison (2007) $( R ^ { + } \gtrsim 5 \times 1 0 ^ { 3 } )$ and in boundary layers by Hutchins & Marusic (2007b) $( \delta ^ { + } \gtrsim 4 \times 1 0 ^ { 3 } )$ 

The very sensitivity of the operator to perturbations that leads to large energy amplification can also cause numerical stability issues associated with the spatial resolution employed in the pipe cross-section. Judicious choice of this resolution, N, is required. This is briefly discussed in Appendix B. 

## 2.6. A model of spectral energy distribution

While the concept of the Navier–Stokes equations as a linear system with a nonlinear feedback forcing was been raised in a control theory context by Sharma et al. (2006), the emphasis here is more towards the receptivity of the flow, as explored for laminar pipe flow by Sharma & McKeon (2009). This approach is comparable to the ‘mother–daughter’ scenario of Boberg & Brosa (1988), where a linear but non-normal process allows small disturbances to feed more energetic disturbances that can dissipate the gained energy. Nonlinear efects then transfer some of this energy to the smaller initial disturbances. The understandings difer to the extent that the ‘mother–daughter’ scenario considers the evolution of structural perturbations, and naturally leads to the transient growth problem of Butler & Farrell (1992b) and others. In contrast, the current work considers the gain response to harmonic forcing, naturally leading to a linear input–output analysis. 

The velocity response modes under investigation propagate in the streamwise and spanwise directions, i.e. as helical waves propagating in the direction of the wavenumber vector, with a complex amplitude distribution in the wall-normal direction. As such they are strongly analogous to the spectral decomposition of spatial and temporal velocity fields from experiments and simulations. Their wavelike nature implies that the propagation (phase) velocity of each mode is given by $U _ { w } = \omega / K$ , where $K = ( k ^ { 2 } + \dot { n } ^ { 2 } ) ^ { \dot { 1 } / 2 }$ , with streamwise component $U _ { x } = \omega / k$ . In global terms, we expect that this analysis will give some insight into the spectral energy storage. 

If all wavenumber–frequency combinations and all singular values, with the appropriate amplitudes, were considered, this analysis would by definition lead to the Reynolds stress tensor required to maintain each of these response modes (the $f _ { k n \omega } \mathbf { s } )$ and the turbulent mean velocity profile at a particular Reynolds number. 

<table><tr><td><eq>Re_{D}</eq></td><td><eq>75 \times 10^{3}</eq></td><td><eq>150 \times 10^{3}</eq></td><td><eq>410 \times 10^{3}</eq></td><td><eq>1 \times 10^{6}</eq></td></tr><tr><td><eq>R^{+}</eq></td><td>1800</td><td>3300</td><td>8500</td><td>19700</td></tr></table>


<sup>Table 1.</sup> Reynolds numbers considered and associated Karm´ an numbers,´ $R ^ { + }$


This would be equivalent to decomposing the full velocity field in the manner of a DNS. Equally, more complicated forcing structure could be decomposed using the orthogonal response modes at diferent $( k , n , \omega )$ combinations. We focus here on the first singular response mode to investigate whether the structure of the resolvent (i.e. the linear Navier–Stokes operator) allows for a simplified understanding of the dominant structure at a given $( k , n , \omega )$ 

In this spirit, the current work explores the $( k , n , \omega , R e )$ parameter space and validates the eficacy of our simple model, by demonstrating that it is capable of capturing classical and empirically observed features of wall turbulence, such as inner and outer scaling, ‘attached’ and ‘detached’ motions and Reynolds number trends. 

## 3. Predictions of the model

In this section, we describe the characteristics of the response modes that are predicted by the preceding analysis. We consider only propagating, helical modes in the streamwise direction, with $k \neq 0 , n \neq 0 .$ , and the Reynolds numbers listed in table 1 with the associated Karm´ an numbers,´ $R ^ { + }$ 

We begin by presenting results for Reynolds numbers $R e = 7 5 \times 1 0 ^ { 3 }$ and $R e =$ $4 1 0 \times 1 0 ^ { 3 } \ : ( R ^ { + } = 1 8 0 0$ and 8500, respectively). The former is representative of the upper range accessible with current DNS techniques, while the latter Reynolds number is high enough to ensure characteristics of ‘high-Reynolds-number’ turbulence (McKeon et al. 2004; McKeon & Morrison 2007; Hutchins & Marusic 2007b). In addition, we know the velocity profiles and the streamwise and wall-normal turbulence statistics and spectra from the Superpipe at, or close to, these conditions. This facilitates future comparison with experimental results (McKeon et al. 2004; Morrison et al. 2004; Zhao & Smits 2007). From these data, we expect that the streamwise turbulent energy across the pipe cross-section lies within the range $5 \times 1 0 ^ { - 2 } \lesssim k \lesssim 5 \times 1 0 ^ { 2 }$ 

## 3.1. Response mode shapes

Figure 2 compares the velocity distributions for response modes with the wavenumber–frequency combinations $( k , n , \omega ) = ( 2 , 2 , 1 )$ and (1, 10, 0.4) for the first three singular values, $\sigma _ { i }$ with $i = 1 , 2 , 3$ . Clearly the higher-order modes generate velocity distributions with more local maxima in the radial direction, apparently i maxima in the streamwise velocity for the modes shown. The first mode is dominated by the streamwise component for both of these modes. The singular value Bode plot for $( k , n ) = ( 1 , 1 0 )$ in figure 3 shows that the first singular value has a distinct variation with ω and is significantly larger than the other singular values. This suggests that the response mode corresponding to $\sigma _ { 1 }$ is likely to dominate in observations of real pipe flow. By comparison, Bailey & Smits (2009) have shown that more than 75 % of the streamwise energy is contained in the first radial POD mode for $R e = 1 5 0 \times 1 0 ^ { 3 }$ Thus we focus on the first mode. 

The literature associated with the amplification properties of the linearized Navier– Stokes operator indicates that maximum amplification of energy is obtained for the streamwise constant perturbations. While we do not consider a k of exactly zero in this study, we do observe similar trends as $k  0 .$ . However we focus instead on the form of the velocity modes with streamwise wavenumber in the range corresponding to that observed in experiments. 


(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/3215c01c454c9cb57856d97efca1a871c07f2ff0a00fe0bc352220027bfceab1.jpg)



(b)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/147d41be03b61513858f532cce9ec2d14e844927917ddf5ccb51170233e41f40.jpg)



(c)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/278415111f34eee574993636a3a80907c8b6b5f495b90d4eb8eba62b269a8522.jpg)



<sup>Figure 2.</sup> Radial variation of the absolute amplitude of each component of velocity for the response modes with $( k , n , \omega ) = ( 2 , 2 , 1 )$ (black) and (1, 10, 0.4) (grey) and associated with the first three singular values, $\sigma _ { i }$ , at $R e = 7 5 \times 1 0 ^ { 3 }$ . (—): abs(u); (− −): abs(v); (· · · ): abs(w), and $i = 1 , 2 , 3$ in (a), (b), (c), respectively.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/817163248eab5590fcac587ecc138608d46805e47650346122cd9131f54fb074.jpg)



<sup>Figure 3.</sup> Variation of singular values $\sigma _ { i }$ with mode number, $i ,$ for $( k , n ) = ( 1 , 1 0 )$ and $R e \ : = \ : 7 5 \times 1 0 ^ { 3 }$ . For a wide range of frequencies, the first singular value is an order of magnitude larger than the second.


Figures 4–6 show the distribution of turbulent energy in the pipe for the first response mode with wavenumber pair $( k , n ) = ( 1 , 1 0 )$ at $R e = 7 5 { \times } 1 0 ^ { 3 }$ , an arrangement which will be shown later to be representative of a VLSM. The streamwise wave speed, $U _ { x } = \omega / k ,$ , is increased from 0.2 to 0.6 from figures 4–6. Note that because $( k , n )$ is held constant between the figures the wave speed in the streamwise direction, $U _ { x }$ , is a constant fraction of the normal wave speed, and that the choice of $k \neq 0 , n \neq 0$ leads to helical mode shapes. Thus the top panels give full information on the complex amplitude of the response mode in each velocity component, observed in terms of the response mode amplitude and the radial phase variations. As expected, the energy for the lower wave speed is concentrated close to the wall, in the inner (wall) region, while for the faster wave the energy is centred in the core of the pipe. This trend is to be expected from Taylor’s frozen turbulence hypothesis if propagating waves are a realistic feature of wall turbulence. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/7f0c5f9479368bd9636a846b2ee57c2fb914687ddb563762d6e12e3a7c868c2e.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/44422ac0bb4c0363f194c671d0645e14d9aed2a327c8e8a1b7b090b7a9d7b3d8.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/39a056d0237732065aa52568e3a31d5cb1138ff7f52f99620b3e4fdc1eb7b282.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/4e8bf8d57d4615a5694c858c5499ab674658aed7817c2defb1dbc4551ad76cb4.jpg)



<sup>Figure 4.</sup> Structure of the velocity field for the first response mode with $( k , n , \omega ) = ( 1 , 1 0 , 0 . 2 )$ at $R e = 7 5 \times 1 0 ^ { 3 }$ . (a–c) u, v and w in the streamwise-wall-normal plane; (d) response mode kinetic energy in the wall-normal-azimuthal plane.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/2b959143d11d4cd679adf67d413933a1037c1c4161126c4555fad6f3e730e29c.jpg)



(b)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/2c7deb8c4da2a3320196e9fc887c9116cf0ebd225d175a631a015439a298ebae.jpg)



(c)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/387f184918b0363e9ed4a5eae4750a92ce6d8728827f63ce525b9c52db55b54a.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/f004459d1d6b1b816ef795b9e4f7042750914af2dad49f31b7399ed862b99aa5.jpg)



<sup>Figure 5.</sup> Structure of the velocity field for the first response mode with $( k , n , \omega ) = ( 1 , 1 0 , 0 . 4 )$ at $R e = 7 5 \times 1 0 ^ { 3 } . ~ ( a - c )$ u, v and w in the streamwise-wall-normal plane; (d) response mode kinetic energy in the wall-normal-azimuthal plane.


For this wavenumber pair, the forcing elicits an energetic response that is concentrated in the streamwise component for each ω, with the relative magnitudes of the azimuthal and radial velocities being frequency-dependent. The response modes for the lower two frequencies shown in figures 4 and 5 have footprints which reach down to the wall. Increasing ω leads to a ‘lifting’ of the streamwise and spanwise velocity components, manifested as a distinctive inclination to the wall of velocity isocontours. At the highest of the three frequencies, shown in figure 6, the mode detaches from the wall and the streamwise and spanwise velocities display something more like a two-level structure than inclined isocontours. For all three frequencies, the wall-normal component shows little phase variation with wall-normal distance. The shapes imply a structure of rolls with streamwise and azimuthal vorticity and strong streaks in the streamwise velocity. Note that the velocity distributions shown in figure 5 are in excellent agreement with the conditionally averaged very large scale structures determined for channel flow by Chung & McKeon (2010) and the streamwise coherence inferred from two-point correlations with a reference point outside the immediate near-wall region in a high-Reynolds-number boundary layer by Guala et al. (2010b), suggesting that coherence of this kind may have particular importance for wall turbulence. Section 3.4 investigates response modes with self similar energy distributions in $y ^ { + }$ and $y / R$ for various wavenumber pairs. We call these ‘inner’ and ‘outer’ scaling modes, respectively. 


(b)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/13ff53e7f0bf2676eb8b2fbbe0728ae5a325d0c65eb0d0931f2239c9250e416c.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/cd30c6d9dbc1b947ec0c224a29bce833f8dbbbc136933739e663a8a3b6ca7921.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/3d22414a410d1502b56b30ce761322c38fc8d3260f6ea0580b938899d946dd57.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/d9fceaaaf76470f7071b29fb5f05b2ae2bfcceb24ceefc8dae7a0531302a8846.jpg)



<sup>Figure 6.</sup> Structure of the velocity field for the first response mode with $( k , n , \omega ) = ( 1 , 1 0 , 0 . 6 )$ at $R e = 7 5 \times 1 0 ^ { 3 }$ . (a–c) u, v and w in the streamwise-wall-normal plane; (d) response mode kinetic energy in the wall-normal-azimuthal plane.


## 3.2. Efect of streamwise wave speed on the radial distribution of perturbation energy

In this section we explore the influence of frequency, or more accurately the streamwise wave speed normalized with the centreline velocity, $U _ { x } / U _ { C L }$ , on the response mode shapes. We use physical arguments concerning the range of wavenumbers and frequencies observed in real flows to guide our selection of (k, n, ω), focusing on combinations that correspond to dominant features in turbulent pipe flow. 

The wavenumber combination corresponding to $( \lambda _ { x } ^ { + } , \lambda _ { z } ^ { + } ) \approx ( 1 0 0 0 , 1 0 0 )$ with an appropriate phase velocity $U _ { x } ^ { + } \sim 1 0 .$ , appears to be representative of the signature of the near-wall cycle in many studies across a range of Reynolds numbers and flow types (e.g. Krogstad, Kaspersen & Rimestad 1998). In other words, it is a universal feature of wall turbulence responsible for the near-wall peak in the streamwise intensity and the wall shear stress. The radial distribution of energy in each velocity component for the response mode with $( k , n ) = ( 2 \pi R ^ { + } / 1 0 0 0 , 2 \pi R ^ { + } / 1 0 0 )$ and streamwise wave speed in the range $0 . 1 \leqslant U _ { x } / U _ { C L } \leqslant 1$ at $R e = 7 5 \times 1 0 ^ { 3 }$ is shown in the composite contour plots of figure 7. The changing amplitudes in each velocity component as the wave speed increases reflect the distribution of energy between components and across the radius for diferent frequencies. The distributions are normalized to give an identical total kinetic energy for each response mode. 

The figure shows that for low wave speeds the contours of constant energy lie at approximately the same wall-normal locations for all three velocity components and that the mode reaches down to the wall (i.e. is ‘attached’). The distribution of energy between the velocity components is consistent with the well-known picture of streamwise rolls and streaks, in which the wall-normal and (double-peaked) azimuthal velocities have a similar order of magnitude and give rise to much larger fluctuating streamwise velocities. This type of distribution is observed for this wavenumber combination at all Reynolds numbers considered, although high radial resolution is required to capture it accurately as the Reynolds number increases. This is directly related to the experimental and computational dificulties associated with an increasing range of scales. 

A transition occurs in the radial and component-wise energy distribution with increasing wave speed. Instead of the near-wall roll/streak pattern described above, the peak energy moves away from the wall and the energy is concentrated in the core region. The wall-normal and streamwise energies are of similar order of magnitude (larger than the azimuthal component of energy), such that the velocity distribution is more indicative of concentrated spanwise vorticity. 

Aspects of the results for this wavenumber pair are representative of the trends observed for other response modes. The location of the peak energy associated with a particular mode moves slowly away from the wall as the frequency is increased. For a range of low ω $( U _ { x } )$ , the energy is concentrated in the near-wall region. For higher $\omega ,$ the energy is concentrated in the core of the pipe. The shape of the velocity profile near the wall constrains the range of possible mode shapes. Specifically, it constrains the radial extent of the mode, providing a minimum distance from the wall 

(b) 


(c)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/0ec2a1341911c168bab1b2e22013d75fcfb9356ff132e3aebc3ec110f4ed6819.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/6a2e2e8526f86071dcce7fa74371ddaa23209a42504a1765cd0845a6d72de895.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/1ebb376fbb0f903ef4617c11563c7d2757407e5aeb20459dc85eabd4a13ad9c1.jpg)



<sup>Figure 7.</sup> Variation of energy distribution with phase speed for $\lambda _ { x } ^ { + } = 1 0 0 0 , \lambda _ { z } ^ { + } = 1 0 0$ at $R e = 7 5 \times 1 0 ^ { 3 } \ : ( R ^ { + } \sim 8 5 0 0 )$ . (a) u; (b) v; (c) w.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/debadc234e7df4c7bbc7fb29b82d8a419aadf46c52ac9f9d3e5947509beb93c6.jpg)



<sup>Figure 8.</sup> (a) Variation of location of peak streamwise perturbation amplitude with streamwise phase speed for response modes with $( k , n ) \ = \ ( \mathrm { { 1 } } , 1 0 ) . \ ( \mathrm { { \longrightarrow } } ) \colon { R e } \ = \ 7 5 \times 1 0 ^ { 3 } .$ $( -- ) \ R e = \hat { 4 } 1 0 \times 1 0 ^ { 3 }$ . The dashed grey lines show the turbulent mean velocity profiles at each Reynolds number. (b) Variation of resolvent norm with streamwise phase speed.


for the energetic peak in the streamwise stress. For example, in figure 7, this occurs at $y ^ { + } \simeq 1 0$ . The wall-normal distance to the peak is Reynolds number dependent. 

## 3.3. Comparison of streamwise wave speeds and local mean velocity

In the following discussion, we take the wall-normal location of the streamwise energy peak to be representative of a nominal response mode centre. This allows comparison between the streamwise component of wave speed and the local mean velocity. From figure 7, we expect that these will not always be equal. Figure 8 shows the variation of peak energy location with streamwise phase speed, for $( k , n ) = ( 1 , 1 0 )$ and Reynolds numbers of $7 5 \times 1 0 ^ { 3 }$ and $4 1 0 \times 1 0 ^ { 3 }$ . Whilst there is a region in the core of the pipe where the wave has a streamwise wave speed that is similar to the local mean velocity at the peak of the streamwise energy, close to the wall there is a significant deviation between the two velocities. This implies that our assumption that the response mode is centred at the streamwise energy peak is incorrect near the wall, or that these modes do not obey Taylor’s hypothesis, or that the modes will not be observed in the flow. In order to distinguish between the distinct behaviour near to and very far from the wall, we designate the former ‘wall response modes’ and the latter ‘critical response modes’, for reasons that will become clearer in § 4. At the transition between the two there will be a response mode with the characteristics of both wall and critical response modes. Figure $8 ( b )$ shows that the first singular value for this wavenumber pair increases with Reynolds number, at least in the region far from the wall (high values of ω). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/49e89d776f7e202396bdf44334091183e06ad38b29e98a1d9000dc7aea7fea0a.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/29e5ea4de687653c4e3942c77f8972357b37275d6e6d0632294fa21af39b81ed.jpg)



(c)



(d)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/8933e4d2663ca8cc37049b4544f9b46d549b6371a35f6e3902d762d0a0bc6f75.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/42df6cabcae72acb8d80e2c8fc17e5241a66b114d6383bced6c0ff34b0c23500.jpg)



<sup>Figure 9.</sup> (a, c) Variation of location of response mode peak amplitude with spanwise wavenumber. $( a , \ b ) \ \lambda _ { x } ^ { + } \ \approx \ 1 0 0 0$ and $\lambda _ { z } ^ { + } = 1 0 \dot { 0 } \ ( - ) , \ 5 0 \ \widetilde { -- } ) , \ 3 0 \ \widetilde { \therefore } \cdot \cdot )$ and 10 (· − ·) at $R e \ : = \ : 7 5 \times 1 0 ^ { 3 }$ . (c, d) k = 1 and n = 10 (—), 100 (−−), 200 (· · · ) and 400 (· − ·) at $R e = 4 1 0 \times 1 0 ^ { 3 }$ . The dashed grey lines show the turbulent mean velocity profiles at each Reynolds number. (b, d) Variation of resolvent norm with streamwise phase speed.


Figure 9 shows the influence of azimuthal wavenumber on the streamwise wave speed corresponding to the peak in streamwise energy, for a response mode representative of the near-wall cycle at $R e \ : = \ : 7 5 \times 1 0 ^ { 3 }$ and another mode with $( k , n ) = ( 1 , 1 0 )$ at $R e = 4 1 0 \times 1 0 ^ { 3 }$ , respectively. For azimuthal wavenumbers that are not ‘too large’, both cases show critical modes in the core of the pipe over a $y ^ { + }$ range that increases with increasing n, with wall modes observed closer to the wall and a transition region in between. However, when the azimuthal wavenumber becomes suficiently large, only wall modes are observed. Then, the peak energy remains at an approximately constant wall-normal location independent of wave speed and the response mode shape is self-similar with decreasing wave speed. In this case, the corresponding singular value is small and almost independent of streamwise wave speed. This dependence on azimuthal wavenumber occurs for all wavenumber– frequency combinations, showing that there is a limited range of $( k , n )$ aspect ratios (long in the streamwise direction) that lead to the observation of critical response modes. 

Wherever the streamwise wave speed is equal to the prescribed local mean velocity, the behaviour approaches that of a ‘critical’ layer. Very large amplitude, spatially and temporally periodic waves have been observed in various shear flows (Maslowe 1986) and explained in the context of critical layers. 

Examination of the resolvent (defined in (2.15)) shows that the system response approaches singular for a phase velocity close to the local mean $( \omega / k \sim U )$ and for high Reynolds number. That is, the flow approaches a state where it supports neutrally stable modes, corresponding to an eigenvalue approaching the imaginary axis. Comparison between figures $9 ( b )$ and $9 ( d )$ shows that the resolvent norm is orders of magnitude larger for such critical modes. This phenomenon is explored further in § 4.2. 

## 3.4. Inner and outer scaling response modes and the efect of Reynolds number

By carefully selecting the streamwise wave speed, we observe scaling behaviour that is surprisingly consistent with that seen in experimental velocity spectra. It is understood that the velocity spectra at high wavenumbers near the wall collapse when scaled on inner units, while the lack of collapse of the intensities arises from the influence of larger scales (Metzger & Klewicki 2001). Similarly, the intensities approach collapse in the core of the pipe as the Reynolds number is increased (McKeon & Morrison 2007). The response modes approach self-similarity when scaled on the classical inner or outer scales. 

Figure 10 shows the $( u , v , w )$ mode shapes for the wavenumber–frequency combination identified above as being representative of the near-wall cycle, $( k , n ) \approx$ $( 2 \pi R ^ { + } / 1 0 0 0 , 2 \pi R ^ { + } / 1 0 0 )$ , with streamwise wave speeds equal to $U _ { x } ^ { + } = 1 0$ and 20. The former velocity is known to correspond to the convection velocity of near-wall structure, while the latter velocity will only correspond to the inner scaling region for suficiently high Reynolds number, when the latter velocity occurs below the outer edge of the log region in the mean velocity. 

Figure 10 shows that these response modes become self-similar when scaled in inner units across nearly two decades in Reynolds number and that they are ‘attached’ in the sense that their footprints reach down to the wall. Remarkably, the peak energy in the streamwise u component for the lower wave speed of $1 0 u _ { \tau }$ is at the appropriate wall-normal location, $y ^ { + } \approx 1 5 { - } 2 0$ , obtained from experimental and computational observations of the near-wall cycle. The increase in the maximum power occurs because the response modes are co-located in plus units, so their extent decreases in dimensional units as the Reynolds number increases, and the total perturbation energy in each mode is normalized to one. That is, the results for $U _ { x } ^ { + } = 1 0$ show good collapse to a single curve when the values on the abscissae are divided by $R ^ { + }$ There is an upper limit to the range of Reynolds number that can be considered due to numerical resolution. This is discussed in Appendix B. However the Reynolds number trend appears to be quite clear. 


(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/6eea8cdfcf4d7ff3b3d10d557041023bf9343d10d2745bb9c6026aff898ec8d1.jpg)



(b)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/f3a6e976f8538f2576248ffc8d3144ce913fcb0ae336b7d4bbc400bea9d8a5e2.jpg)



(c)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/ba83accc60f0cfc5734bfa72c608cd3dddfb315d96dda22e30034c9882ea7b6a.jpg)



(d)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/faf9ecff54ebf8158cfe39fcc01898804346e3e13f58d5e46b411413c84baef9.jpg)



(e)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/beabb58e3d847a077316f0f56f3bab61bf9c465c4639f49f44fd35b830c835db.jpg)



(f)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/8b540bc1832c80253f1e021bdb946ae1466404f8955c9bd3ec3909dc0939ea6b.jpg)



<sup>Figure 10.</sup> Energy distribution over the pipe radius for $( k , n ) = ( 2 \pi R ^ { + } / 1 0 0 0 , 2 \pi R ^ { + } / 1 0 0 )$ , or equivalently, $( \lambda _ { x } ^ { + } , \lambda _ { z } ^ { + } ) \approx ( 1 0 0 0 , 1 0 0 )$ . The equivalence is not exact due to the restriction of integer azimuthal wavenumber. $( a , c , e )$ Streamwise wave speed $U _ { x } ^ { + } = 1 0 ; ( b , d , f ) \ U _ { x } ^ { + } = 2 0 $ Reynolds numbers: $( \longrightarrow ) 7 5 \times 1 0 ^ { 3 } , ( \mathrm { -- } ) 1 5 0 \times 1 0 ^ { 3 } , ( \cdots ) 4 1 \bar { 0 } \times 1 0 ^ { 3 }$ and $( \cdot - \cdot ) 1 \times 1 0 ^ { 6 }$


A similar result can be obtained for response modes that are located in the core of the pipe, i.e. they are expected to scale on outer variables. Figure 11 shows the $( u , v , w )$ mode shapes for $( k , n ) = ( 1 , 1 0 )$ and constant velocity defects, $U _ { C L } ^ { + } - U _ { x } ^ { + }$ The approach to similarity with increasing Reynolds number is slow, in agreement with the scaling of the integrated turbulence intensities (McKeon & Morrison 2007), with the wall-normal component collapsing earliest. 

We see that a straightforward analysis of the resolvent, a linear operator, produces response mode shapes that agree with known scaling remarkably well. In one respect this simply reflects the self-similarity of the mean velocity profile near the wall, in the sense that the response modes are a result of the local shape of the velocity profile, which does not vary in inner units once the Reynolds number is suficiently high. However the recovery of this result underlines the utility of the model for describing turbulent flow. A more formal justification for the scaling will be given in the discussion presented in $\ S 4 .$ 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/1143610f7ca65590e939b900d756d1dd2dee1cda4c9f7c3f5a0b5754365c65f8.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/525d58734183991ff99faa2341c522f7f0a7fce272696ae915f0e30afc780970.jpg)



(c)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/3f1a482c25aeac6adad9840ee168ec52afb5bd44f1d9fa9054c16dbb9073d743.jpg)



(d)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/fdede5bd8ea01fd2c65e0521da3d9a45c92fa9d486d6cf58c720bcf33122d752.jpg)



(e)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/f76ae3c2b22f69829b08872a3b02961708f75ff3f31f4f95e067ed70b9dc06b0.jpg)



(f)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/c1b27fe8372ec8f6842d5368da9934ad85537818646bacda0cdd2be9b65ec037.jpg)



<sup>Figure 11.</sup> Energy distribution over the pipe radius for $( k , n ) = ( 1 , 1 0 ) . ( a , c , e )$ Distribution for streamwise wave speeds such that the velocity deficit is $U _ { C L } ^ { + } - U _ { x } ^ { + } = 4 ; ( b , d , \dot { f } )$ distribution for a velocity deficit of $U _ { C L } ^ { + } - U _ { x } ^ { + } = 2 .$ . Reynolds numbers: $( \longrightarrow ) 7 5 \times 1 0 ^ { 3 } , ( \mathrm { -- } ) 1 5 0 \times 1 0 ^ { 3 } , ( \cdots )$ $4 1 0 \times 1 0 ^ { 3 }$ and $( \cdot - \cdot ) 1 \times 1 0 ^ { 6 }$


As evidenced by the failure of inner scaling to collapse experimental observations of the integrated streamwise energy near the wall, the transition from inner to outer scaling is complex and the range of response modes exhibiting inner and outer scaling at a given flow condition is a function of the Reynolds number. We explore this regime further in the next section. 

## 3.5. The very large scale motions and transition from inner to outer scaling

The existence of inner and outer scaling response modes in our model is consistent with the classical turbulence scaling picture, in which viscous and outer scales are suficient to describe the turbulent behaviour in the inner and outer regions of the flow. However, as described above, recent work suggests that there is some outer influence on the inner structure. For instance, Metzger & Klewicki (2001) and Hutchins & Marusic (2007b) show that the amplitude of the near-wall peak in streamwise energy weakly depends on Reynolds number. We consider here a possible origin for this efect, focusing on the transition between inner and outer scaling of the velocity modes. 

A concatenation of experimental results in wall turbulence in general, and specifically in pipe flow, have shown that a streamwise wavenumber $k = 1$ is representative of the VLSM phenomenon (Kim & Adrian 1999; Morrison et al. 2004; McKeon & Morrison 2007; Monty et al. 2007; Hutchins & Marusic 2007a) although the recent study of Monty et al. (2009) suggests that the exact details vary from flow to flow. The appropriate spanwise wavenumber is less clear; the spanwise measurements in pipe flow of Monty et al. (2007) suggest $\lambda _ { z } \approx 0 . 5 R \ ( n \sim 1 2 )$ , while the POD analysis and correlations of Bailey et al. (2008) indicate that lower values, $n \sim 3 .$ , are more realistic for the VLSMs. We investigate $n = 1 0$ as a compromise that follows the expected critical-layer aspect ratio discussed in § 4 and is in reasonable agreement with the work of both Monty et al. (2007) and Bailey et al. (2008). 

The variation of response mode shape for $( k , n ) = ( 1 , 1 0 )$ with increasing phase speed is shown in figure 12 for $R e = 4 1 0 \times 1 0 ^ { 3 }$ . We have defined a response mode as ‘critical’ when the streamwise wave speed reaches the local mean velocity at the peak response mode energy. The variation of this position with Reynolds number for the wavenumber pair related to the VLSM is illustrated in figure 8. In this case the response mode first becomes critical when $U _ { x }$ is a constant fraction of the centreline velocity, namely $U _ { x } / U _ { C L } \approx 2 / 3$ , independent of Reynolds number. This relationship suggests that for the critical modes the appropriate scaling velocity is the centreline velocity, rather than the friction velocity. This was also proposed by, among others, Jimenez´ et al. (2004), who observed that the so-called ‘global’ modes in channel flow simulations appeared to convect with a velocity equal to $0 . 5 U _ { C L }$ 

The foregoing section has demonstrated that the simple framework presented here for pipe flow is capable of reproducing several features of wall turbulence, from a self-similar distribution of energy for small scales near the wall to a large-scale velocity distribution that is reminiscent of recently observed conditional averaged structure in channels (Chung & McKeon 2010), two-point correlations in medium and high-Reynolds-number boundary layers (Guala et al. 2010b) and energetic POD modes in pipe flow (Duggleby et al. 2007). In a broad sense, the singular value decomposition selects the response mode shape at each $( k , n , \omega )$ combination that is ‘most likely’ to be observed based on receptivity to forcing at that combination, or ‘optimal’ in a sense analogous to that of earlier initial value studies. The amplitude of the response is set by the amplitude of the forcing, which is determined by other (k, n, ω) combinations such that the ensemble of response mode shapes, and specifically the Reynolds stress distribution, is consistent with the base mean flow. Note that a canonical spectral analysis records the integral energy over all modes with the same wavenumbers, so there is not a one-to-one relationship between the information given by the diferent bases corresponding to the one-dimensional power spectrum and the analysis performed here, except in an integral sense. 

## 4. A wall and critical-layer framework

In this section, we show that the simple model presented in § 2 predicts the location of the peak in streamwise turbulent energy associated with a wavenumber pair representative of a VLSM-type motion. We then develop an asymptotic analysis of the linear Navier–Stokes operator in the turbulent case and show that it leads to wall and critical-layer scaling. These concepts are probably more familiar to the reader in 

(a) 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/51bf62e4d0b747da06fcc5e0272f404dc8a0b17ca4a0b304ab20cb44559309d3.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/991533563a39803f2f998c87891762259ee244d6c899b7e1809cfd827ad808a9.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/8fa2121dbacbdab9e92b2ab7c28dd7b008c3de14e7ce9565f5f940f17c0e86e9.jpg)



<sup>Figure</sup> <sup>12.</sup> Efect of phase speed on energy distribution for (k, n) = (1, 10) at $R e = 4 1 0 \times 1 0 ^ { 3 }$ $( R ^ { + } \sim 8 5 0 0 )$ . (a) u; (b) v; (c) w.


the context of laminar, linearly unstable flows, so we present the results with this in mind. 

## 4.1. Scaling of the very large scale motion energy peak

We have observed that the peak energy in the streamwise velocity component for the first critical mode with $( k , n ) = ( 1 , 1 0 )$ occurs for $y / R < 0 . 1$ for all the Reynolds numbers considered here. (This can also be seen in figures 8 and 12.) Thus it is clear that the first critical mode occurs within the log region, at least for suficiently high Reynolds numbers. (Note that a logarithmic profile will give a reasonable approximation for the local velocity at the lower Reynolds numbers, even if the profile does not correspond to an overlap region that is independent of Reynolds number.) Based on this velocity scaling, the location of the energy peak associated with this response mode can be predicted using similarity of the mean velocity in both the inner and core regions, in the form of a logarithmic profile in the overlap region and Reynolds similarity of the outer flow. The inner-scaled deviation of the centreline velocity from a log law is a constant, C. The relationship is 

$$
U ^ {+} (y ^ {+}) = \frac {1}{\kappa} \ln y ^ {+} + B,\tag{4.1}
$$

$$
U _ {C L} ^ {+} = U ^ {+} (y ^ {+} = R ^ {+}) = \frac {1}{\kappa} \ln R ^ {+} + B + C.\tag{4.2}
$$

The velocity reaches a value of two-thirds of the centreline velocity at an inner-scaled wall-normal distance $y _ { 2 / 3 } ^ { + }$ that can be predicted as follows: 

$$
U ^ {+} = \frac {1}{\kappa} \ln y _ {2 / 3} ^ {+} + B = \frac {2}{3} \left(\frac {1}{\kappa} \ln R ^ {+} + B + C\right),\tag{4.3}
$$

or, rearranging, 

$$
y _ {2 / 3} ^ {+} = a R ^ {+ 2 / 3},\tag{4.4}
$$

where $a = \exp [ ( \kappa / 3 ) ( 2 C - B ) ]$ . For a pipe $\kappa = 0 . 4 2 1 , B = 5 . 6 0$ (McKeon et al. 2004) and $C \approx 2$ (McKeon, Zagarola & Smits 2005), so $a = 0 . 8$ 

The agreement is encouraging between the locus of the intersection of the $( k , n ) =$ (1, 10) response mode peak with the mean velocity profile, the prediction of (4.4) and the previously published experimental variation of the VLSM streamwise energy peak shown in figure 13. For the experimental data, the location of the VLSM peak at each Reynolds number was determined by considering the low-wavenumber spectral peak in the hot-wire data set of Morrison et al. (2004), as reported in McKeon (2008). It should be noted that identifying the location of the peak energy relies on the local smoothness of the spectra. Thus the error bars on the peak position shown in the figure are conservative and correspond to the next closest wall-normal locations at which spectra were obtained. While probe resolution efects may be a concern at the highest Reynolds number, the data at $R ^ { + } = 1 9 \times 1 0 ^ { 3 }$ appear to represent an outlier. For the remaining data the agreement with the predicted variation of the peak $y ^ { + }$ is very good, although we have insuficient data to be conclusive. We note that determining the intersection of the locus of the $( k , n ) = ( 1 , 1 0 )$ response mode peak with the mean velocity profile is a stringent test of our observation concerning the phase speed of the VLSMs, since the exact intersection reflects the resolution in $y$ used for the model, the resolution in $\omega$ and the experimental error in the mean velocity profile, all of which make the determination of appropriate error bars extremely dificult. The merge point is consistently a little above the prediction, but this is almost certainly within the accuracy with which we can determine it. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/e1d3327158dd0453c3c5c51ac68c3c9038619886d38a49326f96b1f26746922c.jpg)



<sup>Figure 13.</sup> Comparison of experimental pipe flow results on the $y ^ { + }$ location of the spectral peak in streamwise energy associated with the VLSMs, the intersection of the locus of the streamwise energy peak with the mean velocity profile $( \times )$ and the prediction of (4.4), $y ^ { + } = 0 . 8 R ^ { + 2 / 3 }$ (dashed line). : Superpipe data (Morrison et al. 2004). Note that the highest Reynolds number data point may have been afected by hot-wire spatial resolution (the non-dimensional wire length at this Reynolds number is $l ^ { + } = 3 8 5 )$


Thus we associate the first critical mode at this wavenumber pair, namely the critical mode with the lowest phase velocity, $( k , n , \omega ) = ( 1 , 1 0 , 2 / 3 U _ { C L } )$ , with the experimentally observed VLSM, and infer that this response mode gives a dominant energetic contribution to the turbulent fluctuations. Equation (4.4) represents a nonobservational attempt to predict the location of the peak in the streamwise energy associated with the VLSMs. 

The scaling with the two-thirds power of Reynolds number is also reminiscent of critical-layer arguments for neutrally stable disturbances in linearly unstable laminar flow, thus we expand the critical-layer framework to include forced, propagating modes in turbulent pipe flow. 

## 4.2. A wall and critical-layer framework

A consequence of the decomposition performed in § 2 is that (2.11) could be rewritten in terms of the vertical velocity and vorticity in a coordinate system with the wallparallel directions aligned with and perpendicular to the wavenumber vector, yielding an operator equivalent to the more familiar Orr–Sommerfeld (OS) operator, but with a turbulent base flow (identified earlier as the $( k , n , \omega ) = ( 0 , 0 , 0 )$ response mode). Since the flow is two-dimensional in this frame of reference, the Squire equation is not forced by the solutions of the Orr–Sommerfeld-like equation, as manifest in Squire’s theorem for linearly unstable incompressible flows. As such, we extend the tools of linear stability analysis to explore the scaling of the layers around the critical points, with reference to known results concerning the OS equations. 

To simplify the exposition, we consider the case for laminar plane Poiseuille flow in Cartesian coordinates. Linearized plane flow has unstable (right half-plane) eigenvalues for suficiently high Reynolds number and for the unforced case the ‘neutral curve’ bounds the region of stability in the $R e { \mathrm { - } } k$ plane. Pipe flow is always linearly stable, so has no neutral curve. However, comparable physical processes occur and are manifested as regions of high resolvent norm without actually reaching linear instability. This said, we will work with the standard formulation of the OS equation for a two-dimensional disturbance in a plane flow to aid the discussion, 

$$
(U - \omega / k) (\mathcal {D} ^ {2} - K ^ {2}) \tilde {v} - U ^ {\prime \prime} \tilde {v} - \frac {1}{\mathrm{i} k R e} (\mathcal {D} ^ {2} - K ^ {2}) ^ {2} \tilde {v} = 0.\tag{4.5}
$$

Here $U ^ { \prime \prime }$ is the second derivative of the base profile. 

Scaling analysis of this equation reveals two wall-normal regions in which the action of viscosity is required. The singularity in the inviscid OS (Rayleigh) formulation occurring if $\omega / k = U$ may be resolved by restoring either viscous efects or nonlinearities in a region local to the critical point. We consider the case of viscous critical layers here, with justification to follow. Since the solutions of the Rayleigh equation do not obey the viscous boundary conditions, a second region in which the efects of viscosity are restored is required close to the wall. The scaling of the width of these regions can be determined by consideration of the appropriate terms in (4.5) (for plane flow see Maslowe 1981; Schmid & Henningson 2001; Drazin & Reid 2004). 

Close to the wall, the boundary-layer approximation in a region around $y _ { 1 }$ is given by 

$$
\frac {1}{\mathrm{i} k R e} \mathcal {D} ^ {4} \tilde {v} = - \omega / k \mathcal {D} ^ {2} \tilde {v} = - U _ {x} \mathcal {D} ^ {2} \tilde {v},
$$

with solution 

$$
\tilde {v} (y) = C \exp \left(- (y - y _ {1}) (\mathrm{i} k R e U _ {x}) ^ {1 / 2} \mathrm{e} ^ {- \mathrm{i} \pi / 4}\right),\tag{4.6}
$$

such that the viscous layer around $y _ { 1 }$ has thickness of order $k R e ^ { - 1 / 2 }$ 

At the critical layer centred on $y _ { c }$ the approximation to the OS equation is 

$$
\frac {1}{\mathrm{i} k R e} \mathcal {D} ^ {4} \tilde {v} = (U - \omega / k) \mathcal {D} ^ {2} \tilde {v} \approx U _ {c} ^ {\prime} (y - y _ {c}) \mathcal {D} ^ {2} \tilde {v},
$$

which reduces to an Airy equation for $V ^ { \prime \prime }$ 

$$
\left(\frac {\mathrm{d} ^ {2}}{\mathrm{d} \xi^ {2}} - \xi\right) \frac {\mathrm{d} ^ {2}}{\mathrm{d} \xi^ {2}} V = 0,\tag{4.7}
$$

under the substitutions $\epsilon = ( \mathrm { i } k R e U _ { c } ^ { \prime } ) ^ { - 1 / 3 } , \xi = ( y - y _ { c } ) / \epsilon$ and $\tilde { v } ( y ) = V ( \xi )$ . Therefore the critical-layer thickness is of order $\mathrm { \Delta } y / R \sim k R e ^ { - 1 / 3 }$ and the phase velocity, $U _ { x } = \omega / k ,$ sets the wall-normal position of $y _ { c }$ 

Thus we expect to observe viscous and critical modes with $\left( k R e ^ { - 1 / 2 } \right)$ and $\left( k R e ^ { - 1 / 3 } \right)$ scaling, respectively, in the wall-normal direction. Note that in inner scaling, this corresponds to $y ^ { + } \sim ( R ^ { + } / k ) ^ { 1 / 2 }$ and $y ^ { + } \sim ( R ^ { + 2 } / k ) ^ { 1 / 3 }$ , respectively. 

The two options for the relative locations of the two layers are shown schematically in figure 14: if the layers are distinct (shown in figure 14a) then the critical layer exists at a wall-normal distance $O ( k R e ) ^ { - 1 / 5 }$ and if the critical layer reaches down to the wall, then it will be centred at a wall-normal location $O ( k R e ) ^ { - 1 / 3 }$ (shown in figure 14b). In the OS analysis, these two cases correspond to the upper and lower branches of the neutral stability curve at the Reynolds number under consideration. 

A similar scaling analysis, leading to the same Reynolds number dependencies of the layers in the two branches, can be performed in turbulent pipe flow using the turbulent base profile and with an appropriate Reynolds number for turbulent flow, $R e = R ^ { + }$ . There are no neutral curves because the eigenvalues remain in the left half-plane for all Reynolds number and all wavenumber–frequency triplets. However similar efects to the true OS system are manifested as high system response to forcing, giving a high resolvent norm with the same scaling. Hence we refer to upper and lower branch-type response modes in what follows and consider the implications of wall and critical layers for the scaling of turbulent pipe flow and in particular the implied mechanism for the manifestation of viscous efects outside of the immediate near-wall region. We note that it is well known that the peak in the streamwise velocity occurs in the critical layer, but not necessarily at the exact wall-normal location where the phase velocity of the disturbance equals the local mean flow. Thus there may be a small error in our definition of ‘critical’ in § 3.3, but the u peak remains the most useful locator of the critical layer. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/558d1f302b10a0d883a7eedb8dcf52c5b85a173a8fcb20c10cc742eb38ab9c7d.jpg)



<sup>Figure 14.</sup> Schematic of the scaling of upper (a) and lower (b) branch critical and wall layers in the OS equation.


We conclude this part of the discussion by observing that in laminar pipe flow the Reynolds-number-independence of the form of the velocity profile means that there is a linear relationship between the point at which the velocity reaches two-thirds of the centreline value and the Reynolds number, $y _ { 2 / 3 } ^ { + } \sim R ^ { + }$ . It is known that the linear Navier–Stokes operator is particularly sensitive to perturbation at this point, where the wall and centre mode branches of the spectrum merge (Reddy, Schmid & Henningson 1993). 

## 4.3. Non-normality versus criticality

The foregoing analysis permits a comment on the importance of non-normality to the sensitivity to forcing. As indicated in § 2, the resolvent in (2.15) can become large in two distinct ways, via the non-normality arising from the gradient of the mean velocity, or when the diagonal terms tend to zero at a critical layer. Regarding the non-normal mechanism, the local shear couples the streamwise and wall-normal velocity components, leading to a ‘lifting’ mechanism for streamwise vorticity. On the other hand, the critical-layer arguments arise from arguments that are normal in character, since this mechanism is present even when the mean shear is small. This provides a simple explanation of why critical modes are observed far from the wall in our model and become increasingly dominant at higher Reynolds number. The decomposition performed in this work therefore permits a simple identification of the two efects. 

## 4.4. Very large scale motions as a consequence of critical-layer scaling

We predicted in § 4.1 that the wall-normal location of the peak energy of the response mode associated with the VLSMs scales with $R ^ { + 2 / 3 }$ . The componentwise velocity distributions for the VLSM response mode have been shown in figure 5. Many of the characteristics of this mode are in good agreement with those of the lower branch-type critical layer under the analysis described above. In turbulence terminology, the associated disturbance would be ‘attached’ to the wall in the sense that it has finite amplitude in the near-wall region. This property is consistent with the observations of the ‘footprint’ of the VLSMs reaching down to the wall (Hutchins & Marusic 2007a; Guala et al. 2010b and others) and influencing the instantaneous wall shear stress (Marusic & Heuer 2007). This is a consequence of this response mode retaining characteristics of the wall layer while having the lowest phase velocity which can be considered critical. This phase velocity is a constant fraction of the centreline velocity, in agreement with the conclusions of del Alamo<sup>´</sup> et al. (2004) that the centreline velocity is the appropriate velocity scale for the very long ‘global’ modes. 

The response mode shapes associated with the VLSMs in figure 5 are in good agreement with the structure that can be inferred to give rise to the two-point correlations reported in the near-neutral surface layer by Guala et al. (2010b) and the conditional averages of Chung & McKeon (2010) in channel flow. This suggests that the VLSM response mode predicted here indeed becomes a dominant, viscous structure in the near-wall region as the Reynolds number increases. 

This VLSM response mode also has a concentration of fluctuation energy in the wall-parallel components, in agreement with the experimental evidence that the very long scales are visible in the u and w spectra (although the literature on the latter is relatively scarce due to the experimental dificulty of obtaining well spatially resolved information on the spanwise component), but not in the wall-normal component due to the efect of ‘blocking’ by the wall on eddy distribution. In addition, the spatial variations of the streamwise and wall-normal velocities implies a distribution of Reynolds shear stress that demonstrates the π phase reversal associated with viscous critical layers in the vicinity of the peak in the streamwise energy. This justifies our earlier assumption that viscosity is more important than nonlinearity in the vicinity of the critical layer. The phase relationships between the axial and wall-normal velocity components implies that these scales are ‘active’ (in the sense of Townsend 1976) in that they bear non-negligible Reynolds shear stress, as proposed by Guala et al. (2006), but in contrast to the spirit of Townsend’s original ideas. 

We note also that counter-rotating vortex structure implied by the VLSM response mode shape (figure 5) is a well-known phenomenon associated with lower branch critical-layer solutions, at least in the laminar case (Wang, Gibson & Walefe 2007; Viswanath 2009), and is observed at similar wavenumber pairs, n ∼ 10k, using the current model for laminar flow (Sharma & McKeon 2009). The conditionally averaged cross-stream streamlines and swirl distributions of Hutchins & Marusic (2007b) and Chung & McKeon (2010) confirm that this is the expected shape for the VLSMs in channel flows. This structure is also consistent with the work of del Alamo & Jim<sup>´</sup> enez´ (2006), who showed that the two types of disturbance that experience maximal transient growth in the initial value problem in turbulent channel flow, one inner scaling and one outer scaling disturbance, both resemble streamwise rolls and streaks. 

We conclude our comments on the relationship between VLSMs and critical layers by proposing a partial explanation of the apparent meandering, very long streamwise coherence of VLSMs that is indicated by experimental measurements of streamwise velocity in the spanwise plane for various flows. To this end, figure 15 shows isosurfaces of streamwise velocity for a sum of left- and right-going VLSM-type response modes, i.e. ±n. It seems plausible that the superposition of other response modes on such a pair would reproduce something like the apparent observed meandering coherence of the order of 25δ (Monty et al. 2007). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/01ef15b16e3eebac76658b34229effe57c9c3ffc5c5d8426f7922a8c7b4ffdb5.jpg)



<sup>Figure 15.</sup> Isocontours of positive and negative streamwise velocity for the sum of left- and right-going VLSM response modes, $( k , n , \mathbf { \bar { \omega } } ) = ( 1 , \pm 1 0 , 2 / 3 U _ { C L } )$ . The Reynolds number is $R \breve { e } = \breve { 7 } 5 \times \breve { 1 } 0 ^ { 3 }$


## 4.5. The importance of wall layers

Wall-layer scaling has been implicit in the work of several researchers, including the experimental and theoretical discourses by Sreenivasan & Sahay (1997) and Sahay & Sreenivasan (1999) and the form of the mean velocity in the vicinity of this peak proposed by Sreenivasan & Bershadskii (2006). The mean momentum balance structure identified by Klewicki et al. (2007) describes the scaling in inner units with $R ^ { + 1 / 2 }$ of the Reynolds stress peak location. An analogy between the wall-layer scaling phenomenon and linear stability concepts was drawn by Sreenivasan (1988) who explained the $R ^ { + 1 / 2 }$ dependence in terms of the roll-up of a vortex sheet used to model the vorticity in the boundary layer. Sirovich et al. (1990) observed plane waves in channel flow travelling at a speed corresponding to the mean velocity at the location of the Reynolds stress peak. 

By constraining our study to oblique response modes we have shown that asymptotic analysis of the linear Navier–Stokes operator in the turbulent case leads to wall and critical-layer scaling, as observed for laminar, linearly unstable flows. Such arguments can be extended to discuss local scaling of the turbulent spectrum. While it is understood that the turbulent fluctuations in the near wall region resist inner scaling, the cause of this discrepancy has been accepted for some time to lie in the increase in energy at larger streamwise wavenumbers as the Reynolds number is increased, with the implication that the spectral shape at large k (short wavelengths) has the potential to be self-similar. In fact, this self-similarity is a consequence of wall-layer scaling, which we now demonstrate. 

Applying wall-layer scaling for a response mode with streamwise wavenumber k gives 

$$
\frac {y _ {p k}}{R} \sim \frac {1}{k R ^ {+ 1 / 2}}.\tag{4.8}
$$

For a constant ${ \lambda } _ { x } ^ { + }$ , this can be rewritten in the following way, demonstrating that the peak energy location scaled in inner units will be independent of Reynolds number, provided that the phase velocity also remains constant: 

$$
y _ {p k} ^ {+} \sim \frac {R ^ {+}}{\left(\frac {2 \pi R ^ {+}}{\lambda_ {x} ^ {+}} R ^ {+}\right) ^ {1 / 2}} = \left(\frac {\lambda_ {x} ^ {+}}{2 \pi}\right) ^ {1 / 2}.\tag{4.9}
$$

Based on the results shown earlier for $\lambda _ { x } ^ { + } \approx 1 0 0 0$ , where $y _ { p k } ^ { + } \approx 1 3$ , the constant of proportionality is $O ( 1 )$ . So for the wavenumber range corresponding solely to wall-layer arguments, the spectral shape should be self-similar in inner scaling. This was confirmed in figure 10. Predicting exact self-similarity would require further arguments relating to the Reynolds-number-dependence of the product of the forcing amplitude and the first singular value, which is beyond the scope of this paper. 

## 4.6. Amplitude modulation and the phase relationship between the large and small scales

A region in the flow where an apparent amplitude modulation of the small scales occurs has been identified and explored by Blackwelder & Kovasznay (1972), Bandyopadhyay & Hussain (1984), Hutchins & Marusic (2007b), Mathis et al. (2009) and Guala et al. (2010b). This region can be identified with the concatenation of viscous wall layers at diferent wavenumber/frequency combinations and is required to meet the wall boundary conditions. Thus it must respond to the influence of finiteamplitude critical-layer disturbances. It may be said, then, that it truly represents an amplitude modulation of turbulence activity at the range of scales present in the nearwall flow, the most energetic range of which is known to correspond to wavelengths smaller than the VLSMs. By the arguments made above, this viscous layer, in which the modulation is largest, should scale with $R ^ { + 1 / 2 }$ . This is borne out in the nearneutral atmospheric surface layer with $\delta ^ { + } \sim O ( 1 0 ^ { 6 } )$ in the measurements of Guala et al. (2010b) who show that the diference in energetic content of the small scales between positive and negative excursions of the fluctuation velocity in the VLSM bandpass-filtered signal is concentrated in the region $y ^ { + } < O ( 1 0 ^ { 3 } )$ In addition, the correlation coeficient between the large-scale component and the filtered envelope of the small-scale component of Mathis et al. (2009) shows a distinct discontinuity in gradient that tracks a position $y ^ { + } \sim \delta ^ { + 1 / 2 }$ . We hypothesize that this corresponds to the outer edge of the inner viscous layer associated with the most energetic critical-layer mode, which we identify as a VLSM. 

## 4.7. Implications for the scaling of the fluctuations in turbulent pipe flow

Previous phenomenological observations and the predictions of the critical-layer scaling can be concatenated into a skeletal description of turbulent pipe flow. We showed above that wall-layer scaling implies a similarity over the part of the turbulent spectrum governed by wall modes. Additional arguments for the outer region of the flow (in which only critical modes contribute turbulent energy) seem to require the exact form of the mean velocity profile. However the similarity of the response mode shapes for a constant velocity defect at high Reynolds number in figure 11 suggests that outer scaling of the spectrum can be recovered. Therefore while outer fluctuations should be close to self-similar in outer units, the inner fluctuations will always include contributions from both wall and critical-layer modes. This, perhaps, is one cause of the apparent success of the ‘mixed scaling’ proposed by DeGraaf & Eaton (2000), which leads to collapse of $u ^ { 2 } / ( u _ { \tau } U _ { \infty } )$ over a limited Reynolds number range. In light of the distinct footprints of the diferent classes of response modes, the controversial question of the importance of ‘top-down’ versus ‘bottom-up’ efects may be more appropriately framed in terms of the relative importance of wall and critical layers, with the former tied to the latter through the wall boundary conditions, but with all fluctuations contributing to the shape of the mean profile. 

The distributions of Reynolds shear stress associated with wall and critical modes have distinct shapes and, specifically, are local in $y ^ { + }$ . That is, the Reynolds shear stress is also located in the perturbation layer, close to the peak energy. In addition, this localization goes towards explaining some of the observations of Guala et al. (2006) of the VLSMs, that these low wavenumbers (associated with critical modes in our formulation) are active in the sense that they contribute significantly to the Reynolds shear stress and also that the sign of the wall-normal gradient in shear stress at this wavenumber, $\mathrm { d } ( - u v ( k ) ) / \mathrm { d } y$ , is opposite to that of the smaller scales closer to the wall. The reversal in sign of the mean Reynolds stress associated with a single response mode lends support to the notion of a spatial transfer of turbulent energy away from the wall to the outer region, by simple arguments concerning the sign of the local turbulent energy production. Of course, in the overlap region the integrated shear stress over all response modes is such that local equilibrium concepts are at least approximately met. There is a coupling between the sum of Reynolds shear stress contributions from all response modes and the mean velocity profile that yields those modes. 

For the VLSM response mode, at least, a logarithmic variation in the mean velocity implies that (or perhaps follows from the fact that) this critical layer is always associated with a constant ratio of local to centreline velocity, $( U / U _ { C L } ) ^ { + }$ , with the consequence that knowledge of the location of the centre of the VLSM response mode, which can be experimentally determined from the peak in the streamwise turbulent energy, yields (4.4) relating the log-law constants κ, B and C. Alternatively, if the log-law constants are known, then the peak ofers an alternative way to determine the friction velocity, $u _ { \tau }$ . While the footprint of the VLSM in the streamwise spectrum becomes more dominant as the Reynolds number increases, accurate identification of the location of the maximum becomes more dificult because the distribution around the peak also broadens in $y ^ { + }$ , so these relationships may not prove to be useful in a predictive sense. 

Our key assumption is that the first response modes indicated by the singular value decomposition will be observed in turbulent pipe flow if the wall-normal distribution of the forcing at that (k, n, ω) combination is non-zero, contains an exactly appropriate component and the singular value is large. Clearly there are many other response modes with the same streamwise wavenumbers or frequencies, as observed in the spatio-temporal spectra of, for example, Morrison & Kronauer (1969), but diferent convective velocities which blur the harmonic decomposition. However, Hutchins & Marusic (2007a) have used a synthetic signal to show that an isolated portion of a signal with clear streamwise and spanwise spatial content leads to a broad peak in the spatial power spectrum centred on the true signal wavenumbers. 

We do not address the spatial phase relationship between response modes, however we suggest that the base of knowledge concerning inclined ramp-like structures and the wall-normal arrangement of statistically representative hairpin vortices, together with recent work on the interaction between the large and small scales (Chung & McKeon 2010; Mathis et al. 2009; Guala et al. 2010b) will inform future work in reassembling the response modes predicted here to represent the essence of wall turbulence. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/4afb204c1ca5cc0e37e4b5b3249888379150624d9e457fec8e9647011fedbb9a.jpg)



<sup>Figure 16.</sup> Comparison of the $y ^ { + }$ location of VLSM-related phenomena in zeropressure-gradient turbulent boundary layers over a range of Reynolds number. : location of zero-amplitude modulation in laboratory boundary layers, estimates of the zero modulation location  (Mathis et al. 2009) and the VLSM energetic peak - (Guala et al. 2010b) with various predicted forms. $( - ) \sqrt { 1 5 } \delta ^ { + 1 / 2 }$ (Mathis et al. (2009), also wall-layer prediction), $( -- )$ $0 . 6 7 \delta ^ { + 2 / \frac { 1 } { 3 } }$ (lower branch-type critical-layer prediction), (· · · ) $0 . 7 6 \delta ^ { + 4 / 5 }$ (upper branch-type critical-layer prediction).


## 4.8. Extension to other flows

We have limited the arguments made above to turbulence in pipe flow. However an equivalent formulation to that detailed in § 3.5 can be made for other flows by considering the best values of the Karman and additive constants, and the wake deviation, for other canonical flows and retaining the assumption that the critical layer occurs when $U ( y ) = 2 / 3 U _ { C L }$ (i.e. that the critical layer scales with $y ^ { + } \sim R ^ { + 2 / 3 } )$ ). For channel flow with $\kappa = 0 . 3 8$ $B = 4 . 1 7$ and $C = 0 . 1 7 5$ (Nagib & Chauhan 2008), the estimation of the location of the peak associated with a lower branch-type critical VLSM is given by (4.4), giving 

$$
y _ {2 / 3} ^ {+} \approx 0. 6 2 R ^ {+ 2 / 3}.\tag{4.10}
$$

The diference in the constant arises because of the form of the mean profile close to the centreline (the wake component), rather than the subtlety of the log-law scaling, the potential (lack of) universality of which remains under debate (Nagib & Chauhan 2008). The selection of $k = 1$ to represent the VLSM structure in channel flow is supported by the work of Monty et al. (2009), but there is also significant energy observed at a streamwise wavelength of three channel half-heights, particularly in DNS studies. 

A similar value for the constant, $a = 0 . 6 7 _ { \cdot }$ , is obtained by consideration of the log-law constants in zero-pressure-gradient turbulent boundary layers. The analysis for this flow requires accounting for, or formally proving negligible, the influence of spatial inhomogeneity in the streamwise direction, i.e. the result requires the parallel flow approximation. However there is utility in comparing the prediction of (4.10) with the experimental data. The results are plotted in figure 16 which shows the experimentally determined locations where the degree of amplitude modulation is zero in the data of Mathis et al. (2009) (which they equate with the VLSM energy peak) and several predicted Reynolds number variations. Mathis et al. (2009) proposed $\delta ^ { + 1 / 2 }$ dependence of the peak location, after assuming that the VLSMs inhabit the exact middle of the overlap layer. We have shown earlier that it is also a consequence of wall-layer scaling. The constants for the $\delta ^ { + 4 / 5 }$ scaling were determined by consideration of the point where the local velocity is four-fifths of the free-stream value, in a similar analysis to (4.4). While the $\delta ^ { + 1 \dot { / } 2 }$ and $\delta ^ { + 2 / 3 }$ scalings could be said to describe the lower-Reynolds-number data equally well, only the ${ \delta } ^ { + 1 7 2 }$ curve approaches one of the high-Reynolds-number data points obtained in the near neutral atmospheric surface layer by Mathis et al. (2009) and Guala et al. (2010a, b). Note the large error bars on both these high-Reynolds-number points, indicating the dificulty in distinguishing between scalings using experimental data. The former study determined the higher point from a study with limited resolution close to the wall, while the latter study was performed with a maximum measurement height of the order of 10 % of the equivalent boundary-layer thickness (and can be seen to reveal two spectral peaks). The critical-layer framework provides an interesting interpretation of these two identified spectral energy maxima. 

The data support a scaling with $\delta ^ { + 1 / 2 }$ , particularly if the lower estimate of the VLSM peak energy in the surface layer is taken into account, suggesting that in the boundary layer there is a strong energetic contribution from the viscous wall mode (or, of course, the critical-layer scaling changes due to the spatial inhomogeneity over the spatial VLSM period). The $\delta ^ { + 1 / 2 }$ scaling is in agreement with the observation by Jimenez that the global modes travel with a convective velocity $U _ { s } = 0 . 5 U _ { C L }$ if the mean velocity is given by a log law governed by (4.4). 

However the error bars around the peak in the streamwise turbulent energy identified by Marusic et al. (2009) encompass the point $y ^ { + } = 0 . 7 6 \delta ^ { + 4 / 5 }$ , raising the intriguing possibility that we are observing the upper branch-type configuration of figure 14, with ‘two’ local maxima in the streamwise spectrum at $y ^ { + }$ locations proportional to $\delta ^ { + 1 / 2 }$ or $\delta ^ { + 2 / 3 }$ and $\delta ^ { + 4 / 5 }$ . This may be a dificult hypothesis to prove, given the dificulty of obtaining fully resolved spectral information for Reynolds numbers $2 0 \times 1 0 ^ { 3 } < \delta ^ { + } < 7 \times \bar { 1 } 0 ^ { 5 }$ or distinguishing between two spectral peaks that are close in physical and spectral space. However we note that the streamwise velocity probability density functions reported by, amongst others, Adrian, Meinhart & Tomkins (2000) and Morris et al. (2007) suggest two maxima that can be shown to correspond to approximately 0.5 and 0.8 times the free-stream velocity, which may confirm our hypothesis concerning the special significance of these velocities in the boundary layer. 

The existence of upper and lower branch-type response modes in the diferent canonical configurations of wall turbulence may contribute to the explanation for the emerging, subtle diferences between the flows. In particular we note that the dominance of a diferent branch could afect the Reynolds stress profile with potential implications for the universality of even the mean velocity profile. 

These results have assumed that the VLSM-type response modes occur universally at $k = 1$ , while there is experimental evidence to suggest that the exact streamwise length varies from flow to flow, with the largest and smallest wavelengths observed in pipe and boundary-layer flows, respectively. However the framework presented above can easily be modified to account for this, should it prove to be required. 

## 5. Broader implications

The critical-layer arguments made here have several broader implications for canonical and more general flows. Next, we identify some that are most pertinent to our current areas of study. 

## 5.1. Importance of the linear operator

We have shown that consideration of the preferentially amplified forcing modes associated with the linear operator leads to a prediction for the dominant energetic response mode shapes. Note, however that a linearization per se is not strictly required. This result is in agreement with the understanding that the linear operator alone is responsible for the extraction of energy from the mean flow. This suggests that the response modes predicted by this analysis correspond more to the production and spectral content of energy at a particular wavenumber pair, with the full spectrum determining the rate of transfer between wavenumbers via nonlinear interactions. 

## 5.2. Taylor’s hypothesis

The forcing-response decomposition proposed in this work is consistent with the limited observations of the spatio-temporal spectra in the literature. The conversion between space and time is usually performed using Taylor’s hypothesis of frozen turbulence, which is traditionally stated in terms of the slow evolution of the smallscale turbulence relative to the convective time scale and is believed to hold using the local mean velocity as the convection velocity for all but (possibly) the longest length scales (Dennis & Nickels 2008) and very close to the wall (Morrison & Kronauer 1969). The foregoing analysis suggests an alternative interpretation: the critical-layer framework implies that the dominant response modes (and, by implication, structures) travel with a phase velocity that corresponds to the local mean at or near the peak streamwise mode energy. The reduction in amplitude away from the peak means that in the core part of the flow, the $\left( k - \omega \right)$ joint spectra should be narrow with a peak ridge lying on $\omega = U ( y ) k$ . Nearer the wall, the influence of the wall modes and the critical modes that extend to the wall but have energetic peaks further out will be to broaden the distribution of energy in $\left( k - \omega \right)$ space, remove the symmetry when integrating in k or ω and ultimately lead to an inferred convective velocity that is diferent from the local mean velocity. 

This suggests that issues related to the validity of Taylor’s hypothesis would be better expressed in terms of the symmetry and width of the $k - \omega$ spectrum. The works of Morrison and co-workers (Morrison & Kronauer 1969; Morrison, Bullock & Kronauer 1971), among others, illuminated the deviation of the inferred convective velocity from the local mean, the lack of symmetry near the wall in pipe flow and the spectral broadening that our model suggests. Recent large eddy simulations in turbulent channel flow (Chung & McKeon 2010) reveal similar phenomena; this is an area of current experimental investigation. 

Consideration of the variation of the spanwise wavenumber of energetic scales, the $n - \omega$ spectrum, suggests an additional source for the spatial resolution problems that hamper the majority of laboratory high-Reynolds-number wall turbulence experiments, namely the spanwise extent of the sensing element in viscous units. 

## 5.3. The minimal unit for turbulence

The ‘autonomous’ simulations of Jimenez´ et al. (2004) demonstrated that a DNS of turbulent channel flow with a filter at a certain wall-normal height was capable of capturing the majority of the near-wall statistical features. This informed the ‘topdown’ versus ‘bottom-up’ debate and appeared to indicate that the external flow did not exert any control on the near-wall cycle. In light of the critical-layer analysis, we observe that the wall-normal cutof in these simulations, $y ^ { + } \sim 7 0$ , is above the peak of the VLSM critical mode for the nominal Reynolds number of $R e _ { \tau } \approx 5 5 0$ , for which $y _ { 2 / 3 } ^ { + } \sim 5 0$ , so that even the lowest filter does not exclude the dominant, VLSM critical mode. To this extent, the results are consistent with our hypothesis. The implication for future simulations, then, is that the criterion on the minimum size of an autonomous simulation must be large enough to capture the azimuthal/spanwise and radial/wall-normal extent of the critical mode associated with the VLSM, or the furthest reaching response mode that leads to considerable modulation in a viscous layer near the wall. 

## 5.4. Experimental development length

A simple estimate for the development length required in canonical wall turbulence experiments can be made by assuming the importance, or at least the large singular values, associated with response modes with a streamwise-spanwise aspect ratio of 10:1, as in the VLSMs explored here. The peculiar constraint on azimuthal symmetry in pipe flow requires that n is integer, such that $k \geqslant 0 . 1$ for modes with the required aspect ratio. This is in good agreement with the observed low wavenumber end of the pre-multiplied spectra in the overlap region in pipe flow (McKeon & Morrison 2007), at a wavelength $\lambda _ { x } \approx 6 0 R$ . Combining this figure with the estimates detailed in Zagarola & Smits (1998) to account for the transition length at $( L / R < 1 4 )$ and the length for the shear layers to meet $( L / R \sim 6 0 )$ at $R e _ { D } \sim 1 0 ^ { 5 }$ gives a reasonable estimate for the minimum required development length, $L _ { D } / R > 1 3 4 R$ . This figure is significantly exceeded in the Princeton Superpipe, where all measurements were taken for $L _ { D } / R > 1 6 4 R$ . The estimate is in good agreement with the length $L _ { D } \geqslant 1 6 0 R$ for fully developed statistics in pipe flow (Monty et al. 2001) or $L / R \approx 1 3 4$ in channel flow (Dean & Bradshaw 1976), both at similar Reynolds numbers. This estimate also has implications for simulation, where box sizes can be set without consideration of the same entry efects experienced in experiments. 

## 5.5. Turbulence over rough walls

The wall and critical layers indicated by our model suggest a physical explanation for several keystones of our understanding of rough wall flows. Firstly, for flows that obey Townsend’s hypothesis in the mean velocity, where the efect of the roughness is felt only in setting the friction velocity such that the self-similar form of the smooth wall is retained in the outer region, it is logical that the outer fluctuations would also obey similar scaling to the smooth wall case. This is because the outer region is dominated by response modes whose shape is dictated by the local (i.e. outer) mean velocity profile. 

Secondly, while it is known that the near-wall streamwise intensity peak is suppressed relative to smooth wall values, the modulation efect associated with the VLSMs is still strong over walls with $\nu / u _ { \tau } \ll k < \delta .$ , for example in the near-neutral surface layer under conditions with $k _ { s } ^ { + } \leqslant 5 0$ (Guala et al. 2009b; Mathis et al. 2009). In this flow, the VLSM critical layer is centred outside of the roughness sublayer of order $3 k _ { s } ^ { + }$ . The diference in the wall boundary condition would suggest that the structure of the viscous layer required to meet the wall boundary conditions would be quite diferent from that observed in the smooth wall case, in that it would be significantly less coherent and a strong function of the roughness geometry. However an analysis similar to that given in § 4.2 could be performed on the new mean flow, still yielding a wall layer that must meet the boundary condition in response to the velocity field imposed by critical modes. This is equivalent to stating that modification to the linear operator due to the roughness is confined to the region close to the wall, with the consequence that only the wall layer is significantly afected, for small enough roughness. Thus our critical-layer model has the potential to make further progress in understanding the influence of surface roughness. 

## 5.6. Additional observations

A full investigation of spectral scaling predictions using the critical-layer model is reserved for future work. It also remains to cement the link between our model, statistical experimental data and the emerging picture of the structure of near-wall turbulence. The picture has elements ranging from the VLSM structures discussed above through to observations of hairpin-like vortices, packets and uniform momentum zones (Adrian 2007) and the near-wall cycle (previously thought to be autonomous) that is consistent with the physical arguments of Schoppa & Hussain (2002). We also note that the critical layer arguments hold significance for approaches to control of wall turbulence, specifically suggesting the possible utility of using distributed (harmonic) forcing at the wall. 

## 6. Conclusions

We have described here a resolvent norm model capable of describing the most amplified velocity response modes over the range of streamwise and spanwise wavenumbers and frequencies observed in turbulent pipe flow, and an example of its application to illuminating scaling relationships in wall turbulence. 

To derive the model, we perform a decomposition of the Navier–Stokes equations that allows us to treat the nonlinearity in the perturbation equation (involving the Reynolds stress) as an unknown exogenous forcing, yielding a linear relationship given by the resolvent between the velocity field response and this nonlinearity. By only considering disturbances that are periodic in the wall-parallel directions and in time, we restrict our attention to helical response modes that propagate obliquely relative to the mean velocity, in the direction of the wavenumber vector. This permits us to compare our results to the typical statistical decomposition of point and field experimental measurements and simulations for both temporal and spatial data. The linearity of the equation means that the diferent frequencies and wavenumbers are only coupled through the forcing. 

Of necessity, there is a steady component that varies only in the wall-normal direction, which we identify as the turbulent mean profile. This yields for the perturbations a linear operator identical to that obtained by linearization about the turbulent mean profile. However, we do not assume small perturbations, and such a linearization would set the forcing to zero. The mean profile is suficient information to calculate the resolvent at any other wavenumber–frequency combination, and we use a mean profile determined from the Princeton Superpipe experiments. Equations (2.11) and (2.12) constitute a decomposition of the Navier–Stokes equations into the orthogonal directions associated with Fourier modes in the streamwise and azimuthal directions and in time. 

We then use the singular value decomposition of the resolvent at a given (k, n, ω) to find the forcing shape at a wavenumber–frequency combination that gives the largest velocity field response, under the assumption that it is likely to be a more dominant structure in turbulent flows than other velocity field responses associated with smaller amplification. 

The results of the model lend themselves to an interpretation, at each wavenumber– frequency combination, involving propagating response modes with convection or phase velocity equal to the velocity somewhere in the interior of the flow. Building on the analysis of the OS equation in linearly unstable flows, we identify two regions in which the action of viscosity is required for each wavenumber–frequency combination. They are in the vicinity of the critical layer, where the phase velocity is equal to the local mean velocity, and close to wall, where the boundary condition must be met. We designated these the ‘critical’ and ‘wall’ layers. By analogy with the upper and lower branches of the neutral curve in unstable flow, there exist two relative wallnormal locations for these layers: an upper-branch-type configuration in which the critical layer resides at a distance $y ^ { + } \sim R ^ { + 4 / 5 }$ and is distinct from the wall layer which is centred on $y ^ { + } \sim R ^ { + 1 / 2 }$ , and a lower-branch-type solution in which the critical layer occurs at $y ^ { + } \sim R ^ { + 2 / 3 }$ , overlaps with the wall layer and has a footprint down to the wall. These scalings can be obtained from analysis of the resolvent in the coordinate system rotated to align with the wavenumber vector. The transition from wall to critical response modes in our model occurs when one is responsible for larger amplification than the other. 

It was proposed that key features of wall turbulence can be represented in the framework of a range of propagating response modes with diferent wavenumber– frequency combinations such that they move with diferent convective velocities. The dominant modes that emerge from the resolvent model provide a descriptive basis for the decomposition of the turbulent velocity field and capture some known features of wall turbulence. In some sense, the conclusions of this research represent a return to the wave-like concepts of turbulence research in the mid twentieth century, but with the interpretation that complex coherent structure is a consequence of the assembly of response modes and their relative motions. 

While previous researchers have identified wall-layer scaling for the Reynolds stress (Sreenivasan 1988; Sreenivasan & Sahay 1997; Sreenivasan & Bershadskii 2006; Klewicki et al. 2007) and the importance of propagating waves (Sirovich et al. 1990) in wall turbulence, our extended formulation suggests a picture of organized complexity in wall turbulence that appears to be consistent with a range of results from observations of full flows. In particular, the critical-layer arguments and scaling that are presented here lead to inner scaling of the small scales near the wall and apparent outer scaling of the fluctuations in the core of the pipe, as well as a mechanism for the origin and scaling of the VLSMs in pipe flow, as the critical-layer solutions of the forced linear equation. In addition, the interpretation of the wall layer as the solution which meets the wall boundary condition at each wavenumber–frequency combination implies that there must be an interaction between the critical and wall modes, an interaction that has been identified in recent literature as an amplitude modulation of the near-wall turbulence by the very large scales (Mathis et al. 2009) or the phase relationship between the small and large scales (Chung & McKeon 2009). The broader implications of this scaling include a framework with which to interpret flow over rough walls, which can be considered as a modification to the boundary condition that the wall layer must meet. This is consistent with observations in the literature that while the near-wall flow is disturbed by the roughness, the VLSMs are still observed (e.g. Guala et al. 2010b). 

A further observation concerns the appropriate scaling properties at the very large scales. It is clear that the VLSM wavelength scales on the outer length scale, in our case the pipe radius. The critical-layer scaling requires that the velocity scale should be the centreline velocity, $U _ { C L }$ , which is in agreement with arguments of Jimenez´ et al. (2004) concerning the ‘global’ modes in channel flow. The model suggests that the dominant response mode with streamwise and spanwise wavenumbers representative of the experimental observations of the VLSMs in pipe flow should travel with a phase velocity equal to two-thirds of the centreline velocity, such that the critical layer occurs where $U ( y ) = 2 / 3 U _ { C L }$ . This occurs within the overlap region in the mean velocity for all Reynolds numbers considered here, and as such represents a mechanism by which the efects of viscosity can extend well beyond the immediate vicinity of the wall. This is in agreement with several recent results including studies of the mean velocity profile and mean momentum equation. 

The lack of information in this analysis on the relative phase between response modes precludes immediate identification of structural features such as those we would expect from observations of the real flow, including hairpin-like vortex packets and the near-wall cycle, etc. However these may be construed, at least in part, to be a consequence of the dominant, energetic response modes moving relative to each other with diferent convective velocities. This is a subject of ongoing investigation. 

Extrapolation of the scaling arguments to other flows suggests a fundamental diference between internal and external flows (or at least pipes and boundary layers). While the influence of spatial development in the latter case has not yet been taken into account, preliminary observations suggest that the upper branch type criticallayer solution at VLSM-like a wavenumber pair may dominate, such that the VSLM energy peak scales with $y ^ { + } \sim R ^ { + 4 / 5 }$ instead of the $R ^ { \dot { + } 2 / 3 }$ scaling observed in pipe flow. Experimental confirmation of the critical-layer scaling proposed here is ongoing. 

Finally, the observation that the wall layer must meet the boundary condition suggests that the outlook is optimistic for wall-based control of friction drag. 

The support of NSF CAREER award grant number 0747672 (programme managers William Schultz and H. Henning Winter), a PECASE award through the Air Force Ofice of Scientific Research (programme manager John Schmisseur), grant number FA9550-09-1-0701 (B. J. McKeon), an Imperial College Junior Research Fellowship and the EPSRC (A. S. Sharma) is gratefully acknowledged. We would also like to thank A. Meseguer and L. Trefethen for publishing their pipe code. 

## Appendix A. Interpretation of resolvent analysis

In addition to the type of transfer function analysis presented here, our resolvent analysis can be understood in terms of pseudospectra analysis (Trefethen & Embree 2005). 

The -pseudospectrum of ${ \mathcal { L } } , A _ { \epsilon }$ is defined as 

$$
\Lambda_ {\epsilon} (\mathscr {L}) = \left\{\lambda \in \mathbb {C}: (\lambda I - \mathscr {L}) ^ {- 1} \geqslant \epsilon^ {- 1} \right\}.\tag{A 1}
$$

That is, the -pseudospectrum represents the spectrum of the operator $\mathcal { L }$ under a perturbation with magnitude . This is then interpreted as bounds on the complex plane within which the spectrum of the perturbed operator lies. 

The level curves of the pseudospectrum therefore correspond to the level curves of the resolvent and the spectrum of $\mathcal { L }$ represents the subset of the field of complex numbers, where $\epsilon = 0$ and the resolvent is unbounded. The norm of the resolvent $( | | ( \lambda I - { \mathcal { L } } ) ^ { - 1 } | | _ { 2 } )$ is equal to $\epsilon ^ { - 1 }$ at any particular point λ in the complex plane. 

This is illustrated in figure 17(a), in which the pseudospectrum in laminar pipe flow is compared with the more familiar spectrum. Where the pseudospectrum intrudes significantly on the right half-plane, significant perturbation growth with a nominally stable operator can result (Meseguer $\&$ Trefethen 2003). 

For pipe flow, the spectrum of $\mathcal { L }$ lies in the left half-plane $( { \mathcal { L } }$ is always stable). Since the maximum value of an analytic function on a region of the complex plane lies on that region’s boundary (the maximum modulus principle), the maximal norm of the resolvent taken over the right half of the complex plane of a stable operator lies on the imaginary axis. This corresponds to the system response to harmonic forcing and can be visualized by taking a slice of a pseudospectrum contour plot along the imaginary axis, as shown in figure 17(b). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/e8c70a4366a3c98ab32fc318622f17dd87a0976d15078bd45c7e70ca60cb0d1a.jpg)



<sup>Figure 17.</sup> Spectrum, pseudospectrum and resolvent norm for harmonic forcing, for a disturbance with $\left( k , n \right) ^ { - } = \left( 1 \right.$ , 10) in laminar pipe flow at $R e \ = \ 5 \times 1 0 ^ { 3 }$ . Level curves at $( s I - \mathcal { L } ) ^ { - 1 } = 1 0 ^ { 1 } , 1 0 ^ { 2 } , 1 0 ^ { 3 }$ , etc.


Our resolvent analysis characterizes system non-normality. Performing this characterization by formulating the initial value problem is popular in fluid mechanics. The two approaches are related, but not trivially. It is a consequence of the Hille– Yosida theorem (Curtain & Zwart 1995) that the resolvent obeys 

$$
\| (\lambda I - \mathscr {L}) ^ {- 1} \| _ {2} \leqslant \frac {M}{q - d},
$$

where $q$ is the real part of λ, and M and d are real numbers and 

$$
\| \mathbf {e} ^ {\mathcal {L} t} \| _ {2} = M \mathbf {e} ^ {d t}.
$$

Here M characterizes the transient behaviour, and d the asymptotic response. It is an important open problem in control theory how to analytically determine M for a given d (Blondel & Megretski 2004). The properties of the resolvent in turbulent flow have been studied in the context of the initial value problem in wall shear flows (Butler & Farrell 1992a; del $\mathrm { \AA }$ lamo & Jimenez 2006; Cossu´ et al. 2009) and the response of turbulent channel flow to stochastic forcing (Farrell & Ioannou 1998). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-08/1e01e67e-1452-407a-a4c3-eeab565d192b/6d65952ae73235f6fab2aa00ef59891c80a262ace9846b596f81c13cb3f8f247.jpg)



<sup>Figure 18.</sup> Spectrum and resolvent norm of (turbulent) $\mathcal { L }$ for a disturbance with $( k , n ) = ( 1 , 1 \hat { 0 } )$ at $R e \ : = 7 . 5 \times 1 0 ^ { 4 }$ . (a) The black dots show the spectrum calculated with a resolution of $N = 6 0$ and the light crosses the same calculation for $N = 2 0 0 . \ ( b )$ The resolvent norm across the imaginary axis. Although the spectrum is not well resolved overall in either case, the spectrum near the imaginary axis is well resolved quickly and the resolvent norm is accurate for much lower N than is required for a full spectral analysis.


## Appendix B. Robustness of the resolvent norm to numerical and modelling error

Figure 18 shows the spectrum of the operator $\mathcal { L }$ for the wavenumber pair $( k , n ) =$ (1, 10) in turbulent pipe flow for two diferent spatial resolutions, $N ~ = ~ 6 0$ and $N = 2 0 0$ . We should expect that features prominent in real flows should be robust to operator perturbation (such as underresolution) and as such have a high response to forcing. Inspection of figure 18 demonstrates this to be the case. 

In figure $1 8 ( a )$ , the black dots show the spectrum calculated with a resolution of $N = 6 0$ and the light crosses the same calculation for $N = 2 0 0$ . Figure 18(b) shows the resolvent norm across the imaginary axis. Although the whole spectrum is not well resolved overall at $N = 6 0$ , the spectrum near the imaginary axis is well resolved, suggesting that the dominant part of the spectrum is resolved with low N, and both the resolvent norm and the response mode shape (not shown) are accurate for much lower N than is required for a full spectral analysis. However, high resolution is required to observe near-wall inner scaling response modes at high Reynolds number. These two constraints may be incompatible and limit the extension of these results to higher Reynolds numbers without additional consideration of the numerical technique. 

## REFERENCES



<sup>Adrian, R. J.</sup> 2007 Vortex organization in wall turbulence. Phys. Fluids 19 (041301). 





<sup>Adrian, R. J., Meinhart, C. D. & Tomkins, C. D.</sup> 2000 Vortex organization in the outer region of the turbulent boundary layer. J. Fluid Mech. 422, 1–54. 





<sup>del Alamo, J. C. & Jim´</sup> <sup>enez, J.´</sup> 2006 Linear energy amplification in turbulent channels. J. Fluid Mech. 559, 205–213. 





del Alamo, J. C., Jim<sup>´</sup> enez, J., Zandonade, P. & Moser, R. D.´ <sub>2004</sub> <sub>Scaling</sub> <sub>of</sub> <sub>the</sub> <sub>energy</sub> <sub>spectra</sub> of turbulent channels. J. Fluid Mech. 500, 135–144. 





<sup>Aubry, N., Holmes, P., Lumley, J. L. & Stone, E.</sup> 1988 The dynamics of coherent structures in the wall region of a turbulent boundary layer. J. Fluid Mech. 192, 115–173. 





Bailey, S. C. C., Hultmark, M., Smits, A. J. & Schultz, M. P. <sub>2008 Azimuthal structure of</sub> turbulence in high Reynolds number pipe flow. J. Fluid Mech. 615, 121–138. 





<sup>Bailey, S. C. C. & Smits, A. J.</sup> 2009 The structure of large- and very large-scale motions in turbulent pipe flow. Paper 2009-3684. AIAA. 





<sup>Balakumar, B. J. & Adrian, R. J.</sup> 2007 Large- and very-large-scale motions in channel and boundary layer flows. Phil. Trans. R. Soc. A 365, 665–681. 





<sup>Bamieh, B. & Dahleh, M.</sup> 2001 Energy amplification in channel flows with stochastic excitation. Phys. Fluids 13 (11), 3258–3269. 





<sup>Bandyopadhyay, P. R. & Hussain, A. K. M. F.</sup> 1984 The coupling between scales in shear flows. Phys. Fluids 27 (9), 2221–2228. 





<sup>Blackwelder, R. F. & Kovasznay, L. S. G.</sup> 1972 Time scales and correlations in a turbulent boundary layer. J. Fluid Mech. 15, 1545–1554. 





<sup>Blondel, V. & Megretski, A</sup>. (Ed) 2004 Unsolved Problems in Mathematical Systems and Control Theory. Princeton University Press. 





<sup>Boberg, L. & Brosa, U.</sup> 1988 Onset of turbulence in a pipe. Z. Naturforsch. 43a, 697–726. 





<sup>Butler, K. & Farrell, B.</sup> 1992a Optimal perturbations and streak spacing in wall-bounded turbulent shear flow. Phys. Fluids A5, 774–777. 





<sup>Butler, K. & Farrell, B.</sup> 1992b Three-dimensional optimal perturbations in viscous shear flow. Phys. Fluids 4 (8). 





<sup>Cess, R. D.</sup> 1958 A study of the literature on heat transfer in turbulent tube flow. Tech. Rep. Rep. 8-0529-R24. Westinghouse Research. 





<sup>Chung,</sup> <sup>D.</sup> <sup>&</sup> <sup>McKeon,</sup> <sup>B.</sup> <sup>J.</sup> 2010 Large-eddy simulation investigation of large-scale structures in a long channel flow. (submitted). 





<sup>Cossu, C., Pujals, G. & Depardon, S.</sup> 2009 Optimal transient growth and very large scale structures in turbulent boundary layers. J. Fluid Mech. 619, 79–94. 





<sup>Curtain, R. F. & Zwart, H. J.</sup> 1995 An Introduction to Infinite-Dimensional Linear Systems Theory. Springer. 





<sup>Dean, R. B. & Bradshaw, P.</sup> 1976 Measurements of interacting turbulent shear layers in a duct. J. Fluid Mech. 78, 641–676. 





<sup>DeGraaff, D. B. & Eaton, J. K.</sup> 2000 Reynolds-number scaling of the flat-plate turbulent boundary layer. J. Fluid Mech. 422, 319–346. 





<sup>Dennis, D. & Nickels, T.</sup> 2008 On the limitations of Taylor’s hypothesis in constructing long structures in wall-bounded turbulent flow. J. Fluid Mech. 614, 197–206. 





<sup>Drazin,</sup> <sup>P.</sup> <sup>G.</sup> <sup>&</sup> <sup>Reid,</sup> <sup>W.</sup> <sup>H.</sup> 2004 Hydrodynamic Stability, 2nd edn. Cambridge University Press. 





Duggleby, A., Ball, K. S., Pail, M. R. & Fischer, P. F. <sub>2007 Dynamical eigenfunction</sub> decomposition of turbulent pipe flow. J. Turbul. 8 (43), 1–24. 





<sup>Farrell, B. & Ioannou, J.</sup> 1993 Stochastic forcing of the linearized Navier–Stokes equations. Phys. Fluids 5 (11), 2600–2609. 





<sup>Farrell, B. F. & Ioannou, P. J.</sup> 1998 Perturbation structure and spectra in turbulent channel flow. Theor. Comput. Fluid Dyn. 11, 237–250. 





Gayme, D. F., McKeon, B. J., Papachristodolou, A., Bamieh, B. & Doyle, J. C. <sub>2010 Streamwise</sub> constant model of turbulence in plane Couette flow. (submitted). 





<sup>Guala, M., Hommema, S. E. & Adrian, R. J.</sup> 2006 Large-scale and very-large-scale motions in turbulent pipe flow. J. Fluid Mech. 554, 521–542. 





<sup>Guala, M., Metzger, M. & McKeon, B. J.</sup> 2010a Intermittency in the atmospheric surface layer: unresolved or slowly varying? Physica D (in press). 





<sup>Guala, M., Metzger, M. J. & McKeon, B. J.</sup> 2010b Interactions within the turbulent boundary layer at high Reynolds number. (submitted). 





<sup>Henningson, D. S. & Reddy, S. C.</sup> 1994 On the role of linear mechanisms in transition to turbulence. Phys. Fluids 6 (3), 1396–1398. 





<sup>Hutchins, N. & Marusic, I.</sup> 2007a Evidence of very long meandering features in the logarithmic region of turbulent boundary layers. J. Fluid Mech. 579, 1–28. 





<sup>Hutchins, N. & Marusic, I.</sup> 2007b Large-scale influences in near-wall turbulence. Phil. Trans. R. Soc. A 365, 647–664. 





<sup>Jimenez, J., del´ Alamo, J. C. & Flores, O.´</sup> 2004 The large-scale dynamics of near-wall turbulence. J. Fluid Mech. 505, 179–199. 





<sup>Jovanovic, M. R. & Bamieh, B.</sup> 2004 Unstable modes versus non-normal modes in supercritical channel flows. In Proceedings of the 2004 American Control Conference, Boston, MA. 





<sup>Jovanovic, M. R. & Bamieh, B.</sup> 2005 Componentwise energy amplification in channel flows. J. Fluid Mech. 534, 145–183. 





<sup>Kim, K. C. & Adrian, R. J.</sup> 1999 Very large-scale motion in the outer layer. Phys. Fluids 11, 417–422. 





<sup>Kim, J. & Lim, J.</sup> 1993 A linear process in wall-bounded turbulent shear flows. Phys. Fluids 12 (8), 1885–1888. 





Klewicki, J. C., Fife, P., Wei, T. & McMurtry, P. <sub>2007 A physical model of the turbulent</sub> boundary layer consonant with the mean momentum balance structure. Phil. Trans. R. Soc. A 365, 823–839. 





Kovasznay, L. S. G., Kibens, V. & Blackwelder, R. F. <sub>1970 Large-scale motion in the intermittent</sub> region of a turbulent boundary layer. J. Fluid Mech. 41, 283–325. 





Krogstad, P.-A., Kaspersen, J. H. & Rimestad, S. <sub>1998 Convection velocities in a turbulent</sub> boundary layer. J. Fluid Mech. 10 (4), 949–957. 





<sup>Long, R. R. & Chen, T.-C.</sup> 1981 Experimental evidence for the existence of the ‘mesolayer’ in turbulent systems. J. Fluid Mech. 105, 19–59. 





<sup>Marusic, I. & Heuer, W. D. C.</sup> 2007 Reynolds number invariance of the structure inclination angle in wall turbulence. Phys. Rev. Lett. 99, 114504. 





Marusic, I., McKeon, B. J., Monkewitz, P. A., Nagib, H. M., Smits, A. J. & Sreenivasan, K. R. 2010 Wall-bounded turbulent flows at high Reynolds numbers: recent advances and key issues. Phys. Fluids. (in press). 





<sup>Maslowe, S. A.</sup> 1981 Shear flow instabilities and transition. In Hydrodynamic Instabilities and the Transition to Turbulence (ed. H. L. Swinney & J. P. Gollub), pp. 181–228. Springer. 





<sup>Maslowe, S. A.</sup> 1986 Critical layers in shear flows. Annu. Rev. Fluid Mech. 18, 405–432. 





<sup>Mathis, R., Hutchins, N. & Marusic, I.</sup> 2009 Large-scale amplitude modulation of the small-scale structures of turbulent boundary layers. J. Fluid Mech. 628, 311–337. 





<sup>McKeon, B. J.</sup> 2008 Scaling in wall turbulence: scale separation and interaction. Paper 2008–4237. AIAA. 





McKeon, B. J., Li, J., Jiang, W., Morrison, J. F. & Smits, A. J. <sub>2004 Further observations on the</sub> mean velocity distribution in fully developed pipe flow. J. Fluid Mech. 501, 135–147. 





<sup>McKeon, B. J. & Morrison, J. F.</sup> 2007 Asymptotic scaling in turbulent pipe flow. Phil. Trans. R. Soc. A 365, 771–787. 





<sup>McKeon, B. J., Zagarola, M. V. & Smits, A. J.</sup> 2005 A new friction factor relationship for fully developed pipe flow. J. Fluid Mech. 538, 429–443. 





<sup>Meseguer, A. & Trefethen, L. N.</sup> 2003 Linearized pipe flow to Reynolds number $1 0 ^ { 7 } .$ . J. Comput. Phys. 186, 178–197. 





<sup>Metzger, M. M. & Klewicki, J. C.</sup> 2001 A comparative study of near-wall turbulence in high and low Reynolds number boundary layers. Phys. Fluids 13, 692–701. 





<sup>Metzger, M., McKeon, B. J. & Holmes, H.</sup> 2007 The near-neutral atmospheric surface layer: turbulence and non-stationarity. Phil. Trans. R. Soc. A 365, 859–876. 





Monty, J. P., Hafez, S., Jones, M. B. & Chong, M. S. <sub>2001 Turbulent pipe flow: an analysis of</sub> mean-flow characteristics. In Australasian Fluid Mechanics Conference, pp. 921–924. 





Monty, J. P., Hutchins, N., Ng, H. C. H., Marusic, I. & Chong, M. S. <sub>2009 A comparison of</sub> turbulent pipe, channel and boundary layer flows. J. Fluid Mech. 632, 431–442. 





Monty, J. P., Stewart, J. A., Williams, R. C. & Chong, M. S. <sub>2007 Large-scale features in turbulent</sub> pipe and channel flows. J. Fluid Mech. 589, 147–156. 





Morris, S. C., Stolpa, S. R., Slaboch, P. E. & Klewicki, J. <sub>2007 Near-surface particle image</sub> velocimetry measurements in a transitionally rough-wall atmospheric boundary layer. J. Fluid Mech. 580, 319–338. 





Morrison, W. R. B., Bullock, K. J. & Kronauer, R. E. <sub>1971 Experimental evidence of waves in</sub> the sublayer. J. Fluid Mech. 49 (4), 639–656. 





Morrison, J. F., Jiang, W., McKeon, B. J. & Smits, A. J. <sub>2004 Scaling of the streamwise velocity</sub> component in turbulent pipe flow. J. Fluid Mech. 508, 99–131. 





<sup>Morrison, W. R. B. & Kronauer, R. E.</sup> 1969 Structural similarity for fully developed turbulence in smooth tubes. J. Fluid Mech. 39 (1), 117–141. 





<sup>Nagib, H. M. & Chauhan, K. A.</sup> 2008 Variations of von Karm´ an coeficient in canonical flows.´ Phys. Fluids 20, 101518. 





Reddy, S. C., Schmid, P. J. & Henningson, D. S. <sub>1993 Pseudospectra of the Orr–Sommerfeld</sub> equation. SIAM J. Appl. Math. 53 (1), 15–47. 





<sup>Reynolds, W. C. & Hussain, A. K. M. F.</sup> 1972 The mechanics of an organized wave in shear flow. Part 3. Theoretical models and comparisons with experiment. J. Fluid Mech. 54, 263–288. 





<sup>Reynolds,</sup> <sup>W.</sup> <sup>C.</sup> <sup>&</sup> <sup>Tiederman,</sup> <sup>W.</sup> <sup>G.</sup> 1967 Stability of turbulent channel flow, with application to Malkus’s theory. J. Fluid Mech. 27 (2), 253–272. 





<sup>Sahay, A. & Sreenivasan, K. R.</sup> 1999 The wall-normal position in pipe and channel flows at which viscous and turbulent shear stresses are equal. Phys. Fluids 11 (10), 3186–3188. 





<sup>Schmid, P. J. & Henningson, D. S.</sup> 2001 Stability and Transition in Shear Flows. Springer. 





<sup>Schoppa, W. & Hussain, F.</sup> 2002 Coherent structure generation in near-wall turbulence. J. Fluid Mech. 453, 57–108. 





<sup>Sharma,</sup> <sup>A.</sup> <sup>S.</sup> <sup>&</sup> <sup>McKeon,</sup> <sup>B.</sup> <sup>J.</sup> 2009 Perturbation energy production in pipe flow over a range of Reynolds numbers using resolvent analysis. In Forty-seventh AIAA Aerospace Sciences Meeting, Paper 2009-1513. AIAA. 





Sharma, A. S., McKeon, B. J., Morrison, J. F. & Limebeer, D. J. N. <sub>2006 Stabilising control laws</sub> for the incompressible Navier-Stokes equations using sector stability theory. In Third AIAA Flow Control Conference, Paper 2006-3695. AIAA. 





<sup>Shockling, M. A., Allen, J. J. & Smits, A. J.</sup> 2006 Efects of machined surface roughness on high-Reynolds-number turbulent pipe flow. J. Fluid Mech. 564, 267–285. 





<sup>Sirovich, L., Ball, K. S. & Keefe, L. R.</sup> 1990 Plane waves and structures in turbulent channel flow. Phys. Fluids A 2 (12), 2217–2226. 





<sup>Sreenivasan, K. R.</sup> 1988 A unified view of the origin and morphology of the turbulent boundary layer structure. In Turbulence Management and Relaminarisation; Proceedings of the IUTAM Symposium, Bangalore, India, January 13–23, 1987 (A89-10154 01-34) (ed. H. W. Liepmann & R. Narasimha), pp. 37–61. Springer. 





<sup>Sreenivasan, K. R. & Bershadskii, A.</sup> 2006 The mean velocity distribution near the peak of the Reynolds shear stress, extending also to the bufer region. In IUTAM Symposium on One Hundred Years of Boundary Layer Research (ed. K. R. Sreenivasan, G. E. A. Meier & H.-J. Heinemann), pp. 241–246. Springer Netherlands. 





<sup>Sreenivasan, K. R. & Sahay, A.</sup> 1997 The persistence of viscous efects in the overlap region, and the mean velocity in turbulent pipe and channel flows. In Self-Sustaining Mechanisms of Wall Turbulence (ed. R. Panton), pp. 253–272. Computational Mechanics. 





<sup>Townsend, A. A.</sup> 1976 The Structure of Turbulent Shear Flow. Cambridge University Press. 





<sup>Trefethen, L. N. & Embree, M.</sup> 2005 Spectra and Pseudospectra: The Behavior of Nonnormal Matrices and Operators. Princeton University Press. 





Trefethen, L. N., Trefethen, A. E., Reddy, S. & Driscoll, T. A. <sub>1993 Hydrodynamic stability</sub> without eigenvalues. Science 261 (5121), 578–584. 





<sup>Viswanath,</sup> <sup>D.</sup> 2009 The critical layer in pipe flow at high Reynolds number. Phil. Trans. R. Soc. A 367, 561–576. 





<sup>Waleffe, F.</sup> 1997 On a self-sustaining process in shear flows. Phys. Fluids 9 (4), 883–900. 





<sup>Waleffe, F.</sup> 2001 Exact coherent structures in channel flow. J. Fluid Mech. 435, 93–102. 





<sup>Waleffe, F.</sup> 2003 Homotopy of exact coherent structures in plane shear flows. Phys. Fluids 15 (6), 1517–1534. 





<sup>Wang, J., Gibson, J. & Waleffe, F.</sup> 2007 Lower branch coherent states in shear flows: transition and control. Phys. Rev. Lett. 98 (204501). 





<sup>Wedin, H. & Kerswell, R. R.</sup> 2004 Exact coherent structures in pipe flow: travelling wave solutions. J. Fluid Mech. 508, 333–371. 





<sup>Willis,</sup> <sup>A.,</sup> <sup>Hwang,</sup> <sup>Y.</sup> <sup>&</sup> <sup>Cossu,</sup> <sup>C.</sup> 2009 Drag reduction in pipe flow by optimal forcing. ArXiv 0908.3971.v1. 





<sup>Wu, X. & Moin, P.</sup> 2008 A direct numerical simulation study on the mean velocity characteristics in pipe flow. J. Fluid Mech. 608, 81–112. 





<sup>Young, N.</sup> 1988 An Introduction to Hilbert Space. Cambridge University Press. 





<sup>Zagarola, M. V. & Smits, A. J.</sup> 1998 Mean flow scaling of turbulent pipe flow. J. Fluid Mech. 373, 33–79. 





<sup>Zhao, R. & Smits, A. J.</sup> 2007 Scaling of the wall-normal turbulence component in high-Reynoldsnumber pipe flow. J. Fluid Mech. 576, 457–473. 

