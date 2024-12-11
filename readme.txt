# Author: Daniel Glauber
# File: readme.txt

To run program run the command: python3 sga.py [-h] [-g] [-G] [settings file].
I added additional settings terminateOnFailure and failuresBeforeTermination.
The setting terminateOnFailure allows the user to turn off the termination failsafe mode.
By default terminateOnFailure is set to 1, which means the termination failsafe is on.
To turn off the termination failsafe set terminateOnFailure to 0.
The setting failuresBeforeTermination allows the user to change failures can occur before the program terminates.
By default failuresBeforeTermination is set to 0, which means the program will terminate after the first failure.
To allow multiple failures before termination you can set failuresBeforeTermination to an integer greater than 0.
If failuresBeforeTermination is set to 1, then 1 failure is allowed before the program terminates.
If the default settings file is not found the program will create the file gasettings.dat, which contains the default settings.
If the user's custom settings file is missing a setting or if a setting's value is formatted incorrectly, the user will be asked if they want to continue running the program using the default settings value for the missing setting. 


Conclusions from Experiments:
My program was unable to determine the the actual minimum population size for a string size of 1000000.
The amount of memory that is required to run the program with a string size of 1000000 is greater than my systems total memory.
This is mainly due to how I am storing the solution string. I am storing the solution string as a list of integers of length string size.
In python a single integer has a size of 32bits. This means to run the program with a string size of 1000000 the memory required for a single solution is 4Mb.
Which means the amount of memory required to store all the solutions for the entire population is 4Mb * 107517 = 430Gb.
I could use the numpy library, to reduce the memory required to store a single integer to 8bits, which would reduce the total memory required for the entire population to 1Mb * 107517 = 107.5Gb.
I did not end up using the numpy library, because it is not install on the school's server.      
When the results of the Experiments are plotted on on a graph, with String Size along the x-axis and Population Size along the y-axis, the data follows a power distribution.
The equation for the trendline of the plotted data is f(min population size) = 0.9806(string size)^0.8351
The plotted data closely follows the trendline, since the the R^2 value for the regression equation is within 0.7% of 1.0.
Based on the trendline equation, the minimum population needed for a string size of 100 is 46. 
I determined the actual minimum population size for a string size of 100 to be 49, so my calculated minimum population size is off by about 7%.
Based on the trendline equation, the minimum population needed for a string size of 1000000 is 100483. 
If the calculated minimum population size for a string size of 1000000 is also off by about 7%, then the minimum population needed for a string size of 1000000 is closer to 107517.


Results from Experiments:
"populationSizeN": 7,
"stringSizeN": 20

"populationSizeN": 8,
"stringSizeN": 30

"populationSizeN": 24,
"stringSizeN": 40

"populationSizeN": 34,
"stringSizeN": 50

"populationSizeN": 40,
"stringSizeN": 60

"populationSizeN": 42,
"stringSizeN": 70

"populationSizeN": 46,
"stringSizeN": 80

"populationSizeN": 47,
"stringSizeN": 90

"populationSizeN": 49,
"stringSizeN": 100

"populationSizeN": 54,
"stringSizeN": 110

"populationSizeN": 59,
"stringSizeN": 120

"populationSizeN": 63,
"stringSizeN": 130

"populationSizeN": 66,
"stringSizeN": 140

"populationSizeN": 68,
"stringSizeN": 150

"populationSizeN": 74,
"stringSizeN": 160

"populationSizeN": 77,
"stringSizeN": 170

"populationSizeN": 78,
"stringSizeN": 180

"populationSizeN": 79,
"stringSizeN": 190

"populationSizeN": 86,
"stringSizeN": 200

"populationSizeN": 94,
"stringSizeN": 210

"populationSizeN": 96,
"stringSizeN": 220

"populationSizeN": 99,
"stringSizeN": 230

"populationSizeN": 101,
"stringSizeN": 240

"populationSizeN": 105,
"stringSizeN": 250

"populationSizeN": 108,
"stringSizeN": 260

"populationSizeN": 109,
"stringSizeN": 270

"populationSizeN": 110,
"stringSizeN": 280

"populationSizeN": 113,
"stringSizeN": 290

"populationSizeN": 119,
"stringSizeN": 300

"populationSizeN": 121,
"stringSizeN": 310

"populationSizeN": 122,
"stringSizeN": 320

"populationSizeN": 124,
"stringSizeN": 330

"populationSizeN": 127,
"stringSizeN": 340

"populationSizeN": 129,
"stringSizeN": 350

"populationSizeN": 130,
"stringSizeN": 360

"populationSizeN": 133,
"stringSizeN": 370

"populationSizeN": 135,
"stringSizeN": 380

"populationSizeN": 136,
"stringSizeN": 390

"populationSizeN": 138,
"stringSizeN": 400

"populationSizeN": 142,
"stringSizeN": 410

"populationSizeN": 147,
"stringSizeN": 420

"populationSizeN": 148,
"stringSizeN": 430

"populationSizeN": 149,
"stringSizeN": 440

"populationSizeN": 155,
"stringSizeN": 450

"populationSizeN": 156,
"stringSizeN": 460

"populationSizeN": 160,
"stringSizeN": 470

"populationSizeN": 162,
"stringSizeN": 480

"populationSizeN": 163,
"stringSizeN": 490

"populationSizeN": 168,
"stringSizeN": 500

"populationSizeN": 171,
"stringSizeN": 510

"populationSizeN": 174,
"stringSizeN": 520

"populationSizeN": 177,
"stringSizeN": 530

"populationSizeN": 178,
"stringSizeN": 540

"populationSizeN": 182,
"stringSizeN": 550

"populationSizeN": 184,
"stringSizeN": 560

"populationSizeN": 185,
"stringSizeN": 570

"populationSizeN": 188,
"stringSizeN": 580

"populationSizeN": 189,
"stringSizeN": 590

"populationSizeN": 191,
"stringSizeN": 600