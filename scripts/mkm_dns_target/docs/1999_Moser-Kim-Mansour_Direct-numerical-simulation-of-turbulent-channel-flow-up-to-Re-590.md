# Direct numerical simulation of turbulent channel flow up to $\mathtt { R e } _ { \tau } \mathtt { = } 5 9 0$

Robert D. Moser 

Department of Theoretical and Applied Mechanics, University of Illinois at Urbana—Champaign, Urbana, Illinois 61801 

John Kim 

Department of Mechanical and Aerospace Engineering, University of California, Los Angeles, Los Angeles, California 90095-1597 

Nagi N. Mansour 

NASA Ames Research Center, Moffett Field, California 94035 

~Received 19 November 1998; accepted 30 December 1998! 

Numerical simulations of fully developed turbulent channel flow at three Reynolds numbers up to $\scriptstyle \mathrm { R e } _ { \tau } = 5 9 0$ are reported. It is noted that the higher Reynolds number simulations exhibit fewer low Reynolds number effects than previous simulations at $ { \mathrm { R e } } _ { \tau } = 1 8 0$ . A comprehensive set of statistics gathered from the simulations is available on the web at http://www.tam.uiuc.edu/Faculty/Moser/ channel. © 1999 American Institute of Physics. @S1070-6631~99!02204-7# 

