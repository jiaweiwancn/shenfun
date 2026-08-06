# Wind field simulation

Jakob Mann* 

Danish Maritime Institute, DK-2800 Lyngby, Denmark
Risø National Laboratory, DK-4000 Roskilde, Denmark. 

An efficient algorithm to simulate turbulent, atmospheric or wind tunnel generated wind fields is devised. The method is based on a model of the spectral tensor for atmospheric surface-layer turbulence at high wind speeds and can simulate two- or three-dimensional fields of one, two or three components of the wind velocity fluctuations. The spectral tensor is compared with and adjusted to several spectral models commonly used in wind engineering. Compared to the Sandia method (see Veers, P. S., Three-dimensional wind simulation. Technical Report SAND88–0152, Sandia National Laboratories, 1988) the algorithm is more efficient, simpler to implement, and in some respects more physical. The simulation method is currently used for load calculations on wind turbines and bridges. © 1998 Elsevier Science Ltd. All rights reserved 

## NOMENCLATURE

A Charnock's constant, see eqn (19) $A_{ij}$ The ‘square root’ of $\Phi_{ij}$ , see eqn (46)
B ‘Grid box’ of the simulated wind field, see Fig. 10 $C_{ij}$ Coefficient matrix in the stochastic wind field simulation in eqn (39) $C_{DN}$ Neutral drag coefficient, see eqn (21) or Fig. 2
coh Spectral coherence or squared coherence defined by eqn (7)
E Turbulence energy spectrum, see eqn (9)
f Frequency (Hz), or the Coriolis parameter (rad s $^{-1}$ ), see eqn (18) $\tilde{f}$ Normalized frequency used in the NPD spectrum (eqn (31))
F Spectrum as a function of wave number. The spectrum is two-sided, i.e. $\int_{-\infty}^{\infty} F_i(k_1) dk_1$ equals the variance
k Wave vector $k_i$ Wave number in the $x_i$ direction. $k_1 = 2\pi f/U$ L A length scale of the spectral velocity tensor $L_i$ Length of the simulated wind field in the $i$ direction, see Fig. 10
n Non-dimensional frequency $fz/U$ or exponent used in the NPD spectrum, see eqn (31) $n_i$ Vector of independent Gaussian random variables
N The total number of points in the simulated field 

*To whom correspondence should be addressed. 

$N_{i}$ The number of points in the simulated field in the i direction, see Fig. 10 $R_{ij}(r)$ Covariance between $u_{i}$ and $u_{j}$ at a separation r, see eqn (1)
S Same as F, but as a function of frequency f
sinc(x) The function sin (x)/x
U Mean wind speed $U_{10}$ Mean wind speed at z = 10 m
u Vector of velocity fluctuations $\tilde{u}$ Velocity vector (mean plus fluctuations) $u_{i}$ The ith component of the turbulent velocity fluctuations $u_{*}$ Friction velocity, see eqn (17)
V(B) Volume of the ‘grid box’ B
x Vector of spatial coordinates = $(x_{1}, x_{2}, x_{3}) = (x, y, z)$ x Coordinate in the mean flow direction
y Horizontal coordinate perpendicular to the mean flow direction
z Vertical coordinate
Z Stochastic vector field with uncorrelated increments. Connected to the spectral tensor by eqn (4); see also eqn (3) $z_{0}$ Roughness length, see eqn (17) 

Greek
α The three-dimensional Kolmogorov constant ≈ 1.7
Γ Parameter of the sheared spectral tensor
δ Dirac's delta function 

$\delta_{ij}$ Kronecker's delta function. Is 1 if $i = j$ and 0 otherwise $\Delta L_{i}$ Separation between the points of the simulated field in the $i$ direction, see Fig. 10 $\epsilon$ Dissipation of turbulent kinetic energy $\kappa$ von Kármán constant, see eqn (17) $\sigma_x^2$ Variance of the quantity $x$ $\Phi$ Spectral velocity tensor, see eqn (2) $\chi_{ij}$ Cross-spectrum between $u_i$ and $u_j$ , see eqn (5) 

## 1 INTRODUCTION

If one wants to calculate buffeting forces on a bridge deck it is necessary to simulate the vertical $(w)$ and possibly also the longitudinal wind velocity fluctuations $(u)$ in the horizontal plane swept by the bridge deck. If the mean wind direction is not normal to the bridge deck one may want to simulate all three wind velocity fluctuation components, i.e. w, u and the lateral component v. If, in addition, modelling of the forces on the entire superstructure of bridge is required, one might need to simulate a three-dimensional field of either one, two or three components of the wind. For dynamical load calculations on a wind turbine, probably all three components of the three-dimensional wind field are needed. For other structures, other combinations of spatial dimensions and components may be needed. 

With this in mind, we need to devise a general algorithm to simulate two- or three-dimensional fields of one, two or three components of the wind velocity fluctuations. 

The most ‘correct’ method to simulate a turbulent field would probably be to solve the Navier–Stokes equations directly (by direct numerical simulation, DNS) of an atmospheric flow bounded from below by an aerodynamically rough surface. However, the computational costs of this would be enormous. A cheaper way to do it would be to use large eddy simulation (LES), which is an approximate solution to the Navier–Stokes equations where the motions of the smallest scales are not solved directly but modelled. Still, this requires supercomputers and is usually not justified for practical engineering use. Therefore, in wind engineering, empirical information is generally used. 

Most methods that have been developed to simulate the turbulent wind field are based on empirical forms of the one-point (cross-)spectra and two-point cross-spectra or coherences and phase-spectra. Here a method is described which builds on the model of the spectral tensor for atmospheric surface layer turbulence at high wind speeds developed by Mann. $^{1}$ Although the tensor does not in principle contain more information than the cross-spectra, it leads to a more natural and more direct representation of the three-dimensional turbulent flow. As described in this reference, $^{1}$ the basis for the model is an application of rapid distortion theory implying a linearization of the Navier-Stokes equation, combined with a definition and modelling of eddy lifetimes. The physical considerations are quite crude, but the tensor contains essential aspects of the second-order structure of atmospheric turbulence. The tensor model has been checked and calibrated with data from different atmospheric experiments which have been carried out with the purpose of estimating wind loads on a large suspension bridge and on horizontal-axis wind turbines. It has also been tested successfully in two wind tunnels at the Danish Maritime Institute (DMI). Here we shall fit the tensor model to various widely used atmospheric model spectra. $^{2-4}$ 

The wind field can be represented as a generalized Fourier-Stieltjes integral of its spectral components. The necessary factorization (i.e. 'square root') of the spectral tensor can be accomplished in closed form. A numerical simulation algorithm is obtained by recasting the Fourier representation of the wind field in discrete frequency/ wave-number space, i.e. as a trigonometric series with random coefficients, where the statistics of the coefficients are determined by the spectral tensor. 

The method is considerably faster and simpler than methods based on cross-spectra. Shinozuka and Jan $^{5}$ suggested a quite similar method in general terms, but lack of a realistic spectral tensor of the turbulence in the atmospheric surface layer has prevented its use in wind engineering. The discretization imposes two requirements: if either the width or the height of the domain of the simulated field is not much larger than the length scale of the turbulence, care must be taken to adequately represent the energy of the largest scales. The other requirement is that, to avoid effects of the imposed periodicity, the space domain must have a large enough margin around the structure of interest. 

In Section 2 basic statistical concepts such as the covariance tensor, its Fourier transform, the spectral tensor and different one- and two-point spectra are discussed. Then, in Section 3, a simple isotropic spectral tensor is presented as an introduction to the discussion of the more realistic tensor in Section 4. In Section 5 the spectral tensor mode is compared with and fitted to well known forms of spectra from the literature. Section 6 and the Appendix exposure in detail how to simulate a turbulent velocity field from a spectral tensor. Finally, comparison with other simulation algorithms is discussed briefly in Section 7. 

## 2 DEFINITIONS AND PRELIMINARIES

The atmospheric turbulent velocity field is $\tilde{\boldsymbol{u}}(\boldsymbol{x})$ , where $\boldsymbol{x} = (x_1, x_2, x_3) = (x, y, z)$ is a right-handed coordinate system with the $x$ -axis in the direction of the mean wind field and as the vertical axis. The fluctuations around the mean wind $\boldsymbol{u}(\boldsymbol{x}) = (u_1, u_2, u_3) = (u, v, w) = \tilde{\boldsymbol{u}}(\boldsymbol{x}) - (U(z), 0, 0)$ , are assumed to be homogeneous in space, which is often the case in the horizontal directions but is only a crude approximation in the vertical. Since we are interested in shear generated turbulence, the mean wind field is allowed to vary as a function of $z$ . Because of homogeneity, the covariance tensor 

$$
R _ {i j} (\boldsymbol {r}) = \left\langle u _ {i} (\boldsymbol {x}) u _ {j} (\boldsymbol {x} + \boldsymbol {r}) \right\rangle\tag{1}
$$

is only a function of the separation vector $r$ ( $\langle \rangle$ denotes ensemble averaging). 

