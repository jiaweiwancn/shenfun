# Simple Eulerian time correlation of full-and narrow-band velocity signals in grid-generated isotropic turbulence

By GENEVIÈVE COMTE-BELLOT
École Centrale de Lyon 

AND STANLEY CORRSIN 

The Johns Hopkins University 

(Received 2 July 1970) 

Space-time correlation measurements in the roughly isotropic turbulence behind a regular grid spanning a uniform airstream give the simplest Eulerian time correlation if we choose for the upstream probe signal a time delay which just 'cancels' the mean flow displacement. The correlation coefficient of turbulent velocities passed through matched narrow-band filters shows a strong dependence on nominal filter frequency ( $\sim$ wave-number at these small turbulence levels). With plausible scaling of the time separations, a scaling dependent on both wavenumber and time, it is possible to effect a good collapse of the correlation functions corresponding to wave-numbers from $0\cdot5~cm^{-1}$ , the location of the peak in the three-dimensional spectrum, to $10~cm^{-1}$ , about half the Kolmogorov wave-number. The spectrally local time-scaling factor is a 'parallel' combination of the times characterizing (i) gross strain distortion by larger eddies, (ii) wrinkling distortion by smaller eddies, (iii) convection by larger eddies and (iv) gross rotation by larger eddies. 

## CONTENTS

1. Introduction page 274  
2. Fluid mechanical apparatus 284  
3. Measuring equipment 285  
4. Experimental and computational procedures 288  
5. Experimental results for one-time or one-probe functions 291  
6. The Taylor approximation and a.c. coupling 300  
7. Results for full-band, two-time correlation function moving with the mean motion 301  
8. Approximate rescaling for downstream homogeneity (stationarity in convected frame) 303  
9. Time delay for maximum correlation with two probes 305  
10. Narrow-band, two-time velocity correlation function following the mean flow 307  
11. Computation of narrow-band correlations with mean convective delay from-fullband correlations with all delays 312 

12. Similarity rescaling of the spectrally local correlation functions 314  
Appendix A. Minimization of error due to wake effect of upstream probe 319  
Appendix B. Effect of finite widths of narrow-band filters 321  
Appendix C. Tape recorder deficiencies 324  
Appendix D. The interpretation of time dependence at a point in the tunnel as space dependence: the Taylor approximation 325  
Appendix E. Estimation of integral scale values 330  
REFERENCES 334 

## 1. Introduction

A modest approximation to isotropic turbulence is achieved downstream of a regular grid spanning uniform duct flow (Taylor 1935; Dryden, Schubauer, Mock & Skramstad 1937; Macphail 1940; for further bibliography, Comte-Bellot & Corrsin 1966). The simplicity of Taylor's isotropic turbulence concept has permitted the raising of rather sophisticated theoretical questions. The transverse homogeneity and absence of mean shear in the grid-generated, nearly isotropic turbulence permit relatively complete statistical information to be provided by fewer measurements than will be required for the classical shear flows, such as boundary layer, wake, jet and channel. 

Isotropic turbulence is turbulence whose statistical properties are invariant under all axis rotations and reflexions. Since physically interesting properties include joint probabilities of field variables at two or more space points, isotropy requires homogeneity as well. For simplicity the motion is restricted to be that of a constant density, Newtonian fluid with zero mean velocity everywhere, in an inertial frame. We visualize an infinite space of random, vortical motion, decaying with the passage of time because there is no production of turbulent kinetic energy (as there is in shear flows) to balance the viscous dissipation. 

No one appears yet to have developed a viable experiment in a 'box', which approximates the spatially homogeneous, temporally decaying turbulence described above. Simmons & Salter (1934) discovered that the streamwise evolution of the temporally stationary turbulence field set up by a regular grid spanning a steady, uniform duct flow resembles the time evolution of the mathematical ideal of isotropic turbulence. They and later investigators found that the turbulence is indeed nearly isotropic (for bibliographies see Batchelor 1953; Comte-Bellot & Corrsin 1966). The comparison between this class of experiments and isotropic turbulence theory is commonly made by interpreting streamwise distance $\Delta x_{1}$ in the experiment as time interval $\Delta t$ in the true isotropic turbulence divided by the mean speed $\overline{U}$ of the actual flow in the experimental duct: $\Delta x_{1} \to \overline{U} \Delta t$ . We imagine that an observer travelling at the mean speed of the duct flow will see something like true isotropic turbulence, evolving in time. 

Two-space-point, one-time, double velocity covariance functions have been regular features of research in isotropic turbulence since Taylor introduced the concept and the laboratory approximation in 1935. Frequency spectra were also first associated with turbulence by Taylor (1938), and the signals from single, fixed probes (usually hot-wire anemometers) have been so analyzed since that time. With the low turbulence levels found in the flow region (behind a grid) in which satisfactory transverse homogeneity is found, these are virtually one-dimensional wave-number spectra; hence they are an approximate check on the measured two-point spatial covariances which are their Fourier transforms. Stewart & Townsend (1951) carried out the first systematic measurements of two-space-point, one-time, triple velocity covariance functions, related to the wave-number spectral transfer function, attacked somewhat earlier in theory by Obukhov (1941), Onsager (1945, 1949), Heisenberg (1948), Kovasznay (1948) and others. 

Another dimension was added to the experimental onslaught in the late 1940's and early 1950's, when Favre (1948) and Favre, Gaviglio & Dumas (1950, 1952) made the first systematic measurements of double velocity correlation with separation in both space and time. This was done by recording on magnetic tape the signals from two hot-wires at different spatial positions in the flow, then playing them back with one head shifted along the tape to give a time shift. 

Of particular interest is the time shift which allows the mean velocity to give a flow displacement exactly equal to the probe spatial separation. The corresponding correlation function in time is precisely that which would be measured as autocorrelation by a probe travelling steadily at the mean velocity. It is conceptually the simplest Eulerian correlation function in time; its Fourier transform is the simplest Eulerian frequency spectrum. Hopefully, it corresponds approximately to the fixed point velocity correlation function in a true isotropic (decaying) 'box' turbulence. 

The following were the objectives of the study reported here: 

(i) To extend the experiments of Favre, Gaviglio & Dumas to longer (dimensionless) times for this ‘simple’ Eulerian correlation function following the mean flow. 

(ii) To measure the corresponding correlation functions for very narrow-band, filtered velocity signals, roughly a study of the coherence in time of spatial 'Fourier elements'. The correlation in time of a Fourier element was introduced to turbulence theory by Heisenberg (1948), and has been extensively studied by Kraichnan (1959, etc.) and others.† 

(iii) To devise a rescaling of the (full-band) Eulerian velocity time-correlation which would compensate for the inhomogeneity associated with the inevitable downstream decay of the 'isotropic' turbulence. This would provide theoreticians with a semi-experimental estimate of a basic property of stationary isotropic turbulence. Such a flow is impossible in practice, but convenient for theoretical analysis. In turbulent shear flow, which can be stationary, there are two things destroying the autocorrelation following the mean flow: the 'self-scrambling', which is the entire story in isotropic turbulence, and the straining and rotation associated with the mean velocity gradient (and higher derivatives). In the present experiment, as in isotropic turbulence, only the former exists. 

(iv) To discover a detailed time or frequency spectral rescaling of the three-dimensional, narrow-band correlation functions, such that time-correlation curves for signals of different wave-numbers can all be collapsed into a single curve. 

The first theoretical estimate of a simple velocity correlation function in time was by Inoue (1951) for the Lagrangian case.† Assuming quasi-stationarity, and restricting discussion to a locally isotropic inertial subrange in the spirit of Kolmogorov (1941), he showed that the hypothesis of dependence on solely the energy flux through this part of the frequency space (equal to the total rate of viscous dissipation) gives a linear region in the autocorrelation function: 

$$
_ {L} R _ {1 1} (\Delta t) = 1 - C \frac {\epsilon}{u _ {1} ^ {2}} \Delta t.\tag{1}
$$

The corresponding form of inertial spectral range as a function of frequency is 

$$
_ {L} E \sim \epsilon \omega^ {- 2}.\tag{2}
$$

$\epsilon$ is the rate of dissipation of kinetic energy per unit mass. $C$ is a constant. $\overline{u_1^2}$ is the mean-square value of a turbulent velocity component. Corrsin (1963a) remarked that the same approach, if applied to the Eulerian functions, must yield the same subrange forms. 

Burgers (1951) appears to suggest that under some circumstances the Eulerian function may be nearly equal to the Lagrangian one, because of the possible negligibility of the non-linear (convective) terms in the Eulerian frame expression for acceleration: $[\partial u_{i}]$ $[\partial u_{j}]$ $[\partial u_{k}]$ 

$$
\left[ \frac {\partial u _ {1}}{\partial t} \right] _ {\mathbf {x} _ {0}} = \left[ \frac {\partial u _ {1}}{\partial t} \right] _ {\mathbf {x}} + u _ {j} \left[ \frac {\partial u _ {1}}{\partial x _ {j}} \right] _ {t}\tag{3a}
$$

$$
\approx \left[ \frac {\partial u _ {1}}{\partial t} \right] _ {\mathbf {x}}?\tag{3b}
$$

The subscript denotes the variable held constant. $X_{0}$ is the Lagrangian material co-ordinate, such as particle position at a reference time. If a similar conjecture is valid for higher time derivatives, which enter the two power series for velocity correlations in the two frames, then we could infer approximate equality of the functions themselves. This suggestion has been confirmed to a certain extent by some ‘correlation discard’ computations of Deissler (1961) in isotropic turbulence. Although neither he nor Burgers offered a theoretical argument for $(3b)$ , other than the fact that the neglected terms are of higher power in turbulent velocity, a ‘small’ quantity, a rationale is easy to find. Since velocity is dimensional, and since the basic Eulerian frame is one in which the mean speed is zero, smallness of turbulent velocity is not a directly defined concept; we must investigate further. The ratio of the order of magnitude of the (neglected) convective term to that of the left side of $(3a)$ , the acceleration (Uberoi & Corrsin 1953), decreases with decreasing turbulence Reynolds number. Deissler’s calculation is a small Reynolds number calculation, and the agreement with experiment improves with decreasing $R_{\lambda}$ . 

Burgers' suggestion seems to work roughly for large Reynolds numbers as well (Baldwin & Walsh 1961; Baldwin & Mickelsen 1962; Corrsin 1962b), but this must be for entirely different reasons (Corrsin 1963a). 

Bass (1954) has explored some of the properties, primarily kinematic, of the space-time Eulerian velocity correlation function. This path has been followed further by Meecham (1958), with emphasis on symmetries. Batchelor & Townsend (1948) had generalized the Kármán–Howarth ‘final period’ correlation (vanishingly small Reynolds number) solution to include time as well as space separation. Their results include e.g. the small $\Delta t$ asymptotic form, 

$$
R _ {1 1} (\Delta x _ {1}, 0, 0; t _ {0}, t) \rightarrow \left[ 1 - \frac {(\Delta t) ^ {2}}{4 t ^ {2}} \right] ^ {\frac {5}{4}} \exp \left\{- \frac {(\Delta x _ {1}) ^ {2}}{8 \nu t} \right\},\tag{4}
$$

where $\Delta t \equiv t - t_{0}$ , for correlation between two velocity components directed along the line connecting the observation points. This analysis, the first step in the ‘correlation discard’ sequence, was extended by Deissler (1961) to the next step. 

Favre (1965) has suggested that the Eulerian space-time correlation function can be estimated from the Eulerian space correlation, and the Lagrangian probability density function of material point displacement. Although his formula is in fair agreement with an experiment, this may be fortuitous: it appears that the actual expression tested is implicitly restricted to vanishingly small time separations (such that the Lagrangian autocorrelation is $1 \cdot 0$ ), but the comparison with experiment is made well outside of that asymptotic limit. 

The autocorrelation function in time of a spatial Fourier element $\mathbf{a}(\mathbf{k},t)$ can be identified by following Heisenberg and Kraichnan in expressing the Eulerian turbulent velocity field as a Fourier series: 

$$
\mathbf {u} (\mathbf {x}, t) = \sum_ {\mathbf {k}} \mathbf {a} (\mathbf {k}, t) e ^ {i \mathbf {k} \cdot \mathbf {x}}.\tag{5}
$$

Here k is a wave-number, and it is understood that the physically interesting limit will be a 'box' so large that wave-number spectra such as the spectral energy density, 

$$
{ } _ { B } e _ { 1 1 } ( \mathbf { k } , t ) = \operatorname * { l i m } _ { \mathcal { L } \to \infty } \left\{ \left( \frac { \mathcal { L } } { 2 \pi } \right) ^ { 3 } \overline { { a _ { 1 } ( \mathbf { k } , t ) a _ { 1 } ^ { * } ( \mathbf { k } , t ) } } \right\} ,\tag{6}
$$

can be treated as smooth functions, or can be replaced by them in the sense of Wiener (Wiener 1930; Kampé de Fériet 1939, 1953). The presubscript B denotes a property of an isotropic 'box' turbulence. The overbar denotes average. It is most simply ensemble average in theoretical analysis, usually time average in experiments. Ergodicity is expected in these flows because the integral scales are less than infinity (see e.g. Liepmann 1951). The asterisk denotes complex conjugate. 

The time covariance tensor of $\mathbf{a}$ is 

$$
{ } _ { B } \tilde { e } _ { j l } ( \mathbf { k } ; t _ { 0 } , t ) = \operatorname * { l i m } _ { \mathcal { L } \to \infty } \left\{ \left( \frac { \mathcal { L } } { 2 \pi } \right) ^ { 3 } \overline { { a _ { j } ( \mathbf { k } , t _ { 0 } ) a _ { l } ^ { * } ( \mathbf { k } , t ) } } \right\} .\tag{7}
$$

We can avoid concern over the limiting process by starting with the velocity covariance tensor, $\overline{u_{i}(\mathbf{x}_{0},t_{0}) u_{j}(\mathbf{x},t)}$ . 

If we restrict to homogeneity, this function depends on $r \equiv x - x_{0}$ , instead of the two positions. Then, introducing the symbol 

$$
{ } _ { B } \rho _ { i j } ( \mathbf { r } ; t _ { 0 } , t ) \equiv \overline { { u _ { i } ( \mathbf { x } _ { 0 } , t _ { 0 } ) u _ { j } ( \mathbf { x } _ { 0 } + \mathbf { r } , t ) } } ,\tag{8}
$$

we can replace (7) by 

$$
{ } _ { B } \tilde { e } _ { i j } ( \mathbf { k } ; t _ { 0 } , t ) = \left( \frac { 1 } { 2 \pi } \right) ^ { 3 } \iiint _ { - \infty } ^ { \infty } { } _ { B } \rho _ { i j } ( \mathbf { r } ; t _ { 0 } , t ) e ^ { - i \mathbf { k } . \mathbf { r } } d V ( \mathbf { r } ) .\tag{9}
$$

The inverse of (9) is 

$$
{ } _ { B } \rho _ { i j } ( \mathbf { r } ; t _ { 0 } , t ) = \iiint _ { - \infty } ^ { \infty } { } _ { B } \tilde { e } _ { i j } ( \mathbf { k } ; t _ { 0 } , t )   e ^ { i \mathbf { k } . \mathbf { r } } d V ( \mathbf { k } ) .\tag{10}
$$

The traces, $_B\rho_{jj} \equiv _B\rho(r; t_0, t)$ and $_B\tilde{e}_{ii} \equiv _B\tilde{e}(k; t_0, t)$ , are simple yet important. The simplicity lies in their spherical symmetry for isotropic turbulence. Their importance lies in their close connexion to the turbulent kinetic energy per unit mass: 

$$
{ } _ { B } \rho ( 0 ; t , t ) = \overline { { u _ { j } ( \mathbf { x } , t ) u _ { j } ( \mathbf { x } , t ) } } = 4 \pi \int _ { 0 } ^ { \infty } { } _ { B } \tilde { e } ( k ; t , t ) k ^ { 2 } d k .\tag{11}
$$

The two-time generalizations of the commonly studied 'one-dimensional spectrum function' (e.g. Batchelor 1953, p. 50) are the projections onto Cartesian k-axes of $_{B}\tilde{e}_{ij}(\mathbf{k};t_{0},t)$ , the generalization of the spectral tensor. These functions are important because they are experimentally accessible. The projection onto $k_{1}$ is e.g. proportional to 

$$
{ } _ { B } \mathcal { E } _ { i j } ^ { ( 1 ) } ( k _ { 1 } ; t _ { 0 } , t ) = 2 \iint _ { - \infty } ^ { \infty } { } _ { B } \tilde { e } _ { i j } ( \mathbf { k } ; t _ { 0 } , t ) d k _ { 2 } d k _ { 3 } .\tag{12}
$$

We see from (10) that 

$$
{ } _ { B } \rho _ { i j } ( r _ { 1 } , 0 , 0 ; t _ { 0 } , t ) = \int _ { 0 } ^ { \infty } { } _ { B } \mathcal { E } _ { i j } ^ { ( 1 ) } ( k _ { 1 } ; t _ { 0 } , t ) e ^ { i k _ { 1 } r _ { 1 } } d k _ { 1 } ,\tag{13}
$$

with inverse Fourier transform 

$$
{ } _ { B } \mathcal { E } _ { i j } ^ { ( 1 ) } ( k _ { 1 } ; t _ { 0 } , t ) = \frac { 2 } { \pi } \int _ { 0 } ^ { \infty } { } _ { B } \rho _ { i j } ( r _ { 1 } , 0 , 0 ; t _ { 0 } , t ) e ^ { - i k _ { 1 } r _ { 1 } } d r _ { 1 } .\tag{14}
$$

These covariance functions are easily normalized into correlation coefficient functions (to be called ‘correlation functions’ here): 

$$
{ } _ { B } R _ { i j } ^ { ( 1 ) } ( k _ { 1 } ; t _ { 0 } , t ) \equiv \frac { { } _ { B } \mathcal { E } _ { i j } ^ { ( 1 ) } ( k _ { 1 } ; t _ { 0 } , t ) } { \left\{ { } _ { B } \mathcal { E } _ { ( i ) ( i ) } ^ { ( 1 ) } ( k _ { 1 } ; t _ { 0 } , t _ { 0 } ) \right. } { } _ { B } \mathcal { E } _ { ( j ) ( j ) } ^ { ( 1 ) } ( k _ { 1 } ; t , t ) \} ^ { \frac { 1 } { 2 } } .\tag{15}
$$

The bracketed subscripts are not summed. The $_{B}\mathcal{E}_{(n)(n)}^{(1)}(k_{1};t,t)$ are ordinary ‘one-dimensional’ energy spectra, henceforth written as $_{B}E_{(n)(n)}^{(1)}(k_{1},t)$ . With space separation r, we have 

$$
{ } _ { B } R _ { i j } ( \mathbf { r } ; t _ { 0 } , t ) \equiv \frac { { } _ { B } \rho _ { i j } ( \mathbf { r } ; t _ { 0 } , t ) } { \left\{ { } _ { B } \rho _ { ( i ) ( i ) } ( 0 ; t _ { 0 } , t _ { 0 } ) \right. _ { B } \rho _ { ( j ) ( j ) } ( 0 ; t , t ) \} ^ { \frac { 1 } { 2 } } } ,\tag{16}
$$

where $\pmb{B}\rho_{(n)(n)}(0;t,t)$ is simply $\overline{u_n^2}$ (subscript not summed). With (14) and (16) we can put (15) into the form 

$$
\begin{array}{r l} _ {B} R _ {i j} ^ {(1)} (k _ {1}; t _ {0}, t) & = \frac {\int_ {0} ^ {\infty} {} _ {B} R _ {i j} (r _ {1} , 0 , 0 ; t _ {0} , t) e ^ {- i k _ {1} r _ {1}} d r _ {1}}{\left\{\int_ {0} ^ {\infty} {} _ {B} R _ {(i) (i)} (r _ {1} , 0 , 0 ; t _ {0} , t _ {0}) \cos (k _ {1} r _ {1}) d r _ {1} \int_ {0} ^ {\infty} {} _ {B} R _ {(j) (j)} (r _ {1} , 0 , 0 ; t , t) \cos (k _ {1} r _ {1}) d r _ {1} \right\} ^ {\frac {1}{2}}}. \end{array}
$$

The $_B R_{(n)(n)}$ are even in r. 

(17) 

Favre, Gaviglio & Dumas (1952) measured functions like $_{B}R_{ij}$ in the (inhomogeneous, nearly isotropic) turbulence behind a periodic grid, and pointed out (1954) that the (wave-number) spectrally local time correlation function $_{B}R_{ij}^{(m)}$ can be computed from it. Goal (ii) above was to measure $_{B}R_{11}^{(1)}$ directly. 

$_{B}R_{ij}$ can in turn be computed from $_{B}R_{pq}^{(m)}$ , but in that case the simple spectra must also be given: starting with (13) instead of (14) and using (15), we can show e.g. that 

$$
{ } _ { B } R _ { i j } ( r _ { 1 } , 0 , 0 ; t _ { 0 } , t ) = \frac { \int _ { 0 } ^ { \infty } { } _ { B } R _ { i j } ^ { ( 1 ) } ( k _ { 1 } ; t _ { 0 } , t ) \left[ { } _ { B } E _ { ( i ) ( i ) } ^ { ( 1 ) } ( k _ { 1 } , t _ { 0 } ) \right. { } _ { B } E _ { ( j ) ( j ) } ^ { ( 1 ) } ( k _ { 1 } , t ) ] ^ { \frac { 1 } { 2 } } e ^ { - i k _ { 1 } r _ { 1 } } d k _ { 1 } } { \overline { { \{ u _ { i } ^ { 2 } ( t _ { 0 } ) \overline { { u _ { j } ^ { 2 } ( t ) } } \} ^ { \frac { 1 } { 2 } } } } } .\tag{18}
$$

The $\overline{u_n^2}$ are, of course, just the integrals of the $B E_{(n)(n)}^{(1)}$ over $k_{1}$ . 

For theoretical exploration of isotropic turbulence, the so-called 'three-dimensional spectrum' $_{B}E(k,t)$ is a popular goal. $_{B}E(k,t)dk$ is the energy content of a differentially thick spherical shell in wave-number space, so 

$$
{ } _ { B } E ( k , t ) = 2 \pi k ^ { 2 } { } _ { B } \tilde { e } _ { i i } ( k ; t , t ) .\tag{19}
$$

$_{B}\tilde{e}_{ii}(k;t,t)$ is twice the (spherically symmetric) kinetic energy density in k-space. Its integral over all of k-space is $u_{\alpha}u_{\alpha}$ , while $_{B}E$ is defined to have its integral over k, hence over all of k-space, equal to $\frac{1}{2}u_{\alpha}u_{\alpha}$ . 

The generalization of ${}_{B}E(k,t)$ is thus 

$$
{ } _ { B } \mathcal { E } ( k ; t _ { 0 } , t ) = 2 \pi k ^ { 2 } { } _ { B } \tilde { e } _ { i i } ( k ; t _ { 0 } , t ) ,\tag{20}
$$

whose connexion with $_{B}\mathcal{C}_{ij}^{(n)}$ is identical to that between the spectra.† For example, 

$$
{ } _ { B } \mathcal { E } ( k ; t _ { 0 } , t ) = \frac { 1 } { 2 } k ^ { 3 } \frac { \partial } { \partial k } \left[ \frac { 1 } { k } \frac { \partial } { \partial k } { } _ { B } \mathcal { E } _ { 1 1 } ^ { ( 1 ) } ( k ; t _ { 0 } , t ) \right] .\tag{21}
$$

We can define a ‘three-dimensional’ correlation function, 