Over the past 15 years, direct numerical simulation ~DNS! has been a valuable tool for the investigation of wallbounded turbulent flows. A variety of studies of such simulations have yielded insights into both the statistical and structural characteristics of wall-bounded turbulence.<sup>1–4</sup> One of the simplest wall-bounded turbulent flows to simulate is the flow in a plane channel, which was simulated by Kim, Moin, and $\mathrm { M o s e r } ^ { 5 }$ ~referred to as KMM henceforth!, and which has been simulated by many others since.<sup>6–8</sup> However, most of these simulations have been at a single low Reynolds number, $\mathrm { R e } _ { \tau } { = } u _ { \tau } \delta / \nu { = } 1 8 0 \ ( u _ { \tau }$ and are the friction velocity and channel half-width, respectively!, for which significant low Reynolds number effects are expected. One exception is the simulation of Papavassiliou<sup>9</sup> at $ { \mathrm { R e } } _ { \tau } = 3 0 0 .$ 

As a continuation of the work of KMM, two higher Reynolds number channel simulations have been performed, one at $\mathrm { R e } _ { \tau } { \approx } 3 9 5$ and the other at $\scriptstyle \mathrm { R e } _ { \tau } \approx 5 9 0$ , and new simulations of the KMM $ { \mathrm { R e } } _ { \tau } { \approx } 1 8 0$ case were conducted. Selected data from these simulations have been used in studies by several authors.<sup>3,4,10,11</sup> However, the data has not been generally available. Our purpose in this Brief Communication is to document these new cases and make the statistical data from them available. 

Numerical simulations of all three cases were performed using a variant of the DNS channel code of ${ \mathrm { K M M } } ^ { 5 }$ The numerical method uses a Chebychev-tau formulation in the wall–normal direction ~y! and a Fourier representation in the horizontal directions. Unlike the simulations in KMM, a low-storage third-order Runga–Kutta time discretization is used for the nonlinear terms.<sup>12</sup> Periodic boundary conditions are applied in the streamwise ~x! and spanwise ~z! directions, and the pressure gradient that drives the flow was adjusted dynamically to maintain a constant mass flux through the channel. The periodic domain sizes were selected so that the two-point correlations in the streamwise and spanwise directions would be essentially zero at maximum separation ~half the domain size!, while the number of Fourier/Chebychev modes ~the resolution! was selected so that the energy spectra would be sufficiently small at large wave numbers. The simulation parameters for the three cases are given in Table I in units of channel half-width ~ ! and in 1 units $( \mathrm { R e } _ { \tau } { = } \delta ^ { + }$ $= \delta u _ { \tau } / \nu )$ . Note also that in all three cases there are 13 or more Chebychev grid points below $y ^ { + } = 1 0$ 

The original KMM channel calculation at $ { \mathrm { R e } } _ { \tau } = 1 8 0$ was at such a low Reynolds number that several of the expected features of moderate to high Reynolds number wall-bounded flows were not present. However, the higher Reynolds number cases, particularly $\scriptstyle \mathrm { R e } _ { \tau } = 5 9 0$ , have significantly fewer low-Reynolds number effects. For example, the $ { \mathrm { R e } } _ { \tau } = 1 8 0$ simulation has a very short log layer, if it exists at all. But, as shown in Fig. 1, the mean profiles of the $\mathrm { R e } _ { \tau } { = } 3 9 5$ and $\mathrm { R e } _ { \tau }$ $= 5 9 0$ cases agree out to $y ^ { + } { \approx } 2 0 0 .$ , in an apparent log law. Furthermore, the $ { \mathrm { R e } } _ { \tau } = 1 8 0$ profile does not agree with the higher Re cases beyond $y ^ { + } = 1 0$ . The apparent log law in the $ { \mathrm { R e } } _ { \tau } = 1 8 0$ case has a larger intercept than in the higher Reynolds number flows. This is also a low-Reynolds number effect, which has been previously noted in experimental measurements of channel flows. 

The variation of the mean profiles with Reynolds number is more apparent in Fig. 2~a!, in which $\gamma { = } y ^ { + } d u ^ { + } / d y ^ { + }$ is plotted. In a log layer, this quantity will be constant with value $1 / \kappa .$ With this more sensitive measure, it is clear that the mean profiles for $ { \mathrm { R e } } _ { \tau } = 3 9 5$ and $\scriptstyle \mathrm { R e } _ { \tau } = 5 9 0$ agree for $y ^ { + }$ $\leqslant 7 0$ , suggesting that the high Re law of the wall profile has been attained in this region. For $\scriptstyle \mathrm { R e } _ { \tau } = 5 9 0 .$ , varies linearly from $y ^ { + } { \approx } 8 0$ to $y ^ { + } { \approx } 2 2 0$ , with values of $1 / \gamma$ ~equivalent ! varying from 0.45 to 0.33. Despite appearances to the contrary in Fig. 1, this is not a log region. Except for the wiggles in the  profile, which we attribute to a marginal statistical sample, it appears that the $\scriptstyle \mathrm { R e } _ { \tau } = 3 9 5$ case also has a linearly varying  for ${ \boldsymbol { y } } ^ { + } { > } 8 0$ , though with a different slope. We can only speculate as to whether, with increasing Re, the slope of the curve will reduce to zero in this region. The lack of a true log law in these cases is consistent with the analysis of 


TABLE I. Simulation parameters for the three channel direct numerical simulations. Here $\Delta y _ { c } ^ { + }$ is the y resolution in the center of the channel.


<table><tr><td><eq>Re_{\tau}</eq>Nom.</td><td><eq>Re_{\tau}</eq>Actual</td><td><eq>L_x</eq></td><td><eq>L_z</eq></td><td><eq>N_x \times N_y \times N_z</eq></td><td><eq>\Delta x^+</eq></td><td><eq>\Delta z^+</eq></td><td><eq>\Delta y_c^+</eq></td></tr><tr><td>180</td><td>178.13</td><td>4πδ</td><td><eq>\frac{4}{3}\pi\delta</eq></td><td>128×129×128</td><td>17.7</td><td>5.9</td><td>4.4</td></tr><tr><td>395</td><td>392.24</td><td>2πδ</td><td>πδ</td><td>256×193×192</td><td>10.0</td><td>6.5</td><td>6.5</td></tr><tr><td>590</td><td>587.19</td><td>2πδ</td><td>πδ</td><td>384×257×384</td><td>9.7</td><td>4.8</td><td>7.2</td></tr></table>

George et al.,<sup>11</sup> who suggest that a log profile is not expected for $y ^ { + } < 3 0 0$ or y/ .0.1 $( y ^ { + } > 5 9$ for $\mathrm { R e } _ { \tau } { = } 5 9 0 )$ 

While a log law is expected in a high-Reynolds number turbulent channel according to the classical theory of Millikan,<sup>13</sup> a more recent analysis by George and his colleagues<sup>14,11</sup> and by Barenblatt $e t a l . ^ { 1 5 }$ have suggested that the overlap region between inner and outer scalings in wallbounded turbulence may yield a power law, rather than a log law. Actually, there is some controversy since George and co-workers predict a power law for a boundary layer but a log law for a channel, while Barenblatt et al. get a power law in both cases. To determine if a power law is a better fit to the simulation data, the quantity $\beta { = } ( y ^ { + } / u ^ { + } ) ( d u ^ { + } / d y ^ { + } )$ is plotted in Fig. 2~b!. $\operatorname { I f } u ^ { + }$ behaves like $u ^ { + } { = } A ( y ^ { + } ) ^ { n }$ in some region, then $\beta$ will have a constant value of n in that region. Over the same region that $\gamma$ increases linearly for Re 5590, $\beta$ also increases approximately linearly, though somewhat more slowly. Thus the mean profiles do not exactly obey a power law either. 

Another expected property of a high-Reynolds number channel flow is that the production and dissipation of turbulent kinetic energy will be approximately balanced in the log region. To examine this, the ratio of production to dissipation is plotted in Fig. 3. $\mathrm { A t } \ \mathrm { R e } _ { \tau } { = } 5 9 0$ this ratio is approximately one over a range of $y ^ { + } \ ( 7 0 { \leqslant } y ^ { + } { \leqslant } 2 5 0 )$ , but the ratio is actually slowly increasing over this range. Note that the $ { \mathrm { R e } } _ { \tau }$ 5395 profile agrees with the higher Re profile ~except for statistical wiggles! for $y ^ { + } { \leqslant } 2 0 0 .$ , suggesting that this is representative of the high Reynolds number limit in this region. Again, based on the current data, we cannot say whether for larger Re a broad plateau with value one would exist. 

A third Reynolds number effect in wall-bounded turbulence is in the rms velocity profiles $( \boldsymbol { u } ^ { \prime } , \boldsymbol { v } ^ { \prime }$ , and $w ^ { \prime } )$ . These are plotted in wall units in Fig. 4~a! for the three Reynolds numbers discussed here. In agreement with the observations of Spalart,<sup>16</sup> the peak value of the $u ^ { \prime }$ profile is Reynolds number dependent at these low Reynolds numbers, with the peak varying from 2.65 at Re 5180 to 2.77 at $\scriptstyle \mathrm { R e } _ { \tau } = 5 9 0$ There are even larger variations in the other components. Note that the peak in the $u ^ { \prime }$ profile occurs at $y ^ { + } = 1 4$ , which is well within the region for which the high-Reynolds number limit appears to have been reached as determined from the data discussed above, at least for the 395 and 590 cases. Apparently, the rms velocities are more sensitive to Reynolds number effects than these other quantities. In fact, even the wall-limiting behavior of the rms profiles varies among our different Reynolds numbers. For example, the limiting value at the wall of $u ^ { \prime + } / y ^ { + } = 0 . 4 0 5 .$ , 0.396, and 0.363 for $\scriptstyle \mathrm { R e } _ { \tau } = 5 9 0$ , 395, and 180, respectively. Not surprisingly, the near-wall rms vorticity fluctuations exhibit similar Reynolds number dependence, as is shown in Fig. 5. Remarkably, however, the wall–normal rms vorticity $\omega _ { y } ^ { \prime + }$ collapses for all three Reynolds numbers. Near the wall, $\omega _ { y }$ is dominated by the presence of the streaks through the term $\partial u / \partial z$ . The invariance of $\omega _ { y } ^ { \prime + }$ with Reynolds number is thus consistent with the invariance of the streak spacing in wall units. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-13/f3758667-1f99-4216-abc8-c2baaa5b5d02/c8caaa54de87ea51cdb2a120c230277adb9fb0baeece715a22e943a0207f0be0.jpg)



