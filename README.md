# Recommender-Systems-Coursework

Develop a context-aware recommender system (CARS) music application. Material for Web Technologies can be re-used. 

### Context

A context is "any information useful to characterise the situation of an entity (e.g. a user or an item) that can affect
the way users interact with systems" (Abowd et al., 1999). It is a set of factors that delineate conditions under which 
a user-item pair is assigned a rating. 

There are four types of context:
* Physical: time, position, user's activity, weather, light, temperature
* Social: presence and role of other people around
* Interaction media: device used, type of media browsed
* Modal: user's mood, personality, purpose

### Datasets

Potential datasets:
* [MusicMicro](http://www.cp.jku.at/datasets/musicmicro/index.html)
* [FMA](https://archive.ics.uci.edu/ml/datasets/FMA%3A+A+Dataset+For+Music+Analysis)
* [#nowplaying-RS](https://zenodo.org/record/3248543#.XlelyG52vxB)

As MusicMicro is the simplest, I have used that one. As the dataset is rather limited, using the physical context is my
only option.

### Task

Research, select, justify, and apply to your system techniques for:
* Feature extraction and selection (consider user data, item data, and context)
* 2D / MD recommender techniue (user profiling/modelling)
* Contextual recommendation generation: contextual information filtering / modelling (e.g. pre- or post-filtering, neural collaborative filtering)

UI: develop a simple UI for your application. This can be a Python script. Showcase:
* how does the system recognise the active user? Which user data is gathered - explicit / implicit?
* Output: how are recommendations and/or predictions presented to the user?

### Geolocation

Location data is automatically retrieved from IP address using [ipinfo.io](https://ipinfo.io/developers).

### Resources

* Tutorial on mood [here](https://neokt.github.io/projects/audio-music-mood-classification/)
* Cutting-edge paper [here](https://arxiv.org/abs/1909.03999)
* Presentation [here](https://www.slideshare.net/irecsys/tutorial-context-in-recommender-systems)