We shall use Taylor's frozen turbulence hypothesis $^{6}$ to interpret time series as 'space series' and to serve as a 'dispersion relation' between frequency and wave number. Since the mean wind speed is not constant in space, the wind speed $U$ in the Taylor relation $\tilde{\boldsymbol{u}}(x,y,z,t)=\tilde{\boldsymbol{u}}(x-Ut,y,z,0)$ must be chosen as a vertical average of $U(z)$ (after this discussion we suppress the time argument in $\boldsymbol{u}$ ). 

We aim only to simulate turbulence which has the same second-order statistics, such as variances, cross-spectra etc., as in the real atmosphere. The velocity field is otherwise assumed to be Gaussian. All second-order statistics can be derived from the covariance tensor or its Fourier transform, the spectral tensor: 

$$
\Phi_ {i j} (\boldsymbol {k}) = \frac {1}{(2 \pi) ^ {3}} \int R _ {i j} (\boldsymbol {r}) \exp (- \mathrm{i} \boldsymbol {k} \cdot \boldsymbol {r}) \mathrm{d} \boldsymbol {r}\tag{2}
$$

where $\int dr \equiv \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} dr_{1} dr_{2} dr_{3}$ . The spectral tensor is the basis of the Fourier simulation and we shall only briefly describe the non-isotropic tensor model in Section 4, because it is described in detail by Mann. $^{1,7}$ 

The stochastic velocity field can be represented in terms of a generalized stochastic Fourier–Stieltjes integral: 

$$
\boldsymbol {u} (\boldsymbol {x}) = \int \mathrm{e} ^ {\mathrm{i} \boldsymbol {k} \cdot \boldsymbol {x}} \mathrm{d} Z (\boldsymbol {k})\tag{3}
$$

where the integration is over all wave number space. The orthogonal process Z is connected to the spectral tensor by 

$$
\left\langle \mathrm{d} Z _ {i} ^ {*} (\boldsymbol {k}) \mathrm{d} Z _ {j} (\boldsymbol {k}) \right\rangle = \Phi_ {i j} (\boldsymbol {k}) \mathrm{d} k _ {1} \mathrm{d} k _ {2} \mathrm{d} k _ {3}\tag{4}
$$

which is valid for infinitely small $dk_{i}$ and where * denotes complex conjugation. 

It is very difficult to measure the spectral tensor directly. Instead cross-spectra, defined as 

$$
\chi_ {i j} (k _ {1}, \Delta y, \Delta z) = \frac {1}{2 \pi} \int_ {- \infty} ^ {\infty} R _ {i j} (x, \Delta y, \Delta z) e ^ {- i k _ {1} x} d x\tag{5}
$$

are often measured and are used in practical applications, such as estimation of loads on structures. The connection between the components of the spectral tensor and the cross-spectra is 

$$
\chi_ {i j} \left(k _ {1}, \Delta y, \Delta z\right) = \int_ {- \infty} ^ {\infty} \int_ {- \infty} ^ {\infty} \Phi_ {i j} (\boldsymbol {k}) e ^ {i \left(k _ {2} \Delta y + k _ {3} \Delta z\right)} d k _ {2} d k _ {3}\tag{6}
$$

$F_{i}(k_{1}) = \chi_{ii}(k_{1}, 0, 0)$ (except that from here and in eqn (7) summation over repeated indices is generally used) is the one-point spectrum. 

To distinguish between spectra as functions of wave number $k_{1}( = 2\pi f/U)$ and frequency f we use F for the former and S for the latter, i.e. $S_{i}(f)\mathrm{d}f = F_{i}(k)\mathrm{d}k$ . 

The coherence is defined as 

$$
\operatorname{coh} _ {i j} \left(k _ {1}, \Delta y, \Delta x\right) = \frac {\left| \chi_ {i j} \left(k _ {1} , \Delta y , \Delta z\right) \right| ^ {2}}{F _ {i} \left(k _ {1}\right) F _ {j} \left(k _ {1}\right)}\tag{7}
$$

## 3 THE ISOTROPIC TENSOR MODEL

The spectral tensor of incompressible isotropic turbulence is (see Batchelor $^{8}$ ): 

$$
\Phi_ {i j} (\pmb {k}) = \frac {E (k)}{4 \pi k ^ {4}} \bigl (\delta_ {i j} k ^ {2} - k _ {i} k _ {j} \bigr)\tag{8}
$$

where the energy spectrum, $E(k)$ , is often chosen to be 

$$
E (k) = \alpha \epsilon^ {2 / 3} L ^ {5 / 3} \frac {L ^ {4} k ^ {4}}{(1 + L ^ {2} k ^ {2}) ^ {1 7 / 6}}\tag{9}
$$

as suggested by von Kármán $^{9}$ (L is a length scale, $\alpha$ the Kolmogorov constant and $\epsilon$ the rate of viscous dissipation of specific turbulent kinetic energy). The variance of the wind velocity fluctuations, whose magnitude of the wave vector is in the range $(k, k + dk)$ , is $2E(k)dk$ . 

Using eqn (6) with y = 0 and z = 0 we get the one-point u-spectrum 

$$
F _ {1} (k _ {1}) = \frac {9}{5 5} \alpha \epsilon^ {2 / 3} L ^ {5 / 3} \frac {1}{(1 + L ^ {2} k _ {1} ^ {2}) ^ {5 / 6}}\tag{10}
$$

the v- and w-spectra 

$$
F _ {i} (k _ {1}) = \frac {3}{1 1 0} \alpha \epsilon^ {2 / 3} L ^ {5 / 3} \frac {3 + 8 L ^ {2} k _ {1} ^ {2}}{(1 + L ^ {2} k _ {1} ^ {2}) ^ {1 1 / 6}}\tag{11}
$$

(for i = 2, 3), and all the one-point cross-spectra are zero. The advantage of the isotropic turbulence model is that it describes the spectra and cross-spectra well for high frequencies or separations that are small compared to the length scale of the turbulence. The disadvantages are that the variances of the velocity components are equal, which is not supported by data from the atmospheric surface layer. In fact, $\sigma_{w}^{2}/\sigma_{u}^{2} \approx 0.25$ and $\sigma_{v}^{2}/\sigma_{u}^{2} \approx 0.5 - 0.7$ depending on the averaging time. $^{6}$ Furthermore, isotropy implies that the cross-spectrum, $\chi_{13}$ , must be zero, which is certainly not the case in shear-generated turbulence. 

## 4 THE 'SHEARED' SPECTRAL TENSOR

Only an outline of the derivation of the sheared spectral tensor will be given; details may be found in Mann. $^{1,7}$ 

To model the spectral velocity tensor in a shear flow we linearize the Navier–Stokes equation to estimate the effect of the shear on the turbulence. If we assume the shear to be linear such that $dU/dz$ is constant, we obtain a simple linear differential equation for the time evolution of the spectral tensor or the ‘stretching’ of individual eddies. Also, the wave vector will change as a function of time. Qualitatively, this describes the change in orientation and shape of the eddies due to the mean shear. Given $k(t=0)=(k_{1},k_{2},k_{30})$ as the initial wave vector, the development in time is 

$$
\boldsymbol {k} (t) = \left(k _ {1}, k _ {2}, k _ {3 0} - k _ {1} t \frac {\mathrm{d} U}{\mathrm{d} z}\right)\tag{12}
$$

The boundary layer turbulence is statistically stationary, but the linearized equations describe an evolution in time. 

Assuming the second-order statistics of the initial condition $dZ^{iso}$ to be described by the isotropic von Kármán tensor (eqn (8)) with energy spectrum (eqn (9)), the turbulent field described by $\mathrm{dZ}(k(t), t)$ will become more and more ‘anisotropic’ with time. The linearization is unrealistic, however, in the sense that at some point the stretched ‘eddies’ will break up. To close the problem an equilibrium is postulated whereby eddies of size $\propto |k|^{-1}$ are stretched by the shear over a time proportional to their lifetime $\tau$ . At least for relatively high frequencies and wave numbers (the inertial subrange), $\tau$ is proportional to $k^{-2/3}$ , and we introduce a parameter $\Gamma$ such that the dimensionless lifetime, $\beta$ , can be written as $\beta \equiv dU/dz\tau = \Gamma dU/dz(kL)^{-\frac{2}{3}}$ . A more general model of the dimensionless eddy lifetime $\beta$ outside the inertial subrange is established in Mann. $^{1}$ The physical modelling is far from being rigorous but leads to a qualified guess of the spectral tensor. The usefulness of the tensor depends on how well atmospheric or wind tunnel turbulence is modelled, which has been investigated by Mann et al. $^{1,7,10}$ and in Section 5. 

For the present purpose it is most convenient to present the results in terms of the stochastic process $\mathbf{d}\mathbf{Z}(\mathbf{k})$ as defined in eqns (3) and (4). We define $k_{0}$ as $(k_{1}, k_{2}, k_{30})$ with $k_{30} = k_{3} + \beta k_{1}$ by solving eqn (12). If the ‘initial condition’ $\mathbf{d}\mathbf{Z}^{\mathrm{iso}}(\mathbf{k}_{0})$ has the statistics of the isotropic von Kármán tensor (eqn (8)), then the sheared tensor may be found from eqn (4) and the following equations: 