FIG. 1. The mean velocity profile in wall units.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-13/f3758667-1f99-4216-abc8-c2baaa5b5d02/657702fb5aec3c10572bbfde05f0dc4cc9b8dcc1a9f715235df003a9023cfc68.jpg)



FIG. 2. Diagnostic quantities for a log law $( \gamma ,$ lower curves! and a powe law ~ , upper curves!. Here $\gamma { = } y ^ { + } d u ^ { + } / d y ^ { + }$ is constant with value 1/ in a log law and $\beta { = } ( y ^ { + } / u ^ { + } ) ( d u ^ { + } / d y ^ { + } )$ is constant with value n in a power law, where n is the exponent in the relation $\scriptstyle U ^ { + } = A ( y ^ { + } ) ^ { n }$


Of course, far from the wall, the rms velocity profiles should scale with outer variables, rather than wall variables. The same rms profiles plotted using $u _ { \tau }$ and $\delta$ scalings are shown in Fig. 4~b!. The collapse of the $u ^ { \prime }$ profiles beyond $y / \delta { = } 0 . 4$ is remarkably good, with the two high Reynolds number cases agreeing for $y / \delta { > } 0 . 2 ;$ thus the $u ^ { \prime }$ profiles appear to collapse to their high Re outer-layer limit for $y ^ { + }$ $> 8 0$ . Furthermore, in this outer region, the $u ^ { \prime }$ profile depends linearly on $y / \delta$ until $y / \delta \approx 0 . 8 5$ . The collapse of the $v ^ { \prime }$ and $w ^ { \prime }$ profiles in the outer region is not as spectacular, but it does appear that the two higher Re cases are nearly the same for $y / \delta { > } 0 . 2$ and they appear also to vary linearly over a significant range. 

![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-13/f3758667-1f99-4216-abc8-c2baaa5b5d02/5d2abca3331c7a388a52d5199553c0eabade839dcbb04d6f830e0c82ce679a9d.jpg)



FIG. 3. The ratio of production ~ ! to dissipation ~ ! of turbulent kinetic energy.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-13/f3758667-1f99-4216-abc8-c2baaa5b5d02/8bad9d41845fa8da4d9b3b6f0d08a8ba46fb35467a658b81202ebae40e6e12cd.jpg)


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-13/f3758667-1f99-4216-abc8-c2baaa5b5d02/ed38213894c4bc7fe2d837ad23d0b3f0da201f5b60373deeb7e6fdab1a74c28d.jpg)