$$
{ } _ { B } R ( k ; t _ { 0 } , t ) \equiv \frac { { } _ { B } \mathcal { E } ( k ; t _ { 0 } , t ) } { \{ { } _ { B } E ( k , t _ { 0 } ) { } _ { B } E ( k , t ) \} ^ { \frac { 1 } { 2 } } } .\tag{22}
$$

With (15) and (21), $_{B}R$ can be expressed partly in terms of one-dimensional correlation functions (in time) and spatial spectra: 

$$
{ } _ { B } R ( k ; t _ { 0 } , t ) = \frac { \frac { 1 } { 2 } k ^ { 3 } \frac { \partial } { \partial k } \left\{ \frac { 1 } { k } \frac { \partial } { \partial k } \left[ _ { B } R _ { 1 1 } ^ { ( 1 ) } ( k ; t _ { 0 } , t ) \left\{ _ { B } E _ { 1 1 } ^ { ( 1 ) } ( k , t _ { 0 } ) _ { B } E _ { 1 1 } ^ { ( 1 ) } ( k , t ) \right\} ^ { \frac { 1 } { 2 } } \right] \right\} } { \left\{ _ { B } E ( k , t _ { 0 } ) _ { B } E ( k , t ) \right\} ^ { \frac { 1 } { 2 } } } .\tag{23}
$$

$_{B}E(k,t)$ is of course computable from $_{B}\mathcal{E}_{11}^{(1)}(k_{1};t,t)\equiv_{B}E_{11}^{(1)}(k_{1},t)$ via (21). 

Experimental determination of the wind tunnel turbulence function corresponding to $_{B}R(k;t_{0},t)$ is one of the major goals of the present work.‡ All of the foregoing discussion is relevant to isotropic ‘box turbulence’, i.e. isotropic (hence homogeneous) turbulence viewed in an Eulerian frame in which there is no average velocity. The experiment, however, is carried out in the stationary, inhomogeneous, nearly isotropic turbulence behind a grid normal to a uniform, steady flow. There is clearly a question of how to establish an approximate correspondence between these two somewhat different flows (Corrsin 1963b). 

Basically, we follow Taylor (1935) in identifying $(x_{1}-x_{0_{1}})/\overline{U}$ in the wind tunnel flow with $t-t_{0}$ in the box turbulence. Thus, the spatial inhomogeneity of mean properties, (such as kinetic energy $\frac{1}{2}\overline{u_{i}u_{i}}(x_{1}/\overline{U})$ ), is identified with the temporal decay of the same properties (e.g. $\frac{1}{2}\overline{u_{i}u_{i}}(t)$ ) in the box turbulence. Of course, the quasi-box-turbulence observed in the frame travelling with mean flow speed is still inhomogeneous. $x_{1}$ is the downwind $(\overline{U})$ Cartesian co-ordinate in the wind tunnel (figure 1). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/4e0e9874dc787ccb33210fa1d3a71a743d46fba4abf8df5e489398d4b8f1213b.jpg)



FIGURE 1. Qualitative sketch of upstream end of wind-tunnel test section.


Among the quantities actually measured in the wind tunnel was the two-point, space-time velocity correlation function, 

$$
\frac {\overline {{u _ {1} (\mathbf {x} _ {0} , t ^ {\prime}) u _ {1} (\mathbf {x} , t ^ {\prime} + \Delta t ^ {\prime})}}}{[ \overline {{u _ {1} ^ {2}}} (x _ {0 _ {1}}) \overline {{u _ {1} ^ {2}}} (x _ {1}) ] ^ {\frac {1}{2}}}.\tag{24}
$$

In laboratory co-ordinates the mean-square values depend on downstream distance only. A major hope is that when the time interval is chosen exactly equal to the mean flow convection time between probes, i.e. 

$$
\Delta t ^ {\prime} = \frac {\Delta x _ {1}}{\overline {{{U}}}} \equiv \frac {x _ {1} - x _ {0 _ {1}}}{\overline {{{U}}}},\tag{25}
$$

(24) will approximate the one-space-point velocity autocorrelation in time which would occur in a decaying, isotropic, box turbulence: 

$$
\frac {\overline {{u _ {1} \left(x _ {0 _ {1}} , x _ {0 _ {2}} , x _ {0 _ {3}} , t ^ {\prime}\right) u _ {1} \left[ x _ {0 _ {1}} + \Delta x _ {1} , x _ {0 _ {2}} , x _ {0 _ {3}} , t ^ {\prime} + (\Delta x _ {1} / \bar {U}) \right]}}}\overline {{\left[ u _ {1} ^ {2} \left(x _ {0 _ {1}}\right) u _ {1} ^ {2} \left(x _ {0 _ {1}} + \Delta x _ {1}\right) \right] ^ {\frac {1}{2}}}} = \dot {} _ {B} R _ {\mathbf {1 1}} [ 0, 0, 0; t _ {0}, t _ {0} + (\Delta x _ {1} / \bar {U}) ].\tag{26}
$$

The arguments on the two sides of (26) as written are different. The correspondence is between $x_{0_{1}}$ in the wind tunnel and $t_{0}$ in the box turbulence. $x_{0_{1}}$ is the downstream distance from the grid to the upstream probe. $t_{0}$ is the beginning of the time interval in the box turbulence time correlation. We also use $t_{0}$ as the beginning of the time intervals for the space-time correlations in the wind tunnel. When the wind tunnel turbulence is viewed in a frame moving with the mean flow speed, 

$$
t _ {0} = \int_ {0} ^ {x _ {0 _ {1}}} \frac {d x _ {1}}{\overline {{U}} (x _ {1})}.
$$

Of course, $\overline{U}$ is constant in the entire experimental volume, downstream of the duct contraction. In this moving frame we shall denote the experimental function 

<table><tr><td rowspan="7">or</td><td>Wind tunnel turbulence</td><td>Box turbulence</td></tr><tr><td><eq>R_{ij}(\Delta x_1, \Delta x_2, \Delta x_3; t, 0)</eq></td><td><eq>_B R_{ij}(\Delta x_1, \Delta x_2, \Delta x_3; t, t).</eq>Two-space-point, one-time, double velocity correlation function ((16) and (8), with <eq>t_0 = t</eq>).</td></tr><tr><td><eq>R_{11}(\overline{U}\Delta t, 0, 0; t_0, \Delta t)</eq><eq>R_{11}\left(\Delta x_1, 0, 0; t_0, \frac{\Delta x_1}{\overline{U}}\right)</eq></td><td><eq>_B R_{11}(0; t_0, t_0 + \Delta t).</eq>Two-time, one-space-point, double velocity correlation function. Shortly called ‘full-band Eulerian velocity time-correlation’ ((16) and (8), with r = 0)</td></tr><tr><td><eq>R_{11}^{(1)}(k_1; \overline{U}\Delta t, 0, 0; t_0, \Delta t)</eq></td><td><eq>_B R_{11}^{(1)}(k_1; t_0, t_0 + \Delta t).</eq>One-dimensional narrow-band Eulerian velocity time-correlation ((15), (12), (7), and (5))</td></tr><tr><td><eq>R(k; \overline{U}\Delta t, 0, 0; t_0, \Delta t)</eq></td><td><eq>_B R(k; t_0, t_0 + \Delta t).</eq>Three-dimensional narrow-band Eulerian velocity time-correlation ((22), (20), (7), and (5))</td></tr><tr><td><eq>E_{11}^{(1)}(k_1, t)</eq></td><td><eq>_B E_{11}^{(1)}(k_1, t).</eq>One-dimensional spectrum of <eq>\widehat{u_1^2}</eq></td></tr><tr><td><eq>E(k, t)</eq></td><td><eq>_B E(k, t)</eq>Three-dimensional energy spectrum</td></tr><tr><td colspan="3">TABLE 1. Notation for correlation and spectrum functions</td></tr></table>

on the left side of (26) by $R_{11}[\Delta x_{1},0,0;t_{0},(\Delta x_{1}/\overline{U})]$ . Table 1 presents the correlation and spectrum symbols to be used, together with their ‘analogues’ in the box turbulence problem. 

This $R_{11}$ function is roughly the envelope of the more general space-time correlation functions, and was first measured by Favre, Gaviglio & Dumas (1952). 

To get a spatial Fourier decomposition of $R_{11}$ (analogous to $_{B}R_{11}^{(1)}$ ), measurements were made of the same kind of space-time correlation with the two velocity signals passed through very narrow-band frequency filters. To the extent that 

$$
\frac {\partial}{\partial t} (\mathbf {\Theta}) = - \overline {{{U}}} \frac {\partial}{\partial x} (\mathbf {\Theta}),\tag{27}
$$

for the turbulent velocity field viewed in laboratory co-ordinates (an approximation suggested by Taylor 1938), the frequency spectral decomposition of the hot-wire signal is a wave-number spectral decomposition of the turbulence itself. This is discussed in appendix D. The correspondence indicated by (27) is simply 

$$
\omega \doteq \overline {{U}} k _ {1}.\tag{28}
$$

$\omega$ is the centre frequency of the matched narrow-band filters. With this equivalence, we expect that for the special time delay $\Delta t = \Delta x_{1}/\overline{U}$ , the spectrally local version of (26) will also apply 

$$
R _ {1 1} ^ {(1)} \left(k _ {1}; \Delta x _ {1}, 0, 0; t _ {0}, \frac {\Delta x _ {1}}{\overline {{U}}}\right) \doteq {} _ {B} R _ {1 1} ^ {(1)} \left(k _ {1}; t _ {0}, t _ {0} + \frac {\Delta x _ {1}}{\overline {{U}}}\right).\tag{29}
$$

$R_{11}^{(1)}$ is written for convenience with $k_{1}$ instead of $\omega/\overline{U}$ as first argument, although the filter is in frequency. This is an application of the 'Taylor approximation'. 

Since the grid-generated turbulence is approximately isotropic, we can compute a 'three-dimensional' $R$ from $R_{11}^{(1)}$ and the (simpler) spectrum functions, by an equation whose form is precisely that of (23). 

For stationary turbulence and 'small' time interval, presumably identified by the condition, 

$$
1 - _ {B} \hat {R} (k, \Delta t) \ll 1,\tag{30)†}
$$

Heisenberg (1948) suggested that the characteristic time should be $(u^{\prime}k)^{-1}$ . This is the time required for the large, energy-bearing structure of the turbulence to convect smaller structure of wave-number k a distance equal to $(2\pi)^{-1}$ times the wavelength of the smaller structure. $u^{\prime}$ is the root-mean-square value of a component of the isotropic turbulent velocity. In this small-time range his estimate (whose basis is not explained) is given as 

$$
{ } _ { B } \hat { R } ( k , \Delta t ) \approx 1 - \frac { \Delta t } { 3 ^ { \frac { 1 } { 2 } } \tau _ { H } } \exp \left[ - \frac { 1 } { 1 2 } \left( \frac { \Delta t } { \tau _ { H } } \right) ^ { 2 } \right] \int _ { 0 } ^ { \frac { \Delta t } { ( 1 2 ) ^ { 4 } \tau _ { H } } } \exp \left( \alpha ^ { 2 } \right) d \alpha ,\tag{31}
$$

where $\tau_H \equiv (u'k)^{-1}$ . For $\Delta t \to 0$ , 

$$
_ B \hat {R} (k, \Delta t) \rightarrow 1 - \frac {1}{6} (\Delta t / \tau_ {H}) ^ {2},\tag{32}
$$

which gives an estimate of the simplest Eulerian, narrow-band, time microscale: 

$$
_ {k} t _ {\lambda} = 6 ^ {\frac {1}{2}} (u ^ {\prime} k) ^ {- 1}.\tag{33}
$$

Heisenberg's estimate of $_B\hat{R}(k,\Delta t)$ for 'large' $\Delta t$ requires a trial-and-error solution of an integro-differential equation, and he presents a figure of the result. His analysis includes replacing a fourth moment in terms of second moments as though the narrow-band velocity components are jointly normal. It has since been discovered that 'cumulant discard' hypotheses in turbulence analysis can lead to negative energy spectra when applied to 'full-band' variables in the physical space (O'Brien & Francis 1962; Ogura 1963). On the other hand, it was shown analytically by Rice (1944, 1945) that a particular non-normal 

$$
\dagger_ {B} \hat {R} (k, \Delta t) \equiv {} _ {B} R (k, t _ {0}, t _ {0} + \Delta t) \text {   in   stationary   turbulence. }
$$

random function passed through a band-pass filter approaches normality as the band width is reduced. Presumably this applies to other non-normal signals. Recent remarks on this question as related to turbulence dynamics have been made by Lumley (1970). 

A final remark here about Heisenberg's discussion: he suggests that for 'large' time intervals the characteristic spectral time scale should be $\tau_W \equiv (u' k_E^{\frac{1}{2}} k^{\frac{2}{3}})^{-1}$ , a time introduced by von Weizsäcker (1948) for the inertial subrange, where the Kolmogorov spectrum ( $\approx \epsilon^{\frac{2}{3}} k^{-\frac{5}{3}}$ ) pertains. As we shall see in § 12, this is a special case of the Onsager (1945, 1949) time $\tau_0 \equiv (k^3 E)^{-\frac{1}{2}}$ . $E(k)$ is the three-dimensional spectrum function (equation (19)), $k_E$ is the wave-number characterizing the principal energy-bearing part of the spectrum, roughly the inverse integral length scale and the location of the $E(k)$ peak. $\epsilon$ is the rate of dissipation of kinetic energy per unit mass. 

Kraichnan (1959) has followed Heisenberg in pursuing $_{B}\hat{R}(k,\Delta t)$ in his turbulence theories. A linearized estimate in the inertial range of k-space yielded 

$$
{ } _ { B } \hat { R } ( k , \Delta t ) \approx \int _ { - \infty } ^ { \infty } \exp \left( i k \Delta t \alpha \right) p _ { u _ { 1 } } ( \alpha ) d \alpha ,\tag{34}
$$

where $p_{u_{1}}$ is the probability density function of any velocity component. Empirically, $p_{u_{1}}$ is normal ('Gaussian') in 'isotropic' grid-generated turbulence (Simmons & Salter 1938; Townsend 1947), so 

$$
{ } _ { B } \hat { R } ( k , \Delta t ) \approx \exp [ - \frac { 1 } { 2 } u ^ { \prime 2 } k ^ { 2 } ( \Delta t ) ^ { 2 } ] .\tag{35}
$$

By his Eulerian ‘direct interaction approximation’, Kraichnan (1959) estimated $_{B}\hat{R}$ in a wave-number range where 

$$
\nu k ^ {2} \ll u ^ {\prime} k.\tag{36}
$$

The estimate is 

$$
{ } _ { B } \hat { R } ( k , \Delta t ) \approx \frac { J _ { 1 } ( 2 u ^ { \prime } k \Delta t ) } { u ^ { \prime } k \Delta t } ,\tag{37}
$$

and is in good agreement with (35), apart from its oscillatory character. According to Kraichnan (1964a), (37) is not unique. The condition (equation (36)) is that the viscous decay time of the local spectrum, $\tau_{\nu} \equiv (\nu k^{2})^{-1}$ , be much larger than the time, $\tau_{H} \equiv (u'k)^{-1}$ , required for the energetic large structure (near $k_{E}$ ) to convect the k-structure an appreciable fraction of a k-wavelength. For large Reynolds number turbulence, such a sub-range exists in the inertial range. 

Although these first applications of the direct interaction approximation had some shortcomings (see e.g. Kraichnan 1964b, 1966), detailed numerical solutions for the full k-range gave remarkably good agreement with measured one-time functions (1964a). Kraichnan's application of the approximation to a mixed Eulerian–Lagrangian formulation of the equations of motion has been even more successful in estimating turbulent energy spectra (Kraichnan 1966), yet the success of the method is still mysterious from a theoretical point of view, because it is not a perturbation method of proved convergence (Wyld 1961; Kraichnan 1967). 

## 2. Fluid mechanical apparatus

The closed circuit wind tunnel used in this experiment is described in Comte-Bellot & Corrsin (1966). The test section is about 10 m long, with a cross-section $1 \cdot 0 \times 1 \cdot 3$ m. A special feature is a slight secondary contraction located downstream of the grid to equalize the energies of streamwise and transverse turbulent velocity components (figure 1). 

The earlier paper presents turbulent energy data for several grids and tunnel speeds. Virtually all data reported here were taken in the turbulence generated by a biplane, square rod, polished dural grid with mesh size of 5·08 cm and solidity of 0·34. A few correlation values were measured far behind a similar grid of 2·54 cm mesh, to permit reaching larger dimensionless distances and times in the decaying turbulence. 

All measurements were carried out with air speed $U_0$ approaching the grid at 10m sec $^{-1}$ , hence a grid mesh Reynolds number $U_0 M / v$ of 34000 for 5·08 cm grid. The slight (1·27:1) contraction was located 18 mesh lengths downstream of the grid. The streamwise ( $\overline{u_1^2}$ ) and transverse ( $\overline{u_2^2}$ , $\overline{u_3^2}$ ) components' turbulent energies remained nearly equal to each other as they decayed along the length of the test section: 

$$
\left. \begin{array}{c} \frac {U _ {0} ^ {2}}\overline {{u _ {1} ^ {2}}} = 2 1 \left(\frac {U _ {0} t}{M} - 3 \cdot 5\right) ^ {1 \cdot 2 5}, \\ \frac {U _ {0} ^ {2}}\overline {{u _ {2} ^ {2}}} = \frac {U _ {0} ^ {2}}{\overline {{u _ {3} ^ {2}}} \doteq 2 0 \left(\frac {U _ {0} t}{M} - 3 \cdot 5\right) ^ {1 \cdot 2 5}.} \end{array} \right\}\tag{38}
$$

Here, t is elapsed time in travelling at the mean flow velocity from the grid, 

$$
t \equiv \int_ {0} ^ {x _ {1}} \frac {d x _ {1}}{\overline {{U}} (x _ {1})}.\tag{39}
$$

If $\overline{U}$ were exactly constant, $t$ would be just proportional to downstream distance. The integral velocity scale history in this particular decaying turbulence (reported, along with the energy data, in Comte-Bellot & Corrsin 1966) was approximately $I_{\mathrm{e}}(U,t)$ . 

$$
\frac {L}{M} \doteq 0 \cdot 0 4 8 \left(\frac {U _ {0} t}{M} - 3 \cdot 5\right) ^ {0 \cdot 4},\tag{40}
$$

where 

$$
L \equiv \int_ {0} ^ {\infty} R _ {1 1} (0, \Delta x _ {2}, 0; t, 0) d (\Delta x _ {2}),\tag{41)†}
$$

in principle. 

## 3. Measuring equipment

The hot-wire sensors $(2\cdot5\times10^{-4}$ cm dia., platinum-10%-rhodium, from 0·03 to 0·05 cm long, operated at overheat ratios between 0·3 and 0·4), and basic anemometry equipment, were the same as those described in Comte-Bellot & Corrsin (1966). As usual, the wire sensitivities were determined empirically. Additional electronic devices included a multiplier, variable band-pass filters, magnetic tape recorder and electro-chemical integrator. 

The spectral response of the Shapiro/Edwards constant-current hot-wire unit, with nominal cut-off frequencies of 1 Hz (lower) and 20 000 Hz (upper), is shown in figure 2. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/b8c5e8058bf7c12f2adec1ed83af9927978c82c49c1c1aed5bd6bdea20c5676b.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/fbafcfac2859adcfbdeeb3021210038f80027fb46ff09d5857c176165de160b8.jpg)



FIGURE 2. Frequency response of the basic hot-wire anemometer circuit as used. ○, series no. 98–120; ×, series no. 98–122.


The multiplier, used for cross-correlation functions, was a G.P.S. model MU-500-E-M, operating on the 'quarter-square' principle, with squaring achieved by two shaping networks made of 20 diodes each. Tested with sine waves, it showed an accuracy of $\pm 2\%$ over a frequency range of d.c. to $10\mathrm{kHz}$ and an amplitude ratio of about 8. 

The simple power spectra were measured with a Hewlett–Packard model 302 A (constant band width) wave analyzer. The calibration of band shape at a nominal frequency $(N_{0})$ of 80 Hz is given in figure 3(a). Extension to frequencies below the analyzer's lower limit of 20 Hz was achieved by recording a signal on magnetic tape, then playing it back at higher tape speed. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/7756d528c4329c49a8547b3e99235b8aeb541ac4ab82420ceb07563920b1780f.jpg)



(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/e88bde91f97759d695617909478846a60f06d74ea6f27b95fd763f0f3b7adb4a.jpg)



(b)



FIGURE 3. (a) Comparison between the band-pass filter shapes of the Dytronics 720 and the Hewlett-Packard 302 A. (b) The Dytronics 720 band shapes for the three settings. $N_0 = 1\mathrm{kHz}$ , $V_0 = 2V$ r.m.s. (input).


The narrow-band correlations between two different signals (or cross-spectra) were measured with two Model 720 Dytronics Co. filters used on 'medium' bandwidth setting for frequencies below 2 kHz and 'narrow' bandwidth for higher frequencies. This unit has a bandwidth proportional to nominal frequency. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/9107c7627fff2da0c37be58ef53d36fd0a2e70c0600a1961cfad223969ba817f.jpg)



FIGURE 4. Block diagram of data recording and processing system.


Figures 3(a) and (b) give the filter shape calibrations. Some indication of the effect of bandwidth on the measured correlations is given in appendix B. The two Dytronics units proved to be matched within the precision of our measuring procedures. 

The magnetic tape recorder was a modified Sangamo model 482RB with controllable delay for playback, which permitted measurement of correlation functions with time delays. Recording was frequency modulated with a central frequency of 108 kHz. The useful frequency response for correlation measurements was up to roughly 5 kHz limited by tape jitter (about $\pm10\mu$ sec maximum). Some details are given in appendix C. The tape used was Minnesota Mining and Manufacturing Company 'Scotch', $1\cdot5\times10^{-3}$ in. thick, 1 in. wide. The need for segments running up to 5 min with no 'drop-out' meant that the new tapes had to be tested and selected; not all new tapes met the requirement. 2500-foot reels of tape were used. 

The particular type of machine used records and plays back at two separated stations with a loose section of the tape hanging between the two record/playback heads. The tape length between the two heads is kept fixed (at $L_{R}$ ) during the record phase, and then is set at a series of constant lengths $L_{P}$ during the playback phase. The time delay is therefore $V^{-1}(L_{P}-L_{R})$ , where V is tape speed. Ordinarily the system was operated with V = 60 in. sec $^{-1}$ . The zero delay condition, $L_{P} = L_{R}$ , was determined by recording the same random signal on two tracks, then finding the position at which the autocorrelation function was closest to unity. 

For the experiment, the signals from two different hot-wire anemometers, located at different positions in the turbulence, were recorded on two different 'tracks' on the tape, and through the two different heads. A third track was used with a timing signal of 100 kHz to measure the time shift during playback. The counts of this signal were observed with a reversible counter, Wang Laboratories Model R 5720. 

When broad-band random signals are passed through very narrow filters, the filter outputs usually fluctuate wildly, and are thus difficult to read on ordinary pointer or digital meters. We measured these outputs by integration over time intervals long enough to bring the scatter within reason. Integration was done with an electrochemical instrument (The Texas Research and Electronic Co. SI-100 integrator) whose output is a d.c. voltage. This was read with a digital voltmeter, Cubic Corp. Model V46-P. 

The complete schematic diagram for the electrical measuring system is shown in figure 4. 

## 4. Experimental and computational procedures

For all of the two-point space-time correlations reported here, the upstream hot-wire probe was located at $U_{0}t_{0}/M = 42 \pm 2\dagger$ downstream of the grid, and 