$$
\mathrm{d} \boldsymbol {Z} (\boldsymbol {k}) = \left[ \begin{array}{c c c} 1 & 0 & \zeta_ {1} \\ 0 & 1 & \zeta_ {2} \\ 0 & 0 & k _ {0} ^ {2} / k ^ {2} \end{array} \right] \mathrm{d} \boldsymbol {Z} ^ {\text {iso}} (\boldsymbol {k} _ {0})\tag{13}
$$

where 

$$
\zeta_ {1} = C _ {1} - k _ {2} C _ {2} / k _ {1}, \zeta_ {2} = k _ {2} C _ {1} / k _ {1} + C _ {2}\tag{14}
$$

with 

$$
C _ {1} = \frac {\beta k _ {1} ^ {2} (k _ {0} ^ {2} - 2 k _ {3 0} ^ {2} + \beta k _ {1} k _ {3 0})}{k ^ {2} (k _ {1} ^ {2} + k _ {2} ^ {2})}\tag{15}
$$

and 

$$
C _ {2} = \frac {k _ {2} k _ {0} ^ {2}}{\left(k _ {1} ^ {2} + k _ {2} ^ {2}\right) ^ {\frac {3}{2}}} \arctan \left[ \frac {\beta k _ {1} \left(k _ {1} ^ {2} + k _ {2} ^ {2}\right) ^ {\frac {1}{2}}}{k _ {0} ^ {2} - k _ {3 0} k _ {1} \beta} \right]\tag{16}
$$

which are identical to eqns (3.14)-(3.17) of Mann. $^{1}$ 

In contrast to the isotropic tensor model we have an extra parameter $\Gamma$ which determines the anisotropy of the tensor. Integrating the spectral tensor over the entire wave vector space we obtain the (co-)variances as a function of $\Gamma$ (see Fig. 1). It is seen that, when anisotropy is introduced in this way, $\sigma_{u}^{2} > \sigma_{v}^{2} > \sigma_{w}^{2}$ and $\langle uw\rangle < 0$ , which is confirmed by observations. The larger $\Gamma$ , the larger the difference between the variances. 

Four experimental tests of the model have been carried out. Two are atmospheric, one over water $^{1,10}$ and one over flat terrain $^{11}$ , giving the parameters $L/z = 0.87$ , $\Gamma = 3.2$ and $L/z = 0.91$ , $\Gamma = 2.6$ , respectively. The third test is based on data from the Martin Jensen boundary layer wind tunnel $^{12}$ at the Danish Maritime Institute (DMI), giving $L/z = 0.60$ , $\Gamma = 2.2$ , implying that the turbulence is closer to being isotropic compared to atmospheric turbulence. $^{7}$ The fourth test took place in DMI's wind tunnel used for bridge section model tests. In the setup used for these tests there is almost no shear and $\Gamma = 0.76$ (and $L = 0.39 \, \text{m}$ ) and, consequently, the turbulence is very close to being isotropic; see Fig. 1. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/7aa31f6d1f9977fc6d4445dbfd1624f728b5b62abf951b3ed05566c0424d474b.jpg)



Fig. 1. (Co-)variances divided by the isotropic variance $(\Gamma = 0)$ for the spectral tensor model as functions of the parameter $\Gamma$ (from Mann $^{1}$ ).


To simulate atmospheric turbulence we shall not rely solely on the two atmospheric experiments mentioned above, and in the next section we shall compare the spectra tensor model to commonly used spectra and coherences. 

Mann $^{1}$ also tried to model the vertical inhomogeneity of the turbulence caused by the presence of the ground, but this model is considerably more complex than the one used here. 

## 5 ATMOSPHERIC TURBULENCE CLOSE TO THE SURFACE

Here we compare the tensor model of Section 4 to spectra and coherences from the literature. We shall not give an exhaustive review of spectral models but select a few modern models which the author believes are used in wind engineering. The purpose is to estimate the parameter $\Gamma$ , $L$ and $\alpha \epsilon^{2/3}$ for a given mean wind speed $U$ and height above the surface $z$ and, in the case of a land surface, also for a given roughness length $z_0$ . 

The logarithmic mean wind profile defines the roughness length: 

$$
U (z) = \frac {u _ {*}}{\kappa} \mathrm{ln} (z / z _ {0})\tag{17}
$$

where $u_{*} \equiv (-\langle uw\rangle)_{z \to 0}^{1/2}$ is the friction velocity and $\kappa = 0.40$ the von Kármán constant. $^{6,13}$ 

ESDU $^{14}$ gives a slightly more accurate wind profile: 

$$
U (z) = \frac {u _ {*}}{\kappa} \left(\ln \left(z / z _ {0}\right) + 3 4. 5 f z / u _ {*}\right)\tag{18}
$$

with the Coriolis parameter $f \equiv 2\Omega \sin \phi$ , where $\Omega$ is th angular velocity (rad s $^{-1}$ ) of the Earth and $\phi$ the geographical latitude. The profile (eqn (18)) is valid up to z = 300 m; below 30 m eqn (17) is a good approximation to eqn (18). Throughout this paper we use $f = 10^{-4}$ s $^{-1}$ . 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/5ad0701e4a9434d17b71d4bd11d534f6f8512603503b2b21c967c0f900d098a3.jpg)



Fig. 2. The neutral drag coefficient $C_{DN}$ as a function of mean wind speed at z = 10 m. The broad line is from Charnock's relation, eqns (19) and (17). The thin lines are empirical relations from Geernaert $^{17}$ and the dotted line is from NPD; $^{18}$ see eqn (28).


Charnock $^{15}$ argued that over the sea the roughness length is related to $g = 9 \cdot 8 \, m \, s^{-2}$ , the acceleration due to gravity, and the friction velocity by 

$$
z _ {0} = A \frac {u _ {*} ^ {2}}{g}\tag{19}
$$

where A, the Charnock constant, must be determined experimentally. On the basis of an extensive literature study of ocean data, Garratt $^{16}$ found that the best fit of eqn (19) is $A = 0.0144$ . A slightly newer value is given by ESDU: $^{14}$ 

$$
A = 0. 0 1 6 7\tag{20}
$$

which will be used in this paper. From eqn (17) it can be seen that the neutral drag coefficient 

$$
C _ {\mathrm{DN}} = \left(\frac {u _ {*}}{U (1 0 \mathrm{m})}\right) ^ {2}\tag{21}
$$

is independent of wind speed over land (where $z_{0}$ is almost always independent of wind speed). Over the ocean, however, $C_{DN}$ increases monotonically with U, as can be seen by solving eqns (19) and (17). This is shown in Fig. 2 as a broad line, together with several recent empirical relations. The figure gives a good impression of the uncertainty in estimates of drag coefficients. Among the various reasons for this variability are atmospheric stability, surface currents, ‘wave age’, length of the fetch over water, and water depth. $^{[17,16,19]}$ The spectral density of velocity fluctuations is, in general, proportional to the drag coefficient, so the uncertainty of the former is probably of the same order as that of the latter. 

## 5.1 Code and textbook spectra

## 5.1.1 Surface layer scaling

This is used in many spectral models, implying that length scales are proportional to z and that variances are proportional to $u_{*}^{2}$ . Therefore, it is convenient to normalize the spectra with $u_{*}^{2}$ and present them as functions of either $n \equiv fz / U$ or $k_{1}z$ . All spectra in this paper are 'two-sided', implying that $\int_{\infty}^{-\infty} S(f)\mathrm{d}f$ is equal to the variance. $^{1}$ 

The spectra of Kaimal et al. $^{3,20}$ are 

$$
\frac {f S _ {u} (f)}{u _ {*} ^ {2}} = \frac {k _ {1} F _ {u} (k _ {1})}{u _ {*} ^ {2}} = \frac {5 2 \cdot 5 n}{(1 + 3 3 n) ^ {5 / 3}}\tag{22}
$$

$$
\frac {f S _ {v} (f)}{u _ {*} ^ {2}} = \frac {8 \cdot 5 n}{(1 + 9 \cdot 5 n) ^ {5 / 3}}\tag{23}
$$

and 

$$
\frac {f S _ {w} (f)}{u _ {*} ^ {2}} = \frac {1 \cdot 0 5 n}{1 + 5 \cdot 3 n ^ {5 / 3}}\tag{24}
$$

Kaimal's spectra are based on measurements over flat homogeneous terrain in Kansas. One of the main findings of Kaimal $^{3}$ is the jump in spectral energy density at low frequencies as the stability of the atmosphere changes from stable (cooling from below) to unstable (warming from below). The spectra of Kaimal presented here are ‘neutral approached from the stable side’. Kaimal shows that the neutral spectra approached from the unstable side have significantly more energy at low frequencies. This is the most pronounced for the $v$ -spectrum. 

The spectra of Simiu and Scanlan $^{4}$ have the same functional shapes as Kaimal's but the numerical constants are different: 

$$
\frac {f S _ {u} (f)}{u _ {*} ^ {2}} = \frac {1 0 0 n}{(1 + 5 0 n) ^ {5 / 3}}\tag{25}
$$