FIG. 4. Rms velocity profiles in ~a! wall coordinates and ~b! global coordinates. Profiles for three Reynolds numbers are shown: $\mathrm { R e } _ { \tau } { = } 5 9 0 , 3 9 5 ,$ and 180. The peak rms velocities generally increase with Reynolds number.


![image](https://cdn-mineru.openxlab.org.cn/result/2026-07-13/f3758667-1f99-4216-abc8-c2baaa5b5d02/65791ea1ddc867a24136080b6682cc3834fe030b6640e077747875318be56642.jpg)



FIG. 5. Rms vorticity profiles in wall coordinates. Profiles for three Reynolds numbers are shown: $\mathrm { R e } _ { \tau } { = } 5 9 0 ,$ 395, and 180. The rms vorticities generally increase with Reynolds number.


The results above suggest that the high Re channel flow simulation discussed here is at sufficiently large Reynolds number to be free of the most obvious low-Reynolds number effects. Furthermore, the three simulations taken together give a good indication of the Reynolds number effects over the range $1 8 0 { \leqslant } \mathrm { R e } _ { \tau } { \leqslant } 5 9 0$ . Thus, the results of these simulations are fertile ground for a detailed investigation of the statistical properties of wall-bounded turbulence. To facilitate such investigations, many statistical quantities have been evaluated from the three simulation cases discussed here. These data are available as ASCII files on the web at http:// www.tam.uiuc.edu/Faculty/Moser/channel. The data include mean, Reynolds stress, skewness, and flatness profiles, terms in the Reynolds stress transport equations, spectra and twopoint correlations, and velocity and pressure probability density functions. In addition, other quantities will be made available at this site as they are extracted from the simulations. 

## ACKNOWLEDGMENTS

The numerical simulations reported here were performed when the authors were at the NASA–Ames Research Center. Computer time was also provided by the NASA–Ames Research Center, and is gratefully acknowledged. 



<sup>1</sup>W. Rodi and N. N. Mansour, ‘‘Low Reynolds number k2 modeling with the aid of direct simulation data,’’ J. Fluid Mech. 250, 509 ~1993!. 





<sup>2</sup>N. N. Mansour, J. Kim, and P. Moin, ‘‘Reynolds-stress and dissipationrate budgets in a turbulent channel flow,’’ J. Fluid Mech. 194, 15 ~1988!. 





<sup>3</sup>H. M. Blackburn, N. N. Mansour, and B. J. Cantwell, ‘‘Topology of finescale motions in turbulent channel flow,’’ J. Fluid Mech. 310, 269 ~1996!. 





<sup>4</sup>J. Kim and R. A. Antonia, ‘‘Isotropy of the small scales of turbulence at low Reynolds number,’’ J. Fluid Mech. 251, 219 ~1993!. 





<sup>5</sup>J. Kim, P. Moin, and R. D. Moser, ‘‘Turbulence statistics in fully developed channel flow at low Reynolds number,’’ J. Fluid Mech. 177, 133 ~1987!. 





<sup>6</sup>S. L. Lyons, T. J. Hanratty, and J. B. McLaughlin, ‘‘Large-scale computer simulation of fully-developed turbulent channel flow with heat transfer,’ Int. J. Numer. Methods Fluids 13, 999 ~1991!. 





<sup>7</sup>J. Rutledge and C. A. Sleicher, ‘‘Direct simulation of turbulent flow and heat transfer in a channel. Part I: Smooth walls,’’ Int. J. Numer. Methods Fluids 16, 1051 ~1993!. 





<sup>8</sup>N. Kasagi, Y. Tomita, and A. Kuroda, ‘‘Direct numerical simulation of passive scalar field in a turbulent channel flow,’’ Trans. ASME 114, 598 ~1992!. 





<sup>9</sup>D. V. Papavassiliou, Ph.D. thesis, Department of Chemical Engineering, University of Illinois, Urbana–Champaign, 1996. 





<sup>10</sup>J. Jimenez, ‘‘A selection of test cases for the validation of large-eddy simulations of turbulent flows,’’ Advisory Report No. AGARD-AR-345, AGARD, 1998. 





<sup>11</sup>W. K. George, L. Castillo, and M. Wosnik, ‘‘A theory for turbulent pipe and channel flow at high Reynolds numbers,’’ TAM Report No. 872, Department of Theoretical and Applied Mechanics, University of Illinois at Urbana—Champaign, 1997. 





<sup>12</sup>P. R. Spalart, R. D. Moser, and M. M. Rogers, ‘‘Spectral methods for the Navier–Stokes equations with one infinite and two periodic directions,’’ J. Comput. Phys. 96, 297 ~1991!. 





<sup>13</sup>C. M. Millikan, A Critical Discussion of Turbulent Flows in Channels and Circular Tubes, in Proceedings of the 5th International Congress of Applied Mechanics ~Wiley, New York, 1938! ~pp. 386-392!. 





<sup>14</sup>W. D. George and L. Castillo, ‘‘Zero-Pressure-Gradient Turbulent Boundary Layer,’’ Appl. Mech. Rev. 50, 689 ~1997!. 





<sup>15</sup>G. I. Barenblatt, A. Chorin, and V. M. Prostokishin, ‘‘Scaling laws for fully developed flow in pipes,’’ Appl. Mech. Rev. 50, 413 ~1997!. 





<sup>16</sup>P. R. Spalart, ‘‘Direct simulation of a turbulent boundary layer up to $\mathrm { R e } _ { \theta } { = } 1 4 \bar { 1 } 0 , ^ { 3 } \ .$ J. Fluid Mech. 187, 61 ~1988!. 

