# AeroGap

## Overview

A Python tool that analyzes 2025-2026 Bureau of Transportation Statistics (BTS) data to identify top unserved airline O&D (origin & destination) markets with high passenger demand within the U.S.

### Why I Built This

I'm an avgeek (aviation enthusiast) and data nerd. While I love to take connecting flights even when nonstop service exists ([I once flew DFW to ABQ via... ORD](https://my.flightradar24.com/kin_on_a_plane)), I'm also aware that many passengers in the system are forced to connect simply because nonstop options don't exist.

This reality hits me every time I look around the cabin while munching on my obligatory [inflight fruit and cheese plate](https://news.alaskaair.com/alaska-airlines/most-popular-fruit-cheese-platters-national-cheese-day-2021/). I always wonder where the other passengers on my flights connect to or from, especially if a consistent stream of passengers on the same flight all want to reach the same unserved destination, but can't and instead are forced to take [_Tour de O'Hare_](https://www.reddit.com/r/unitedairlines/comments/1uup4bw/first_lap_of_the_ord_500_almost_complete_think_we/) while they connect in Chicago. To me, finding those nonstop service gaps is true food for thought (although the Tillamook sharp cheddar is also pretty good).

### Key Insights

The difference between a profitable airline and one facing bankruptcy could simply be in network planning. Unserved O&D markets may present significant opportunities, especially if one end of the market is an airline hub.

When I ran my analysis on my home airport of Portland (PDX), a rapidly expanding hub for Alaska Airlines, unlike some others for the airline (_cough cough_ SFO), it revealed that two of the top unserved markets from Portland during certain months were Philadelphia and St. Louis. Honestly, I was surprised that we didn't have nonstop service to those cities, but that is no longer the case. I'm guessing the network planners at Alaska knew about this too, because in May 2026, [the airline launched new nonstop flights to Philly and St. Louis](https://news.alaskaair.com/destinations/alaska-airlines-adds-13-new-routes/), so those markets fell off the graph in May.

Of course, network planners evaluate factors beyond demand to justify new routes, but I just thought it was cool to see a major airline act on the same unserved markets that my analysis found. And it's also a great time to be a PDX-based Alaska flyer, of which I am one. (Did I mention those fruit and cheese plates?) ✈️

## Getting Started

Have Python 3.13+ installed on your machine. You do not need to download any data, as I've already included the relevant data in this repo.

```bash
# Clone the repo
git clone https://github.com/kin027/aerogap.git
cd aerogap

# Create the virtual environment
python -m venv venv

# Activate it on macOS and Linux
source venv/bin/activate

# Activate it on Windows (Command Prompt)
venv\Scripts\activate

# Activate it on Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the program
python main.py
```

## Libraries Used

- pandas (to analyze the T-100 and DB1C tables)

- Plotly (to design the graph)

- dash (to make the graph interactive with the slider)

- pywebview (to open a new window to show the graph in)

- Tkinter (to create the GUI)

- threading (to allow concurrent execution)

## Data Sources

- [BTS, Airline Origin and Destination Survey (DB1C), Market](https://www.bts.gov/topics/airlines-and-airports/origin-and-destination-survey-data-market)
  - A 40% sample of airline tickets from reporting carriers reporting origin, destination and other itinerary details of passengers transported
  - Released monthly with a 75-day lag
  - I used data from July 2025 to May 2026

- [BTS, Air Carrier Statistics (Form 41 Traffic), T-100 Domestic Segment (All Carriers)](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EEE)
  - Contains domestic and international airline market and segment data
  - Released monthly with a 2-3 month lag
  - I used data from July 2025 to May 2026

### Note About the Data

When I first stumbled upon the Bureau of Transportation Statistics (BTS) DB1B data tables, I knew that I just needed to pair them with T-100 tables to identify those unserved markets. I tried to use data from 2025, the most recent full year since I started this, but the tables for the second half of the year were nowhere to be found, so I had to settle for 2024 data.

A bit of digging revealed that DB1B data for the second half of 2025 never existed to begin with. The Biden administration [overhauled airline reporting requirements in 2023](https://www.federalregister.gov/documents/2023/01/31/2022-28535/updates-to-the-origin-destination-survey-of-airline-passengers), and those upgrades went live in July 2025, replacing the DB1B with a newer, more robust table: the DB1C. The new data is so much more comprehensive that mixing it with the old data would skew the results, so I’m using data exclusively from July 2025 onward.

While more data is good for me to play around with, it's probably not good for my machine. Each monthly file would be massive if I saved them as CSVs. Like 6 GB massive. With six months of data here, there was no way I was going to store 36 GB of CSVs on my disk. Luckily, the download link also included an option to save the data as parquets, reducing the total size of the DB1C tables down to 3 GB, or 500 MB per monthly file. As that is still too large for GitHub, I have a helper script, DB1C_merger.py, read from each file only seven of the [54](https://www.bts.gov/sites/bts.dot.gov/files/DB1C_Description_for_Market.pdf) (!) columns that I need and concatenate them into a final_db1c.csv, which is located in the root folder.

## Limitations

- Raw demand per se does not justify a new route
  - So you should be cautious with drawing network planning conclusions from this analysis
  - Other factors to consider include fares, seasonality, operational constraints, opportunity cost of sending the aircraft elsewhere, cannibalism of traffic on existing routes, etc.

- While the ticket sample size increased from the DB1B's 10% to the DB1C's 40%, passenger counts are still scaled approximations rather than precise figures
  - So smaller regional routes have wider margins of error (though the increase in sample size was designed to mitigate this)

- The data is not real time
  - So my analysis represents a historical snapshot as opposed to active booking trends

## Future Improvement Plans

- ~~Allowing filtering the data by month to highlight seasonality~~ (Implemented!)

- ~~Showing the airport name upon hover of a bar~~ (Implemented!)

- Formatting the slider better (e.g. with the tooltip)
