<h2>MusicPad</h2>
<p>This project ended up being very different from my project proposal. I initially wanted to build
a VOIP app to communicate between devices and then working with the audio I ended up with from that.
After thinking on it some more, I really didn't see a way that I could work directly with the audio if
I were to do that because everything is basically done through libraries. The music pad idea came from
assignment 3 partially because I enjoyed working on the random music generation, but wanted to make it
more interactive.</p>

<p>I had watched a show on apple tv+ called "Watch the Sound With Mark Ronson", and one of the episodes
dedicated a lot of time to the Roland tr-505 and Roland tr-808 synthesizers. It was my favorite 
episode and I wanted to make something kind of similar.</p>

<p>In order to make the app interactive, I wanted to use pygame. Luckily I was able to find
some good resources to get me started. After I was able to attach music to buttons, and turn the buttons
off and on, I started working on adding sounds through sampling. I used the sounddevice library to get
recordings through my macbook, and while it works, the sound quality isn't great. Still, the app is at
the point where one of the instruments can become anything recorded by the user and incorporated into
the audio which I thought was pretty cool.</p>

<p>I wanted to modify the audio to some degree, so the first button I added to do that was to turn
square wave filtering on and off. I ended up creating a second set of audio with the filers applied
and using them whenever the square wave button would be turned on. It took some work, but I got it 
working pretty well. The hard part, was filtering the recorded audio with the square wave filter and 
then going back and forth between the two versions, just like the default music samples. After
spending a lot of time on this, I decided to move on a bit. It's the first thing I will revisit
once I get a chance to work on this project some more.</p>

<p>There are also button to increase and decrease both the number of beats played (default is 8) and
the bpm (default is 240). It's pretty cool getting a looping beat working and then speeding it up or
down with the buttons. Or adding a bunch of beats and making some pretty intricate sound samples.</p>

<h3>Sources:</h3>
<p>

https://simpleaudio.readthedocs.io/en/latest/

https://www.youtube.com/watch?v=F3J3PZj0zi0

https://stackoverflow.com/questions/16778878/python-write-a-wav-file-into-numpy-float-array

https://numpy.org/doc/stable/reference/generated/numpy.convolve.html

https://medium.com/the-seekers-project/coding-a-basic-reverb-algorithm-an-introduction-to-audio-programming-d5d90ad58bde




</p>