# AeroGap Analyzer

## Overview

A Python tool that analyzes 2024 Bureau of Transportation Statistics (BTS) data to identify unserved airline markets with high passenger demand.

### Why I Built This

I'm an avgeek (aviation enthusiast) and data nerd. While I love to take connecting flights even when nonstop service exists ([not too long ago I flew from DFW to ABQ via... ORD!](https://my.flightradar24.com/kin_on_a_plane)), I'm also aware that many passengers are required to connect because no nonstop option was available for them.

As a result, each time I step onboard another plane, I always wonder where the other passengers connect to or from. That curiosity drove me to build this tool and explore unserved markets from the airports I frequent.

### Key Insights

Running this analysis on my frequented airports revealed interesting unserved markets I hadn't considered. Without this, I never would've known that the top unserved airport from PDX (Portland, OR) is MSY (New Orleans). In 2024, over 39,000 passengers had to connect to reach the Big Easy. 

The difference between a profitable airline and one facing bankruptcy could simply be in network planning. Unserved O/D (origin/destination) pairs like PDX-MSY present significant market opportunities, especially if one end of the route is an airline hub.

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
3. Install the dependencies (you don't need to download the datasets themselves as I've already included the final ones in the repo):
```bash
pip install -r requirements.txt
```
4. Run the program!
```bash
python main.py
```

## Data Sources

I got data from the Bureau of Transportation Statistics (BTS), a part of the U.S. Department of Transportation. Airlines report their traffic data to the BTS each month.

- [BTS DB1B Market table for quarters 1-4 of 2024](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EFI&Yv0x=D) (to get passenger flow data)

- [BTS T-100 Segment (All Carriers) table for all of 2024](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EEE) with DepScheduled, Passengers, UniqueCarrierName, Origin, Dest, Year, Class fields (to identify airport pairs connected with a nonstop flight)

## Libraries Used

- pandas (to analyze the T-100 and DB1B tables)

- Matplotlib (to create the bar graph)

- Tkinter (to create the GUI)

## Limitations

Obviously there are some limitations that come out of analyzing only two datasets:

- You should probably be cautious with using solely this analysis to determine whether an airline should start new routes because the demand is just one piece of the network planning puzzle.
  - Other factors to consider include fares, seasonality, operational constraints, aircraft availability, etc.

- The data is not real-time; it comes from BTS data tables that the government releases only once a quarter (with a six-month delay).
  - 2024 data is analyzed because that is the most recent year with a full year of data.

- The exact passenger count is unknown because the DB1B tables are only a random 10% sample of tickets, so DB1B counts are multiplied by 10 to approximate the actual count.
    
- Routes with an airport outside the U.S. are excluded because the DB1B tables only have American airports.

- City pairs with seasonal flights are excluded because they will show up in the T-100 at some point for the year, even if flights are not operated during every month.