$\dagger$ This station was identified by the time symbol $t_{0}$ . The (small) range of values was simply a matter of chance and convenience with different probes, and corresponds to the adjustability of the upstream probe holder. $\Delta x_{1} = \overline{U}(t - t_{0}) / M$ was properly determined in each case. 

approximately on the centreline of the wind tunnel test section. For $U_{0}t/M > 40$ , there was no detectable difference between a position behind a grid rod and a position behind a grid hole. This upstream probe was mounted on a movable support whose position was read on a dial gauge which was marked to a least scale division of $10^{-3}$ in. The accuracy of the probe separation values is estimated at about $\pm 0\cdot05$ mm, about a quarter of the hot-wire lengths. Probe separations up to 4M were set by moving the front probe. The associated changes in $t_{0}$ had negligible effect on the measured functions of $(t-t_{0})$ which were the main goal of the study. 

The upstream hot-wire probe had its needles (jeweller's broaches) spaced 1·2 cm apart to reduce the wake close behind the wire. The central 0·4 mm of wire spanning the needle tips was etched to be the sensor, the balance retaining its $10^{-3}$ in. dia. silver casing. 

The downstream probe was mounted on a sliding carriage for large streamwise motions, with built-in lead screws for large vertical and horizontal motions. For lateral displacements up to 1 in. a small sliding carriage was driven by a micrometer head with least divisions of $10^{-3}$ in. Here, too, the accuracy of wire positioning was estimated at $\pm0\cdot05$ mm. The zero-separation readings were estimated by viewing closely spaced wires through a telescope with a scale. 

The following quantities were measured behind the 5·08 cm grid: 

(a) $u_1^2, u_2^2, u_3^2$ over the length of the test section (see Comte-Bellot & Corrsin 1966). 

(b) The one-probe autocorrelation function, $R_{11}(0,0,0;t,\Delta t)$ at $U_0t / M = 42$ . 

(c) $R_{11}(\Delta x_1, 0, 0; t, 0)$ at $U_0t / M = 42, 98, 171$ . 

(d) $R_{11}(0, \Delta x_2, 0; t, 0)$ at $U_0t / M = 42, 98, 171$ . 

(e) $R_{22}(0, \Delta x_2, 0; t, 0)$ at $U_0 t / M = 42$ . 

(f) $R_{11}(\Delta x_1, 0, 0; t_0, \Delta t)$ , with special emphasis on the class $\Delta t = \Delta x_1 / \overline{U}$ . The upstream probe was at $U_0 t / M = U_0 t_0 / M \doteq 42$ . 

(g) Energy spectrum of single wire probe signal, $E_{11}^{(1)}(k_{1},t)$ , the Fourier transform of $R_{11}(0,0,0;t,\Delta t)$ , at $U_{0}t/M=42,98,171$ . 

(h) $R_{11}^{(1)}(k_{1};\Delta x_{1},0,0;t_{0},\Delta t)$ , the correlation between narrow-band-filtered $u_{1}$ signals from two probes, with the upstream probe at $U_{0}t/M=42$ . The principal case was with $\Delta t=\Delta x_{1}/\overline{U}$ . $k_{1}=\omega/\overline{U}$ . 

(a), (f) and (g) were also measured behind the 2·54 cm grid. 

Next we list sources of systematic error in these measurements, with brief remarks on what, if anything, was done to correct the data for each. 

(i) Background ('free stream') velocity and temperature disturbances in the flow, plus electronic noise and pickup. Readings were taken of each function with the turbulence generating grid removed. Where these were appreciable, they were subtracted from the grid-in readings in an appropriate way (e.g. for turbulence level readings, the mean square of the error signal was subtracted from the mean square of the total signal). This method is correct for the extraneous electronic signals, somewhat rational for the temperature fluctuations and the fluid velocities due to sound, but less rational for the 'free stream turbulence', which may be changed by interaction with the grid-generated turbulence. Fortunately, the errors were virtually negligible except at the high frequency end of the spectra. 

(ii) Mechanical vibration of hot-wire or its supports. This was visually undetectable, and no spectral spikes in the appropriate frequency ranges were found. 

(iii) Finite hot-wire length. Since the wires lengths were about equal to or smaller than the Kolmogorov microscales, errors due to the associated spatial resolution deficiencies were also negligible except at very high wave-numbers. No corrections were made. 

(iv) Finite bandwidths of wave analyzers. For power spectrum measurement with narrow-band pass filters, in principle one solves an integral equation (appendix B). When the filter is narrow enough its transfer function can be approximated by a 'Dirac function', and no equation solving or data correcting is required. This was the case for the Hewlett-Packard analyzer and the spectra encountered here. The Dytronics filter band shape is more pointed at the narrowest setting, but has slower decrease at the 'tails'. We confirmed the negligibility of imperfect frequency resolution for most of the measurements by recording some correlations with three different filter bandwidths. 

(v) Contamination of turbulence by the wake of the upstream probe. This effect was bypassed by recording data for several positions laterally outside of the wake and extrapolating to the desired position (appendix A). 

(vi) Tape jitter. This effect was measured, and found to be negligible in the frequency range of data reported here (appendix C). 

(vii) Integrator drift and non-linearity. Calibration showed a slight dependence of sensitivity on total charge ( $\sim$ output voltage), an effect reported by the manufacturer in the literature accompanying the device. To minimize this effect, the integrator was operated in the middle half of its range, where the effect could actually be made negligible. The integrator also had a measurable drift with zero input, the rate depending on the scale position. Appropriate correction was applied to the recorded readings. 

(viii) Limitations of the Taylor approximation for interchangeability of frequency and wave-number. Taylor (1938) pointed out that in flows where the mean speed $\overline{U}$ is much larger than the r.m.s. turbulent velocity the time record of a fixed probe is virtually the same as a spatial record at an instant of time, i.e. the turbulence structure is nearly ‘frozen’ during the time required for passage of a blob large enough to contain all the significant structure. Limitations of this for the full turbulent velocity have been inspected theoretically by Lin (1953) and by Uberoi & Corrsin (1953). A detailed experimental test in terms of correlation functions, repeated in this paper, was made by Favre, Gaviglio & Dumas (1952). Lumley (1965) presented a detailed theoretical analysis. In the absence of mean shear, we are concerned with (a) changes in turbulence structure which occur during the mean convective transit past the probe (such fluctuations would preclude the exact interpretation of fixed-probe frequency spectra as wave-number spectra), and (b) fluctuations in convective transit of small structure due to superposed convective effect of the large structure. By estimates explained in appendix D, it was concluded that these effects were small enough that the 

Taylor approximation could be used. Consequently, all spectra measured as frequency spectra of signals in time are presented here as wave-number spectra, representing spatial Fourier decomposition. The transformation is simply 

$$
k _ {1} = \omega / \overline {{{U}}}.\tag{42}
$$

(ix) Lack of d.c. coupling in hot-wire circuitry. As remarked in § 2, the fact that our electronic system is a.c. coupled (figure 2) precludes measurement of the spectrum down to zero frequency (or wave-number), and in principle makes 'directly' measured integral scales equal to zero (appendix E). The measured spectra could have been corrected for the electronic system response spectrum to yield better accuracy at the smaller frequencies, but, since the measured spectra had levelled off at the low end (figures 8(a), (b)), and could not be corrected all the way to zero frequency anyway, no effort was made to apply this correction. A corresponding error must of course exist in the data for the autocorrelation function from a single probe record at large time differences (figure 31). No correction was applied, but it can be worked out from the given circuit response. 

Some years after most of the data were processed, it was found that the coupling circuit at the tape recorder input had been appreciably 'loaded' by an input impedance of 10 kΩ, to give a low frequency cut-off of about 5 Hz instead of the desired 1 Hz characteristic of the hot-wire system. Figure 31 in appendix E shows the direct effect of this low frequency cut-off on the measured time autocorrelation. For $\overline{U}\Delta t/M > 8$ , full band, space-time correlation values are also affected. Therefore, these functions were remeasured with the 1 Hz low cut-off. The remeasurements were made with a Princeton Applied Research Company Model 101 Correlator. 

There is no appreciable effect on the narrow-band space-time correlation functions presented, because these all correspond to filter frequencies $\omega = \overline{U} k_{1}$ much larger than 5 Hz. 

## 5. Experimental results for one-time or one-probe functions

Comte-Bellot & Corrsin (1966) presented the mean kinetic energy of the component turbulent velocities. The empirical curves (which fitted the experimental points about as well as those of Comte-Bellot & Corrsin 1966, figure 12) are given (from Comte-Bellot & Corrsin 1966, table 3) as (38) here. 

Figure 5(a) gives the transverse† correlation coefficient functions measured with $x_{2}$ -separation of $u_{1}$ velocities at three distances from the grid, 

$$
R _ {1 1} (0, \Delta x _ {2}, 0; t, 0).
$$

Figure 5(b) gives the longitudinal correlation coefficient functions $R_{11}(\Delta x_1, 0, 0; t, 0)$ . For small $\Delta x_1$ , the values were inferred by extrapolating to $\Delta x_2 = 0$ some measured values of $R_{11}(\Delta x_1, \Delta x_2, 0; t, 0)$ (see appendix A). 

† The terms ‘transverse’ and ‘longitudinal’, used to identify correlation functions, here refer to the relative directions of velocity components and point separation vector, not to directions relative to the mean wind. Thus, $R_{11}(0,\Delta x_{2},0;t,0)$ and $R_{22}(\Delta x_{1},0,0;t,0)$ are ‘transverse’ (corresponding to Kármán–Howarth ‘g functions’), while $R_{11}(\Delta x_{1},0,0;t,0)$ and $R_{22}(0,\Delta x_{2},0;t,0)$ are ‘longitudinal’ (corresponding to Kármán–Howarth ‘f functions’). 

Comte-Bellot & Corrsin (1966) reported that this turbulence field is possibly isotropic insofar as the component turbulent energies are nearly equal (which is indicated here by (38)). With the spatial correlation functions we can make more detailed tests. The most direct is a simple comparison of two transverse (or two longitudinal) correlation functions which are in different directions; e.g. is 

$$
R _ {1 1} (0, r, 0; t, 0) = R _ {3 3} (0, r, 0; t, 0)?\tag{43}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/cbdf9331aeba2bc2e440556f537435d7e8f6ec8619b5b9f5ae0ed771e1b4099f.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/05c130745d006ee77ff9549c09104540bdc4825a1be2ef2b04d359b6bc7878c0.jpg)



(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/6f2de9bcb3936eaae3e054b773a8b7cbbc76c6ae6e5405c43590197b3aff12bb.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/42980b0a1ab7283441ffe98543831548b62b47357c8e8a909aabe9e08121626c.jpg)



(b)



FIGURE 5. Downstream evolution of (a) a 'transverse', and (b) a 'longitudinal' spatial correlation function. $U_0 t / M$ : ○, 42; □, 98; ▲, △, 172.


Here $\Delta x_{2} \equiv r$ . These are both $g$ -type. Similarly, is 

$$
R _ {1 1} (r, 0, 0; t, 0) = R _ {2 2} (0, r, 0; t, 0)?\tag{44}
$$

Here $\Delta x_{1}$ and $\Delta x_{2}$ are in turn called r to give both sides of the equation the same symbolic argument. These are f-type. Figures 6(a), (b) show tests of (43) and (44). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/6c6770555d7e2609ae75ce3f0c58eb70f91593f88137a93569df63102815c678.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/7bfcb4c010c431760f5bc5b1dc81b5e45cd45d7ecc8db6969ce63fcee5a13084.jpg)



(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/dff81592fafc7fa7bf758a0b3bb2c1bab55baa606afecb4b898cddd34641b4ad.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/1c356a1b8b3b759a1402b2c1ae87a38762e350a5bddbcbac5a9c31fafbba9dfe.jpg)



(b)



FIGURE 6. A test of isotropy by comparison of two different (a) transverse, and (b) longitudinal correlation functions. $U_0 t / M = 42$ . (a) $\bigcirc$ , $R_{11}(0,r,0;t,0)$ ; $\times$ , $R_{33}(0,r,0;t,0)$ . (b) $\bigtriangleup$ , $R_{22}(0,r,0;t,0)$ ; $\bigcirc$ , $R_{11}(r,0,0;t,0)$ .


The degree of isotropy does not appear to be uniformly good. The disagreement between $R_{11}(r,0,0;t,0)$ and $R_{22}(0,r,0;t,0)$ at large r is perhaps to be expected, (a) because of actual inhomogeneity in the $x_{1}$ direction due to turbulence decay, and (b) because the turbulent large structure has a large time constant, and can be expected to maintain the obvious anisotropy of the grid-generation procedure for the lifetime of the turbulence (Batchelor & Stewart 1950). On the other hand, the disagreement between $R_{11}(0,r,0;t,0)$ and $R_{33}(0,r,0;t,0)$ at moderate r is a more disappointing deficiency in the field. 

A second check on the degree of isotropy is by use of the Kármán–Howarth (1938) kinematic relation between transverse and longitudinal correlations, first used by MacPhail (1940), who found that his grid turbulence showed good agreement with this isotropic relation. Stewart & Townsend (1951) also found good agreement. The isotropy test is 

$$
g (r, t) = f (r, t) + \frac {r}{2} \frac {\partial f}{\partial r},\tag{45}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/88cd0a43ad39695d3e093f435c23f0d769f5df1b7399622911db7e7c84b6c4a5.jpg)



(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/d2b92dfbe970445a5215d2dec3946456c0c35160100c07a700e93bc61e8ad6d2.jpg)



(b)



FIGURE 7(a), (b). For legend see facing page.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/0e59e6f231b72ec2964dc22d2dc409547f223ba49c4a6c65d247cb2e08a8cbd7.jpg)



(c)



FIGURE 7. A test of isotropy by use of continuity equation in the manner of von Kármán & Howarth (1938). $U_0 t / M$ : (a) 42, (b) 98, (c) 172. ○, directly measured; ——, computed from $R_{11}(r, 0, 0; t, 0)$ .


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/f196b5887918b60681cb415198863773e20128976d7d4dc271c7d3a7ac16d167.jpg)



(a)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/d4797beeb8127be8e4b8511f2bbff11386418ae7b4a02fde009323d5074d928d.jpg)



(b)



FIGURE 8. Downstream evolution of one-dimensional energy spectrum. $U_0 = 10 \, \text{msec}^{-1}$ . (a) $5\cdot 08 \, \text{cm grid}, U_0 t / M: \bigcirc, 42; \bigtriangleup, 98; \square, 171$ ; (b) $2\cdot 54 \, \text{cm grid}, \bigcirc, 45; \bigtriangleup, 120; \square, 240; \diamond, 385$ .


where g is any transverse, spatial correlation coefficient function and f is any longitudinal one. Figures 7(a)–(c) show tests at three different distances from the grid. In various curves, r may represent $\Delta x_{1}$ , $\Delta x_{2}$ and $\Delta x_{3}$ , depending on the velocity component directions. These indicate rather good agreement with the isotropic relation. Since the greatest discrepancy is at the intermediate distance, it may be a result of an unidentified systematic error. 

<table><tr><td colspan="5">(a) 2 in. grid<eq>E_{11}^{(1)}(k_1,t)\text{cm}^3\text{sec}^{-2}</eq></td></tr><tr><td><eq>k_1\text{cm}^{-1}</eq></td><td><eq>\frac{tU_0}{M}=42</eq></td><td><eq>\frac{tU_0}{M}=98</eq></td><td><eq>\frac{tU_0}{M}=171</eq></td><td></td></tr><tr><td>0·05</td><td><eq>5·70×10^2</eq></td><td></td><td></td><td></td></tr><tr><td>0·10</td><td><eq>6·93×10^2</eq></td><td><eq>2·97×10^2</eq></td><td><eq>1·81×10^2</eq></td><td></td></tr><tr><td>0·15</td><td><eq>6·83×10^2</eq></td><td><eq>2·81×10^2</eq></td><td><eq>1·48×10^2</eq></td><td></td></tr><tr><td>0·20</td><td><eq>6·18×10^2</eq></td><td><eq>2·31×10^2</eq></td><td><eq>1·18×10^2</eq></td><td></td></tr><tr><td>0·25</td><td><eq>5·45×10^2</eq></td><td><eq>1·90×10^2</eq></td><td><eq>9·40×10^1</eq></td><td></td></tr><tr><td>0·30</td><td><eq>4·70×10^2</eq></td><td><eq>1·60×10^2</eq></td><td><eq>7·83×10^1</eq></td><td></td></tr><tr><td>0·40</td><td><eq>3·52×10^2</eq></td><td><eq>1·15×10^2</eq></td><td><eq>5·46×10^1</eq></td><td></td></tr><tr><td>0·50</td><td><eq>2·67×10^2</eq></td><td><eq>8·50×10^1</eq></td><td><eq>3·94×10^1</eq></td><td></td></tr><tr><td>0·75</td><td><eq>1·63×10^2</eq></td><td><eq>5·04×10^1</eq></td><td><eq>2·25×10^1</eq></td><td></td></tr><tr><td>1·00</td><td><eq>1·14×10^2</eq></td><td><eq>3·30×10^1</eq></td><td><eq>1·39×10^1</eq></td><td></td></tr><tr><td>1·50</td><td><eq>6·68×10^1</eq></td><td><eq>1·74×10^1</eq></td><td><eq>7·15×10^0</eq></td><td></td></tr><tr><td>2·00</td><td><eq>4·20×10^1</eq></td><td><eq>1·12×10^1</eq></td><td><eq>4·02×10^0</eq></td><td></td></tr><tr><td>2·50</td><td><eq>3·01×10^1</eq></td><td><eq>7·52×10^0</eq></td><td><eq>2·33×10^0</eq></td><td></td></tr><tr><td>3·00</td><td><eq>2·13×10^1</eq></td><td><eq>5·05×10^0</eq></td><td><eq>1·32×10^0</eq></td><td></td></tr><tr><td>4·00</td><td><eq>1·14×10^1</eq></td><td><eq>2·31×10^0</eq></td><td><eq>5·45×10^{-1}</eq></td><td></td></tr><tr><td>6·00</td><td><eq>3·95×10^0</eq></td><td><eq>6·62×10^{-1}</eq></td><td><eq>1·12×10^{-1}</eq></td><td></td></tr><tr><td>8·00</td><td><eq>1·63×10^0</eq></td><td><eq>1·74×10^{-1}</eq></td><td><eq>2·69×10^{-2}</eq></td><td></td></tr><tr><td>10·00</td><td><eq>7·43×10^{-1}</eq></td><td><eq>5·95×10^{-2}</eq></td><td><eq>6·75×10^{-3}</eq></td><td></td></tr><tr><td>12·50</td><td><eq>3·06×10^{-1}</eq></td><td><eq>1·82×10^{-2}</eq></td><td><eq>1·69×10^{-3}</eq></td><td></td></tr><tr><td>15·00</td><td><eq>1·53×10^{-1}</eq></td><td><eq>6·12×10^{-3}</eq></td><td><eq>4·62×10^{-4}</eq></td><td></td></tr><tr><td>17·50</td><td><eq>6·93×10^{-2}</eq></td><td><eq>2·23×10^{-3}</eq></td><td><eq>1·36×10^{-4}</eq></td><td></td></tr><tr><td>20·00</td><td><eq>3·71×10^{-2}</eq></td><td><eq>7·93×10^{-4}</eq></td><td><eq>5·46×10^{-5}</eq></td><td></td></tr><tr><td>22·50</td><td></td><td><eq>2·98×10^{-4}</eq></td><td><eq>2·17×10^{-5}</eq></td><td></td></tr><tr><td colspan="5">(b) 1 in. grid<eq>E_{11}^{(1)}(k_1,t)\text{cm}^3\text{sec}^{-2}</eq></td></tr><tr><td><eq>k_1\text{cm}^{-1}</eq></td><td><eq>\frac{tU_0}{M}=45</eq></td><td><eq>\frac{tU_0}{M}=120</eq></td><td><eq>\frac{tU_0}{M}=240</eq></td><td><eq>\frac{tU_0}{M}=385</eq></td></tr><tr><td>0·10</td><td><eq>2·86×10^2</eq></td><td><eq>1·26×10^2</eq></td><td><eq>6·30×10^1</eq></td><td><eq>3·60×10^1</eq></td></tr><tr><td>0·15</td><td><eq>2·74×10^2</eq></td><td><eq>1·16×10^2</eq></td><td><eq>5·75×10^1</eq></td><td><eq>3·64×10^1</eq></td></tr><tr><td>0·20</td><td><eq>2·38×10^2</eq></td><td>—</td><td><eq>5·56×10^1</eq></td><td><eq>3·41×10^1</eq></td></tr><tr><td>0·25</td><td><eq>2·31×10^2</eq></td><td><eq>1·05×10^2</eq></td><td><eq>5·35×10^1</eq></td><td><eq>3·18×10^1</eq></td></tr><tr><td>0·35</td><td><eq>1·93×10^2</eq></td><td><eq>9·45×10^1</eq></td><td><eq>4·50×10^1</eq></td><td><eq>2·70×10^1</eq></td></tr><tr><td>0·50</td><td><eq>1·70×10^2</eq></td><td><eq>7·00×10^1</eq></td><td><eq>3·30×10^1</eq></td><td><eq>1·91×10^1</eq></td></tr><tr><td>0·75</td><td><eq>1·51×10^2</eq></td><td><eq>4·40×10^1</eq></td><td><eq>1·96×10^1</eq></td><td><eq>1·08×10^1</eq></td></tr><tr><td>1·00</td><td><eq>1·25×10^2</eq></td><td><eq>3·30×10^1</eq></td><td><eq>1·20×10^1</eq></td><td><eq>6·90×10^0</eq></td></tr><tr><td>1·50</td><td><eq>1·06×10^2</eq></td><td><eq>1·71×10^1</eq></td><td><eq>5·22×10^0</eq></td><td><eq>2·60×10^0</eq></td></tr><tr><td>2·50</td><td><eq>4·40×10^1</eq></td><td><eq>8·50×10^0</eq></td><td><eq>2·10×10^0</eq></td><td><eq>8·20×10^{-1}</eq></td></tr><tr><td>3·50</td><td><eq>2·42×10^1</eq></td><td><eq>3·93×10^0</eq></td><td><eq>8·93×10^{-1}</eq></td><td><eq>2·40×10^{-1}</eq></td></tr><tr><td>5·00</td><td><eq>1·47×10^1</eq></td><td><eq>1·46×10^0</eq></td><td><eq>2·53×10^{-1}</eq></td><td><eq>7·20×10^{-2}</eq></td></tr><tr><td>7·50</td><td><eq>4·12×10^0</eq></td><td><eq>3·54×10^{-1}</eq></td><td>—</td><td><eq>1·19×10^{-2}</eq></td></tr><tr><td>10·00</td><td><eq>1·94×10^0</eq></td><td><eq>1·00×10^{-1}</eq></td><td><eq>1·56×10^{-2}</eq></td><td><eq>1·97×10^{-3}</eq></td></tr><tr><td>15·00</td><td><eq>3·32×10^{-1}</eq></td><td><eq>1·02×10^{-2}</eq></td><td><eq>1·13×10^{-3}</eq></td><td><eq>9·55×10^{-5}</eq></td></tr><tr><td>20·00</td><td><eq>1·14×10^{-1}</eq></td><td><eq>1·60×10^{-3}</eq></td><td><eq>6·60×10^{-5}</eq></td><td><eq>4·52×10^{-6}</eq></td></tr><tr><td>25·00</td><td><eq>2·64×10^{-2}</eq></td><td><eq>2·40×10^{-4}</eq></td><td><eq>7·75×10^{-6}</eq></td><td><eq>8·56×10^{-7}</eq></td></tr><tr><td>35·00</td><td><eq>2·81×10^{-3}</eq></td><td><eq>6·15×10^{-5}</eq></td><td><eq>5·70×10^{-7}</eq></td><td>—</td></tr></table>

