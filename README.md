# Lambda Engine
A pygame game engine written in python

## Engine Notes:

**Scriptable Objects**
- Note that all initScripts (Scripts attatched to gameObjects that run on initialization), and runtimeScripts (Scripts attatched to gameObjects that run during runtime) must include "self" as their first dependancy to achieve proper functionality and not include any other dependencies, this means that all outside / input variables used in these functions must use global variables. (This also applies to initScripts and runtimeScripts for the camera and other objects with these variables)

**Routines**
- This engine includes a system for routines, which allow for functions to be run across multiple frames
- All routines must be run through a routineManager, which must be updated once per frame
- Any function to be used as a routine must have dependancy, currentFrame (currentFrame must be an integer)