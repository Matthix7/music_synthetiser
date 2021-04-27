# music_synthetiser
A Python3 program that allows you to play music without anything else than a computer. Keyboard and sounds are fully customisable, feel free to share improvements and new instruments !

## Instruments
For now, instruments (ie harmonics played) available are :
 - diapason (only pure note)
 - carillon (sounds like bells)
 - accordion (based on a record of my own accordion, but might be improved)
 - custom_synthetiser (a set of harmonics that I like)

## Configurations
For now, only one keyboard can be used for playing music.
Two (AZERTY) configurations are currently available, both with an *accordion-style* buttons layout:
 - single  
![single](https://github.com/Matthix7/music_synthetiser/blob/master/doc/single_accordion_keyboard.png)
 - double  
![double](https://github.com/Matthix7/music_synthetiser/blob/master/doc/double_accordion_keyboard.png)



## Playing Music
### On Ubuntu
 - Open a terminal
 - Install the requirements : `sudo apt update && pip install pynput && python3 -m pip install sounddevice`
 - Got into folder `Music_Scripts`
 - Type `python3 my_accordion.py`
 - Have fun !
 - To stop, press `Escape` or `Ctrl+C`.  
*Note : you can change the instrument and the keyboard configuration in the bottom lines of `my_accordion.py`.*
 
 
 ## Customising the code
 ### Keyboard configuration
 You can create new configuration by creating new files following the template of `double_keyboard.py`.  
 Don't forget to include them on top of `my_accordion.py`. Bottom lines of `__init__` method of class `Accordion` should be modified too in order to use the new configurations.
 
 ### New instruments
 An instrument is defined by a set of harmonics. These are written in method `get_harmonics` of `my_accordion.py`.
 The fundamental is not written (this is why the list of harmonics for *diapason* is empty). All others are expressed as tuples:
  - First component of each tuple is the ratio `harmonic_frequency/fundamental_frequency`. 
  - Second component is the ratio `harmonic_amplitude/fundamental_amplitude`. Therefore, all is normalised.  
  
 *Sound library* lines `__init__` method of class `Accordion` should be modified too in order to use the new instruments. You should also change your instruments dynamics here : 
  - instrument.crescendo_duration is about 1/3 of the duration the button has to be pushed for the note to reach standard volume.
  - instrument.decrescendo_duration is about 1/3 of the duration the button has to be released for the note to go down to silence.
 
 
 
 
 
