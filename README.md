docker build -t python-container .

docker run -it --rm -v /Users/gavinkd/repos/yt-audio:/var python-container

The commands above:
	•	Builds a new Docker image named python-container from the current directory.
	•	Runs a new container based on that image and names it python-container-instance.
	•	Opens a bash shell inside the newly created container for you to interact with it.

You can run this command after you clone repo to start cli app