The $u_{1}$ -energy spectra measured from single probe signals at $U_{0}t/M = 42, 98, 171$ are presented in figure 8(a) and table 2. These are measured as frequency spectra, but, since the relevant Taylor approximation is well satisfied, they are interpreted as ‘one-dimensional’ wave-number spectra $E_{11}^{(1)}(k_{1}, t)$ . 

As mentioned in § 4, these data are corrected for electronic noise and empty-tunnel disturbances. The spatial resolution limitations due to non-zero hot-wire length were within the experimental scatter. 

Since a few space-time correlation measurements (§ 7) were taken behind the 2·54 cm mesh, square rod grid, in order to be able to reach larger $U_0 t / M$ , four spectra behind that grid are given in figure 8(b) and table 2 ( $U_0 t / M = 45, 120, 240, 385$ ). This case was also run at $U_0 = 10 \, \text{m sec}^{-1}$ , so the grid mesh Reynolds number was 17000. The turbulent energy decay in this case is included in Comte-Bellot & Corrsin (1966, table 3). 

Figure 9 and table 3 contain ‘three-dimensional’ turbulent energy spectra $E(k,t)$ computed from the data of figure 8(a) under the assumption of isotropy: 

$$
E (k, t) = \frac {1}{2} k ^ {3} \frac {\partial}{\partial k} \left\{\frac {1}{k} \frac {\partial}{\partial k} E _ {1 1} ^ {(1)} (k, t) \right\}.\tag{46}
$$

This expression differs by a factor of two from that in Batchelor (1953), because here the 'one-dimensional' spectrum $E_{11}^{(1)}(k_1)$ is scaled over the semi-infinite $k_1$ axis instead of the infinite axis. Equation (46) was carried out by graphica differentiation of faired curves. The viscous dissipation spectra $2\nu k^2 E(k,t)$ are plotted on the same Cartesian figure to give an impression of the degree of separation between the zones which contribute most to the integrals of the curves: 

$$
\frac {1}{2} \overline {{u _ {i} u _ {i}}} = \int_ {0} ^ {\infty} E d k,\tag{47}
$$

$$
\epsilon = 2 \nu \int_ {0} ^ {\infty} k ^ {2} E d k.\tag{48}
$$

The Kolmogorov wave-numbers, 

$$
k _ {K} = \eta^ {- 1} = (\epsilon / \nu^ {3}) ^ {\frac {1}{4}},\tag{49}
$$

associated with the dissipative eddies, are 34, 21 and $15 \, cm^{-1}$ for stations $U_{0}t/M = 42$ , 98 and 171, respectively. We observe that most of the dissipation occurs in scales a bit larger than $\eta$ . 

For convenience we have tabulated the streamwise r.m.s. velocity, the dissipation rate, Kolmogorov microscale, Taylor microscale and turbulence Reynolds number for the three principal downstream stations behind the 5·08 cm and 2·54 cm grids (table 4). The dissipation rate is obtained most accurately from the actual energy decay rate, as is the Taylor microscale: 

$$
\epsilon = - \frac {3}{2} \overline {{U}} \frac {d \overline {{u _ {1} ^ {2}}}}{d x _ {1}},\tag{50}
$$

$$
\lambda = \left\{\frac {1 0 \nu \overline {{u _ {1} ^ {2}}}}{\overline {{U}} \frac {d \overline {{u _ {1} ^ {2}}}}{d x _ {1}}} \right\} ^ {\frac {1}{2}} = \left\{\frac {1 5 \nu \overline {{u _ {1} ^ {2}}}}{\epsilon} \right\} ^ {\frac {1}{2}},\tag{51}
$$

$$
R _ {\lambda} = \sqrt {u _ {1} ^ {2}} \lambda / \nu .\tag{52}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/c5d936cde9089bdd8f713116db525ba68e5758279e30d5b6de9bb98eda138b62.jpg)



FIGURE 9. Downstream evolution of three-dimensional energy and dissipation spectra. 5·08 cm grid. Dissipation is $2\nu k^{2}E = 0 \cdot 28k^{2}E$ cm sec $^{-2}$ .


<table><tr><td rowspan="2"><eq>k\ cm^{-1}</eq></td><td colspan="3"><eq>E(k,t)\ cm^{3}\ sec^{-2}</eq></td></tr><tr><td><eq>\frac{tU_{0}}{M}=42</eq></td><td><eq>\frac{tU_{0}}{M}=98</eq></td><td><eq>\frac{tU_{0}}{M}=171</eq></td></tr><tr><td>0·15</td><td>—</td><td>—</td><td><eq>4·97×10^{1}</eq></td></tr><tr><td>0·20</td><td><eq>1·29×10^{2}</eq></td><td><eq>1·06×10^{2}</eq></td><td><eq>9·20×10^{1}</eq></td></tr><tr><td>0·25</td><td><eq>2·30×10^{2}</eq></td><td><eq>1·96×10^{2}</eq></td><td><eq>1·20×10^{2}</eq></td></tr><tr><td>0·30</td><td><eq>3·22×10^{2}</eq></td><td><eq>1·95×10^{2}</eq></td><td><eq>1·25×10^{2}</eq></td></tr><tr><td>0·40</td><td><eq>4·35×10^{2}</eq></td><td><eq>2·02×10^{2}</eq></td><td><eq>9·80×10^{1}</eq></td></tr><tr><td>0·50</td><td><eq>4·57×10^{2}</eq></td><td><eq>1·68×10^{2}</eq></td><td><eq>8·15×10^{1}</eq></td></tr><tr><td>0·70</td><td><eq>3·80×10^{2}</eq></td><td><eq>1·27×10^{2}</eq></td><td><eq>6·02×10^{1}</eq></td></tr><tr><td>1·00</td><td><eq>2·70×10^{2}</eq></td><td><eq>7·92×10^{1}</eq></td><td><eq>3·94×10^{1}</eq></td></tr><tr><td>1·50</td><td><eq>1·68×10^{2}</eq></td><td><eq>4·78×10^{1}</eq></td><td><eq>2·41×10^{1}</eq></td></tr><tr><td>2·00</td><td><eq>1·20×10^{2}</eq></td><td><eq>3·46×10^{1}</eq></td><td><eq>1·65×10^{1}</eq></td></tr><tr><td>2·50</td><td><eq>8·90×10^{1}</eq></td><td><eq>2·86×10^{1}</eq></td><td><eq>1·25×10^{1}</eq></td></tr><tr><td>3·00</td><td><eq>7·03×10^{1}</eq></td><td><eq>2·31×10^{1}</eq></td><td><eq>9·12×10^{0}</eq></td></tr><tr><td>4·00</td><td><eq>4·70×10^{1}</eq></td><td><eq>1·43×10^{1}</eq></td><td><eq>5·62×10^{0}</eq></td></tr><tr><td>6·00</td><td><eq>2·47×10^{1}</eq></td><td><eq>5·95×10^{0}</eq></td><td><eq>1·69×10^{0}</eq></td></tr><tr><td>8·00</td><td><eq>1·26×10^{1}</eq></td><td><eq>2·23×10^{0}</eq></td><td><eq>5·20×10^{-1}</eq></td></tr><tr><td>10.00</td><td><eq>7·42×10^{0}</eq></td><td><eq>9·00×10^{-1}</eq></td><td><eq>1·61×10^{-1}</eq></td></tr><tr><td>12·50</td><td><eq>3·96×10^{0}</eq></td><td><eq>3·63×10^{-1}</eq></td><td><eq>5·20×10^{-2}</eq></td></tr><tr><td>15·00</td><td><eq>2·33×10^{0}</eq></td><td><eq>1·62×10^{-1}</eq></td><td><eq>1·41×10^{-2}</eq></td></tr><tr><td>17·50</td><td><eq>1·34×10^{0}</eq></td><td><eq>6·60×10^{-2}</eq></td><td>—</td></tr><tr><td>20·00</td><td><eq>8·00×10^{-1}</eq></td><td><eq>3·30×10^{-2}</eq></td><td>—</td></tr></table>


TABLE 3. Numerical data for three-dimensional spectra behind 2 in. grid, computed from one-dimensional spectra


As a check on the measurements, $\lambda$ was computed also from the measured spectra, giving values within about $5\%$ . 

The hypothetical longitudinal integral scales $L_{f}$ obtained by extrapolating the one-dimensional spectra to $k_{1} = 0$ (see §6 and appendix E) are included, along with hypothetical transverse integral scales $L$ (which could be designated $L_{g}$ ), estimated by integrating $R_{11}(0,r,0;t,0)$ from 0 to a finite $r$ (about $5M$ to $6M$ ), where the curves have approximately returned to the abcissa from below. 

<table><tr><td><eq>M</eq>(cm)</td><td><eq>\frac{U_0t}{M}</eq></td><td><eq>\sqrt{\overline{u_1^2}}</eq>(cm sec<eq>^{-1}</eq>)</td><td><eq>\epsilon</eq>Dissipation rate (cm<eq>^2</eq>sec<eq>^{-3}</eq>)</td><td><eq>\eta</eq>Kolmogorov micro-scale (cm)</td><td><eq>\lambda</eq>Taylor transverse micro-scale (cm)</td><td><eq>L</eq>transverse integral scale (cm)</td><td><eq>L_f</eq>longitudinal integral scale (cm)</td><td><eq>\frac{R_\lambda}{\sqrt{u_1^2}\lambda} \nu</eq></td><td><eq>\lambda</eq><eq>\overline{L}^{R_\lambda}</eq></td></tr><tr><td rowspan="3">5·08</td><td>42</td><td>22·2</td><td>4740</td><td>0·029</td><td>0·484</td><td>1·27</td><td>2·40</td><td>71·6</td><td>27·3</td></tr><tr><td>98</td><td>12·8</td><td>633</td><td>0·048</td><td>0·764</td><td>1·88</td><td>3·45</td><td>65·3</td><td>26·5</td></tr><tr><td>171</td><td>8·95</td><td>174</td><td>0·066</td><td>1·02</td><td>2·28</td><td>4·90</td><td>60·7</td><td>27·1</td></tr><tr><td rowspan="4">2·54</td><td>45</td><td>20·5</td><td>7540</td><td>0·026</td><td>0·355</td><td>0·60</td><td>—</td><td>48·6</td><td>28·7</td></tr><tr><td>120</td><td>10·6</td><td>731</td><td>0·046</td><td>0·581</td><td>0·90</td><td>—</td><td>41·1</td><td>26·5</td></tr><tr><td>240</td><td>6·75</td><td>145</td><td>0·069</td><td>0·845</td><td>1·07</td><td>—</td><td>38·1</td><td>30·0</td></tr><tr><td>385</td><td>5·03</td><td>48·5</td><td>0·091</td><td>1·09</td><td>1·20</td><td>—</td><td>36·6</td><td>33·2</td></tr></table>


TABLE 4. Gross properties of turbulence at various stations behind 2 in. and 1 in. grids


Presumably an accurately measured $R_{11}(0, r, 0; t, 0)$ would also have zero integral over the full axis, because of the a.c. coupling of the measuring circuit and the non-infiniteness of the experiment. It is encouraging that these hypothetical $L$ 's and $L_f$ 's, although computed by different methods and from independent data, agree with each other in the sense that they approximate the isotropic requirement, $L_1 = 2L_1$ (53) 

$$
L _ {f} = 2 L.\tag{53}
$$

Also tabulated is the possible constant $(\lambda / L) R_{\lambda}$ , proposed by von Kármán & Howarth (1938). A recent rough theoretical estimate is 17 (Corrsin 1964). Batchelor (1953) remarked on the empirical constancy of $(L_f \overline{U} / (\overline{u_1^2})^{\frac{3}{2}}) d\overline{u_1^2} / dx_1$ during decay of grid-generated 'isotropic' turbulence. Simple algebra shows that 

$$
\frac {\lambda}{L} R _ {\lambda} = 2 0 \left[ - \frac {L _ {f} \overline {{U}}}{(\overline {{u _ {1} ^ {2}}}) ^ {\frac {3}{2}}} \frac {\bar {d u _ {1} ^ {2}}}{\bar {d x _ {1}}} \right] ^ {- 1}.\tag{54}
$$

The data in figure 6.1 of Batchelor (1953) suggest a range 

$$
0 \cdot 8 \leqslant - \frac {L _ {f} \overline {{{U}}}}{(\overline {{{u _ {1} ^ {2}}}}) ^ {\frac {3}{2}}} \frac {d \overline {{{u _ {1} ^ {2}}}}}{d x _ {1}} \leqslant 1 \cdot 3\tag{55}
$$

for the configurations tested. With (54), this indicates 

$$
2 5 \geqslant \frac {\lambda}{L} R _ {\lambda} \geqslant 1 5,\tag{56}
$$

a range much like table 4 and the rough theoretical estimate cited. 

## 6. The Taylor approximation and a.c. coupling

As remarked in §4(viii), Taylor (1938) suggested the very useful approximation that, in some cases, the time sample of turbulent velocity at a fixed space point is very nearly equal to what one would observe by a spatial record (along $\Delta x_{1} = \overline{U}\Delta t$ ) at a fixed time. A particular direct test is given by comparison of $R_{11}(\Delta x_1,0,0;t_0,0)$ with $R_{11}(0,0,0;t_0,\Delta x_1 / \overline{U})$ , figure 27. This kind of check, first made by Favre, Gaviglio & Dumas (1952), shows that in this unsheared turbulence, with $\sqrt{u_1^2}\ll \overline{U}$ , the Taylor approximation is good over the time and space ranges for which correlation can be measured with viable accuracy. For large separations in space and/or time (where the correlation magnitudes may be measured with accuracies poorer than perhaps $\pm 15\%$ ), we might expect the Taylor approximation to deteriorate, because these correlations are associated with the 'big eddies', which take a long time to be convected past the probe. A rough estimate (appendix D) indicates, however, that e.g. for the vastly simplified two-segment spectrum model outlined Comte-Bellot & Corrsin (1966) ( $E\sim k^{4\dagger}$ for $0\leqslant k\leqslant k_L$ ; $E\sim k^{-\frac{5}{3}}$ for $k_{L}\leqslant k\leqslant k_{K}$ ; $E = 0$ for $k > k_{K}$ ), the approximation remains good even for the very large eddies. 

As mentioned earlier, the very low frequency data are distorted by the deficiency in response of the electronic circuitry below about 1 Hz (figure 2). Since in turbulent motion the large eddies are associated with the low frequencies (even in a frame convected with the mean flow), this deficiency also must introduce errors into the one-time correlation data for large separation ( $\Delta x_{1}$ or $\Delta x_{2}$ ) of the two probes. We make no attempt to devise and apply corrections in this paper, but they may be required in some future investigation. Some discussion is offered in appendix E. 

Here we simply repeat the well-known (though rarely mentioned, and occasionally forgotten) fact that a.c. coupled circuitry can give only correlation functions with zero integral. If the experimental accuracy were good enough, both curves in figure 27 would show zero integral scale. The non-zero values presented in table 4 of Comte-Bellot & Corrsin (1966) and table 4 here, are scales characteristic of hypothetical turbulence which is presumed consistent with the actual turbulence for all but the largest eddies. 

A final remark about the best possible validity of the Taylor approximation: like may other turbulent flows, this one is inhomogeneous in the mean velocity direction. Therefore, an instantaneous spatial sample of $u_{1}$ over $x_{1}$ is a realization of a non-stationary random variable. Yet a temporal sample of $u_{1}$ at fixed x is a realization of a stationary random variable. No matter how small the turbulence level, we cannot expect the statistical properties to be identical. 

† We should note Saffman's (1967) improvement by correction and generalization of the Loitsianskii (1939) attempt to identify an integral invariant in decaying isotropic turbulence. 

## 7. Results for full-band, two-time correlation function moving with the mean motion

A principal experiment result of this report is the extension of previous measurements of the double velocity correlation function effectively translating with the mean velocity $\overline{U}$ of the fluid, 

$$
R _ {1 1} (\Delta x _ {1}, 0, 0; t _ {0}, \Delta x _ {1} / \overline {{U}}) \equiv R _ {1 1} (\overline {{U}} \Delta t, 0, 0; t _ {0}, \Delta t).
$$

Here we follow Favre, Gaviglio & Dumas in using two hot-wire probes displaced in the mean velocity direction $(\Delta x_{1})$ , with a magnetic tape recorder to delay the 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/ebadac342910cb043da4035a190415b6a980b68fa99730b4740e05757e09051f.jpg)



FIGURE 10. Some measured space-time correlation functions. The envelope is essentially time correlation in a frame translating with the mean speed $\overline{U}$ . $U_0 t_0 / M = 42$ .


upstream signal for just the time $\Delta t = \Delta x_{1}/\overline{U}$ . It is this correlation function, which may be the closest wind tunnel approximation to the theoretical two-time correlation function at a fixed point in isotropic turbulence with zero mean velocity ('box turbulence'), $_{B}R_{11}(0, 0, 0; t_{0}, t_{0} + \Delta t)$ . 

Some data were taken with $\Delta t \neq \Delta x_{1} / \overline{U}$ , particularly to find out whether $R_{11}(\Delta x_{1}, 0, 0; t_{0}, \Delta t)$ attained a maximum at $\Delta t = \Delta x_{1} / \overline{U}$ . The answer is essentially 'yes', although there are very small systematic departures due to (a) the random self-convection of the turbulence, and (b) the downstream evolution (inhomogeneity) of turbulence properties such as energy and scales. These two effects are discussed in §9. 

Figure 10 is a typical set of experimental space-time correlation curves with one wire behind the other. The upstream hot-wire was at $U_{0}t/M = 42$ , the other wire at $\Delta x_{1}/M = 4, 8, 18$ farther downstream. All of the curves are given without data points. The curve at $\Delta x_{1}/M = 4$ is an extrapolation to $\Delta x_{2} = 0$ of a family of $R_{11}(\Delta x_{1}, \Delta x_{2}, 0; t_{0}, \Delta t)$ . This extrapolation was necessitated by the extraneous presence around $\Delta x_{2} = 0$ of the wake of the upstream wire (appendix A). The wake effect became negligible for $\Delta x_{1}$ greater than about 8M. The curves for 8M and 18M were obtained with the P.A.R. correlator. 

Figure 11, and table 5, give the Eulerian correlation function following the mean motion, $R_{11}(\overline{U}\Delta t,0,0;t_{0},\Delta t)$ . The data from earlier studies are included for comparison. Possibly the new values of $R_{11}$ are larger because we avoided the wake of the upstream wire and extrapolated to $\Delta x_{2}=0$ ; other authors do not mention this precaution. This wake contains an appreciable amount of new small-scale turbulent energy created by the locally intense shear zone near the wire (Kellogg 1965). This new (short-lived) constituent evidently reduces the total correlation for small and moderate probe separation. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/a97d1249ee02bb1dedd68f0dd34ce2bd76488cab6ffdc7cd961218e8277a6890.jpg)



FIGURE 11. Time correlation in a frame translating with the mean speed $\overline{U}$ . Prior experiments: $\triangle$ , $\nabla$ , Favre et al.; $\square$ , Klebanoff & Frenkiel. New data: $\bullet$ , 5·08; $\bigcirc$ , 2·54 cm grid. $U_0 t_0 / M = 42$ .


<table><tr><td colspan="2"><eq>M = 5 \cdot 08 \text{ cm}</eq></td><td colspan="2"><eq>M = 2 \cdot 54 \text{ cm}</eq></td></tr><tr><td><eq>\overline{\overline{U}\Delta t}</eq></td><td></td><td><eq>\overline{\overline{U}\Delta t}</eq></td><td></td></tr><tr><td><eq>\overline{M}</eq></td><td><eq>R_{11}(\overline{U}\Delta t, 0, 0; t_0, \Delta t)</eq></td><td><eq>\overline{M}</eq></td><td><eq>R_{11}(\overline{U}\Delta t, 0, 0; t_0, \Delta t)</eq></td></tr><tr><td>0·375</td><td>0·94</td><td>8</td><td>0·545</td></tr><tr><td>0·75</td><td>0·89</td><td>18</td><td>0·39</td></tr><tr><td>1·3</td><td>0·83</td><td>125</td><td>0·107</td></tr><tr><td>2·5</td><td>0·765</td><td>225</td><td>0·0685</td></tr><tr><td>4·0</td><td>0·72</td><td>340</td><td>0·0095</td></tr><tr><td>6·0</td><td>0·58</td><td>—</td><td>—</td></tr><tr><td>8·0</td><td>0·535</td><td>—</td><td>—</td></tr><tr><td>12</td><td>0·46</td><td>—</td><td>—</td></tr><tr><td>18</td><td>0·40</td><td>—</td><td>—</td></tr><tr><td>27</td><td>0·30</td><td>—</td><td>—</td></tr><tr><td>36</td><td>0·255</td><td>—</td><td>—</td></tr><tr><td>48</td><td>0·21</td><td>—</td><td>—</td></tr><tr><td>90</td><td>0·125</td><td>—</td><td>—</td></tr><tr><td>125</td><td>0·10</td><td>—</td><td>—</td></tr><tr><td>172</td><td>0·07</td><td>—</td><td>—</td></tr><tr><td colspan="2">Upstream probe at:<eq>t_0U_0/M = 42</eq></td><td colspan="2">Upstream probe at:<eq>t_0U_0/M = 45</eq></td></tr></table>


TABLE 5. Numerical data for full-band two-time correlation functions following the mean flow


We note that this correlation function has not become negative within the range of this experiment. Presumably it becomes negative eventually, because the integral scale must be zero (appendix E). Limitations of wind tunnel length and desired Reynolds numbers precluded larger values of $\Delta x_{1}/M = \overline{U}\Delta t/M$ . In fact, the correlation following the mean flow is so persistent that the turbulent energy behind the 2·54 cm grid has decreased by a factor of 17·3 between the upstream probe ( $U_{0}t/M = 45$ ) and the last downstream position ( $U_{0}t/M = 385$ ). At this last position, the turbulence Reynolds number has dropped to $R_{\lambda} \approx 35$ . 

As in the case of the spatial correlation functions, we can, nevertheless, infer a hypothetical integral time scale by extrapolating and integrating what we have. With no physical grounds for supposing that $_{B}R_{11}(0,0,0;t,t+\Delta t)$ must become negative in true isotropic 'box turbulence', we simply extrapolate monotonically to zero. The resulting integral time scale is $T \approx 180$ msec. This method of computational inference is somewhat like extrapolating the corresponding frequency spectrum to a finite zero-frequency intercept. 

The Taylor type of microscale, the abcissa-intercept of the vertex-osculating parabola, 1 [ -2² ]-1 

$$
t _ {\lambda} \equiv - \frac {1}{2} \left[ \frac {\partial^ {2}}{\partial (\Delta t) ^ {2}} R _ {1 1} (\overline {{{U}}} \Delta t, 0, 0; t _ {0}, \Delta t) \right] _ {\Delta t = 0} ^ {- \frac {1}{2}},\tag{57}
$$

is found to be 6·2 msec. 

## 8. Approximate rescaling for downstream homogeneity (stationarity in convected frame)

As a matter of basic interest, and because some turbulent shear flows are spatially homogeneous along the flow direction (notably fully developed pipe flows), we shall re-examine $R_{11}(\overline{U}\Delta t,0,0;t_{0},\Delta t)$ in a $\Delta t$ co-ordinate rescaled to compensate for the downstream inhomogeneity. The ‘amplitude’ of the random variable $u_{1}(x_{1}+\overline{U}\Delta t,x_{2},x_{3},t_{0}+\Delta t)$ is already normalized by the use of the correlation coefficient function $R_{11}$ rather than the covariance function. Therefore, we need consider only the rescaling of $\Delta t\equiv t-t_{0}$ . 

