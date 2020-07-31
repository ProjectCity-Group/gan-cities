# Contributions Log

## Thomas Allen (Project Lead, Main City Generator)

After the project was approved, I spent a good chunk of time researching the different approaches available. I reviewed the papers written on GANs, Wasserstein-GANS, and Deep Convolutional GANs. I decided to try a simple GAN that had been proven to work on pictures of everyday objects, and see if the results warranted a more complex model.

Since Christopher was still working on data collection for real maps, I used [ProbableTrain's MapGenerator](https://github.com/ProbableTrain/MapGenerator) to generate roughly 80,000 procedurally generated maps.

With the first set of data, I began training, but the GAN would always fail to converge or enter mode collapse. Nothing seemed to be able to improve training, despite various modifications to the model.

I suspected a problem with the learning gradient, and so tried implementing a model based on the [Wasserstein GAN (WGAN)](https://arxiv.org/abs/1701.07875) as well as [WGAN with a gradient penalty](https://arxiv.org/abs/1704.00028), but those models
encountered the same problems as the initial one - they would invariably suffer from mode collapse or simply fail to converge.

Doing more research, it seemed that GANs in general have [trouble with images that are not noisy](https://www.gwern.net/Faces#why-dont-gans-work). That is they work when trained on pictures of faces and objects, where color
changes across the picture are gradual instead of abrupt (as in maps). The best candidate that had proven itself to be useful in training images with large areas of the same
color was Nvidia's StyleGAN.

Due to time constraints, I ended up training using Nvidia's StyleGAN2 model instead of replicating it. The training took 5 days in total. On a side note, this was the major
challenge with my portion of the project - the large amount of time needed to train a network to determine whether or not it was working. The initial GAN models I prototyped
would often train for up to 8 hours before undergoing mode collapse.

The remaining time on the project was spent compiling everything and determining library version requirements, as there were a lot of incompatibilities present. In addition,
I ended up having to make changes to Nvidia's dnnlib code to allow tensorflow to run on linux.

## Christopher Ward (City Map Data Collection)
​
I have had previous experience with scraping data off websites using Python, so I figured I'd be best suited for data collection within this project. Previously I was scraping YouTube meta-data through the Youtube-api so I still was entering new territory with trying to collect map images. There is no pre-existing api for the SnazzyMaps website, the source of all of the label-less map images, so I had to get creative and figure out what my options were.
​
### What I did
​
It took an extended period of trial and error, but I was able to remotely interact with the onsite elements through a Selenium chrome-based webdriver. I would send requests through the embedded google map element and screenshot the displayed results once the page loaded up. I had a dataset of ~20,000 cities and automated the map screenshot, cropping and eventually filtering process. The automation process started on  **6/17/2020** and finished around **7/1/2020**, while filtering was worked on from **7/1/2020** till the conclusion of the project around **7/31/2020**
​
Filtering was focused on removing poor quality map data, examples include: open ocean, barren land, singular highways, or most of the city being cropped out of frame. This process was done by looking at the file size of each image, as you increase the file size, image complexity increases, with the maximum 500kb images having complex urban roadways in cities such as Hong Kong, New York, and Mumbai. For the GAN we submitted the lower cutoff point is approximately 50kb, which is at minimum some road systems, perhaps intersperced with parkland or bodies of water. Ideally future modifications to the dataset and filters would be able to get higher quality images of 100kb or 150kb, which are almost guaranteed to be more complex transit maps. 
​
### Challenges
​
One problem that I delt with for a while was removing all of the advertisements on screen, my first iterations had issues where removing an advertisement would break the zoom-in feature. I narrowed down the problem to how the site organizes elements by their xpath and was able to put in a fix.
​
Another issue that I encountered but was unable to optimize completely was the speed at which I'm able to record data. The biggest bottleneck had to do with the speed at which the map could load. I had to place wait functions in my code in order to give each map location time to load. There are two waits 3 seconds in length intended for loading purposes, the first is for allowing google maps to return recommended map locations and the second is waiting for the map image themselves to load. On top of this, there's an additional 1 second wait needed to take a screenshot. This means that at minimum, each location takes 7 seconds to document. Obviously when dealing with a dataset size of ~20,000 cities it takes a very long time to document all of them, and I've broken the proces over multiple days, but I still have a lot of entries left. Thankfully I was able to get 40,000+ high quality images needed for our GAN.

## Eric Lehmann (User Interface)

At the start of the project, I had never created a functional GUI before. As other members of the team seem to want some basic graphical functionality, but were interested in other areas such as creating the models and scraping maps for training data, I volunteered early on to focus on our GUI interface. My initial work was identifying the right toolkit and python package to complete our work in. After discussing the results of my research with the team, a group decision was reached to work with PyGObject. This was decided on 6/17/2020

The initial request was for model selection to occur through a combobox, and have relevant widgets appear for each model i.e. pix2pix requires a "Load PNG" functionality that is unused for CityGan. I had difficulty in getting PyGObject to keep UI elements that were not onscreen utilizing this method, and it was later dropped in favor of utilizing a Notebook tabbed interface.
The initial scope of the project was described to include paramaters for the output from the models. Appropriate widgets to tweak these paramaters were developed and later discarded as these parameters did not make it into the final iteration of the project. This significant work is reflected in f759e990741fb3a93849e7a31f9bf9e5e460eea4 and in the preliminary_ui.png available in screenshots directory. This work was completed between 6/17/2020 and 7/1/2020.
As the project neared it's final released, I worked to finalize the GUI, properly implement multithreading, and accomadate for additional features under development by other team members, such as implementing the drawing functionality for pix2pix).


## Jacob Roberge (Pix2Pix GAN)

For the first group meeting I volunteered to work on the machine learning aspect of the project. I have never creating a machine learning model before this project and because of that I required multiple weeks to learn the basics of machine learning. Initially I was planning on working with Thomas to develop a randomly map generator using GAN. During my research I learned about Pix2Pix GAN and shared that research with the team. After some discussion the team decided to create two models one for Pix2Pix and another GAN model.

​
After I thought I had a basic grasp of machine learning I sought out a machine learning library. I thought Keras would be perfect as it was simple and easy to use. Then after depressingly learning that my once powerful gaming rig would not be sufficient for training a machine learning model I looked into using a remote machine. I first started using a service called Paperspace for my training with a cost of around 50 cents per hour. After learning about how Colab was a free alternative I transferred to using it instead.

​
Thomas was able to provide me with a test dataset that he made using a procedural map generator. I made a small Opencv program to make input maps from the original maps. These input maps consisted of white roads with a black background. After figuring out how to load in the dataset I was pleasantly surprised that the Pix2Pix model worked well for this application. Using only an hour to train the dataset a workable model was created.

​
Then I worked on the API to interface with my model alongside saving and loading functionality. After that I worked on some bug fixes with loading the model and passing a numpy array to the GUI. Following this I created markdown documentation for the framework using Sphinx.

​
After the midterm presentation I worked on shaping the dataset from Christopher to be better conducive to training a Pix2Pix model. First I needed to fill the roads in using opencv morphological transformations since the roads were two different colors. After training a test model using 2000 images I found that the model was only changing the colors of the background and roads. To make the model more interesting I made an algorithm that took 5000 images from Christopher’s provided 45,982 images based on having yellow roads, water, and parks.

## Adrian Wright (Fantasy Map Data Collection)
​
**6/21/2020**
First I began with attempting to build the original code from https://github.com/watabou/TownGeneratorOS. Haxe boasts that all source written in Haxe can be source-to-source converted to python. After struggling with Haxe and reading up on how to use it I was able to translate classes that didn't use openfl. This was generated on **6/26/2020**.
​
```
# Generated by Haxe 4.1.2
# coding: utf-8
import sys
class com_watabou_geom_Circle:
    __slots__ = ("x", "y", "r")
    def __init__(self,x = None,y = None,r = None):
        if (x is None):
            x = 0
        if (y is None):
            y = 0
        if (r is None):
            r = 0
        self.x = x
        self.y = y
        self.r = r
class haxe_iterators_ArrayIterator:
    __slots__ = ("array", "current")
    def __init__(self,array):
        self.current = 0
        self.array = array
    def hasNext(self):
        return (self.current < len(self.array))
    def next(self):
        def _hx_local_3():
            def _hx_local_2():
                _hx_local_0 = self
                _hx_local_1 = _hx_local_0.current
                _hx_local_0.current = (_hx_local_1 + 1)
                return _hx_local_1
            return python_internal_ArrayImpl._get(self.array, _hx_local_2())
        return _hx_local_3()
class python_internal_ArrayImpl:
    __slots__ = ()
    @staticmethod
    def _get(x,idx):
        if ((idx > -1) and ((idx < len(x)))):
            return x[idx]
        else:
            return None
class python_internal_MethodClosure:
    __slots__ = ("obj", "func")
    def __init__(self,obj,func):
        self.obj = obj
        self.func = func
    def __call__(self,*args):
        return self.func(self.obj,*args)
```
​
This makes a circle object from the original Haxe.
​
```
package com.watabou.geom;
class Circle {
	public var x	: Float;
	public var y	: Float;
	public var r	: Float;
	public function new( x:Float=0, y:Float=0, r:Float=0 ) {
		this.x = x;
		this.y = y;
		this.r = r;
	}
}
```
`/usr/share/haxe/std/sys/thread/Deque.hx:26: characters 8-52 : This class is not available on this target`
_Not sure why it's calling a deque, at this point I just want the model and its counterparts turned into python. I really wish Haxe could build into python, or anything really source-to-source as they claim but it's still just as good as any other recompiler. It's disappointing really._
​
https://lib.haxe.org/t/python/
http://www.openfl.org/learn/haxelib/tutorials/
https://haxe.org/manual/target-cpp-file-format.html
https://haxe.org/manual/target-syntax.html
https://www.reddit.com/r/Python/comments/24j43h/haxe_can_now_generate_python/
​
After learning all I could about Haxe source-to-source I had begun to realize that the code may never be turned into python. https://haxe.org/documentation/introduction/compiler-targets.html was my main guide, but after countless hours lost to reading and searching for anything I could find on the recompilation of Haxe I found that all I really needed was the images of the maps so I wrote a scraper for the public site and gathered my 1000 samples to train **6/30/2020**. I then began learning more about the training process and, with the group, concluded that a version of the site would need to be run that made maps but without the labels, buttons, and compass. Looking at the Haxe the removal of those features was easy. However getting the original repository to build turned out to be a popular issue. The main issue ended up being the fact that specific versions of some libraries are needed to run the server. Now armed with https://github.com/grandemk/TownGeneratorOS, I set off attempting to get it to build as is.
**7/10/2020**
```
Source/com/watabou/towngenerator/mapping/PatchView.hx:26: characters 52-62 : Unknown identifier : onRollOver
Source/com/watabou/towngenerator/mapping/PatchView.hx:26: characters 52-62 : For function argument 'listener'
Source/com/watabou/towngenerator/wards/Ward.hx:96: characters 85-97 : Not enough arguments, expected min:Int, max:Int
Source/com/watabou/towngenerator/wards/Ward.hx:96: characters 81-97 : Void should be Int
Source/com/watabou/towngenerator/wards/Ward.hx:96: characters 81-97 : For function argument 'x'
```
This was the first time I got the code to build at all, and it was apparently full of bugs that couldn't be resolved. After spending days reading tutorials on Haxe and documentation.
​
https://haxe.org/documentation/introduction/building-haxe.html
https://haxe.org/videos/tutorials/haxe-examples/how-to-setup-openfl-and-compile-haxe-for-ios.html
https://lib.haxe.org/p/openfl/
https://lib.haxe.org/p/lime/
https://haxe.org/manual/compiler-usage-hxml.html
​
During this time fellow teammates also attempted to build/run/recompile the code, all reaching the same pitfalls I was meeting.
​
**7/19/2020**
I finally gave up on getting it to run at all, instead I set my sights on helping out with the GUI, finally a chance to work in python for something that will end up in the final release. We then lost AC for multiple days, internet the others, I had to watch my younger brother more and my other classes had work that needed to get done so I placed the project on a back burner for a week.
**7/23/2020**
After trying to get gtk installed on my wsl I realized a VM would be needed. I can't use hyper-v so I downloaded virtualbox, all throughout High School I had worked in virtual environments learning Information Systems stuff from our technical college component. This time however I was meet with the most and widest array of issues installing the VM. After trying as many configs I could think of, my team recommended torrenting the iso because it worked for them. It was a better idea than anything I had so I started. I then caught a virus that took 10 hours to regain control of my computer and get back to working order.
```
Adrian Wright  2:48 AM
the  torrent gave me a virus , keyboard  not working . fixing now
2:49
****
2:50
quick driver updater auto installed , keyboard  not inputting
2:51
using malwarebytes now
```
I then tried importing a teammates .OVA to see if I could get the VM to start. Yet again, another failure. I have yet to get a VM to run on this machine and now code using an IDE to catch any errors, pushing to remote so my teammates can run my code.