$$
\frac {f S _ {v} (f)}{u _ {*} ^ {2}} = \frac {7 \cdot 5 n}{(1 + 9 \cdot 5 n) ^ {5 / 3}}\tag{26}
$$

and 

$$
\frac {f S _ {w} (f)}{u _ {*} ^ {2}} = \frac {1 \cdot 6 8 n}{1 + 1 0 n ^ {5 / 3}}\tag{27}
$$

## 5.1.2 Deviations from surface layer scaling

Such deviations are found in the model spectra from ESDU. $^{2}$ Also, the spectra of the Norwegian Petroleum Directorate (NPD $^{18}$ ) and Højstrup et al. $^{21}$ do not obey surface layer scaling, but these are only limited to u-spectra. 

The Engineering Science Data Unit (ESDU) wind profile, spectra and coherences $^{2,14,22}$ are derived from many sources from all over the world spanning several decades. ESDU proposes that the turbulence intensities and length scales in the surface layer are dependent on mean wind speed. The argument is that the boundary layer depth increases with increasing wind speed, implying larger scales of the turbulence. The other models, relying on surface layer scaling, do not contain any information on the boundary layer depth and they contain no explicit reference to the mean wind speed. The equations of ESDU are, compared to all other spectral models discussed here, by far the most complicated. Therefore we shall not cite them explicitly. The most important input parameters are, as for the other spectral models, surface roughness $z_{0}$ , height above the surface z, and the mean wind speed at some height. Less important inputs are the displacement height, which we shall ignore, and the Coriolis parameter which, as mentioned previously, is taken to be $f = 10^{-4} s^{-1}$ . The models we use are valid for the neutral atmosphere over homogeneous terrain. Note that ESDU also gives guidelines for changes in spectra for some types of inhomogeneous terrain. 

The u-spectrum of NPD $^{18}$ applies to winds over oceans and assumes the drag coefficient to be 

$$
C _ {\mathrm{DN}} = 0. 5 2 5 \times 1 0 ^ {- 3} (1 + 0. 1 5 U _ {1 0})\tag{28}
$$

(see Fig. 2). Integrating $dU/dz = u_{*}/(\kappa z) = \sqrt{C_{\mathrm{DN}}} U_{10}/(\kappa z)$ (eqn (28)) implies that 

$$
U (z) = U _ {1 0} \left(1 + C \ln \frac {z}{1 0 m}\right)\tag{29}
$$

with 

$$
C = 0 \cdot 0 5 7 3 (1 + 0 \cdot 1 5 U _ {1 0}) ^ {1 / 2}\tag{30}
$$

where $U_{10}$ has to be measured in metres per second. When discussing the NPD spectrum we also assume the unit of z to be metre, f is Hz and $S_{u}$ is $m^{2}s^{-2}Hz^{-1}$ . The spectral density of the longitudinal wind component is 

$$
S _ {u} (f) \frac {1 6 0 \left(\frac {U _ {1 0}}{1 0}\right) ^ {2} \left(\frac {z}{1 0}\right) ^ {0 . 4 5}}{\left(1 + \tilde {f} ^ {n}\right) ^ {\frac {5}{3 n}}}\tag{31}
$$

with 

$$
\tilde {f} = 1 7 2 f \left(\frac {z}{1 0}\right) ^ {2 / 3} \left(\frac {U _ {1 0}}{1 0}\right) ^ {- 4 / 3}\tag{32}
$$

and $n = 0.468$ . This spectrum implies that the variance 

$$
\sigma_ {u} ^ {2} = 0 \cdot 0 0 3 0 9 \frac {U _ {1 0} ^ {2 \cdot 7 5}}{z ^ {0 \cdot 2 1 7}}\tag{33}
$$

will decrease with height and is not constant as implied by surface layer scaling. Furthermore, the integral length scale 

$$
\text { length   scale } \propto z ^ {2 / 3} U _ {1 0} ^ {1 / 4}\tag{34}
$$

will not be proportional to height but will grow somewhat slower and will also increase a little with wind speed. This is not consistent with surface layer scaling where, under neutral conditions, it is constant with wind speed. 

Højstrup et al. $^{21}$ suggested that spectra at low frequencies do not obey surface layer scaling because the low frequency part scales with the height of the boundary layer, not z. To verify their model they used data selected for neutrality and high wind speeds ( $11 < U < 23 \, m s^{-1}$ ) from both over sea and land sites in Denmark. The u-model is $^{2}$ 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/d6f879808de9d675dfd81d3203d4ae7e2a45ee49f80c9f3485cb38dae6df2834.jpg)



Fig. 3. Comparison of spectral models. For the comparison $z = 40 \, \text{m}$ and $U = 40 \, \text{m} \, \text{s}^{-1}$ (over the sea) are chosen. For $u$ , ESDU, eqns (22), (25), (35) and (31) are used; for $v$ and $w$ , ESDU, eqns (23) and (26), and ESDU, $^2$ eqns (24) and (27), respectively Eqn (18) together with eqn (19) gives $u_* = 1 \cdot 78 \, \text{m} \, \text{s}^{-1}$ and $z_0 = 0 \cdot 0054 \, \text{m}$ .


$$
\frac {f S _ {u} (f)}{u _ {*} ^ {2}} = \left(\frac {2 \cdot 5 n _ {t}}{1 + 2 \cdot 2 n _ {t} ^ {5 / 3}} + \frac {5 2 \cdot 5 n}{(1 + 3 3 n) ^ {5 / 3}}\right) \frac {1}{1 + 7 \cdot 4 (z / A) ^ {2 / 3}}\tag{35}
$$

where the 'neutral length scale' $A = 3000 \, \text{m}$ and $n_t = fA / L$ . The second term in the parentheses is the Kaimal spectrur (eqn (22)). 

All spectral models are compared in Fig. 3 for a specific choice of U and z. Generally, ESDU has larger length scale compared to those by Kaimal and by Simiu and Scanlar which are similar. NPD and Højstrup support ESDU's large u-scale. ESDU, though, has the most peaked spectra and, a high wave numbers, slightly lower spectral densities. A spectra agree fairly well at high wave numbers but have substantial scatter at low wave numbers. 

## 5.2 Comparison with the 3-D spectral model

Here we fit the spectral tensor of Section 4 to models that describe all three component spectra, namely the ones by Kaimal, Simiu and Scanlan and ESDU (as described in section 5.1). 

We obtain the parameters $\Gamma$ , $L$ and $\alpha \epsilon^{2/3}$ by making a simultaneous least-squares fit to the $u$ -, $v$ - and $w$ -mode spectra for wave numbers in the range $0.5 < k_1 L < 10^6$ . For the models obeying surface layer scaling the fits are shown in Figs 4 and 5. For the Kaimal spectra 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/01dc74fb4d04c09b57de5c3e661d2be6ab201159c7ca7f973d6c34d9930cee7b.jpg)



Fig. 4. Fit of spectra derived from eqns (4), (6) and (13), the 'sheared spectral tensor' of Section 4 (curves with dots), to the models of Kaimal (eqns (22)-(24)). The resulting parameters are given by eqn (37).


$$
\Gamma = 3 {\cdot} 9
$$

$$
L = 0. 5 9 z
$$

$$
\alpha \epsilon^ {2 / 3} = 3 \cdot 2 \frac {u _ {*} ^ {2}}{z ^ {2 / 3}}
$$

where the dependence on z is a consequence of surface layer scaling. For the Simiu and Scanlan spectra 

$$
\Gamma = 3 \cdot 8
$$

$$
L = 0 {\cdot} 7 9 z
$$

$$
\alpha \epsilon^ {2 / 3} = 2 \cdot 8 \frac {u _ {*} ^ {2}}{z ^ {2 / 3}}
$$

and for both models $u_{*}$ can be obtained from the logarithmic profile, eqn (17) (or (eqn (18)), over land or from Fig. 2 over water. 

It is more complicated to get the parameters from the 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/cbdf0b5f65b07ad53b0350eaa22baec737215dea9fece512988fdc890f062108.jpg)



Fig. 5. The ‘sheared spectral tensor’ of Section 4 (curves with dots) fitted to the models by Simiu and Scanlan (eqns (25)–(27)). The result is given by eqn (38).


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/5aace2fb499d79640e14ef8df37259ca32a6a85fbaa4ff5435b45eff0756c69f.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/77ddd7acbfc30a24f13945cb8db155845add929c3ef572c4146588741045b9fc.jpg)



Fig. 6. The parameters of the spectral tensor model derived from fits to the ESDU model spectra for turbulence over the sea. Given U and z, all three parameters can be extracted from these plots.


ESDU models because the spectra no longer depend on U, z and $z_{0}$ in a simple way. For each set $\{U, z, z_{0}\}$ , a fit to the tensor model has to be calculated. We do that on a mesh limited by $10 < U < 80 \, m s^{-1}$ , $5 < z < 300 \, m$ over the sea (where $z_{0}$ is implicitly given by the two others) and, in addition, by $0.0001 < z_{0} < 1 \, m$ over land. The result for the sea is shown in Fig. 6 and, for land with $z_{0} = 0.03 \, m$ , in Fig. 7. As an example of the use of these graphs, suppose that the parameters for $U(z = 80 \, m) = 20 \, m s^{-1}$ over the sea are wanted. From the upper plot of 