We use the simplest possible method (Townsend 1954; see also Batchelor & Townsend 1956), with a 'local' characteristic time made up of an Eulerian integral length scale and a root-mean-square component turbulent velocity: 

$$
d \Theta \equiv \frac {(\overline {{u _ {1} ^ {2}}} (t)) ^ {\frac {1}{2}}}{L _ {f} (t)} d t,\tag{58}
$$

where $t = t_{0} + \Delta x_{1}/\overline{U}$ . The successful rescaling of narrow-band space-time correlation functions ( $\S 12$ ) could yield a more sophisticated approach, but that has not yet been followed. 

Figure 12(a) is an approximation to $\tilde{R}_{11}(\overline{U}\Theta,0,0;\Theta)$ , the form we might expect if we could keep the turbulence field stationary in co-ordinates translating with the mean flow. Figure 12(b) is $\tilde{F}_{11}(\Omega)$ , its Fourier transform. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/36f0c844565e330f15972bc5417f18f174edc38d8e48b9247e7c3d0695630e35.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/264857ca731591b524817797285773dc00fce05a46e72e9238a53d409d695a99.jpg)



FIGURE 12. (a) Time correlation, and (b) frequency spectrum in a frame translating with the mean speed $\overline{U}$ , roughly 'compensated' for the evolution of turbulence. (b) is the Fourier transform of (a).


Some theoretical estimates exist for these functions. 

Using Kolmogorov's approach, Inoue arrived at a linear law for the 'inertial subrange' in the Lagrangian one-particle velocity correlation function (Inoue 1950, 1951; Corrsin 1962a). Corrsin (1963a) remarked that this should be equally applicable to the simplest Eulerian 'one point' function in the absence of mean velocity. In the present context this suggests a region in which 

$$
1 - \hat {R} _ {1 1} (\overline {{{U}}} \Delta t, 0, 0, \Delta t) = C \epsilon \Delta t.\tag{59}
$$

Figure 12(a) shows no significant confirmation of (59), but there is also no reason to expect an inertial subrange to exist in turbulence at these modest Reynolds numbers (see e.g. Corrsin 1958). 

The frequency spectrum at a spatial point travelling with the mean flow is just the Fourier transform of this correlation. Kolmorogov theory gives an inertial subrange form 

$$
\widehat {F} _ {\mathbf {1 1}} (\omega) = K \epsilon \omega^ {- 2}.\tag{60}
$$

Figure 12(b) shows no perceptible $\omega^{-2}$ range. This is consistent with the absence of identifiable wave-number spectral regions proportional to $k_{1}^{-\frac{5}{3}}$ or $k^{-\frac{5}{3}}$ . Presumably this, too, reflects the smallness of the turbulence Reynolds number. 

The rescaled experimental simple Eulerian time correlation function has also been extrapolated monotonically to zero and integrated to get an integral time scale estimate of $\tilde{T} \approx 84$ msec. The 'microscale' $\tilde{t}_{\lambda}$ is essentially the same as $t_{\lambda}$ , the unscaled value, 6·2 msec. 

These numbers provide a chance to check a rough theoretical estimate (Corrsin 1962a) that $(\tilde{t}_{\lambda} / \tilde{T})\sqrt{R_{\lambda}}\approx 3.$ (61) 

The rescaled experimental value is 0·6. 

## 9. Time delay for maximum correlation with two probes

For the simplest Eulerian statistics in time we want data like those which might be recorded at rest in a (decaying) 'box turbulence'. Therefore, the time delay $(\Delta t)_{e} = \Delta x_{1}/\overline{U}$ , which just cancels the wind tunnel speed, is of clear interest. 

It is also interesting to ask whether this particular delay time between the signals of two probes spaced $\Delta x_{1}$ apart happens to give the maximum correlation for the $\Delta x_{1}$ . Experimentally (figure 10) the answer is ‘yes’, approximately. The experiments showed $(\Delta t)_{m}/(\Delta t)_{e}=1\cdot00\pm0\cdot004$ . In principle, however, the time delay for maximum correlation, $(\Delta t)_{m}$ , is slightly smaller than $(\Delta t)_{e}$ . To display this inequality crudely, we consider the hypothetical case of non-decaying, homogeneous, unsheared turbulence. Figure 13 is a qualitative sketch of the $(\Delta x_{1},\Delta t)$ -plane in ‘correlation space’ travelling with the mean flow. The isocorrelation contours must be symmetric; assume for simplicity they are convex. Then we see that for a single probe in this box turbulence the maximum correlation will be observed at any prescribed $\Delta t$ if the probe remains at rest. This is illustrated by the fact that a vertical (constant $\Delta t$ ) line on the sketch always meets its isocorrelation contour of largest correlation value just at $\Delta x_{1}=0$ . 

To consider the more general observations, imagine two $u_{1}$ -probes a fixed distance $\alpha_{1}$ apart in a box turbulence. They translate at speed $\overline{U}$ in the $x_{1}$ (and $\alpha_{1}$ ) direction. We record the two signals and play them back with any relative time delay $\Delta t$ . The relative position of the two played back signals in space-time is a diagonal line through correlation space (figure 13). The maximum $\widehat{R}_{11}$ encountered for given $\alpha_{1}$ and $\overline{U}$ is at the point where the straight line trajectory is tangent to an isocorrelation curve, $\Delta t \equiv (\Delta t)_{m}$ . 

For fixed probe spacing $\alpha_{1}$ and larger mean speed $\overline{U}$ , the sampling trajectory would be a steeper line passing through the same $\alpha_{1}$ . For fixed $\overline{U}$ and smaller $\alpha_{1}$ , the sampling trajectory would be a line parallel to the one sketched. The latter is analogous to the data of figure 10. If there were no downstream decay of the wind tunnel turbulence, the functions would be identical. 

To emphasize the difference between $(\Delta t)_{m}$ and $(\Delta t)_{e} \equiv \alpha_{1}/\overline{U}$ , consider the qualitative sketch in figure 13. We see that 

$$
(\Delta t) _ {m} <   (\Delta t) _ {e}\tag{62}
$$

in this non-decaying turbulence. In an important sense, Eulerian space-time correlations measured with $\Delta t = (\Delta t)_{e}$ , analogous to $_{B}\hat{R}_{ij}(0,0,0,\Delta t)$ , are the simplest Eulerian time correlations. $(\Delta t)_{e}$ is also the envelope tangent point for a member of the family of curves in figure 10. 

For a rough analytical estimate of the ratio of $(\Delta t)_{m}$ to $(\Delta t)_{e}$ , we arbitrarily pick a Gaussian correlation function, 

$$
{ } _ { B } \hat { R } _ { 1 1 } ( \Delta x _ { 1 } , 0 , 0 , \Delta t ) = \exp \left\{ - \frac { \pi } { 4 } \left[ \frac { ( \Delta x _ { 1 } ) ^ { 2 } } { L _ { f _ { 0 } } ^ { 2 } } + \frac { ( \Delta t ) ^ { 2 } } { T _ { 0 } ^ { 2 } } \right] \right\} .\tag{63}
$$

The ‘measured’ correlation functions are those with $\Delta x_{1} = \alpha_{1} - \overline{U} \Delta t$ . We put $(\partial/\partial(\Delta t))_{B} \widehat{R}_{11}(\alpha_{1} - \overline{U} \Delta t, 0, 0, \Delta t) = 0$ to get the $\Delta t$ value for maximum $_{B} \widehat{R}_{11}$ along this diagonal line in $(\Delta x_{1}, \Delta t)$ space: 

$$
(\Delta t) _ {m} = \frac {\alpha_ {1} / \overline {{U}}}{1 + L _ {f _ {0}} ^ {2} / (\overline {{U}} ^ {2} T _ {0} ^ {2})}.\tag{64}
$$

From the turbulence data behind the 5·08 cm grid transformed to rough stationarity (§ 8), we find 

$$
L _ {f _ {0}} \approx T _ {0} \sqrt {u _ {1 0} ^ {2}}.\tag{65}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/d94f09cf76f143f6fcb6caaeebe5e21adf504945b02557ce919af4c39d3e8aca.jpg)



FIGURE 13. Qualitative sketch of space-time isocorrelation contours in (hypothetical) non-decaying 'box' turbulence. The correlation function below is that measured by a probe moving along the oblique trajectory above.


Furthermore, $\alpha_{1} / \overline{U} = (\Delta t)_{e}$ , and it is interesting to rewrite (64) as 

$$
(\Delta t) _ {m} \approx \frac {(\Delta t) _ {e}}{1 + \overline {{{u _ {1} ^ {2}}}} / \overline {{{U}}} ^ {2}}.\tag{66}
$$

Equation (64) or (66) says that the time delay $(\Delta t)_{e}$ , which allows the second probe to arrive at the original position of the first probe in stationary box turbulence, is not the delay which gives maximum correlation. Further, it says that the maximum arrives sooner, i.e. 

$$
(\Delta t) _ {m} <   (\Delta t) _ {e}.\tag{67}
$$

From figure 13 we see that this must be true for any family of convex isocorrelation contours. 

At first glance (67) may seem paradoxical, because the autocorrelation of a fixed probe certainly is an upper bound for the magnitude (avoiding zeros in oscillatory correlations) of any two-probe cross-correlations. Figure 13 shows the resolution of the 'paradox'. $(\Delta t)_m < (\Delta t)_e$ , because the fixed point autocorrelation drops off more during the time $(\Delta t)_e - (\Delta t)_m$ than the spatial correlation drops off over the remaining distance $\overline{U}[(\Delta t)_e - (\Delta t)_m]$ . 

In the present experiments $\overline{u_{1}^{2}/\overline{U}^{2}} < 10^{-3}$ , which is just beyond the accuracy of the $\Delta t$ measurements. 

The ‘box turbulence’ defined by travelling downstream in the wind tunnel at the mean flow speed is both non-stationary and inhomogeneous. Since each of the two probes in that frame moves in such a way that the length and time scales in its neighbourhood remain independent of time, the $(\Delta t)_{m}$ expression looks like (64), with constant ‘effective’ values of $L_{f}$ and T. For a rough approximation, these might be chosen as the averages of the values at the two probes ( $L_{①}$ , $L_{②}$ , $T_{①}$ , $T_{②}$ ). Then the generalization of (66) would be 

$$
(\Delta t) _ {m} \approx \frac {(\Delta t) _ {e}}{1 + (\overline {{{u _ {1} ^ {2}}}}) _ {\mathrm{eff}} / \overline {{{U}}} ^ {2}},\tag{68}
$$

where 

$$
\sqrt {(\overline {{{u _ {1} ^ {2}}}}) _ {\mathrm{eff}}} \equiv \frac {L _ {①} + L _ {②}}{T _ {①} + T _ {②}}.
$$

The turbulence levels in this flow are so small that, for all practical purposes, $(\Delta t)_{m} \doteq (\Delta t)_{e}$ . 

## 10. Narrow-band, two-time velocity correlation function following the mean flow

The principal experimental result in this report is the set of space-time correlations of $k_{1}$ -spectrally ‘local’ velocity signals in a frame travelling with the mean motion. These are listed as (h) in §4, and may be regarded as the spatial Fourier decomposition of the ‘full-band’ function reported in §7. The corresponding ‘box turbulence’ function is $_{B}R_{11}^{(1)}(k_{1};t_{0},t)$ , defined in (15). Of course, $R_{11}^{(1)}$ is not very local in k-space; it includes contributions at wave-number magnitudes spanning the entire range $k_{1}\leqslant k\leqslant\infty$ . The genuinely local function is the spectral density field itself (in box turbulence, $\frac{1}{2B}\rho_{ii}(\mathbf{k},t,t)$ ). The ‘next most local’ function in common use is the ‘three-dimensional spectrum’, $E(k,t)$ , the integral of the spectral density over a spherical shell. It is used in dimensional arguments, below and later. 

The filtered space-time correlation function with matched narrow-band filters set at frequency $\omega\left(=\overline{U}k_{1}\right)$ can be written as $R_{11}^{(1)}(k_{1};\Delta x_{1},\Delta x_{2},\Delta x_{3};t_{0},\Delta t)$ . Figure 14 presents the cases of initial interest, $R_{11}^{(1)}(k_{1};\overline{U}\Delta t,0,0;t_{0},\Delta t)$ . The full-band function is included for contrast. As with the full-band function, the time delay $\tau_{e}\equiv(\Delta x_{1})/\overline{U}$ approximated the delay for maximum correlation within the accuracy of the measurement. No negative values were encountered in this function, although narrow-band space-time correlations with independent delay $\Delta t$ do oscillate. 

<table><tr><td rowspan="2"><eq>\overline{U}\Delta t/M...</eq><eq>k_1(cm^{-1})</eq></td><td colspan="14"><eq>R_{11}^{(1)}(k_1; \overline{U}\Delta t, 0, 0; t_0, \Delta t)</eq></td></tr><tr><td>0·375</td><td>0·75</td><td>1·3</td><td>2·5</td><td>4</td><td>6</td><td>8</td><td>12</td><td>18</td><td>27</td><td>36</td><td>48</td><td>90</td><td>172</td></tr><tr><td>0·05</td><td>—</td><td>0·995</td><td>0·97</td><td>0·95</td><td>—</td><td>0·91</td><td>0·87</td><td>0·80</td><td>—</td><td>—</td><td>0·48</td><td>—</td><td>0·25</td><td>0·13</td></tr><tr><td>0·10</td><td>0·985</td><td>0·98</td><td>0·96</td><td>0·93</td><td>0·91</td><td>0·89</td><td>0·85</td><td>0·78</td><td>0·68</td><td>0·56</td><td>0·49</td><td>0·40</td><td>0·25</td><td>0·12</td></tr><tr><td>0·25</td><td>0·98</td><td>0·965</td><td>0·93</td><td>0·90</td><td>0·86</td><td>0·81</td><td>0·79</td><td>0·68</td><td>0·545</td><td>—</td><td>0·34</td><td>0·275</td><td>0·105</td><td>0·04</td></tr><tr><td>0·50</td><td>0·975</td><td>0·94</td><td>0·88</td><td>0·81</td><td>0·78</td><td>0·67</td><td>0·59</td><td>0·48</td><td>0·315</td><td>—</td><td>0·13</td><td>0·06</td><td>—</td><td>—</td></tr><tr><td>0·76</td><td>0·97</td><td>0·91</td><td>0·85</td><td>0·79</td><td>0·72</td><td>0·54</td><td>0·465</td><td>0·30</td><td>0·14</td><td>0·055</td><td>0·04</td><td>0·017</td><td>—</td><td>—</td></tr><tr><td>1·01</td><td>0·96</td><td>0·90</td><td>0·83</td><td>0·74</td><td>0·60</td><td>0·435</td><td>0·36</td><td>0·21</td><td>0·095</td><td>—</td><td>0·025</td><td>—</td><td>—</td><td>—</td></tr><tr><td>1·52</td><td>0·95</td><td>0·86</td><td>0·77</td><td>0·64</td><td>0·475</td><td>0·315</td><td>0·20</td><td>0·10</td><td>0·03</td><td>—</td><td>0·01</td><td>—</td><td>—</td><td>—</td></tr><tr><td>2·28</td><td>0·915</td><td>0·83</td><td>0·69</td><td>0·54</td><td>0·315</td><td>0·15</td><td>0·085</td><td>—</td><td>0·018</td><td>—</td><td>0·00</td><td>—</td><td>—</td><td>—</td></tr><tr><td>3·03</td><td>0·88</td><td>0·79</td><td>0·60</td><td>0·39</td><td>0·20</td><td>0·06</td><td>0·02</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>4·04</td><td>0·85</td><td>0·75</td><td>0·54</td><td>0·28</td><td>0·09</td><td>0·025</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>5·05</td><td>0·815</td><td>0·72</td><td>0·48</td><td>0·18</td><td>0·03</td><td>0·015</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>7·6</td><td>0·76</td><td>0·65</td><td>—</td><td>0·08</td><td>—</td><td>0·00</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>10·1</td><td>0·70</td><td>0·55</td><td>—</td><td>0·04</td><td>0·00</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr></table>

<table><tr><td rowspan="2"><eq>\overline{U}\Delta t/M...</eq><eq>k_1(cm^{-1})</eq></td><td colspan="13"><eq>R(k;\overline{U}\Delta t,0,0;t_0,\Delta t)</eq></td></tr><tr><td>0·375</td><td>0·75</td><td>1·3</td><td>2·5</td><td>4</td><td>6</td><td>8</td><td>12</td><td>18</td><td>36</td><td>48</td><td>90</td><td>172</td></tr><tr><td>0·25</td><td>1·0</td><td>1·0</td><td>0·995</td><td>0·99</td><td>0·98</td><td>0·975</td><td>0·965</td><td>0·95</td><td>0·93</td><td>0·87</td><td>0·81</td><td>0·61</td><td>0·28</td></tr><tr><td>0·50</td><td>1·0</td><td>1·0</td><td>0·98</td><td>0·97</td><td>0·95</td><td>0·93</td><td>0·905</td><td>0·86</td><td>0·78</td><td>0·56</td><td>0·44</td><td>0·22</td><td>—</td></tr><tr><td>0·76</td><td>1·0</td><td>0·99</td><td>0·97</td><td>0·95</td><td>0·91</td><td>0·865</td><td>0·81</td><td>0·70</td><td>0·54</td><td>0·26</td><td>0·17</td><td>—</td><td>—</td></tr><tr><td>1·01</td><td>1·0</td><td>0·98</td><td>0·955</td><td>0·92</td><td>0·86</td><td>0·785</td><td>0·71</td><td>0·55</td><td>0·32</td><td>0·10</td><td>0·04</td><td>—</td><td>—</td></tr><tr><td>1·52</td><td>1·0</td><td>0·96</td><td>0·92</td><td>0·86</td><td>0·78</td><td>0·685</td><td>0·58</td><td>0·34</td><td>0·14</td><td>0·02</td><td>—</td><td>—</td><td>—</td></tr><tr><td>2·28</td><td>1·0</td><td>0·93</td><td>0·87</td><td>0·77</td><td>0·65</td><td>0·495</td><td>0·37</td><td>0·16</td><td>0·04</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>3·03</td><td>0·99</td><td>0·91</td><td>0·825</td><td>0·69</td><td>0·54</td><td>0·35</td><td>0·19</td><td>0·05</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>4·04</td><td>0·97</td><td>0·88</td><td>0·76</td><td>0·59</td><td>0·40</td><td>0·19</td><td>0·07</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>5·05</td><td>0·95</td><td>0·85</td><td>0·705</td><td>0·47</td><td>0·25</td><td>0·04</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>7·6</td><td>0·88</td><td>0·75</td><td>0·535</td><td>0·23</td><td>0·05</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr><tr><td>10·1</td><td>0·82</td><td>0·65</td><td>0·43</td><td>0·08</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td><td>—</td></tr></table>

Also, as with both $R_{11}(\Delta x_{1},0,0;t_{0},0)$ and $R_{11}(\overline{U}\Delta t,0,0;t_{0},\Delta t)$ , the small $\Delta x_{1}$ ranges could not be measured directly, but had to be inferred by extrapolating to $\Delta x_{2}=0$ some measurements of $R_{11}^{(1)}(k_{1};\overline{U}\Delta t,\Delta x_{2},0;t_{0},\Delta t)$ . Especially for the high wave-numbers, this extrapolation process was very uncertain (appendix A). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/bb2a443e043e044bd58a4696b5e0774be64d75c23a7cea115562e6e8ce965da2.jpg)



FIGURE 14. Narrow-band space-time correlation functions in a frame travelling with the mean speed $\overline{U}$ . $U_0 t_0 / M = 42$ . ---, $R_{11}$ total signal (full-band case, figure 11).


$$
\left. \begin{array}{c c c c} \bigcirc 0 \cdot 1 0 & \otimes 0 \cdot 7 6 & \oplus 2 \cdot 2 8 & \triangle 5 \cdot 0 5 \\ \square 0 \cdot 2 5 & \bigtriangledown 1 \cdot 0 1 & \triangle 3 \cdot 0 3 & \ominus 7 \cdot 6 0 \\ \triangle 0 \cdot 5 0 & \diamond 1 \cdot 5 2 & \oplus 4 \cdot 0 4 & \square 1 0 \cdot 1 0 \end{array} \right\} (k _ {1} \mathrm{cm} ^ {- 1})
$$

Each curve in figure 14 is in principle the envelope of an array of space-time correlations with identically filtered signals (centre frequency $\omega = \overline{U} k_{1}$ ). Lack of time prevented us from collecting data for this wide range of $\Delta t$ for each $k_{1}$ and $\Delta x_{1}$ . Figure 15 is a schematic sketch to identify a single typical curve of which figure 14 shows the envelope. 

As might be expected, the velocity field structure of lower wave-number (hence larger scale) tends to retain its correlation over a longer time interval. This behaviour is not, however, inevitable. Construct dimensionally the simplest kinematic time for ‘eddies’ of wave-number magnitude k, 

$$
T _ {k} (k) \equiv \frac {L _ {k} (k)}{v _ {k} (k)},\tag{69}
$$

where $L_{k}$ is a length characterizing them and $v_{k}$ a velocity. $T_{k}$ will be a monotonically decreasing function of k only if $L_{k}$ and $v_{k}$ have appropriate relative forms. The simplest choices are 

$$
L _ {k} = k ^ {- 1} \quad \text { and } \quad v _ {k} \sim [ k E (k, t) ] ^ {\frac {1}{2}},\tag{70}
$$

where $E$ is the 'three-dimensional spectrum'. To be more specific, consider a spectral region in which $E(k,t)$ can be approximated by a power law, $E \sim k^{-n}$ , for any $t$ . 

$$
T _ {k} \sim k ^ {\frac {1}{2} (n - 3)},
$$

and $T_{k}$ decreases with increasing k only if n < 3. We conclude that $T_{k}$ is probably a monotonically decreasing function of k over most of the spectral range covered in this study. Only at the high-wave-number (viscous) end of the spectrum might we look for departures. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/63877b8d3bf33490c2cd86341b15ed02a22f41ecc96f5be48a86c879b89a0cfb.jpg)



FIGURE 15. Qualitative sketch of three narrow-band space-time correlation functions. Each curve of figure 14 is essentially the envelope of a set of such curves. $U_{0}t_{0}/M = 42$ . k is constant. a, b: constants, a < b.


The foregoing analytical discussion is conducted in terms of wave-number magnitude k and three-dimensional spectrum $E(k,t)$ , because, in terms of dynamic properties, the thin spherical shell in wave-number space is a relatively local region (see e.g. figures 2, 4 and 5 in Corrsin 1959). Like the one-dimensional spectrum $E_{11}^{(1)}(k_{1},t)$ , $R_{11}^{(1)}(k_{1};\overline{U}\Delta t,0,0;t_{0},\Delta t)$ is not very local in wave-number space. Thus, the assignment of e.g. a characteristic time appropriate for these functions at any $k_{1}$ value would be a risky business. We should instead focus on the corresponding three-dimensional spectrum and its generalization, the three-dimensional, narrow-band, space-time correlation function. 

Just as we can calculate $E(k,t)$ from $E_{11}^{(1)}(k_{1},t)$ in isotropic turbulence (Heisenberg 1948; see e.g. Batchelor 1953), so we can calculate a three-dimensional, space-time correlation following the mean motion by operating on $R_{11}^{(1)}$ with a transformation identical in form to (23). 

