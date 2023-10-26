# HeriTours

HeriTours is a web-based mobile app for exploring NSW local heritage.

Nothing in our demo is fake! Everything you see is real and implemented!

## Screenshots

Some sample screenshots:

![Home](1.png)

![Map](2.png)

![Citizen Science](3.png)

# This Repo

## Installation Instructions

See README.md in app/

## Security 

Note that this project has not been audited for security. Please use at your own risk.

## The Technology details

*Front-end:*

- A web-based mobile front-end written in TypeScript using React, Zustand and Emotion.
- Leaflet for map visualizations.
- HTML5 Geolocation API for live position updates
- Fetch API for requests
- Fetch insights from a dashboard hosted on Tableau public, a free platform

*Back-end:*
- A Python-based server written using FastAPI and Pydantic
- An SQLite3 database to store user responses
- Dashboards designed and served by Tableau Public
- Custom shortest-path planning logic for creating a tour
- Full text search using TF-IDF based vectors from Scikit-learn

*Data-science:*
- Data manipulation using geopandas, pandas, scikit-learn
- Clues generated using free credits on OpenAI

*Data:*
- 2021 ABS Census
- NSW State Heritage Register Centroids
- NSW State Heritage Inventory
- Historic Heritage Information Management System (HHIMS)


# Submission Information

## Problem

We wish to help NSW Heritage, NSW Citizens and Future Generations. We started with the following challenges:

- Even though heritage surrounds us, they're often hidden from our awareness. Citizens have stories of heritage that aren't shared or public.
- Our citizens and communities feel a lack of connection with other, without realising the remarkable common history that we share and can celebrate.
- Heritage demands constant protection and care. Without care, there is danger that those items will be lost to future generations. We have so much valuable heritage in our state, and managing this heritage requires the involvement and participation of every citizen - in caring for the heritage items, as well as curating the data about the items.

## Solution

We started with the idea that we wanted to build a tool that we, and our families and colleagues, would actually want to use. The key insight we learned is that we often don't understand the heritage that surrounds us. So, our solution is to expose this through an engaging mobile app.

The solution is a web-based mobile app that uses your location, as well as your interests to instantly generate **engaging tours personalised to you!**. 

The app is fully functional. It will adapt to any location in the state, and it uses the NSW Heritage list. Once deployed, it saves user insights to a local database that can be fed back into the work of Heritage NSW. The application could be easily extended to a more complete heritage collection (World, National, State and Local).


## Data Story

We began with the NSW State Heritage Items on the NSW SEED initiative website. We structured our analysis around the 1700+ centroid data points of state heritage items. Some data manipulation was required, including translation of the coordinate system into WGS-84 for use in the app.

We connected these items to the detailed heritage information and significance statements on the NSW State Heritage Inventory Map - we retrieved the data on each of the items in the register.

Since heritage statements appear to be written for a more technical audience, we used Generative AI (OpenAI free credits) to translate the descriptions into engaging and provocative questions to give users the sense of a playful treasure hunt. 

Data manipulation also occurs during user interaction. When the user performs a search, the NSW State Heritage items are sorted and ranked based on the search similarity and the distance from the user. A shortlist of 'tour stops' is generated, then the app searches for an optimal route to visit each of the sites in the least amount of time.

Local insights were used in the application to generate interest and engagement. The sources of the local insights were:

- 2021 ABS census data: country of birth and indigenous status data were summarised by LGA and displayed based on the LGA of the heritage item / site selected by the user
- Historic Heritage Information Management System: the status of heritage sites and items (e.g. SHR listing, section 170 listing) was summarised by LGA and displayed based on the LGA of the heritage item / site selected by the user

## End User Experience

HeriTours creates heritage themed tours for users of the app generating engagement and interest with heritage items in New South Wales.

At the home page, users are presented with a search box and a list of predefined tours:

- The "Local Surprises" tour is created from the nearest 10 heritage items, the other tours are automatically generated based on the theme and your current location.
- The search bar allows users to enter a query to search the entire heritage register. Users might enter terms like "bridge", "dam", "trade union", place names, people: any terms that appear in the heritage register.

When the user selects a tour or enters a query, the server will generate a customised tour. This is then shown on a map, as a series of connected markers (and an additional marker with the current location). Every stop has an associated "fun" clue to entice the user to visit the site. For example, the Macquarie Lighthouse Site is represented by the clue ""What is the oldest continuously operating navigational beacon site in Australia?".

Users can click on a site to learn more:

- The can see the NSW Heritage data
- They can understand how the site connects to the local community by understanding demographics of the local area
- They can contribute, as citizen scientists to the story-telling and conservation surrounding the site ("Your Stories")


The latter - "Your Stories" - provides a fun and engaging way for the public to engage with the heritage item.

The public can vote on the site: to develop rankings and insights into popularity.

The Heritage department can configure citizen-science and monitoring questions in the app to efficiently monitor the site. This can assist with preservation and conservation activity, as well as a way of efficiently crowd-sourcing insights to improve data about the site. Three sample questions are included, but these could include even complex tasks such as attempting to identify whether archival photographs match the site. Users may collect points for assisting with heritage.


Finally the public can share their stories about each site, and see the stories of others. This may not only increase community engagement but also provide a tool for historians and engaged members of the public to uncover hidden or previously lost stories about our local history.


## Next Steps

Future developments to the application aim to improve user experience, through:

- A chatbot assistant provide rapid responses to questions that users may have
- Incorporating an end-to-end public transport trip plan so users can enjoy a trip end-to-end using public transport and active travel
- Allowing users to share photos and videos alongside their stories
- Showcasing upcoming heritage events related to the tour themes
- A system of points and badges to encourage the public and schoolchildren to compete in learning about history
- Increasingly compelling games, similar to Pokemon Go (e.g., Heritage Go?)
- Incorporating archival photos from State Library and other sources