Table 1. Parameters of the spectral tensor derived from different sources for $U$ (40 m) = 40 m s $^{-1}$ at sea


<table><tr><td></td><td><eq>\Gamma</eq></td><td><eq>L</eq>(m)</td><td><eq>\alpha\epsilon^{2/3}</eq>(<eq>m^{4/3}</eq><eq>s^{-2}</eq>)</td></tr><tr><td>Great Belt</td><td>3·2</td><td>35</td><td>0·79</td></tr><tr><td>Kaimal</td><td>3·9</td><td>24</td><td>0·86</td></tr><tr><td>Simiu</td><td>3·8</td><td>31</td><td>0·76</td></tr><tr><td>ESDU</td><td>4·5</td><td>66</td><td>0.62</td></tr></table>

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/fadabf5239a571e0e2cb144e93080fb9775049cdeb1c1683194c179e71361bcf.jpg)



Fig. 7. Same as Fig. 6, but for the atmosphere over land with a roughness length of $z_{0} = 0.03$ m.


Fig. 6 we get $L = 33 \, \text{m}$ and $\alpha \epsilon^{2/3} = 0 \cdot 1 \, \text{m}^{4/3} \, \text{s}^{-2}$ . The lower plot gives $\Gamma = 4 \cdot 5$ . 

Another example is shown in Table 1 where the Great Belt data from Mann $^{1}$ are extrapolated using neutral surface scaling to $U(40\ m)=40\ m\ s^{-1}$ . The spectral fit for these values of U and z is shown in Fig. 8. 

Finally, we compare literature coherences and coherences derived from the spectral tensor by eqns (6) and (7). The coherences given by Simiu and Scanlan $^{4}$ are 

$$
\sqrt {\operatorname{coh} _ {i i}} (k _ {1}) = \exp (- C n), \text { with } n \equiv k _ {1} / 2 \pi\tag{38}
$$

For i = 1, $C = 16\Delta y$ for lateral separation and $C = 10\Delta z$ for vertical. For i = 2, the values of C are two-thirds of the i = 1 case. For i = 3, only the value for the lateral separation is given: $C = 8\Delta y$ . At small separations the ESDU and tensor coherences are almost identical because both are based on the assumption of isotropy of the smallest scales; see the ‘ $\Delta y = 6 \, m$ ’ plot of Fig. 9. At larger separations the differences increase. 

## 6 FOURIER SIMULATION

Having discussed the spectral tensor in relation to literature spectra, we now describe how to simulate a velocity field $\boldsymbol{u}(\boldsymbol{x})$ . 

We approximate the integral (eqn (3)) by a discrete Fourier series: 

$$
u _ {i} (\boldsymbol {x}) = \sum_ {\boldsymbol {k}} \mathrm{e} ^ {\mathrm{i} \boldsymbol {k} \cdot \boldsymbol {x}} C _ {i j} (\boldsymbol {k}) n _ {j} (\boldsymbol {k})\tag{39}
$$

where the lth component of x is $x_{l}=n\Delta L_{l}$ with $n=1,\ldots,N_{l}$ . The symbol $\Sigma_{k}$ denotes the sum over all wave vectors k with components $k_{i}=m2\pi/L_{i}$ , with integer $m=-N_{i}/2,\ldots,N_{i}/2$ ; $n_{j}(k)$ are independent Gaussian stochastic complex variables with unit variance; and $C_{ij}(k)$ are coefficients to be determined. See Fig. 10. The great advantage of eqn (39) is that, once the coefficients are known, it can be evaluated very quickly by the fast Fourier transform (FFT). $^{23}$ 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/5345ab972d474649c92b6258dd7f6813824b19d6b6b2c82edefd921876a40b07.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/f9084c0c009ec39749dbea1a56ffcf31ae0ada4245a12d5443d4a5b5aa5f120c.jpg)



Fig. 8. Example with z = 40 m and $U = 40 \, m s^{-1}$ of the fit of the spectral tensor model (curves with dots) to the ESDU models.


Solving eqn (39), we obtain (approximately, see Appendix A). 

$$
C _ {i j} (\boldsymbol {k}) n _ {j} (\boldsymbol {k}) = \frac {1}{V (\mathrm{B})} \int_ {\mathrm{B}} u _ {i} (\boldsymbol {x}) e ^ {- i \boldsymbol {k} \cdot \boldsymbol {x}} \mathrm{d} \boldsymbol {x}\tag{40}
$$

were $V(B) = L_{1}L_{2}L_{3}$ is the volume of B and $\int_{B}dx$ means integration over the box B. From eqn (40) it is easy to see that $n_{j}(k)$ have to be Gaussian when $u_{i}(x)$ is a Gaussian field. Many authors relax this constraint and let $n_{j}(k)$ have random phase but a fixed absolute value. $^{5,23,24}$ Using this approach, every sample will get exactly the same variance and, given a wave number (or vector) the estimated power spectral density at this wave number will be the same for all realizations of the same process. This might be advantageous in some situations, but it is in contrast to power spectral density estimates of stationary time series which have 100% rms. $^{25,26}$ The difference between the two approaches is discussed in detail by Grigoriu. $^{27}$ In practice there is little difference and both models could be used. However, the Gaussian approach is usually easier to analyse theoretically and we shall stick to that in this paper. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/25c55646121c8dd586d695b0355e355aa92f1e6918a23337b6ab027296f8085f.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/6baad67020b5dc6846f1ec47932fb63d76ffb6aa2da438bc32322965d6fae0e1.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/667f71093b2c5ffdd528d14f57077b40ffb788637393e8b99a70eb7ed287bd8d.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/a36a39072bd986e78fc3fd16947018dfa49121cdef5c2f87d2b6df9a3f684bb0.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/e44fb74be96ae955943f52c0216e35896d4803549f0589f03940e7e9834f13a6.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/16c8ad2181d22b80f2acc7b48c18e9f91466fcfdf4d9071b96334888cbd185d0.jpg)



Fig. 9. Square root coherence comparison. The solid lines are from ESDU (with $U = 40 \, \text{m} \, \text{s}^{-1}$ and $z = 40 \, \text{m}$ ), the dotted from Simiu and the dashed from the spectral tensor with parameters fitting the ESDU spectra.


To find the coefficients $C_{ij}(\boldsymbol{k})$ we calculate the covariance tensor of eqn (40), obtaining 

$$
\begin{array}{l} C _ {i k} ^ {*} (\boldsymbol {k}) C _ {j k} (\boldsymbol {k}) \\ = \frac {1}{V ^ {2} (\mathrm{B})} \int_ {\mathrm{B}} \int_ {\mathrm{B}} \langle u _ {i} (\boldsymbol {x}) u _ {j} (\boldsymbol {x} ^ {\prime}) \rangle \mathrm{e} ^ {\mathrm{i} \boldsymbol {k} \cdot \boldsymbol {x}} \mathrm{e} ^ {- \mathrm{i} \boldsymbol {k} \cdot \boldsymbol {x} ^ {\prime}} \mathrm{d} \boldsymbol {x} \mathrm{d} \boldsymbol {x} ^ {\prime} \\ = \frac {1}{V ^ {2} (\mathrm{B})} \iint R _ {i j} (\boldsymbol {x} - \boldsymbol {x} ^ {\prime}) 1 _ {\mathrm{B}} (\boldsymbol {x}) 1 _ {\mathrm{B}} (\boldsymbol {x} ^ {\prime}) \mathrm{e} ^ {\mathrm{i} \boldsymbol {k} \cdot (\boldsymbol {x} - \boldsymbol {x} ^ {\prime})} \mathrm{d} \boldsymbol {x} \mathrm{d} \boldsymbol {x} ^ {\prime} \end{array}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/1504bc49f3cf870084fdbd0533eaf5afba2731f7ae39c5e31f3f6c9887993a32.jpg)


Fig. 10. The box B consists of $N_{1} \times N_{2} \times N_{3}$ points and has side lengths $L_{i}, i = 1, 2, 3$ , so the separation between the points in the i-direction is $\Delta L_{i} = L_{i}/N_{i}$ . U is the mean wind speed and T is the simulation time. 