The faired curves of figure 14 were multiplied by faired spectral curves, replotted on a Cartesian scale, and differentiated graphically as required by (23). The three-dimensional spectra in the denominator had been computed similarly from the one-dimensional spectra. The $R(k; \overline{U} \Delta t, 0, 0; t_0, \Delta t)$ points in figure 16 show scatter because of the inaccuracies of the graphical differentiation process. 

In both figures 14 and 16, the dotted line extrapolations at the small time intervals were actually carried out on Cartesian scales, where the vertex intercept behaviour is clear: all curves must go through the value $1 \cdot 0$ as a maximum. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/1b6dd7a252515c492f51574dc11c8db99af35b8760ed2238f423dccaf6b4f4d5.jpg)



FIGURE 16. Three-dimensional space-time correlation functions in a frame travelling with the mean speed U, computed from data of figures 9(a) and 14. Kolmogorov wave-number: 34–15 cm $^{-1}$ ; spectral peak: 0·5–0·3 cm $^{-1}$ . $U_{0}t_{0}/M = 43$ . ---, $R_{11}$ total signal (full-band, three-dimensional, space-time correlation).


$$
\left. \begin{array}{c c c c} \bigcirc 0 \cdot 2 5 & \bigtriangledown 1 \cdot 0 1 & \triangle 3 \cdot 0 3 & \ominus 7 \cdot 6 0 \\ \triangle 0 \cdot 5 0 & \diamond 1 \cdot 5 2 & \text {①} 4 \cdot 0 4 & \square 1 0 \cdot 1 0 \\ \otimes 0 \cdot 7 6 & \oplus 2 \cdot 2 8 & \triangle 5 \cdot 0 5 \end{array} \right\} (k \mathrm{cm} ^ {- 1})
$$

<table><tr><td><eq>\overline{U}\Delta t</eq> <eq>\overline{M}</eq></td><td><eq>R_{11}</eq> measured</td><td><eq>R_{11}</eq> computed from <eq>R_{11}^{(1)}</eq> and <eq>E_{11}^{(1)}</eq></td><td><eq>R_{11}</eq> computed from <eq>R</eq> and <eq>E</eq></td></tr><tr><td>0·75</td><td>0·89</td><td>0·91</td><td>0·93</td></tr><tr><td>2·5</td><td>0·765</td><td>0·77</td><td>0·79</td></tr><tr><td>4</td><td>0·72</td><td>0·685</td><td>0·695</td></tr><tr><td>8</td><td>0·535</td><td>0·545</td><td>0·53</td></tr><tr><td>18</td><td>0·39</td><td>0·365</td><td>0·345</td></tr><tr><td>36</td><td>0·255</td><td>0·23</td><td>0·22</td></tr><tr><td>48</td><td>0·21</td><td>0·19</td><td>0·175</td></tr><tr><td>90</td><td>0·125</td><td>0·11</td><td>—</td></tr><tr><td>172</td><td>0·07</td><td>0·05</td><td>—</td></tr></table>


TABLE 8. Consistency checks


The full-band (total signal) correlation coefficient function $R_{11}(\overline{U}\Delta t,0,0;t_{0},\Delta t)$ is also drawn in figure 16 for contrast. In co-ordinates travelling with the mean flow it can be seen at once that there is no such thing as a 'three-dimensional full-band correlation function' to be computed from $R_{11}$ . $\frac{1}{3}R_{jj}$ may come to mind, but in isotropic turbulence this is equal to $R_{11}$ . 

A consistency check among the (independent) measurements of $R_{11}$ , $R_{11}^{(1)}$ and $E_{11}^{(1)}$ can be obtained by using the equality, 

$$
R _ {1 1} (\overline {{U}} \Delta t, 0, 0; t _ {0}, \Delta t) = \int_ {0} ^ {\infty} R _ {1 1} ^ {(1)} (k _ {1}; \overline {{U}} \Delta t, 0, 0; t _ {0}, \Delta t) \left[ \frac {E _ {1 1} ^ {(1)} (k _ {1} , t _ {0}) E _ {1 1} ^ {(1)} (k _ {1} , t _ {0} + \Delta t)}{\overline {{u _ {1} ^ {2}}} (t _ {0}) \overline {{u _ {1} ^ {2}}} (t _ {0} + \Delta t)} \right] ^ {\frac {1}{2}} d k _ {1},\tag{72}
$$

which is essentially (18) with $r_1 = 0$ . Table 8 indicates satisfactory agreement. 

A supplementary consistency check on the several graphical differentiation operations required to calculate the three-dimensional functions from the measured one-dimensional ones can be obtained from the similar equality 

$$
R _ {1 1} (\overline {{U}} \Delta t, 0, 0; t _ {0}, \Delta t) = \frac {2}{3} \int_ {0} ^ {\infty} R (k; \overline {{U}} \Delta t, 0, 0; t _ {0}, \Delta t) \left[ \frac {E (k , t _ {0}) E (k , t _ {0} + \Delta t)}{\overline {{u ^ {2}}} (t _ {0}) \overline {{u ^ {2}}} (t _ {0} + \Delta t)} \right] ^ {\frac {1}{2}} d k.\tag{73}
$$

This too shows satisfactory agreement in table 8. 

11. Computation of narrow-band correlations with mean convective delay from full-band correlations with all delays 

Favre et al. (1954) pointed out that narrow-band space-time correlation functions like $R_{11}^{(1)}(k_{1};\overline{U}\Delta t,0,0;t_{0},\Delta t)$ can be inferred in principle from data on the general full-band space-time correlation functions like $R_{11}(\Delta x_{1},0,0;t_{0},\Delta t)$ . Equation (17) is the appropriate procedure in the case of box turbulence. 

To test the viability of this method of determining $R_{11}^{(1)}$ , we compare a directly measured case (cross-plotted from figure 14) with one computed from a measured $R_{11}(\Delta x_{1}, 0, 0; t_{0}, \Delta t)$ . In laboratory co-ordinates, and in terms of correlation coefficient functions and spectra, (17) takes on the operational form, 

$$
R _ {1 1} ^ {(1)} (\omega / \overline {{{U}}}; \overline {{{U}}} \Delta t, 0, 0; t _ {0}, \Delta t) = 4 \frac {\int_ {0} ^ {\infty} R _ {1 1} (\overline {{{U}}} \Delta t , 0 , 0 ; t _ {0} , \Delta t + \tau) \cos (\omega \tau) d \tau}{\left[ \frac {E _ {1 1} (\omega / \overline {{{U}}} , t _ {0}) E _ {1 1} (\omega / \overline {{{U}}} , t _ {0} + \Delta t)}{\overline {{{u _ {1} ^ {2}}}} (t _ {0}) \overline {{{u _ {1} ^ {2}}}} (t _ {0} + \Delta t)} \right] ^ {\frac {1}{2}}}.\tag{74}
$$

Since no $R_{11}(\Delta x_{1},0,0;t_{0},\Delta t)$ curve was measured over the full range of $\Delta t$ , the most extensive case, at $\Delta x_{1}/M=\overline{U}\Delta t/M=8$ , has been completed with a plausible extrapolation (figure 17). The extrapolation was governed by three conditions: (i) to make the integral scale equal to zero, a requirement of the a.c. coupling, (ii) to have a single negative region (an arbitrary decision), (iii) to avoid negative correlation values of magnitudes greater than 0·02 (because larger negative values are almost never observed for full-band turbulence signals). 

The $R_{11}^{(1)}$ comparison is figure 18. The agreement is very good for $k_{1} < 2~cm^{-1}$ , indicating experimental consistency and reasonable extrapolation. Other extrapolations were tried, but these changed only the low frequency end of the Fourier transform. For larger wave-numbers, the limited computational accuracy for the Fourier transform precludes the use of (74). In this range, direct measurements of $R_{11}^{(1)}$ are clearly preferable. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/1301bb2d15ffae5ba662da840bd7d6c6b41678bfd8c68b560dd79e1c59b91db1.jpg)



FIGURE 17. The space-time correlation curve for $\Delta x_{1} = 8M$ in figure 11. ---, arbitrary extrapolation.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/7005a483d1fead579f83d9d7cf5fbe66226b69908c950bd2ca5c39893f40e3a2.jpg)



FIGURE 18. Narrow-band space-time correlation function for fixed probe separation ( $\Delta x_{1}=8M$ ) as a function of wave-number. ☐, directly measured (from figure 14); ——, computed from $R_{11}(8M,0,0;t_{0},8M/\overline{U}+\Delta t)$ (from figure 17 by the method of Favre et al.).


## 12. Similarity rescaling of the spectrally local correlation functions

Some new insight into turbulent structure may result if we can devise a similarity basis which can collapse all of the spectrally local correlation functions of figure 16 into a single curve. Since these cover a large spectral range, extending from the spectral peak to the Kolmogorov wave-number, it is unlikely that simple dimensional arguments alone will suffice; we shall have to consider physical mechanisms. The functions to be rescaled are correlation coefficient functions, hence already dimensionless and normalized. Therefore, we direct our efforts to rescaling the time interval. In a stationary isotropic turbulence with zero mean speed we would be seeking a characteristic time spectrum $\tau(k)$ such that 

$$
\widehat {R} (k; 0, 0, 0, \Delta t)
$$

is a universal function of $\Delta t / \tau(k)$ , independent of $k$ . But, since our turbulence is non-stationary in the convected frame, we have the more difficult task of finding a characteristic time spectrum $\tau(k,t)$ such that $R(k;\overline{U}\Delta t,0,0;t_0,\Delta t)$ is a universal function of $\mathcal{C}^{t_0 + \Delta t}\cdot dt$ 

$$
\theta (k, t _ {0}, \Delta t) \equiv \int_ {t _ {0}} ^ {t _ {0} + \Delta t} \frac {d t _ {1}}{\tau (k , t _ {1})}.\tag{75}
$$

We write $\tau(k,t)$ instead of $\tau(k,x_{1})$ , because we shall be in the frame travelling with the mean flow. 

Among possible spectrally local characteristic times are those suggested by Onsager (1945, 1949), $\tau_{0}(k) = [k^{3}E(k)]^{-\frac{1}{2}}$ (76) 

$$
\tau_ {0} (k) \equiv [ k ^ {3} E (k) ] ^ {- \frac {1}{2}},
$$

von Weizsäcker (1948), 

$$
\tau_ {W} (k) \equiv [ u ^ {\prime} k _ {E} ^ {\frac {1}{3}} k ^ {\frac {2}{3}} ] ^ {- 1},\tag{77}
$$

and Heisenberg (1948), 

$$
\tau_ {H} (k) \equiv [ u ^ {\prime} k ] ^ {- 1}.\tag{78}
$$

Each of these has been tried in (75) as a rescaling basis. The first two give only a partial collapse of the $R(k;\overline{U}\Delta t,0,0;t_{0},\Delta t)$ curves, but $\tau_{H}$ is successful in some spectral regions. We consider possible physical meanings of these three times. Then we shall devise a more detailed phenomenological spectral coherence time $\tau_{*}$ which proves quite successful over most of the experimental range. 

$\tau_{0}(k)$ could be regarded as merely the simplest local ‘inertial’ time obtainable by dimensional analysis. But it has phenomenological meaning as well. Consider spectrally local velocity and length to be 

$$
v _ {k} \equiv (k E) ^ {\frac {1}{2}}, l _ {k} \equiv k ^ {- 1}.\tag{79}
$$

The spectrally local vorticity and strain rate are then 

$$
\omega_ {k} = s _ {k} \sim v _ {k} / l _ {k} = (k ^ {3} E) ^ {- \frac {1}{2}} = \tau_ {0}.\tag{80}
$$

Alternatively, $\tau_{0}$ is the time required for velocity $v_{k}$ to carry material a distance $l_{k}$ . $\tau_{W}(k)$ , suggested by von Weizsäcker for the intertial subrange, turns out to be $\tau_{0}(k)$ in the special case of a Kolmogorov inertial subrange spectrum, 

$$
E \approx \epsilon^ {\frac {2}{3}} k ^ {- \frac {5}{3}}.\tag{81}
$$

To see this we also use the inertial expression for energy dissipation rate, 

$$
\epsilon \approx u ^ {\prime 3} k _ {E}.\tag{82}
$$

$\tau_{H}(k)$ is essentially the time required for the energetic part of the turbulence (whose wave-number is of order $k_{E}$ , representing large scale) to convect small structure at k a distance $l_{k}$ . There seem to be at least three conditions necessary for $\tau_{H}$ to be physically meaningful. First, the ‘eddies’ at wave-number k must be much smaller than those doing the principal convecting: 

$$
k \gg k _ {E},\tag{83}
$$

so that many wavelengths are contained in a length $k_{E}^{-1}$ . 

Secondly, the fine structure must be a ‘frozen pattern’ while it is convected a distance $l_{k}$ , a kind of local turbulent Taylor approximation, e.g. 

$$
\tau_ {0} (k) \geqslant \tau_ {H} (k).\tag{84}
$$

In terms of wave-number and spectrum, this is 

$$
v _ {k} \ll u ^ {\prime} \quad \text { or } \quad [ k E ] ^ {\frac {1}{2}} \ll u ^ {\prime}.\tag{85}
$$

For a spectrum decreasing rapidly enough at k, this is consistent with (83). 

Thirdly, the large structure itself must remain unchanged during the time in which it convects the fine structure a distance $l_{k}$ : 

$$
\tau_ {0} (k _ {E}) \geqslant \tau_ {H} (k).\tag{86}
$$

With E estimated by the Kolmogorov spectrum, (85) is stronger than (83). 

In order to devise a more general time spectrum for rescaling the collection of spectrally local correlation functions, we should consider various physical mechanisms in the turbulence that act to destroy the coherence of an individual Fourier element. Generally, the mechanisms can be described as random translation, random rotation and random distortion. 

Structure at wave-number k undergoes ‘pure’ translation and rotation only in convection by fluctuations whose wave-numbers are much smaller. It suffers distortion through both the ‘homogeneous’ straining action of structure at smaller wave-numbers and the inhomogeneous convection by structure at larger wave-numbers. Of course, the ‘self-destruction’ by structure at the same wave-number is important (in a sense, dominant); but it can be included by representing each mechanism as acting over a spectral range extending to k itself. 

The four coherence-destroying mechanisms may have characteristic times as follows: 

(i) Convection by larger eddies: 

$$
\tau_ {C} (k) \sim l _ {k} / v _ {<   k}.\tag{87}
$$

(ii) Rotation by larger eddies: 

$$
\tau_ {R} (k) \sim 1 / \omega_ {<   k}.\tag{88}
$$

(iii) Straining distortion by larger eddies: 

$$
\tau_ {S} (k) \sim 1 / s _ {<   k}.\tag{89}
$$

(iv) Phase-surface wrinkling by smaller eddies, a quasi-diffusive effect: 

$$
\tau_ {D} (k) \sim l _ {k} ^ {2} / D _ {> k}.\tag{90}
$$

$l_{k}$ is a characteristic scale of eddies of wave-number k, $v_{<k}$ is a velocity characteristic of all structure at wave-numbers less than k, $\omega_{<k}$ is vorticity characteristic of all structure at wave-numbers less than k, $s_{<k}$ is strain-rate characteristic of all structure at wave-numbers less than k, $D_{>k}$ is a ‘turbulent viscosity’, characteristic of all structure at wave-numbers greater than k. 

Mechanisms (iii) and (iv) are obviously important in energy spectral transfer as well. Howells (1960) suggested a passive-scalar mixing theory based on these two; he pointed out that this way of thinking about the phenomena may be more nearly valid for mixing of scalars than for turbulence dynamics. 

Roughly speaking, we can choose 

$$
l _ {k} = k ^ {- 1},\tag{91}
$$

$$
v _ {<   k} = \left[ \int_ {0} ^ {k} E (p) d p \right] ^ {\frac {1}{2}},\tag{92}
$$

$$
\omega_ {<   k} = \left[ \int_ {0} ^ {k} p ^ {2} E (p) d p \right] ^ {\frac {1}{2}},\tag{93}
$$

$$
s _ {<   k} = \left[ \int_ {0} ^ {k} p ^ {2} E (p) d p \right] ^ {\frac {1}{2}},\tag{94}
$$

$$
D _ {> k} = \left[ \int_ {k} ^ {\infty} p ^ {- 2} E (p) d p \right] ^ {\frac {1}{2}}.\tag{95}
$$

Omitting consideration of factors of order 1 (or $\pi$ ), we define a 'convection time', $\left[\int^{k}\dots\right]^{-\frac{1}{2}}$ 

$$
\tau_ {C} (k) \equiv \left[ k ^ {2} \int_ {0} ^ {k} E d p \right] ^ {- \frac {1}{2}},\tag{96}
$$

the time it would take for a steady rectilinear motion, whose speed equals the root-mean-square of the turbulent velocities at wave-numbers below k, to travel a distance $k^{-1}$ . We also define a ‘rotation time’, 

$$
\tau_ {R} (k) \equiv \left[ \int_ {0} ^ {k} p ^ {2} E d p \right] ^ {- \frac {1}{2}},\tag{97}
$$

the time it would take a rigidly rotating motion, whose vorticity equals the root-mean-square of the turbulent vorticity at wave-numbers below k, to rotate through a half radian. 

Further, we characterize the quasi-homogeneous strain effect by the same expression, the 'strain time', 

$$
\tau_ {S} (k) \equiv \left[ \int_ {0} ^ {k} p ^ {2} E d p \right] ^ {- \frac {1}{2}},\tag{98}
$$

the time in which a fluid line would grow by a factor of $e^{\frac{1}{2}}$ in a homogeneous, constant strain-rate field whose value is equal to the root-mean-square strain-rate at wave-numbers below k, aligned with the fluid line. 

Finally, we characterize the phase-plane wrinkling mechanism as a diffusion phenomenon, with coherence-destroying ‘diffusion time’, 

$$
\tau_ {D} (k) \equiv \left[ k ^ {4} \int_ {k} ^ {\infty} p ^ {- 2} E d p \right] ^ {- \frac {1}{2}},\tag{99}
$$

the time in which the amplitude of a sinusoidal scalar field (or rectilinear velocity field) of wave-number k would decrease by a factor e due to diffusivity (or viscosity) $D_{>k}$ . 

For the lack of any more sophisticated analysis at present, we neglect the interactions among these four mechanisms, so that they act simply in parallel. Then the net characteristic time $\tau_{*}(k)$ due to all four is given by 

$$
\frac {1}{\tau_ {*}} \approx \frac {c _ {C}}{\tau_ {C}} + \frac {c _ {R}}{\tau_ {R}} + \frac {c _ {S}}{\tau_ {S}} + \frac {c _ {D}}{\tau_ {D}},\tag{100}
$$

where the constants may be of order unity. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/8afa233b66c4f28c67f50fb163abf90081f402e2cea5b3c4a377bee9e0c38a38.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/496ba576f78adee6846554736f020f547e19fb82f638e629677b6d605cd75800.jpg)



FIGURE 19. Assorted characteristic times as functions of wave-number, computed for $U_0 t / M = 42$ .


The oversimplicity of the discussion means that there is little point in attempting analytical assignment of mutually consistent values of the C's, so we simply estimate them all as unity, giving the final time-scale spectrum, 

$$
\tau_ {*} (k) = \left\{\frac {1}{\tau_ {C}} + \frac {1}{\tau_ {R}} + \frac {1}{\tau_ {S}} + \frac {1}{\tau_ {D}} \right\} ^ {- 1},\tag{101}
$$

which is, of course, a function of time. 

Empirical curves of these five time spectra, along with $\tau_{0}$ , $\tau_{W}$ , $\tau_{H}$ and the viscous decay time, 

$$
\tau_ {\nu} \equiv (k ^ {2} \nu) ^ {- 1},\tag{102}
$$

are plotted in figures 19 and 20 for three different distances behind the grid. 

Figure 21 displays the success achieved in rescaling the narrow-band correlation coefficient functions $R(k; \overline{U} \Delta t, 0, 0; t_0, \Delta t)$ , presented in figure 16. Evidently the oversimplifications of mechanism independence and unit dimensionless constants are either viable, or lead to compensating errors. 

In figure 21 the extreme wave-number cases lie outside the general collapse region, but we note that $k = 0.25 \, cm^{-1}$ is near the spectral peak, near the region where the turbulence may still remember details of its grid-generation, so we expect no universal form (Batchelor & Stewart 1950). The $k = 7 \cdot 60$ case is far into the viscous dissipation region, and we have neglected the likely influence of viscous effects on e.g. $\tau_{D}$ , so it is not surprising that the $k = 7 \cdot 60$ and $10 \cdot 1$ 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/010b222201e93d0cae056e834e774f604cc53b6e79cd8be71fdcf6af8175bca3.jpg)



FIGURE 20. The downstream evolution of the combined characteristic time spectrum $\tau_{*}$ . $U_{0}t / M = 171$ , 98, 42.


cases do not scale as well as the others. For wave-numbers from 0·50 to 5 cm $^{-1}$ , the collapse due to rescaling the time interval by 

$$
\theta_ {*} (k, t _ {0}, \Delta t) \equiv \int_ {t _ {0}} ^ {t _ {0} + \Delta t} \frac {d t _ {1}}{\tau_ {*} (k , t _ {1})}\tag{103}
$$

is within the experimental scatter. Equation (103) is a specific case of (75). 

A byproduct of the present analysis should be a more proper ‘renormalization’ of the complete decaying turbulence, i.e. a more appropriate time rescaling than that in § 8. A shortage of time has postponed work on this problem. 

This work was supported primarily by the U.S. National Science Foundation, Engineering Division, and the U.S. Office of Naval Research, Fluid Dynamics Branch. It was presented at the 18th Annual Meeting, Division of Fluid Dynamics, American Physical Society, November 1966; also at the Euromech Symposium on the Structure of Turbulence, University of Southampton, March 1967. G. C.-B. was a Post-Doctoral Fellow at Johns Hopkins during the experiments (on leave from University of Grenoble), with later work done partly at University of Grenoble and l'École Centrale de Lyon. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/f9785f8fc367c938ab6457bbe4db650231e7a4d18061d5c2ff2f9ac5e31bb57e.jpg)



FIGURE 21. The collapse effected by rescaling the narrow-band space-time correlation functions of figure 16, in terms of the combined characteristic time $\tau_{*}$ .


$$
\left. \begin{array}{c c c c} \square 0 \cdot 2 5 & \nabla 1 \cdot 0 1 & \triangle 3 \cdot 0 3 & \ominus 7 \cdot 6 0 \\ \triangle 0 \cdot 5 0 & \diamond 1 \cdot 5 2 & \textcircled {1} 4 \cdot 0 4 & \square 1 0 \cdot 1 0 \\ \otimes 0 \cdot 7 6 & \oplus 2 \cdot 2 8 & \triangle 5 \cdot 0 5 & \end{array} \right\} (k   \mathrm{cm} ^ {- 1})
$$

We thank particularly A. Y.-S. Kuo for his important contributions to the experiments. J. Shlien, V. G. Harris, D. Kennedy, J. Newton, A. Eberhard, C. Wolf, and F. Ali helped from time to time on experiments or computations. F. Paquet and V. Griggs drew most of the figures, and J. Zee and P. Brougham prepared the typescript. Finally, we gratefully acknowledge manuscript corrections by R. Blackwelder, and useful conversations with Professors H. Ribner and O. M. Phillips. 

## Appendix A. Minimization of error due to wake effect of upstream probe

