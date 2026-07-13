# AeroGap Analyzer

## Overview

A Python tool that analyzes 2024 Bureau of Transportation Statistics (BTS) data to identify unserved airline markets with high passenger demand.

### Why I Built This

I'm an avgeek (aviation enthusiast) and data nerd. While I love to take connecting flights even when nonstop service exists ([not too long ago I flew from DFW to ABQ via... ORD!](https://my.flightradar24.com/kin_on_a_plane)), I'm also aware that many passengers are required to connect because no nonstop option is available for them.

As a result, each time I get on a plane and munch on Biscoff cookies, I always wonder where everyone else on my flight connects to or from. That curiosity led me to find the tables I used for this (linked below) and identify unserved markets from the airports I frequent.

### Key Insights

Running this analysis on my frequented airports revealed interesting unserved markets I hadn't considered. Without this, I never would've known that the top unserved airport from PDX (Portland, OR) is MSY (New Orleans). In 2024, over 39,000 passengers had to connect to reach the Big Easy.

The difference between a profitable airline and one facing bankruptcy could simply be in network planning. Unserved O&D (origin and destination) pairs like PDX-MSY present significant market opportunities, especially if one end of the route is an airline hub.

As it turns out, one end is! Alaska Airlines makes PDX a hub, and they must have seen the same data because they [launched service between PDX and MSY in January 2025](https://news.alaskaair.com/loyalty/alaska-airlines-launches-seasonal-daily-flight-between-portland-and-new-orleans/). Of course, network planners look at factors beyond demand to justify new routes, but I just thought it was cool to see a major airline act on the same unserved market that my analysis found. ✈️

**Try the AeroGap Analyzer out with your home airport to discover where people are going that airlines aren't!**

## Getting Started

Make sure you have Python 3.13 or higher installed.

Note for Linux users: You may need to install Tkinter manually if it isn't included in your distro's default Python package:

```bash
sudo apt-get install python3-tk
```

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

- [BTS Airline Origin and Destination Survey (DB1B) Market table](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFI&Yv0x=D) for quarters 1-4 of 2024 (to get passenger flow data)

- [BTS Air Carrier Statistics (Form 41 Traffic) - All Carriers (T-100) table](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EEE) for all of 2024 with DepScheduled, Passengers, UniqueCarrierName, Origin, Dest, Year, Class fields (to identify airport pairs connected with a nonstop flight)

## Libraries Used

- pandas (to analyze the T-100 and DB1B tables)

- Matplotlib (to create the bar graph)

- Tkinter (to create the GUI)

## Limitations

Obviously there are some limitations that come out of analyzing only two datasets:

- You should probably be cautious with using solely this analysis to determine whether an airline should start new routes because the demand is just one piece of the network planning puzzle.
  - Other factors to consider include fares, seasonality, operational constraints, aircraft availability, etc.

- In the context of the fast-paced industry, the 2024 data used here is kind of old.
  - 2025 data is available, [but in July of that year, the DB1B was replaced by the DB1C, which has more detailed data that I will implement later](https://www.federalregister.gov/documents/2023/01/31/2022-28535/updates-to-the-origin-destination-survey-of-airline-passengers).

- The exact passenger count is unknown because the DB1B tables are only a random 10% sample of tickets, so DB1B counts are multiplied by 10 to approximate the actual count.
- Routes with an airport outside the U.S. are excluded because the DB1B tables only have American airports.

- City pairs with seasonal flights are excluded because they will show up in the T-100 at some point for the year, even if flights are not operated during every month.

## Future Improvement Plans

- Using 2025 data.

- Moving the graph to plotly.

- Filtering the data by month to highlight seasonality.

- Showing the airport name upon hover of a bar.
