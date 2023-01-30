# Carbon Dioxide Dissolution Simulation 

_Lukas Rieder_

Here will be my explanaition of the  equations and assumptions from the Book (Steven <Meerson , John Hedges). The squared brackets imply the concentration is meant:

$$ c( CO_3^{-2} ) = \[ CO_3^{-2} \]. $$

Also because carbonic acid $H_2 CO_3$ is very unstable and it is difficult to distinguish it from  $\[ CO_2(aq) \]$ both compounds are combined to:

$$ \[CO_2 \] = \[CO_2(aq) \]+ \[H_2 CO_3 \].$$

Thus the first dissociation constant is actually a combined one of two reactions ( $ CO_2(aq) + H_2 O ->  H_2 CO_3 -> HCO_3^{-} + H^{+} $ ).

The dissociation constansts $K_1^{'}$ $K_2^{'}$ as well as the Henrys law constant $K_H$  are Temperature dependent. This dependece is rather complex to describe so I wont show the equations for the temperature dependence here.

All equations neccessary to describe/solve the full carbonate system are listed below:


<!--- This is an HTML comment in Markdown. For some reason the regular Latex _{i}  is not accepted. Use just _i instead. Because [ ] referes to
links in markdown files   the squared brackets have to be typed in this way:  \[   \] . In the equations leave enough whitespaces especially at end and beginning. For biger subscripts longer than one character: to prevent the blog software from interpreting the underscores as meaning italics use '\_{xy}' instead of '_{xy}' -->

<!---  https://www.mathelounge.de/509545/mathjax-latex-basic-tutorial-und-referenz-deutsch -->

1. total dissolved inorganic carbon: $$ DIC = \[ CO_2 \] + \[ HCO_3^- \] + \[ CO_3^{-2} \] $$

2. alkalinity **extremely** simplified (carbonate alkalinity):  $$ A_C=\[ HCO_3^{-} \]  +2 \cdot \[ CO_3^{-2} \] + \[ OH^{-} \] - \[ H^{+} \] $$

3. First Dissociation Constant of carbonic acid: $$ K_1^{'} = \frac{ \[HCO_3^{-} \] \cdot \[H^{+}\] }{ \[CO_2 \] } $$

4. Second Dissociation Constant of carbonic acid: $$ K_2^{'}=\frac{ \[CO_3^{-2} \] \cdot \[H^{+} \] }{ \[ HCO_3^{-}  \] } $$

5. Solubility of Gas (Henrys law constant for ): $$ K_H=\frac{ \[CO_2 \]  }{ f\_{CO_2,a} } $$

6. Dissociation Constant of water:  $$ K_w = \[H^{+} \] \[OH^{-} \]  $$

7. When other weak acids (HB) are involved:  $$ K_{HB} = \frac{ \[ H^{+} \] \[ B^{-} \]}{ \[HB \]} $$




There are many 
However the Simulation you find here is not calculated with the strong simplification of Alkalinity. Everything is calculated with [phreeqpython](https://github.com/Vitens/phreeqpython) a python toolbox designed for solving environmental chemistry problems.

The current global mean level of atmospheric partial pressure of CO2 gas you can get from [Mauna Loa Observatory](https://gml.noaa.gov/ccgg/trends/global.html).

The Alkalinity of the water will be simulated with adding solid NaHCO3 to the solution, this is one of the main components of Baking Soda and will dissolve fast in water.

Keep in mind that this simulation shows the solution in equilibrium with the given partial pressure of CO2. This is the open system solution. 

When measuring in fresh produced solutions or insitu the reaction kinetics need to be considered.

Another resource I can highly recommend to understand the carbonate system is the Hydrochemistry & Water Analysis software and the instructions by  [aqion](https://www.aqion.de/site/71).


In the plot the Electrical Conductivity of the solution is displayed. Keep in mind that it is the electrical conductivity for the given temperature and not the generally used EC corrected to 25°C.
The electrical conductivity however has a very strong temperature dependence as you can see when playing around with the slider.