A familiar difficulty in measurement with one probe downstream of the other is the extraneous disturbance at the downstream probe caused by the upstream probe wake. A common practice for reducing consequent measurement error is to place the downstream probe just outside of the wake, and to assume that the (perhaps $2^{\circ}$ to $5^{\circ}$ ) misalignment with the mean flow direction gives a negligible change in e.g. correlation, compared with the desired aligned case. Some authors neglect to mention a procedure for reducing this wake error. 

Its importance can be seen from the comparisons of typical correlation measurements in table 9, one set made with the downstream wire directly behind the upstream wire $(\Delta x_{2}=0)$ , and the other set obtained by extrapolating to $\Delta x_{2}=0$ the correlation values obtained for a series of $\Delta x_{2}$ positions outside the wake. 

The wake error can be large, even for full-band or small-wave-number correlations. Therefore, the technique used in all cases with possible interference was to measure the desired function for several lateral distances $\Delta x_{2}$ outside the wake, then to extrapolate these values of $R_{11}(\overline{U}\Delta t,\Delta x_{2},0;t_{0},\Delta t)$ to the $\Delta x_{2}=0$ limit. Symmetry in $\Delta x_{2}$ dictated zero slope at $\Delta x_{2}=0$ . 

<table><tr><td><eq>k_1</eq></td><td><eq>R_{11}^{(1)}(k_1; \bar{U}\Delta t, 0, 0; t_0, \Delta t)</eq>measured directly</td><td><eq>R_{11}^{(1)}(k_1; \bar{U}\Delta t, 0, 0; t_0, \Delta t)</eq>by extrapolation</td></tr><tr><td>Full band</td><td>0·775</td><td>0·89</td></tr><tr><td>0·50</td><td>0·83</td><td>0·94</td></tr><tr><td>2·28</td><td>0·63</td><td>0·83</td></tr><tr><td>5·05</td><td>0·45</td><td>0·72</td></tr><tr><td>10·1</td><td>0·19</td><td>0·55</td></tr><tr><td></td><td colspan="2">TABLE 9. <eq>\bar{U}\Delta t/M = 0·75</eq></td></tr></table>

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/ee1e5c55339a65ccf7fdab9735222a45b90b7e92db6214e05ef26c7f50a703d5.jpg)



FIGURE 22. Typical space-time correlation functions with downstream probe outside the wake of the upstream probe. $\Delta x_{1} / M = 4$ . $\Delta x_{2} / M$ : $\square, 0\cdot 05; \bigcirc, 0\cdot 125; \diamond, 0\cdot 225; \triangle, 0\cdot 4$ .


Figure 22 shows typical full-band space-time correlation curves at a series of $\Delta x_{2}$ for a single stream-wise spacing, $\overline{U}\Delta t = 4M$ . Here the detectable half-width of the wake is about $0\cdot 15M$ , so the $\Delta x_{2} = 0\cdot 05M$ data are presumably slightly reduced by the wake. The 'experimental value' of $R_{11\max}(4M,0,0;\Delta t)$ is obtained by cross-plotting the peak values against $\Delta x_{2}$ and extrapolating to $\Delta x_{2} = 0$ . This corresponds to the dashed curve in figure 23(c). 

Figure 23 shows an assortment of analogous extrapolations to $\Delta x_{2} = 0$ for some narrow-band space-time correlation functions. The $\Delta x_{2} = 0$ intercepts (obviously quite inaccurate for small $\overline{U}\Delta t / M$ and large $k_{1}$ ) give the data points in figure 14. 

The special cases for $\Delta x_{1}=0$ and $\Delta t=0$ were measured much more extensively in order to help guide the extrapolations, and are given in figure 24. The full-band curve is just the Kármán–Howarth g function (figure 5(a)). 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/84dce2ed5fd0906b6361213d23a5667dbeb51539531a5ecef0138ef487ab1798.jpg)



FIGURE 23. Typical extrapolations used to avoid error due to wake of upstream probe. $\overline{U}\Delta t / M$ : (a) 0·375, (b) 0·75, (c) 4.


## Appendix B. Effect of finite widths of narrow-band filters

For power spectrum measurement with narrow-band-pass filters, in principle one solves an integral equation: 

$$
S _ {\text { measured }} (\omega) = \frac {\int_ {0} ^ {\infty} \phi \left(\omega^ {\prime} , \omega\right) S \left(\omega^ {\prime}\right) d \omega^ {\prime}}{\int_ {0} ^ {\infty} \phi \left(\omega^ {\prime} , \omega\right) d \omega^ {\prime}},\tag{B 1}
$$

where $\phi$ is the filter function, $\omega$ is radian frequency. When the filter shape $\phi(\omega',\omega)$ is narrow enough compared with the spectrum to be measured, e.g. when 

$$
\frac {\Delta (\omega)}{S (\omega)} \left| \frac {d S}{d \omega} \right| \ll 1,\tag{B 2}
$$

where $\Delta(\omega)$ is an effective bandwidth, then $\phi$ can often be treated as a Dirac function in (B 1), giving 

$$
S _ {\text { measured }} (\omega) \doteq S (\omega).\tag{B 3}
$$

It seems likely that condition (B 2) is irrelevant when the filter function is symmetric about a centre frequency. Then an inequality involving the second derivative of S is appropriate. 

A possible choice for $\Delta (\omega)$ might be 

$$
\Delta (\omega) \equiv \phi_ {\mathrm{max}} ^ {- 1} \int_ {0} ^ {\infty} \phi (\omega^ {\prime}, \omega) d \omega^ {\prime}.\tag{B 4}
$$

But in testing the bandwidth effect we used a simpler choice (in cyclic frequency): $\Delta N$ in figure 31 is the difference between the frequencies at which the mean 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/c20c8d11d468297865c77d8f1c2dde4ab29eb67296397000a07f2e95e32e6427.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/ba3c46ff08cd45c05b0e08444df7a6472f9f5b3e353928f991945d1cbd0c7395.jpg)



FIGURE 24. The limiting case $(\Delta x_{1} = 0)$ of the curves in figure 23. ---, $R_{11}$ total signal (full-band transverse correlation function).


$$
\begin{array}{c c c c} \bigcirc 0 \cdot 1 0 & \triangle 0 \cdot 5 0 & \diamond 1 \cdot 5 2 & \triangle 5 \cdot 0 5 \\ \square 0 \cdot 2 5 & \otimes 0 \cdot 7 6 & \triangle 3 \cdot 0 3 & \square 1 0 \cdot 1 0 \end{array} \left. \begin{array}{l} (k _ {1} \mathrm{cm} ^ {- 1}) \end{array} \right.
$$

square response was 15 db down from the peak. Condition (B 2) held for the Hewlett–Packard analyzer (figure 3(a)) and the spectra encountered here. The Dytronics filter band shape (figure 3(b)) is more pointed at the narrowest setting ('high selectivity'), but has a slower decrease at the 'tails'. In fact, the decrease is so slow that it is imprudent to rely on (B 2) and (B 4) as a sufficient condition. Instead, we determined some values of $R_{11}^{(1)}$ with all three bandwidth settings of the Dytronics filters: figure 25. The change in measured $R_{11}^{(1)}$ at fixed nominal $k_{1} = \overline{U} / (2\pi f_{0})$ , with varying $\Delta f$ , is the effect of bandwidth. 

For measurements in the frequency range $f < 200 \, Hz$ it was decided to use the low selectivity (wide) setting, for $200 \leqslant f \leqslant 600 \, Hz$ the medium selectivity, 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/fdb6e9c4fe4ed381852b91c2099043ccd064ab56b040c269ff4b17c621dfe416.jpg)



FIGURE 25. Typical extrapolations used to correct for effect of finite band width in measurement of narrow-band space-time correlations. $\overline{U}\Delta t/M = 0\cdot75$ ; $\Delta x_{2}/M = 0\cdot05$ .


for $f > 600\mathrm{Hz}$ the high selectivity. It is convenient to use as wide a band as permissible at each frequency, because in practice the signal from a wider band fluctuates less wildly, and is therefore easier to measure. This is presumably a reflection of the Fourier form of the Heisenberg 'uncertainty principle', which says in this application that the response time of a filter is inversely proportional to its bandwidth. A quantitative example is given by Lumley & Panofsky (1964) for the special case of a Gaussian input signal with simple exponential autocorrelation function. For a relative r.m.s. error of $\epsilon$ in spectrum measurement using a rectangular bandpass filter of width $\Delta \omega$ , the required averaging time is 

$$
T = \frac {2 \pi \sqrt {2}}{\Delta \omega \epsilon^ {2}}.\tag{B 5}
$$

The highest selectivity seemed still inadequate for the 4 kHz region, and the extrapolation to $\Delta f$ seemed very uncertain, so these data are omitted from the report. 

When the filter function has the form, 

$$
\phi (\omega^ {\prime}, \omega) = \psi (\omega^ {\prime} - \omega),\tag{B 6}
$$

as in the Hewlett–Packard Wave Analyzer, (B 1) can be easily solved for $S(\omega)$ , and the filter need not approximate a Dirac function. 

On the other hand, when the filter function has the form, 

$$
\phi (\omega^ {\prime}, \omega) = \beta (\omega^ {\prime} / \omega),\tag{B 7}
$$

as in the Dytronics filters, the inversion of (B 1) is difficult. 

## Appendix C. Tape recorder deficiencies

Although magnetic tape recorders are useful devices for storing information and especially for thus permitting correlation measurements with time delay, they introduce errors into the measurement process. Some sources are the following: 

(i) resolution limitations and noise in the magnetization and pickup operations, 

(ii) inaccuracies in the signal modulation and demodulation processes, when modulation is used, 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/1756cd2f8a162f02885ef83b2cff5b6244bb8b7adea1f3fd4406507af4e500ce.jpg)



FIGURE 26. Correlation function performance of Sangamo tape recorder: maximum correlation coefficient attainable in playback of a recorded sine wave of frequency N kHz.


(iii) ‘drop-outs’ (i.e. lost counts in the timing signal caused usually by dirt on the tape), 

(iv) extraneous signals due to imperfect mechanical translation of the tape in both record and playback steps ('jitter', 'flutter', etc.). 

Ordinarily, it was possible to avoid drop-out errors by careful selection and handling of the tape. The magnetization, detection, modulation, and demodulation are done with sufficient accuracy in these units that no special correction needed to be developed. Most of the record-playback error seems to be due to imperfect motion of the tape. 

Rather than try to isolate individual sources, however, we simply recorded sinusoidal signals at various frequencies and measured their autocorrelation function maxima (which should be 1·00) in playback. The results (figure 26) are a bit scattered, but they seem to show accuracy to about 1% from d.c. to perhaps 3 kHz. No narrow-band correlation data are presented in this report for frequencies above 2 kHz, but meaningful data could probably be obtained at higher frequencies by using corrections based on figure 26. 

## Appendix D. The interpretation of time dependence at a point in the tunnel as space dependence: the Taylor approximation

Taylor (1938) suggested that, when the turbulence level is low enough (i.e. $(\overline{u_{i}u_{i}})^{\frac{1}{2}}\ll\overline{U}$ ), the evolution in spatial pattern of a lump of fluid during its transit past a fixed probe may be so slight that the pattern is effectively ‘frozen’ during passage. Then probe-signal changes with time are due only to spatial nonuniformities being convected past the probe at speed $\overline{U}$ . This idea is often referred to as ‘Taylor’s hypothesis’; the term ‘Taylor’s approximation’ may be better. A theoretical estimate of its range of validity in flow carrying isotropic turbulence was made by Lin (1953), who also introduced the important notion of shear-caused failure of the approximation. Uberoi & Corrsin (1953) offered a somewhat different estimate for the isotropic case. Both indicated that the ‘frozen pattern’ requirement for Taylor’s approximation is well satisfied in the nearly isotropic turbulence far behind periodic grids spanning wind tunnel test sections. 

It should be noted that, if the pattern were indeed 'frozen', then the spacetime correlation coefficient with time delay equal to mean transit time between probes $(\Delta t = \Delta x_{1} / \overline{U})$ would always equal unity. In other words, 

$$
R _ {1 1} (\Delta x _ {1}, 0, 0; t _ {0}, \Delta x _ {1} / \overline {{U}}) = 1 {\cdot} 0 0
$$

for all $\Delta x_{1}$ . The very fact that this drops below 1·00 (see e.g. figure 14) shows that the Taylor approximation is not exact. 

The first actual (experimental) confirmation of the approximation was by Favre et al. (1952) in grid turbulence, for small and moderate probe separations; Frenkiel & Klebanoff (1966) also found good agreement. Favre et al. (1964) found that, in a boundary layer, Lin's concern about the effect of shear is appropriate. Heskestad (1965) suggested a rough 'correction' for estimating spatial structure from temporal data when the Taylor approximation is nearly applicable. Fisher & Davies (1964) pursued the approximation into spectrally local detail; and Lumley (1965) presented the most extensive analysis. 

In spectral space the Taylor approximation consists in replacing measured frequency $\omega$ by $k_{1}\overline{U}$ , so that e.g. a frequency spectrum $S(\omega)$ , measured with a single $u_{1}$ probe, is taken to be equal to the wave-number spectrum $E_{11}^{(1)}(\omega/\overline{U})$ . In correlation space, the corresponding expression, $\Delta t_{measured} \leftrightarrow \Delta x_{1}/\overline{U}$ , connects a measured autocorrelation function of time with a spatial autocorrelation: 

$$
R _ {1 1} (\Delta x _ {1}, 0, 0; t _ {0}, 0) \doteq R _ {1 1} (0, 0, 0; t _ {0}, \Delta x _ {1} / \overline {{{U}}}).\tag{D 1}
$$

In the present experiments this type of correspondence is used for correlations of pairs of narrow-band signals as well. The two-probe 'space-time correlation' $R_{11}^{(1)}(k_1; \Delta x_1, \Delta x_2, \Delta x_3; t_0, \Delta t)$ is actually measured as 

$$
\frac {e _ {1} (\omega ; x _ {0 _ {1}} , x _ {0 _ {2}} , x _ {0 _ {3}} ; t ^ {\prime}) e _ {1} (\omega ; x _ {0 _ {1}} + \Delta x _ {1} , x _ {0 _ {2}} + \Delta x _ {2} , x _ {0 _ {3}} + \Delta x _ {3} ; t ^ {\prime} + \Delta t)}{[ \overline {{e _ {1} ^ {2}}} (\omega ; x _ {0 _ {1}}) \overline {{e _ {1} ^ {2}}} (\omega ; x _ {0 _ {1}} + \Delta x _ {1}) ] ^ {\frac {1}{2}}}\tag{D 2}
$$

in laboratory co-ordinates. $e_{1}$ is the voltage fluctuation of a $u_{1}$ -probe. The argument $\omega$ denotes narrow band-pass filtration centred at frequency $\omega$ . 

In this appendix we exploit our new spectral coherence time $\tau_{*}(k)$ to state in the sense of Fisher & Davies a spectrally local condition necessary for use of the Taylor approximation in unsheared, laterally homogeneous turbulence. We also introduce a new condition, one which bounds the permissible downstream inhomogeneity. We find experimentally that the Taylor approximation (used in this work to infer the turbulent energy spectra in wave-number) is well confirmed, except perhaps at very small wave-numbers, where the homogeneity is not good. 

For the hypothetical case of fully isotropic (hence homogeneous) turbulence convected past a ‘fixed’ probe at velocity $\overline{U}$ , Taylor’s original notion of a ‘frozen pattern’ might be given the spectrally local requirement that 

$$
\tau_ {*} (k) \geqslant 1 / (\overline {{{U}}} k),\tag{D 3}
$$

i.e. that the turbulent structure of size $k^{-1}$ have a coherence time much larger than its convective passage time. 

Actually, the convective passage time depends directly on wave-number components $k_{1}$ in the $\overline{U}$ -direction rather than on k. For any Fourier element whose constant phase surfaces have a normal at angle $\alpha$ to the $\overline{U}$ -direction, the operable wavelength scale is $\Lambda_{1} = (2\pi)/(k \cos \alpha)$ . For an isotropic field, the appropriate analysis gives a directional average wavelength $\tilde{\Lambda}_{1} = 2\pi/k$ , a result which includes the fact that the relative rate at which a probe encounters ‘zero-surfaces’ of any Fourier element is $\cos \alpha$ . 

We might therefore want to replace (D 3) by something like 

$$
\tau_ {*} (k) \gg 6 / \overline {{{U}}} k,\tag{D 4}
$$

which is not significantly different. 

The difference between (D 3) and earlier criteria for the same case is in the choice of coherence time. $\tau_{0}(k) \equiv [k^{3}E(k)]^{-\frac{1}{2}}$ has been a customary choice in the past. The success of $\tau_{*}(k)$ in scaling spectrally local autocorrelation functions in time (see figure 21) suggests that it is the appropriate time. Since $\tau_{*}(k) < \tau_{0}(k)$ , the condition $\tau_{0}(k) \gg (\overline{U} k)^{-1}$ instead of (D 3) would be non-conservative. 

The small structure is convected by turbulent large structure as well as by $\overline{U}$ . Can this subvert the Taylor approximation even where (D 3) is satisfied? The main effect of having convecting speed $\overline{U} + u_1$ , with $u_1 (\ll \overline{U})$ taking on random values (though fixed during the passage time $[( \overline{U} + u_1) k]^{-1})$ , is to spread the contribution of single wave-number component $k_1$ over a band in $\omega$ . This phenomenon was mentioned by Fisher & Davies, and it was estimated by 

Lumley; it is negligible in the present experiment. Heskestad (1965) estimated the full-band error due to this self-convection of the turbulence. The effect is obviously small for small turbulence level. In the present experiment this, too, is negligible. 

No matter how well condition (D3) is satisfied, the Taylor approximation can never be entirely valid in decaying grid-turbulence, because the probe signal $e_{1}(t')$ is statistically stationary in $t'$ while the 'corresponding' velocity component 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/fd6f518da3bf0c4879122ba0618800b0cc129cd096afd98dd2cd93a81b3ef3e3.jpg)



FIGURE 27. Test of Taylor approximation for equivalence of streamwise spatial correlation and time autocorrelation of the signal from a single probe.


$$
+, R _ {1 1} \left(\Delta x _ {1}, 0, 0; t _ {0}, 0\right); \odot , R _ {1 1} \left(0, 0, 0; t _ {0}, \Delta x _ {1} / \bar {U}\right).
$$

spatial distribution $u_{1}(x_{1})$ is statistically non-stationary in $x_{1}$ . A relevant strong inequality necessary for the Taylor approximation may be 

$$
\frac {1}{E (k ; x _ {1})} \left| \frac {\partial E}{\partial x _ {1}} \right| \frac {1}{k} \ll 1,\tag{D 5}
$$

or we may want to look directly at the inhomogeneity of the one-dimensional spectrum, and require 

$$
\frac {1}{E _ {1 1} \left(k _ {1} ; x _ {1}\right)} \left| \frac {\partial E _ {1 1}}{\partial x _ {1}} \right| \frac {1}{k _ {1}} \ll 1.\tag{D 6}
$$

Before putting numbers into the necessary conditions (D 3) and (D 5) or (D 6) for the present experiment, we can make a direct empirical check. Where the Taylor approximation is good, we should find that equation (D 1) is satisfied. Consistent with the full-band data of Favre et al., figure 27 shows that this is indeed satisfied (in the sense that the difference is much smaller than the local value) out to the first zero. Beyond there, the accuracy of both sets of data is too low to permit a conclusion. There is no precise local correspondence between a $\Delta x_{1}$ value and a wave-number value (see remarks in appendix A), but, in the loosest sense, we conclude that the approximation may be good at least for wave-numbers above the inverse of the $\Delta x_{1}$ at which this $R_{11}$ has its first zero. 

Next, we use the experimental results to inspect the two necessary conditions, (D 3) and (D 6). 

The ‘frozen pattern’ condition, (D 3), turns out empirically to be well satisfied for both ends of the wave-number range. Figure 28 shows this for our ‘worst’ case, $U_{0}t/M = 42$ . Analytically, the trend can be seen by computing $\tau_{*}(k)$ for a simplified Kolmogorov model: 

$$
\begin{array}{l} E (k) \approx e ^ {\frac {2}{3}} k _ {E} ^ {- \frac {1 7}{3}} k ^ {4} \quad \text { for } \quad 0 \leqslant k \leqslant k _ {E}, \\ E (k) \approx e ^ {\frac {2}{3}} k ^ {- \frac {5}{3}} \quad \text { for } \quad k _ {E} \leqslant k \leqslant k _ {K}, \\ E (k) = 0 \quad \text { for } \quad k > k _ {K}. \end{array}
$$

$k_{E}$ characterizes the peak of $E(k)$ and $k_{K}$ is the inverse of the Kolmogorov microscale. The resulting statements of condition (D 3) are the following: for $0 \leqslant k \leqslant k_{E}$ , 

$$
\overline {{U}} k \tau_ {*} (k) \approx \frac {1 \cdot 2 \left(\frac {k _ {E}}{k}\right) \left(\frac {\overline {{U}}}{u _ {1} ^ {\prime}}\right)}{1 \cdot 4 \left(\frac {k}{k _ {E}}\right) ^ {\frac {3}{2}} + \left[ 1 - \frac {8}{1 7} \left(\frac {k}{k _ {E}}\right) ^ {3} \right] ^ {\frac {1}{2}}} \gg 1.\tag{D 7}
$$

For $k_{E} \leqslant k \leqslant k_{K}$ , 

$$
\begin{array}{r l} \overline {{U}} k \tau_ {*} (k) & \approx \left(\frac {k}{k _ {E}}\right) \left(\frac {\overline {{U}}}{u _ {1} ^ {\prime}}\right) \left\{1 \cdot 3 \frac {k}{k _ {E}} \left[ 1 - \frac {1 5}{1 7} \left(\frac {k _ {E}}{k}\right) ^ {\frac {8}{3}} \right] ^ {\frac {1}{2}} + 1 \cdot 6 \left[ \frac {2 1}{1 7} \left(\frac {k}{k _ {E}}\right) ^ {\frac {4}{3}} - 1 \right] ^ {\frac {1}{2}} \right. \\ & \qquad \left. + 0 \cdot 6 \left(\frac {k _ {K}}{k _ {E}}\right) ^ {\frac {2}{3}} \left(\frac {k}{k _ {K}}\right) ^ {2} \left[ \left(\frac {k _ {K}}{k}\right) ^ {\frac {8}{3}} - 1 \right] ^ {\frac {1}{2}} \right\} ^ {- 1} \gg 1. \end{array}\tag{D 8}
$$

To confirm that these are consistent at $k = k_{E}$ when $R_{\lambda}$ is large enough, we need only use a rough theoretical estimate for the ratio of Kolmogorov wave-number $k_{K}$ to ‘energetic’ wave-number $k_{E}$ (e.g. Corrsin 1959, 1964): 

$$
k _ {K} / k _ {E} \approx R _ {\lambda} ^ {\frac {3}{2}} / 1 0.\tag{D 9}
$$