where $1_{\mathrm{B}}(\pmb{x}) = 1$ if $\pmb{x} \in \mathrm{B}$ and 0 otherwise. Using the change of variables $\pmb{r} = \pmb{x} - \pmb{x}'$ and $s = \pmb{x} + \pmb{x}'$ having the Jacobian $|\partial (\pmb {r}, s) / \partial (\pmb {x}, \pmb{x}')| = 8$ , we get 

$$
\begin{array}{r l} C _ {i k} (\boldsymbol {k}) C _ {k j} (\boldsymbol {k}) & = \frac {1}{8 V ^ {2} (\mathrm{B})} \int R _ {i j} (\boldsymbol {r}) \mathrm{e} ^ {- \mathrm{i} \boldsymbol {k} \cdot \boldsymbol {r}} \int 1 _ {\mathrm{B}} \left(\frac {\boldsymbol {s} + \boldsymbol {r}}{2}\right) 1 _ {\mathrm{B}} \\ & \times \left(\frac {\boldsymbol {s} - \boldsymbol {r}}{2}\right) \mathrm{d} s \mathrm{d} \boldsymbol {r} \end{array}\tag{42}
$$

The inner integration can be carried out according to 

$$
\begin{array}{l} \int 1 _ {\mathrm{B}} \left(\frac {s + r}{2}\right) 1 _ {\mathrm{B}} \left(\frac {s - r}{2}\right) \mathrm{d} s \\ = \left\{ \begin{array}{c} \prod_ {l = 1} ^ {3} 2 (L _ {l} - | r _ {l} |) \text { for } | r _ {l} | <   L _ {l} \text { for   all } l \\ 0 \text { otherwise } \end{array} \right. \end{array}\tag{43}
$$

so, using the convolution theorem and noting that the Fourier transform of $L - |r|$ (for $|r| < L$ and else 0) is $L^2$ sinc $^2$ ( $kL/2$ ), we get 

$$
C _ {i k} ^ {*} (\boldsymbol {k}) C _ {j k} (\boldsymbol {k}) = \int \Phi_ {i j} \left(\boldsymbol {k} ^ {\prime}\right) \prod_ {l = 1} ^ {3} \operatorname{sinc} ^ {2} \left(\frac {\left(k _ {l} - k _ {l} ^ {\prime}\right) L _ {l}}{2}\right) d \boldsymbol {k} ^ {\prime}\tag{44}
$$

where $\operatorname{sinc} x \equiv (\sin x) / x$ . For $L_{l} \gg L$ , the $\operatorname{sinc}^{2}$ -function is 'delta-function-like', in the sense that it vanishes away from $k_{l}$ much faster than any change in $\Phi_{ij}$ , and the area beneath the $\operatorname{sinc}^{2}$ -curve is $2\pi / L_{l}$ . Therefore, we get 

$$
C _ {i k} ^ {*} (\boldsymbol {k}) C _ {j k} (\boldsymbol {k}) = \frac {(2 \pi) ^ {3}}{V (\mathrm{B})} \Phi_ {i j} (\boldsymbol {k})\tag{45}
$$

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/3b7d5b1ae91c1c367dbaf49c1b83408178b9fcf0670ded1615439ffbaa6d250b.jpg)



Fig. 11. Vertical and horizontal cross-sections of the u-fluctuations of simulated non-isotropic turbulence, with $\Gamma = 3$ .


The solution to eqn (45) is 

$$
C _ {i j} (\boldsymbol {k}) = \frac {(2 \pi) ^ {3 / 2}}{V (\mathrm{B}) ^ {1 / 2}} A _ {i j} (\boldsymbol {k}) = (\Delta k _ {1} \Delta k _ {2} \Delta k _ {3}) ^ {1 / 2} A _ {i j} (\boldsymbol {k})\tag{46}
$$

with $A_{ik}^{*}A_{jk}=\Phi_{ij}$ and $\Delta k_{l}=2\pi/L_{l}$ . This result should be expected when comparing eqn (3) to eqn (39). 

An example of a simulated non-isotropic velocity field with $\Gamma = 3$ is shown in Fig. 11. It is seen on the upper plot that the shear tilts the elongated fluctuations. Similar plots of the w-components show much less elongation and a shorter length scale. 

## 6.1 Problems with discretization and periodicity

Two problems occur when simulating a field by the Fourier series (eqn (39)) with the coefficients of eqn (46). The first is that for many applications the dimensions of the simulated box of turbulence need not be much larger than the length scale of the turbulence model L. Therefore eqn (45) may not be a good approximation to eqn (44). However, almost always for practical applications $L_{1} \gg L$ , so we can at least reduce (44) to 

$$
\begin{array}{r l} C _ {i k} ^ {*} (\boldsymbol {k}) C _ {j k} (\boldsymbol {k}) & = \frac {2 \pi}{L _ {1}} \int \Phi_ {i j} (k _ {1}, k _ {2} ^ {\prime}, k _ {3} ^ {\prime}) \\ & \times \prod_ {l = 2} ^ {3} \mathrm{sinc} ^ {2} \left(\frac {(k _ {l} - k _ {l} ^ {\prime}) L _ {l}}{2}\right) \mathrm{d} \boldsymbol {k} _ {\perp^ {\prime}} \end{array}
$$

where $\int d\boldsymbol{k}_{\perp}\equiv\int_{-\infty}^{\infty}\int_{-\infty}^{\infty}dk_{2}dk_{3}$ . This integration, which has to be done numerically $^{3}$ , is here limited to wave vectors, k, obeying $k=|k|<3/L$ . Outside this volume we consider eqn (45) a good approximation to eqn (44), regardless of the dimensions of the box. This discretization problem is illustrated by Figs 12 and 13. Fig. 12 shows that close to k = 0, $\Phi_{ij}(k)$ varies rapidly, implying that (45) may be a poor approximation to (44). Fig. 13 indicates that eqr (47) must be used if $L_{l}$ (l = 2 or 3) is less than $\sim8L$ . 

The second problem is that the simulated velocity field (eqn (39)) is periodic in all three directions. Originally, Shinozuka and Jan $^{5}$ suggested perturbing the wave vectors in (39) to avoid this problem. However, this would corrupt the efficiency of the FFT. Our solution to the problem is to use a larger spatial window. In Fig. 14 the coherence of vertical velocity fluctuations for a vertical separation 

$$
\operatorname{coh} _ {w w} \left(k _ {1}, z\right) \equiv \frac {\left| \chi_ {3 3} \left(k _ {1} , z\right) \right| ^ {2}}{\chi_ {3 3} \left(k _ {1} , 0\right) ^ {2}}\tag{48}
$$

calculated from the sheared velocity tensor with $\Gamma = 4$ , is shown together with coherences calculated from simulations with $2048 \times 32 \times 32$ points and dimensions $256L \times 3L \times 3L$ . Since the simulated field is periodic the coherence goes to 1 as $z \to L_3 = 3L$ . In a structural response analysis the space domain ( $L_2$ and $L_3$ ) should be chosen large enough to contain roughly twice the structure of interest in each dimension. However, if $L_l \gg L$ , or in the structure is insensitive to low frequency fluctuations, the structure might cover more than half the simulated field in each direction. 

A final point is that the simulated spectra are typically attenuated at high wave numbers (or frequencies), as seen from Fig. 13. The reason is that the wind speed is spatially averaged over a small volume roughly of the size $\Delta L_{1} \times \Delta L_{2} \times \Delta L_{3}$ . In most engineering applications it is exactly this averaged field which is needed, but if the unaveraged 'point velocities' are required they can still be simulated with our technique. Details of this aliasing problem are scrutinized in Appendix A. 

## 6.2 2- or 3-D fields of one, two or three components

In this section we outline which parts of the spectral tensor to use for simulations of fields with a 2- or 3-D domain of one, two or three velocity components, and how to factorize these. The algorithms of this paper are not needed for one-dimensional domain, i.e. simulation of wind fluctuations in one point as a function of time. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/cfbf5b7279da0d5466db46d3a1606834c68bf77e11ae9cfe580ed998937ba798.jpg)



Fig. 12. $\Phi_{11}(k)$ (in arbitrary units) at $k_{1} = 0\cdot 2 / L$ and $2 / L$ , with $\Gamma = 3$ .


## 6.2.1 3-D domain

If all three velocity components are required, the full tensor $\Phi_{ij}(\boldsymbol{k})$ should be used. If only two are needed, e.g. $i = 1$ and $j = 3$ , the tensor 

$$
\left( \begin{array}{c c} \Phi_ {1 1} (\boldsymbol {k}) & \Phi_ {1 3} (\boldsymbol {k}) \\ \Phi_ {1 3} (\boldsymbol {k}) & \Phi_ {3 3} (\boldsymbol {k}) \end{array} \right)\tag{49}
$$

suffices and if only one component is needed, e.g. i = 1, $\Phi_{11}(\boldsymbol{k})$ is used. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/af6c58dc424b9e2d761610979bc57b482573a826ada7fc79dccbbb465f59200e.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/85f0207cc76323682f7a3243dfaca625a93cc8534d06a5663d8308970c898175.jpg)



Fig. 13. The discretization problem illustrated by a w-spectrum with $\Gamma = 3.0$ . The thin line is the target spectrum, the dotted line is the average spectrum obtained by using eqn (46) and the dashed line is an average spectrum using eqn (47). (a) Average spectra of 100 simulations with box dimensions $32L \times 4L \times 4L$ ( $512 \times 32 \times 32$ points). (b) Average spectra of 20 simulations with $32L \times 8L \times 8L$ ( $512 \times 64 \times 64$ points).


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-26/1ce57473-52ae-45d7-b998-20b9389b8ed3/a3f9ad7ae4d9e35fbb3802183afbd05ee1df78ae67f74a2d131290dac7592fb0.jpg)



