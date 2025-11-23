# How to run

From the root directory of the repo run:\
`poetry run visualise --algo <algo> --visualiser <manim/matplotlib> --size <size> --steps <num-steps>`\

The manim video will show up in \
`media/videos/1080p60/GraphColouringAnimation.mp4`\

To run the progression video, install manim locally and run `manim -qm progression.py GraphCreation`\

To run code for jsonl data, run `poetry run visualise --algo colouring --visualiser manim --file <filename>`

The matplotlib animation should show on the screen (idk how to save them)