Evidently (D 7), hence (D 3), is increasingly well satisfied as $k \to 0$ . For $R_{\lambda}$ large enough that $k_{K} \gg k_{E}$ , we find a typical in-between estimate at $k = k_{E}$ : $\overline{U} k_{E}\tau_{*}(k_{E}) \approx 0 \cdot 6(\overline{U}/u_{1}')$ , which is much larger than unity in this flow. 

Turning next to the quasi-homogeneity requirement for the Taylor approximation, (D 5), we see, from the empirical results in figure 29, that it is well satisfied over the full spectral range. The data for figure 29 are for $U_0 t / M = 42$ , the 'worst' case. It is interesting to note from figure 29, however, that the analogous strong inequality condition on the one-dimensional spectrum, (D 6), is not fulfilled for the very largest eddies. We can take the crudest sort of analytical look at homogeneity conditions (D 5) and (D 6) by using the grossest sorts of measures in the energetic spectral range and in the dissipative spectral range. 

For the energetic part of the spectrum, these are roughly equivalent to 

$$
\frac {L}{\overline {{u _ {1} ^ {2}}}} \left| \frac {d \overline {{u _ {1} ^ {2}}}}{d x _ {1}} \right| \ll 1,\tag{D 10}
$$

a condition not too well met in grid turbulence of this type for $U_{0}t/M < 100$ (Corrsin 1963b). 

For the dissipative part of the spectrum, we can put $k = k_{K}$ into (D 5), and, for simplicity, assume the Kolmogorov isotropic inertial subrange spectrum as $E(k) \approx \epsilon^{\frac{2}{3}} k^{-\frac{k}{2}}$ . Then (D 5) becomes 

$$
\frac {2}{3} \frac {\nu^ {\frac {3}{4}}}{\epsilon^ {\frac {5}{4}}} \left| \frac {d \epsilon}{d x _ {1}} \right| \ll 1.\tag{D 11}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/4121fab066a248df411a4ea4eb2b59fef45064f9848f8d279664ab4fa4f7de16.jpg)



FIGURE 28. Test of (D 3), a spectrally local condition necessary for the Taylor approximation.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/76313efc51f980ab1ca491d5263a38a07d994974b623c96f8ce41b5b15d1c404.jpg)



FIGURE 29. Tests of (D 5) and (D 6), two spectrally local homogeneity conditions necessary for the Taylor approximation. ——, $1/E_{11}^{(1)}|\partial E_{11}^{(1)}/\partial x_1|1/k_1$ ; ---, $1/E|\partial E/\partial x_1|1/k$ .


Inserting the empirical results for $\epsilon$ (e.g. as computed from the energy decay, (38)), we find (D 11) well satisfied. The largest value of the left side in the experimental region is $2 \times 10^{-4}$ , at $U_{0}t/M = 42$ . 

Our conclusion, based on both the empirical and the theoretical estimates of (D 3) and (D 6), is that the Taylor approximation is usable in flows of this type except, possibly at extremely low wave-numbers (large separation distances in correlation space), where the ‘frozen pattern’ condition holds, but the homogeneity condition may not. This casts doubt on the usefulness of comparing theoretical ‘box turbulence’ correlation functions for large space and/or time separations with the corresponding functions measured in wind tunnel flows. 

## Appendix E. Estimation of integral scale values

## (i) The non-existence of integral scales in real experiments

Among the statistical properties of physical interest in random fields like turbulence are the ‘integral scales’. The ‘integral scale’ of a stationary random function (a concept probably introduced by Taylor 1921) is ordinarily defined to be the integral of the autocorrelation coefficient function: 

$$
I _ {\gamma} \equiv \frac {1}{\overline {{{{\gamma^ {2}}}}}} \int_ {0} ^ {\infty} \overline {{{{\gamma (t) \gamma (t + \tau)}}}} d \tau = \frac {1}{\mu_ {\gamma} (0)} \int_ {0} ^ {\infty} \mu_ {\gamma} (\tau) d \tau ,\tag{E 1}
$$

where $\gamma(t)$ is a stationary random function with zero mean value. The Fourier transform connexion between autocovariance and spectrum gives the familiar proportionality between $I_{\gamma}$ and the spectrum value at zero frequency: 

$$
E _ {\gamma} (\omega) = \frac {2}{\pi} \int_ {0} ^ {\infty} \mu_ {\gamma} (\tau) \cos (\omega \tau) d \tau .\tag{E 2}
$$

Therefore, with $\omega = 0$ , 

$$
I _ {\gamma} = \frac {\pi}{2} \frac {E _ {\gamma} (0)}{\overline {{{\gamma^ {2}}}}}.\tag{E 3}
$$

If t is time, $I_{\gamma}$ has the dimensions of time, and may sometimes be thought of as a characteristic fluctuation time. This interpretation is fully appealing only if $\mu_{\gamma}(\tau) \geqslant 0$ (figure 30). For the purposes of this discussion we shall assume that the integral scale is of interest. 

A real experiment, however, lasts only a finite time, so it is clear that $E_{\gamma}(0) = 0 = I_{\gamma}$ for any real signal. Real experiments are also non-infinite in size, so we conclude analogously that spatial integral scales are also zero in principle. 

How shall we interpret the non-zero ‘measured’ integral scales presented by so many experimenters through the years? Evidently, these must be the integral scales of hypothetical infinite fields which do not actually exist, but are consistent with the real fields and are much easier to analyze theoretically because they may be stationary in time and/or space. 

## (ii) The non-measurability of integral scales with real instruments

Suppose we actually have a phenomenon of infinite duration. Can we measure its integral scale? The answer is, of course, ‘no’ in principle. 

(a) Finite observation time. The most obvious reason is that we can't observe/record the signal over an infinite interval, so we can't reach $\omega = 0$ even if our instrument is 'd.c.-coupled' (i.e. responds faithfully down to zero frequency). This limitation applies to recorded signals processed by digital computer, as well as to analog-circuit processing. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/5e3828ea1046bff07485f10674876364b47f61b8ec2cefb0eae1a060baf49654.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/121ba775479d14eafe00cbbdaa381693e2fc2c8f2dc956313d2a6a5b9a8cbcbc.jpg)



FIGURE 30. Contrasting types of correlation functions, sketched with their 'integral scales' $L_{\gamma}$ may not be a plausible measure of 'average duration' if $\mu_{\gamma}$ has an appreciable negative region.


(b) Instrument response time as $\omega\to0$ . Another reason is that the response time of our device, presumably a variable band-pass filter to determine $E_{\gamma}(\omega)$ , becomes infinite as the band-width $\Delta\omega$ approaches zero. To measure $E_{\gamma}(\omega)$ as $\omega\to0$ , we must have $\Delta\omega\to0$ as well. 

(c) Limitations of a.c.-coupled systems. For a variety of reasons, it is often convenient to use 'a.c.-coupling', as we have in the present investigation. If the low end cut-off frequency $\omega_{L}$ is smaller than $t_{\mathrm{max}}^{-1}$ , the inverse of the duration of the experiment, no information is lost. In practice, $\omega_{L}$ is, however, considerably larger than $t_{\mathrm{max}}^{-1}$ . For example, many of the measurements reported here were made with $\omega_{L}/(2\pi)=1\mathrm{Hz}$ , whereas the signals were averaged over perhaps 60 sec, so $t_{\mathrm{max}}^{-1}=\frac{1}{60}\mathrm{sec}^{-1}$ , and some information is lost. The lost information may not, however, be significant to the research. At a convecting speed of 10 m sec $^{-1}$ , 1 Hz corresponds to a length of 10 m. But the wind tunnel is only 1 m wide, so some of the signal fluctuations at frequencies below 10 Hz are due to eddies larger than the duct width; hence, they are not relevant to the study of 'unbounded' turbulence. 

The foregoing remarks utilize the Taylor approximation, and are not concerned with the basic frequencies of the turbulent motion in a frame convected with the mean flow. Our rough estimate of the fundamental integral time scale in that frame gave $T \approx 0.18$ sec, which suggests that interesting events in the turbulence may be occurring at frequencies well below 5 Hz. Unfortunately these events (which are appropriate to nearly isotropic turbulence, because $u'T \approx 4 \text{ cm} = O(L)$ ) must be mixed up in the recorded signal with the convected fluctuations characteristic of eddies as large as the duct. 

A demonstration of the influence of $\omega_{L}$ , the low cut-off, on temporal autocorrelation can be computed easily by assuming an exponentially correlated input function and a ‘measuring circuit’ with a resistance–capacitance high-pass 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/25dc76d48faccc268d9238aabb3fa71a68700759d762ea55ab62bb279a2fe6fc.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/f65dd8cc4ff1ad16b69c83523996e2c7c61e10cf343139fb2d88649ea0709fec.jpg)



FIGURE 31. Demonstration of the effect of low-frequency cut-off (Hz) on measured time autocorrelation function. $U_0 t / M = 42$ , ——, 1; ——, 5; ——, 10.


filter (6 db/octave cut-off), as in e.g. Anderson (1966).† Direct measurements using a single-probe signal at $U_0 t / M = 42$ , at a mean speed of $\overline{U} = 12 \cdot 7 \, \text{m sec}^{-1}$ , are shown in figure 31. The nominal ('3 db') values of lower cut-off frequency are $\omega_L / (2\pi) = 1 \, \text{Hz}$ , $5 \, \text{Hz}$ and $10 \, \text{Hz}$ . As we might expect, the effect is greatest at larger $\tau$ , but it is important to note that it extends well below $\omega_L^{-1}$ . 

The effects of $\omega_{L}$ on measurements of 2-probe spatial correlation functions cannot be computed without a correct theory of turbulent motion, but we expect the lowest frequencies to be associated with the biggest eddies. For the convected spatial inhomogeneities this is obvious. For the turbulence self-convection (the only time dependence in the $\overline{U}$ -convected frame), the association arises in our concepts of spectrally local characteristic times such as $\tau_{0}$ or even $\tau_{*}$ . Figure 32 is an experimental demonstration of the effect. For the same $\omega_{L}$ , the one-probe correlation has a larger negative region than does the two-probe correlation. 

Similar effects were observed in space-time correlation data for different $\omega_{L}$ . 

† The presentations of Nayar, Siddon & Chu (1969), and by Lumley (1970) are also useful. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/c4013d23539baa3de493139dba606b3d096a6d2fc0de13798df68315ae4c58bf.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/87395cf7148aebda9c7eac43de2e9079f0563190728bd876b39a1dd767a6cd36.jpg)



FIGURE 32. Effect of low-frequency cut-off (Hz) on measured spatial correlation function. $U_0 t / M = 42$ , 1; +, 10; △, 1000.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-08-03/45a8a41b-9b73-4266-b667-6a6d282609f8/abf4df0e7030103487ddf6da617f59e2fe0eac103c3c1ef52b31a3726cfa81d8.jpg)



FIGURE 33. Qualitative sketch of a method for determining an integral scale of a hypothetical isotropic turbulence consistent with actual nearly isotropic turbulence in a duct of characteristic size W. The (parabolic) small- $k_{1}$ form of the hypothetical field is known on mathematical grounds.


## (iii) Actual procedures for integral scale 'measurement'

The commonest techniques for ‘measuring’ integral scales, e.g. in time, are based on extrapolation of a partially measured $\mu_{\gamma}(\tau)$ function (to be able to apply (E 1)) and/or extrapolation of a partially measured $E_{\gamma}(\omega)$ function (to be able to apply (E 3)). For reasons given earlier, we can determine $\mu_{\gamma}(\tau)$ only in some finite range $0 \leqslant \tau \leqslant \tau_{max}$ , and $E_{\gamma}(\omega)$ only for $\omega \geqslant \omega_{min}$ . 

The forms of the extrapolations may depend primarily on artistic taste, or they may be based on some theoretical concepts of asymptotic behaviour. The crucial point is that physically correct extrapolations must give $I_{\gamma}=0$ . So we don't make correct extrapolations. Instead, we make what might be called 'simple extrapolations', hoping that they correspond to a mathematically possible flow field which is identical to the real field at moderate and large frequencies and wave-numbers. This hypothetical field must have infinite duration in time if we give it a non-zero integral time scale (and extend it to infinity in whatever spatial direction we give it an integral length scale). The real spectrum and the hypothetical spectrum merge at the frequency (or wave-number) which characterizes the low cut-off (or inverse size) of the experiment or of the measuring system, whichever is larger. 

Figure 33 is a qualitative sketch of how we might extrapolate to zero the data for $E_{11}(k_1)$ in nearly isotropic turbulence. Mathematically we know that $[E_{11}(k_1)]_{\text{isotropic}}$ must begin at $k_1 = 0$ as a downward parabola, so we try to fit the 'best parabola'. 

## REFERENCES



ANDERSON, O. K. 1966 On the distortion of measured correlation functions caused by the frequency response of the measuring system. DISA Information, 3, 21–27. 





BALDWIN, L. V. & MICKELSEN, W. R. 1962 Turbulent diffusion and anemometer measurements. J. Eng. Mech. Div., Proc. Am. Soc. Civil Engrs, 88, 37–69. 





BALDWIN, L. V. & WALSH, T. J. 1961 Turbulent diffusion in the core of fully developed pipe flow. A.I.Ch.E. J. 7, 53–61. 





BASS, J. 1954 Space and time correlations in a turbulent fluid. University of California, Publications in Statistics, 2 (3) 55–84. 





BATCHELOR, G. K. 1953 The Theory of Homogeneous Turbulence. Cambridge University Press. 





BATCHELOR, G. K. & STEWART, R. W. 1950 Anisotropy of the spectrum of turbulence at small wave-numbers. Quart. J. Mech. Appl. Math. 3, 1–8. 





BATCHELOR, G. K. & TOWNSEND, A. A. 1948 Decay of turbulence in the final period. Proc. Roy. Soc. A 194, 527–543. 





BATCHELOR, G. K. & TOWNSEND, A. A. 1956 Turbulent diffusion. Surveys in Mechanics (ed. G. K. Batchelor and R. M. Davies), 352–399. Cambridge University Press. 





BURGERS, J. 1951 On turbulent fluid motion. Hydrodynamics Lab., CALTECH, Rept. E-34.1. 





COMTE-BELLOT, G. & CORRSIN, S. 1966 The use of a contraction to improve the isotropy of grid-generated turbulence. J. Fluid Mech. 25, 657–682. 





CORRSIN, S. 1958 Local isotropy in turbulent flow. NACA Res. Mem. 58 B11. 





CORRSIN, S. 1959 Outline of some topics in homogeneous turbulent flow. J. Geophys. Res. 64, 2134–2150. 





CORRSIN, S. 1962a Theories of turbulent dispersion. Proc. Intern. Colloq. on Turbulence (Marseille 1961), Centr. Nat. Rech. Sci. 27–52. 





CORRSIN, S. 1962b Discussion of Baldwin & Mickelsen (1962). J. Eng. Mech. Div., Proc. Am. Soc. Civil Engrs, 88, 151–153. 





CORRSIN, S. 1963a Estimates of the relations between Eulerian and Lagrangian scales in large Reynolds number turbulence. J. Atmos. Sci. 20, 115–119. 





CORRSIN, S. 1963b Turbulence: experimental methods. Handbuch der Physik 8 (ed. S. Flügge and C. Truesdell), no. 2, 524–590. Springer. 





CORRSIN, S. 1964 The isotropic turbulent mixer. Part 2. Arbitrary Schmidt numbers. A.I.Ch.E. J. 10, 870–877. 





DEISSLER, R. G. 1961 Analysis of multipoint-multitime correlations and diffusion in decaying homogeneous turbulence. NASA, Tech. Rept. R-96. 





DRYDEN, H. L., SCHUBAUER, G. B., MOCK, W. C. & SKRAMSTAD, H. K. 1937 Measurements of intensity and scale of wind tunnel turbulence and their relation to the critical Reynolds number of spheres. NACA Rept. 581. 





FAVRE, A. 1948 Mesures statistiques de la correlation dans le temps. Proc. 7th Int. Cong. for Appl. Mech., London, 2, 44–55. 





FAVRE, A. 1965 Review on space-time correlations in turbulent fluids. J. Appl. Mech. 32E, 241–257. 





FAVRE, A., GAVIGLIO, J. & DUMAS, R. 1951 Mesures de la correlation dans le temps et l'espace et spectres de la turbulence en soufflerie. Colloque Intern. de Mecanique, Poitiers 1950. Publ. Sci. et Tech. Ministere Air 251, 293–309. 





FAVRE, A., GAVIGLIO, J. & DUMAS, R. 1952 Appareils de mesures de la correlation dans le temps et l'espace. Quelques mesures de correlation dans le temps et l'espace en soufflerie. Proc. 8th Int. Cong. for Appl. Mech., Istanbul, 304–314, 314–324. 





FAVRE, A., GAVIGLIO, J. & DUMAS, R. 1954 Correlation dans le temps et l'espace, avec filtre de bande, en aval d'une grille de turbulence. La Recherche Aeronautique, 40, 7–14. 





FAVRE, A., GAVIGLIO, J. & FOHR, J. P. 1964 Repartition spectrale de correlations spatiotemporelles de vitesse, en couche limite turbulente. Proc. 11th Int. Cong. for Appl. Mech., Munich, 878–888. 





FISHER, M. J. & DAVIES, P. O. A. L. 1964 Correlation measurements in a non-frozen pattern of turbulence. J. Fluid Mech. 18, 97–116. 





FRENKIEL, F. N. & KLEBANOFF, P. S. 1966 Space-time correlations in turbulence. Dynamics of Fluids and Plasmas (ed. S. I. Pai), 257–274. Academic. 





HEISENBERG, W. 1948 On the statistical theory of turbulence. Z. Phys. 124, 628–657. (Trans. NACA TM 1431.) 





HESKESTAD, G. 1965 A generalized Taylor hypothesis with application for high Reynolds number turbulent shear flows. J. Appl. Mech., Trans. ASME E 32, 735–739. 





HOWELLS, I. D. 1960 An approximate equation for the spectrum of a conserved scalar quantity in a turbulent fluid. J. Fluid Mech. 9, 104–106. 





INOUE, E. 1950 On the turbulent diffusion in the atmosphere 1. J. Met. Soc. Japan, 28, 441–455. 





INOUE, E. 1951 On the turbulent diffusion in the atmosphere 2. J. Met. Soc. Japan, 29, 246–252. 





KAMPÉ DE FERIET, J. 1939 Les fonctions aleatoires stationnaries et la théorie statistique de la turbulence homogene. Ann. Soc. Sci. Bruxelle, 59, 145–194. 





KAMPÉ DE FERIET, J. 1953 Fonctions aléatoires et théorie statistique de la turbulence. Théorie des Fonctions Aléatoires (A. Blanc-Lapierre and R. Fortet), ch. 14. Paris: Masson. 





KÁRMÁN, T. VON & HOWARTH, L. 1938 On the statistical theory of isotropic turbulence. Proc. Roy. Soc. A 164, 192–215. 





KELLOGG, R. M. 1965 Evolution of a spectrally local disturbance in a grid-generated turbulent flow. Ph.D. dissertation, Johns Hopkins University. 





Kolmogorov, A. 1941 The local structure of turbulence in incompressible viscous fluid for very large Reynolds numbers. C. R. Akad. Sci. SSSR 30, 301–305. 





Kovasznay, L. S. G. 1948 Spectrum of locally isotropic turbulence. J. Aero. Sci. 15, 745–753. 





KRAICHNAN, R. H. 1959 The structure of isotropic turbulence at very high Reynolds numbers. J. Fluid Mech. 5, 497–543. 





KRAICHNAN, R. H. 1964a Decay of isotropic turbulence in the direct interaction approximation. Phys. Fluids, 7, 1030–1048. 





KRAICHNAN, R. H. 1964b Kolmogorov's hypothesis and Eulerian turbulence theory. Phys. Fluids, 7, 1723–1734. 





KRAICHNAN, R. H. 1966 Isotropic turbulence and inertial-range structure. Phys. Fluids, 9, 1728–1752. 





KRAICHNAN, R. H. 1967 Invariance principles and approximation in turbulence dynamics. Dynamics of Fluids and Plasmas, 239–255. Academic. 





LIEPMANN, H. W. 1951 Aspects of the turbulence problem. ZAMP 3, 321–426. 





LIN, C. C. 1953 On Taylor's hypothesis and the acceleration terms in the Navier-Stokes equations. Quart. Appl. Math. 10, 295-306. 





LOITSIANSKII, L. G. 1939 Some basic laws of isotropic turbulent flow. Cent. Aero. Hydrodyn. Inst. Moscow, Rept. 440. (Trans. NACA TM 1079.) 





LUMLEY, J. L. & PANOFSKY, H. A. 1964 The Structure of Atmospheric Turbulence. Interscience. 





LUMLEY, J. L. 1965 Interpretation of time spectra measured in high-intensity shear flows. Phys. Fluids, 8, 1056–1062. 





LUMLEY, J. L. 1970 Stochastic Tools in Turbulence. Academic. 





MACPHAIL, D. C. 1940 An experimental verification on the isotropy of turbulence produced by a grid. J. Aero. Sci. 8, 73–75. 





MEECHAM, W. C. 1958 Relatian between time symmetry and reflection symmetry of turbulent fluids. Phys. Fluids, 1, 408–410. 





NAYAR, B. M., SIDDON, T. E. & CHU, W. T. 1969 Properties of the turbulence in the transition region of a round jet. Toronto, Inst. Aerosp. Studies, Tech. Note 131. 





O'BRIEN, E. E. & FRANCIS, G. C. 1962 A consequence of the zero fourth cumulant approximation. J. Fluid Mech. 13, 369–382. 





OBUKHOV, A. M. 1941 On the energy distribution in the spectrum of a turbulent flow. Izvest. Akad. Nauk, Ser. Geogr. i. Geofiz. 453–463. (C. R. Acad. Sci. SSSR 32 (1), 19–21, précis.) 





OGURA, Y. 1963 A consequence of the zero-fourth cumulant approximation in the decay of isotropic turbulence. J. Fluid Mech. 16, 33–40. 





ONSAGER, L. 1945 The distribution of energy in turbulence. (Abstract only.) Phys. Rev. 68, 286. 





ONSAGER, L. 1949 Statistical hydrodynamics. Nuovo Cimento (9) (suppl.), 279–287. 





RICE, S. O. 1944 Mathematical analysis of random noise. Bell. Syst. Tech. J. 23, 1–51. (Also 1954 Selected Papers on Noise and Stochastic Processes, ed. N. Wax. Dover.) 





RICE, S. O. 1945 Mathematical analysis of random noise. Bell. Syst. Tech. J. 24, 52-162. 





SAFFMAN, P. 1967 Note on decay of homogeneous turbulence. Phys. Fluids, 10, 1349. 





SIMMONS, L. F. G. & SALTER, C. 1934 Experimental investigation and analysis of the velocity variations in turbulent flow. Proc. Roy. Soc. A 145, 212–234. 





SIMMONS, L. F. G. & SALTER, C. 1938 An experimental determination of the spectrum of turbulence. Proc. Roy. Soc. A 165, 73–89. 





STEWART, R. W. & TOWNSEND, A. A. 1951 Similarity and self-preservation in isotropic turbulence. Phil. Trans. A 243, 359–386. 





TAYLOR, G. I. 1921 Diffusion by continuous movements. Proc. London Math. Soc. (2) 20, 196–212. 





TAYLOR, G. I. 1935 Statistical theory of turbulence. Proc. Roy. Soc. A 151, 421–478. 





TAYLOR, G. I. 1938 The spectrum of turbulence. Proc. Roy. Soc. A 164, 476–490. 





TOWNSEND, A. A. 1947 The measurement of double and triple correlation derivatives in isotropic turbulence. Proc. Camb. Phil. Soc. 43, 560–570. 





TOWNSEND, A. A. 1954 The diffusion behind a line source in homogeneous turbulence. Proc. Roy. Soc. A 224, 487–512. 





UBEROI, M. S. & CORRSIN, S. 1953 Diffusion of heat from a line source in isotropic turbulence. NACA Rept. 1142. 





WEIZSÄCKER, C. F. VON 1948 Das spectrum der turbulenz bei grossen Reynoldsschen zahlen. Z. Phys. 124, 614–627. 





WIENER, N. 1930 Generalized harmonic analysis. Acta Math. 55, 117–258. 





WYLD, H. W. 1961 Formulation of the theory of turbulence in an incompressible fluid. Ann. Phys. 14, 143–165. 

