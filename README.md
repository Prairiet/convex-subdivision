# Convex Subdivision
Computer Geometry Project

# Installation
Simply run this to quickly install all requirements.
Setting up a Python environment is recommended.

If you don't want to create an environment, skip this step. Otherwise, run the following code:

`python -m venv [ENVIRONMENT NAME]`

Then install all requirements:

`pip install -r requirements.txt`

Now you should be able to run the program.

## The Problem
Subdivide any simple polygon down to as few convex polygons as possible.

## The Approach
A simple way to achieve this is through a triangulation algorithm, such as the ear-trimming algorithm. This is the baseline.

This project's approaches builds off of said algorithm by finding and removing unneeded edges. The first is a simple rule of thumb, while the other works similarly to a flood fill algorithm.

## The Result
Without increasing time complexity nor space complexity, on 100 each of randomly generated 20-gons, 50-gons, and 100-gons, the flood-style algorithm uses approximately 40% less edges and thus creates 40% less sub-polygons than the baseline.