Fig. 14. Illustration of periodicity. Simulated (dots) and model w-coherences (curves) as functions of vertical coordinate z. The vertical dimension of the box is $L_{3} = 3L$ .


In the three-component case the factorization (see discussion of eqn (46)) of the isotropic tensor (eqn (8)) is 

$$
A (\boldsymbol {k}) = \frac {E ^ {1 / 2} (k)}{(4 \pi) ^ {1 / 2} k ^ {2}} \left( \begin{array}{c c c} 0 & k _ {3} & - k _ {2} \\ - k _ {3} & 0 & k _ {1} \\ k _ {2} & - k _ {1} & 0 \end{array} \right)\tag{50}
$$

and the factorization of the anisotropic tensor is obtained by multiplying eqn (50) by the matrix on the right-hand side of eqn (13). 

To take the ‘square root’ of eqn (49) we can use the general identity $A_{ik}A_{jk}=P_{ij}$ , where 

$$
P = \left( \begin{array}{c c} p _ {1 1} & p _ {1 2} \\ p _ {1 2} & p _ {2 2} \end{array} \right)\tag{51}
$$

with 

$$
A = \left(T + 2 \sqrt {D}\right) ^ {- 1 / 2} \left( \begin{array}{c c} p _ {1 1} + \sqrt {D} & p _ {1 2} \\ p _ {1 2} & p _ {2 2} + \sqrt {D} \end{array} \right)\tag{52}
$$

where $T = \operatorname{Tr}(P) = p_{11} + p_{22}$ and $D = \det(P) = p_{11}p_{22} - p_{12}^2$ . 

For the one-component case the factorization is simply the square root, e.g. $\sqrt{\Phi_{11}(\boldsymbol{k})}$ . 

## 6.2.2 2-D domain

If the domain is two-dimensional, e.g. in the $x_{1}$ and $x_{2}$ directions, the expression above must be integrated with respect to $k_{3}$ , e.g. 

$$
\Phi_ {i j} ^ {\mathrm{2D}} (k _ {1}, k _ {2}) = \int_ {- \infty} ^ {\infty} \Phi_ {i j} (\pmb {k}) \mathrm{d} k _ {3}\tag{53}
$$

In this case there is no neat factorization like eqn (50) so we have to use Choleski decomposition $^{26}$ in the 3-D case and eqn (52) in the 2-D case. 

In analogy to eqn (47) we have to modify eqn (53) when $(k_{1}^{2} + k_{2}^{2})^{1/2} < 3/L$ . The coefficients in the Fourier series now 

become 

$$
\begin{array}{r l} & C _ {i k} ^ {*} (k _ {1}, k _ {2}) C _ {j k} (k _ {1}, k _ {2}) \\ & = \frac {2 \pi}{L _ {1}} \int_ {- \infty} ^ {\infty} \int_ {- \infty} ^ {\infty} \Phi_ {i j} (k _ {1}, k _ {2} ^ {\prime}, k _ {3} ^ {\prime}) \\ & \times \operatorname{sinc} ^ {2} \left(\frac {(k _ {2} - k _ {2} ^ {\prime}) L _ {2}}{2}\right) \mathrm{d} k _ {2} ^ {\prime} \mathrm{d} k _ {3} ^ {\prime} \end{array}\tag{54}
$$

## 6.3 Implementation and speed

The implementation of the model includes three steps: 

1. Evaluate the coefficients $C_{ij}(k)$ , either by eqn (46) or if necessary, by eqn (47), using the factorizations discussed in the previous section. 

2. Simulate the Gaussian variable $n_{j}(\boldsymbol{k})$ and multiply. 

3. Calculate $u_{i}(\boldsymbol{x})$ from eqn (39) by FFT. 

The time consumption in the first step is proportional to the total number of points $N = N_{1}N_{2}N_{3}$ in the simulation. The required time to perform the FFT is $O(N \log_{2} N)^{26}$ . 

The first two steps in the $2048 \times 32 \times 32$ one-component simulation used in the coherence calculations of Fig. 14 took 30 s on an Intel Pentium 100 MHz computer. The FFT used 50 s and input/output 60 s, giving a total execution time of $2\frac{1}{2}$ minutes. If the integral (eqn (47)) is not used only a few seconds are saved on the execution time whereas the spectra are poorly simulated as illustrated by Fig. 13. A three-component simulation on the same grid took 70 s for steps $1 + 2$ , 150 s for step 3 and 180 s for I/O, giving a total execution time of seven minutes. A $8192 \times 64$ one-component simulation used 85 s for steps $1 + 2$ , 10 s for step 3 and 15 s for I/O; a total of less than two minutes. 

## 7 CONCLUSION

In this presentation we simulate a stochastic field from spectral tensor. This has not been done before for a realistic spectral velocity tensor for atmospheric surface layer turbulence, apparently because no such tensor model has been available. The spectral tensor of Mann $^{1}$ has been fitted to and compared with spectra and coherences from Kaimal, Simiu $^{4}$ and ESDU. $^{2,22}$ In general, taking the uncertainty of the atmospheric spectra into account, the tensor-derived spectra fit well with those in the literature. However, the ESDU spectra are markedly more peaked. 

The simulation algorithm is in principle a special case of the general paper by Shinozuka and Jan $^{5}$ which besides the often used cross-spectral matrix method, also provides a spectral tensor based method. There are some differences, however: Shinozuka and Jan use eqn (46) which, in our specific study, is shown not to be a good approximation to the exact eqn (44). This is because the spectral tensor of Mann has large second derivatives at low wave numbers. Furthermore, variances and spectra components are not random in Shinozuka and Jan, only the phases. The consequences of choosing only random phases are discussed by Shinozuka and Deodatis $^{23,24}$ and by Grigoriu. $^{27}$ 

The two most time-consuming steps in our algorithm are the evaluation of the spectral tensor, since the time it takes is proportional to the number of points in the simulations $N = N_{1}N_{2}N_{3}$ , and the FFT procedure which takes a time proportional to $N \log_{2} N$ . 

Methods based on cross-spectra often have the decomposition of $N_{1}$ cross-spectral matrices as the most time-consuming step. The fastest algorithm to do this known to the authors is proportional to $N_{1}N_{2}^{2}N_{3}^{2}$ (Winkelaar $^{28}$ ), i.e. considerably slower than our simulation method. Winkelaar's method is based on the Sandia method $^{29}$ which uses of the order of $N_{1}N_{2}^{3}N_{3}^{3}$ multiplications in its original implementation. Winkelaar's study uses coherences and not complex cross-spectra, in which case potentially important phase information is lost. Simulations based on Winkelaar $^{28}$ would thus never show tilted velocity fluctuations as in the upper plot of Fig. 11. Furthermore, our method automatically produces incompressible fields. 

The size of the fields produced by our algorithm is, in its current implementation, limited to the size of the computer's memory. In case one needs larger fields, say a large fraction of the computer's disk space, there are two ways to extend the method. Either one can implement an external storage FFT (Press et al. $^{26}$ , chap. 12.6) or one can try to extend the low memory usage hybrid Fourier transform and filtering approach of Li and Kareem $^{30}$ to three-dimensional fields. It is probably very difficult to extend the method to non-Gaussian fields. A good starting point would be Gurley et al. $^{31}$ . 

## ACKNOWLEDGEMENTS

The author is grateful to Steen Krenk, University of Lund, and Leif Kristensen, Risø, for numerous suggestions and comments. This research was supported in part by the Danish Technical Research Council (STVF) and the Danish Energy Agency through the project WAsP Engineering (EPF-97, 1363/97-0004). 

## REFERENCES



1. Mann, J. The spatial structure of neutral atmospheric surface-layer turbulence. J. Fluid Mech., 1994, 273, 141–168. 





2. ESDU International, Characteristics of atmospheric turbulence near the ground. Part II: Single point data for strong winds (neutral atmosphere). London, 1985. 





3. Kaimal, J. C., Wyngaard, J. C., Izumi, Y. & Coté, O. R. Spectral characteristics of surface-layer turbulence. Q. J. R. Meteorol. Soc., 1972, 98, 563–598. 





4. Simiu, E. & Scanlan, R. H., Wind Effects on Structures, 2nd edn. John Wiley & Sons, New York, 1986. 





5. Shinozuka, M. & Jan, C.-M. Digital simulation of 





random processes and its application. J. Sound and Vibration, 1972, 25(1), 111–128. 





6. Panofsky, H. A. & Dutton, J. A., Atmospheric Turbulence. John Wiley & Sons, New York, 1984. 





7. Mann, J., Models in micrometeorology. Technical Report R–727, Risø National Laboratory, Roskilde, 1994. 





8. Batchelor, G. K., The Theory of Homogeneous Turbulence. Cambridge University Press, Cambridge, 1953. 





9. von Kármán, T. Progress in the statistical theory of turbulence. Proc. Natl Acad. Sci., 1948, 34, 530–539. 





10. Mann, J., Kristensen, L. & Courtney, M. S., The Great Belt coherence experiment—a study of atmospheric turbulence over water. Technical Report R–596, Risø National Laboratory, Roskilde, 1991. 





