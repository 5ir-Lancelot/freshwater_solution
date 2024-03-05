# Carbonate System modelling

_Lukas Rieder_

Here will be my explanaition of the  equations and assumptions from the Book (Steven Emerson , John Hedges). The squared brackets imply the concentration is meant:

$$ c( CO_3^{-2} ) = \[ CO_3^{-2} \]. $$

Also because carbonic acid $H_2 CO_3$ is very unstable and it is difficult to distinguish it from  $\[ CO_2(aq) \]$ both compounds are combined to:

$$ \[CO_2 \] = \[CO_2(aq) \]+ \[H_2 CO_3 \].$$

Thus the first dissociation constant is actually a combined one of two reactions ( $ CO_2(aq) + H_2 O ->  H_2 CO_3 -> HCO_3^{-} + H^{+} $ ).

The dissociation constansts $K_1^{'}$ $K_2^{'}$ as well as the Henrys law constant $K_H$  are Temperature dependent. This dependece is rather complex to describe so I wont show the equations for the temperature dependence here.

All equations neccessary to describe/solve the full carbonate system are listed below:


<!--- This is an HTML comment in Markdown. For some reason the regular Latex _{i}  is not accepted. Use just _i instead. Because [ ] referes to
links in markdown files   the squared brackets have to be typed in this way:  \[   \] . In the equations leave enough whitespaces especially at end and beginning. For bigger subscripts longer than one character: to prevent the blog software from interpreting the underscores as meaning italics use '\_{xy}' instead of '_{xy}' -->

<!---  https://www.mathelounge.de/509545/mathjax-latex-basic-tutorial-und-referenz-deutsch -->

1. total dissolved inorganic carbon: $$ DIC = \[ CO_2 \] + \[ HCO_3^- \] + \[ CO_3^{-2} \] $$

2. alkalinity **extremely** simplified (carbonate alkalinity):  $$ A_C=\[ HCO_3^{-} \]  +2 \cdot \[ CO_3^{-2} \] + \[ OH^{-} \] - \[ H^{+} \] $$

3. First Dissociation Constant of carbonic acid: $$ K_1^{'} = \frac{ \[HCO_3^{-} \] \cdot \[H^{+}\] }{ \[CO_2 \] } $$

4. Second Dissociation Constant of carbonic acid: $$ K_2^{'}=\frac{ \[CO_3^{-2} \] \cdot \[H^{+} \] }{ \[ HCO_3^{-}  \] } $$

5. Solubility of Gas (Henry's law constant $H$ \[L atm / mol \] ): $$ K_H=\frac{ \[CO_2 \]  }{ H } $$

6. Temperature dependence of Henry's law constant $H(T)$,  $ H\_{ref} $ is the Henry's law constant of CO2 at the reference temperature $ T_\{ref}=298.15 K $ and the Temperature $T$ must be used in Kelvin:  $$ H(T) = H\_{ref} \cdot exp(2400 \cdot (\frac{1}{T} - \frac{1}{T\_{ref}})) $$

7. Dissociation Constant of water:  $$ K_w = \[H^{+} \] \[OH^{-} \]  $$

8. When other weak acids (HB) are involved:  $$ K_{HB} = \frac{ \[ H^{+} \] \[ B^{-} \]}{ \[HB \]} $$




However the model you find here is not calculated with the simplification of alkalinity. Everything is calculated with [phreeqpython](https://github.com/Vitens/phreeqpython) a python toolbox designed for solving environmental chemistry problems.

The current global mean level of atmospheric partial pressure of CO2 gas you can get from [Mauna Loa Observatory](https://gml.noaa.gov/ccgg/trends/global.html).


# Ion Activity Product (IAP) and Saturation Index (SI)

<!--- when using curly braces the underscores also need to be escaped with \
-->

The law of mass action in (1) determines the activities at the state of equilibrium, $ \{A\}\_{eq} $ and $ \{B\}\_{eq}$:

(1) $$ K\_{sp} \\,=\\, \\dfrac{\\{A\\}^{a}\\{B\\}^{b}}{\\{A\_{a}B\_{b}\\}}
\\,=\\, \\{A\\}^{a}\\{B\\}^{b} $$


(2) 	chem equilibrium: 	
$$ K_{sp} = \{A\}\_{eq}^{a} \{B\}\_{eq}^{b} $$

However, a real solution may not be in the state of equilibrium. The non-equilibrium state is 
described by the ion activity product (IAP). It has the same math form as the equilibrium constant $K_{sp}$,
but involves the actual activities, $ \{A\}\_{actual} $ and $ \{B\}\_{actual}$:

(3) 	non-equilibrium:  $$ IAP = \{A\}\_{actual}^{a} \{B\}\_{actual}^{b} $$

The decadic logarithm of the ratio of IAP to Ksp defines of the saturation index:
(4) 	saturation index: 	SI

The saturation index is a useful quantity to determine whether the water is saturated,
undersaturated, or supersaturated with respect to the given mineral:

- SI = 0 	IAP = $K_{sp}$ saturated  (in chem equilibrium)
- SI < 0 	IAP < $K_{sp}$ undersaturated
- SI > 0 	IAP > $K_{sp}$ supersaturated


