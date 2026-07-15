# AeroGap Analyzer

## Overview

A Python tool that analyzes 2025-2026 Bureau of Transportation Statistics (BTS) data to identify unserved airline markets with high passenger demand.

### Why I Built This

I'm an avgeek (aviation enthusiast) and data nerd. While I love to take connecting flights even when nonstop service exists ([not too long ago I flew DFW to ABQ via... ORD](https://my.flightradar24.com/kin_on_a_plane)), I'm also aware that many passengers in the system are forced to connect simply because nonstop options don't exist.

This reality hits me every time I look around the cabin while munching on my obligatory [inflight fruit and cheese plate](https://news.alaskaair.com/alaska-airlines/most-popular-fruit-cheese-platters-national-cheese-day-2021/). I always wonder where the other passengers on my flights connect to or from, especially if a consistent stream of passengers on the same flight all want to reach the same unserved destination, but can't and instead are forced to take [_Tour de O'Hare_](https://www.reddit.com/r/unitedairlines/comments/1uup4bw/first_lap_of_the_ord_500_almost_complete_think_we/) while they connect in Chicago. To me, finding those gaps is true food for thought (although the Tillamook sharp cheddar is also pretty good).

### Key Insights

Running this analysis on airports around the Pacific Northwest, where I'm from, revealed interesting unserved markets I hadn't considered. Without this, I never would've known that the top domestic unserved airport from Boise (BOI) in December 2025 was Honolulu (HNL). During that period, an estimated 1787 passengers, or a daily average just shy of 58 passengers, connected to get to O'ahu.

The difference between a profitable airline and one facing bankruptcy could simply be in network planning. Unserved O&D (origin and destination) pairs like BOI-HNL present significant market opportunities, especially if one end of the route is an airline hub.

As it turns out, one end is! (Kind of.) After [their acquisition of Hawaiian Airlines](https://news.alaskaair.com/company/alaska-airlines-completes-acquisition-of-hawaiian-airlines-expanding-benefits-and-choice-for-travelers/), Alaska effectively now has Honolulu as a hub, and the airline also has a sizable focus city operation out of Boise. They must have seen the same data, because literally the day before I finished upgrading this project, [they announced that they will launch nonstop BOI-HNL flights in December 2026](https://news.alaskaair.com/company/alaska-and-hawaiian-increase-seasonal-hawaii-flying-with-new-honolulu-boise-and-honolulu-spokane-service-along-with-adjustments-to-south-pacific/). (_Daily_ service on a 167-seat Boeing 737 MAX 8 is an... interesting... choice, though.) 

One factor that probably sweetened the pot for Alaska is that the second most popular unserved market from Boise in December 2025 was actually neighboring Kahului (OGG). That means that the airline could seamlessly route Maui-bound passengers through HNL onto Hawaiian metal for the short island hop, helping fill those BOI-HNL flights better.

Of course, network planners evaluate factors beyond demand to justify new routes, such as this route likely cannibalizing loads on their existing BOI-SEA/PDX-HNL flights. I just thought it was cool to see a major airline act on the same unserved market that my analysis found. ✈️

**Try the AeroGap Analyzer out with your home airport to discover where people are going that airlines aren't!**

## Getting Started

Make sure you have Python 3.13 or higher installed.

1. Clone this repository:

```bash
git clone https://github.com/kin027/aerogap.git
cd aerogap
```

2. Create a virtual environment:

```bash
# Create the environment
python -m venv venv

# Activate it:
# On macOS and Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate

# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1
```

3. Install the dependencies (you don't need to download the data tables themselves as I've already included the final ones in the repo):

```bash
pip install -r requirements.txt
```

4. Run the program!

```bash
python main.py
```

## Data Sources

I downloaded data from the Bureau of Transportation Statistics (BTS), a part of the U.S. Department of Transportation. Airlines report their traffic data to the BTS each month.

- [BTS Airline Origin and Destination Survey (DB1C) Market table](https://www.bts.gov/topics/airlines-and-airports/origin-and-destination-survey-data-market) for July 2025 to March 2026 (to get passenger flow data)

- [BTS Air Carrier Statistics (Form 41 Traffic) T-100 Domestic Segment (All Carriers) table](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EEE) for 2025-2026 with DepScheduled, Seats, Origin, Dest, Year, Month, Class fields (to identify airport pairs connected with a nonstop flight)

### Note About the Data

When I first stumbled upon the Bureau of Transportation Statistics (BTS) DB1B data tables, I knew that I just needed to pair them with T-100 tables to identify those unserved markets. I tried to use data from 2025, the most recent full year since I started this, but the tables for the second half were nowhere to be found, so I had to settle for 2024 data.

A bit of digging revealed that DB1B data for the second half of 2025 never existed to begin with. The Biden administration [overhauled airline reporting requirements in 2023](https://www.federalregister.gov/documents/2023/01/31/2022-28535/updates-to-the-origin-destination-survey-of-airline-passengers), and those upgrades went live in July 2025, replacing the DB1B with a newer, more robust table: the DB1C. The new data is so much more comprehensive that mixing it with the old data would skew the results, so I’m using data exclusively from July 2025 onward.

While more data is good for me to play around with, it's probably not good for my machine. Each monthly file would be massive if I saved them as CSVs. Like 6 GB massive. With six months of data here, there was no way I was going to store 36 GB of CSVs on my disk. Luckily, the download link also included an option to save the data as parquets, reducing the total size of the DB1C tables down to 3 GB or 500 MB per monthly file. As that is _still_ too large for GitHub, I have a helper script, DB1C_merger.py, read from each file only five of the [54](https://www.bts.gov/sites/bts.dot.gov/files/DB1C_Description_for_Market.pdf) (!) fields that I need and concatenate them into a final_db1c.csv, which is located in the root folder.

## Libraries Used

- pandas (to analyze the T-100 and DB1C tables)

- plotly (to design the graph)

- dash (to make the graph interactive with the slider)

- pywebview (to open a new window to show the graph in)

- Tkinter (to create the GUI)

- calendar (to convert the month number in each data table to its month name)

- threading (to allow concurrent execution)

## Limitations

- You should probably be cautious with using solely this analysis to determine whether an airline should start new routes because the demand is just one piece of the network planning puzzle.
  - Other factors to consider include fares, seasonality, operational constraints, opportunity cost of sending the aircraft elsewhere, cannibalism of traffic on existing routes, etc.

- Because the DB1C tables track a random 40% ticket sample, all counts are multiplied by 2.5 to approximate total market traffic.

- Routes with an airport outside the U.S. are excluded because the public DB1C tables include only domestic traffic.
  - DB1C tables for international traffic exist but [must be requested from the government](https://www.bts.gov/topics/airlines-and-airports/restricted-data).

## Future Improvement Plans

- ~~Using more recent recent data.~~ (Implemented!)

- ~~Allowing filtering the data by month to highlight seasonality.~~ (Implemented!)

- ~~Showing the airport name upon hover of a bar.~~ (Implemented!)

- Formatting the slider better (e.g. with the tooltip).