11. Courtney, M. S., An atmospheric turbulence data set for wind turbine research. In Wind Energy Conversion, Proceedings of the 1988 BWEA Wind Energy Conference. Mechanical Engineering Publications, 1988, pp. 89–94. 





12. Smitt, L. W. & Brinch, M., A new wide boundary layer wind tunnel at the Danish Maritime Institute. In Aerodynamics of Large Bridges, ed. A. Larsen. A. A. Balkema, 1992, pp. 137–144. 





13. Landau, L. D. & Lifshitz, E. M., Fluid Mechanics. Pergamon Press, Oxford, 1987. 





14. ESDU International, Characteristics of wind speed in the lower layers of the atmosphere near the ground: Strong winds (neutral atmosphere). London, 1982. 





15. Charnock, H. Wind stress on a water surface. Q. J. R. Meteorol. Soc., 1955, 81, 639–640. 





16. Garratt, J. R. Review of drag coefficients over oceans and continents. Monthly Weather Rev., 1977, 105, 915–929. 





17. Geernaert, G. L. On the importance of the drag coefficient in air–sea interactions. Dynamics of Atmospheres and Oceans, 1987, 11, 19–38. 





18. Norwegian Petroleum Directorate, Regelverksamling for petroleumsvirksamheten. 1994 (in Norwegian). 





19. Brown, R. D. & Swail, V. R. Over-water gust factors. Ocean Eng., 1991, 18(4), 363–394. 





20. Kaimal, J. C. & Finnigan, J. J., Atmospheric Boundary Layer Flows, their Structure and Measurement. Oxford University Press, New York, 1995. 





21. Højstrup, J., Larsen, S. E. & Madsen, P. H., Power spectra of horizontal wind components in the neutral atmospheric boundary layer. In Ninth Symposium on Turbulence and Diffusion, ed. N. O. Jensen, L. Kristensen and S. E. Larsen. American Meteorological Society, 1990, pp. 305–308. 





22. ESDU International, Characteristics of atmospheric turbulence near the ground. Part III: Variations in space and time for strong winds (neutral atmosphere). London, 1986. 





23. Shinozuka, M. & Deodatis, G. Simulation of stochastic processes by spectral representation. Appl. Mech. Rev., 1991, 44(4), 191–203. 





24. Shinozuka, M. & Deodatis, G. Simulation of multidimensional gaussian stochastic fields by spectral representation. Appl. Mech. Rev., 1996, 49(1), 29-53. 





25. Bendat, J. S. and Piersol, A. G., Random Data: Analysis and Measurement Procedures. Wiley-Interscience, 1971. 





26. Press, W. H., Flannery, B. P., Teukolsky, S. A. & 





Vetterling, W. T., Numerical Recipes, 2nd edn. Cambridge University Press, Cambridge, 1992. 





27. Grigoriu, M., On the spectral representation method in simulation. Prob. Eng. Mech., 1993, 8, 75–90. 





28. Winkelaar, D., Fast three dimensional wind simulation and the prediction of stochastic blade loads. In Proceedings from the 10th ASME Wind Energy Symposium, Houston, TX, 1991. 





29. Veers, P. S., Three-dimensional wind simulation. Technical Report SAND88-0152, Sandia National Laboratories, 1988. 





30. Li, Y. & Kareem, A. Simulation of multivariate random processes: Hybrid DFT and digital filtering approach. J. Eng. Mech., ASCE, 1993, 119, 1078–1098. 





31. Gurley, K. R., Karrem, A. & Tognarelli, M. A. Simulation of a class of non-normal random processes. Int. J. Non-Lin. Mech., 1996, 31(5), 601–617 



## APPENDIX A ON ALIASING IN THE WIND SIMULATION

The inverse of eqn (39) is not exactly eqn (40) but more precisely 

$$
C _ {i j} (\boldsymbol {k}) n _ {j} (\boldsymbol {k}) = \frac {1}{N} \sum_ {\boldsymbol {x}} u _ {i} (\boldsymbol {x}) \mathrm{e} ^ {- \mathrm{i} \boldsymbol {k} \cdot \boldsymbol {x}}\tag{A.1}
$$

where $N = N_{1}N_{2}N_{3}$ and $\sum_{x}$ is the sum over all $x$ defined in the text after eqn (39). Then 

$$
\begin{array}{r l} C _ {i k} ^ {*} (\boldsymbol {k}) C _ {j k} (\boldsymbol {k}) & = \frac {1}{N ^ {2}} \sum_ {\boldsymbol {x}} \sum_ {\boldsymbol {x} ^ {\prime}} \mathrm{e} ^ {\mathrm{i} \boldsymbol {k} \cdot (\boldsymbol {x} - \boldsymbol {x} ^ {\prime})} R _ {i j} (\boldsymbol {x} - \boldsymbol {x} ^ {\prime}) \\ & = \frac {1}{N ^ {2}} \sum_ {n} \exp (\mathrm{i} \boldsymbol {k} \cdot \boldsymbol {\xi}) R _ {i j} (\boldsymbol {\xi}) \prod_ {l = 1} ^ {3} (N _ {l} - | n _ {l} |) \end{array}\tag{A.2}
$$

where $\sum_{n}$ is the sum over all vectors of integers $n = (n_1, n_2, n_3)$ with $-N_M \leq n_m \leq N_m$ , $m = 1, 2, 3$ , and $\xi_m = n_m \Delta L_m$ . Inverse Fourier transforming the right-hand side of eqn (A.2) with respect to $k$ , we get 

$$
\begin{array}{l} \frac {1}{N ^ {2}} \sum_ {n} \delta (\boldsymbol {x} - \boldsymbol {\xi}) R _ {i j} (\boldsymbol {\xi}) \prod_ {l = 1} ^ {3} (N _ {l} - | n _ {l} |) \\ = \frac {R _ {i j} (\boldsymbol {x})}{N ^ {2}} \sum_ {n} \delta (\boldsymbol {x} - \boldsymbol {\xi}) \prod_ {l = 1} ^ {3} (N _ {l} - | n _ {l} |) \end{array}
$$

This product of the correlation tensor and the sum of Dirac delta functions is now Fourier transformed to get the convolution 

$$
C _ {i k} ^ {*} (\boldsymbol {k}) C _ {j k} (\boldsymbol {k}) = \frac {1}{N ^ {2}} \Phi_ {i j} (\boldsymbol {k}) * f (\boldsymbol {k})\tag{A.3}
$$

where the operator * denotes the convolution and $f(k)$ is the Fourier transform of 

$$
\begin{array}{l} \sum_ {n} \delta (\boldsymbol {x} - \boldsymbol {\xi}) \prod_ {l = 1} ^ {3} (N _ {l} - | n _ {l} |) \\ = \prod_ {l = 1} ^ {3} \sum_ {n _ {l} = - N _ {l}} ^ {N _ {l}} (N _ {l} - | n _ {l} |) \delta (x _ {l} - \xi_ {l}) \end{array}
$$

i.e. 

$$
f (\boldsymbol {k}) = \prod_ {l = 1} ^ {3} \sum_ {n _ {l} = - N _ {l}} ^ {N _ {l}} (N _ {l} - | n _ {l} |) \exp (\mathrm{i} k _ {l} \xi_ {l})
$$

The general identity 

$$
\sum_ {n = - N} ^ {N} (N - | n |) \exp (\mathrm{i} n a) = \frac {\sin^ {2} (N a / 2)}{\sin^ {2} (a / 2)}\tag{A.4}
$$

is now substituted into eqn (A.3), which then becomes 

$$
C _ {i k} ^ {*} (\boldsymbol {k}) C _ {j k} (\boldsymbol {k}) = \int \Phi_ {i j} \left(\boldsymbol {k} ^ {\prime}\right) \frac {1}{N ^ {2}} \prod_ {l = 1} ^ {3} \frac {\sin^ {2} \left(\left(k _ {l} - k _ {l} ^ {\prime}\right) L _ {l} / 2\right)}{\sin^ {2} \left(\left(k _ {l} - k _ {l} ^ {\prime}\right) \Delta L _ {l} / 2\right)} d \boldsymbol {k} ^ {\prime}\tag{A.5}
$$

When the $N_{i}$ s are large, eqn (A.5) can be approximated by 

$$
\begin{array}{l}C_{ik}^{*}(\boldsymbol {k})C_{jk}(\boldsymbol {k})\\ = \frac{(2\pi)^{3}}{V(\mathrm{B})}\sum_{\substack{n_{i} = -\infty \\ l = 1,2,3}}^{\infty}\Phi_{ij}\left(\boldsymbol {k} + 2\pi \left(\frac{n_{1}}{L_{1}},\frac{n_{2}}{L_{2}},\frac{n_{3}}{L_{3}}\right)\right) \end{array}\tag{A.6}
$$

Spectra from a simulation using eqn (A.6) with $-2 \leq n_{l} \leq 2$ instead of $-\infty \leq n_{l} \leq \infty$ (l = 1, 2, 3) increase the spectral density at high wave numbers so that the simulated and target spectra coincide in Fig. 13. 